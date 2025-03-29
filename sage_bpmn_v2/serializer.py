import logging
from typing import List, Optional

from lxml import etree
from lxml.etree import Element, ElementTree

from sage_bpmn_v2.helpers.consts import BPMN_NS
from sage_bpmn_v2.helpers.data_classes import (
    AtomicFlowElement,
    EndEvent,
    ExclusiveGateway,
    ExecutionListener,
    ExtensionProperty,
    Process,
    SubProcess,
    ScriptTask,
    ServiceTask,
    SequenceFlow,
    StartEvent,
    UserTask,
    ZeebeHeader,
    ZeebeFormDefinition,
    ZeebeAssignment,
    ZeebeInput,
    ZeebeTaskDefinition,
    ZeebeOutput
)
from sage_bpmn_v2.helpers.enums import BPMNTag

logger = logging.getLogger(__name__)

TAG_TO_CLASS = {
    BPMNTag.START_EVENT: StartEvent,
    BPMNTag.END_EVENT: EndEvent,
    BPMNTag.USER_TASK: UserTask,
    BPMNTag.EXCLUSIVE_GATEWAY: ExclusiveGateway,
    BPMNTag.SUB_PROCESS: SubProcess
}


class BPMNParser:
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.tree: Optional[ElementTree] = None
        self.root: Optional[Element] = None

    def load(self) -> None:
        self.tree = etree.parse(self.xml_file)
        self.root = self.tree.getroot()

    def parse(self) -> Process:
        if self.tree is None or self.root is None:
            self.load()

        process_el = self.root.find(".//bpmn:process", namespaces=BPMN_NS)
        if process_el is None:
            raise ValueError("No <process> element found in BPMN XML.")

        process_id = process_el.get("id")
        is_executable = process_el.get("isExecutable", "false").lower() == "true"

        documentation_el = process_el.find("bpmn:documentation", namespaces=BPMN_NS)
        documentation = (
            documentation_el.text.strip() if documentation_el is not None else None
        )

        flow_elements: List[AtomicFlowElement] = []

        for elem in process_el:
            tag = etree.QName(elem).localname
            if tag in {"documentation", "extensionElements"}:
                continue

            parsed_elem = self._parse_flow_element(elem)
            if parsed_elem:
                flow_elements.append(parsed_elem)

        # Process-level extension elements
        process_ext_props: List[ExtensionProperty] = []
        process_exec_listeners: List[ExecutionListener] = []
        self._parse_extension_elements(
            process_el,
            target=None,
            ext_props=process_ext_props,
            exec_listeners=process_exec_listeners,
        )
        version_tag = next(
            (prop.value for prop in process_ext_props if prop.name == "zeebe:versionTag"), None
        )
        process_ext_props = [p for p in process_ext_props if p.name != "zeebe:versionTag"]

        return Process(
            id=process_id,
            isExecutable=is_executable,
            documentation=documentation,
            versionTag=version_tag,
            flowElements=flow_elements,
            extensionProperties=process_ext_props,
            executionListeners=process_exec_listeners,
        )

    def _parse_flow_element(self, elem: Element) -> Optional[AtomicFlowElement]:
        tag = etree.QName(elem).localname
        elem_id = elem.get("id")
        name = elem.get("name")

        if not elem_id:
            logger.warning(f"Skipping element <{tag}>: missing required 'id' attribute.")
            return None

        try:
            tag_enum = BPMNTag(tag)
        except ValueError:
            logger.warning(f"Unhandled BPMN tag: <{tag}>")
            return None

        documentation_el = elem.find("bpmn:documentation", namespaces=BPMN_NS)
        documentation = documentation_el.text.strip() if documentation_el is not None else None

        element_obj = None

        if tag_enum == BPMNTag.USER_TASK:
            element_obj = UserTask(id=elem_id, name=name, documentation=documentation)
            self._parse_user_task_extensions(elem, element_obj)

        elif tag_enum == BPMNTag.SCRIPT_TASK:
            script = self._parse_script(elem)
            element_obj = ScriptTask(id=elem_id, name=name, documentation=documentation, script=script)

        elif tag_enum == BPMNTag.SERVICE_TASK:
            element_obj = ServiceTask(id=elem_id, name=name, documentation=documentation)
            self._parse_service_task_extensions(elem, element_obj)

        elif tag_enum == BPMNTag.SUB_PROCESS:
            subprocess = SubProcess(id=elem_id, name=name, documentation=documentation)

            for sub_elem in elem:
                sub_tag = etree.QName(sub_elem).localname
                if sub_tag in {"documentation", "extensionElements"}:
                    continue

                parsed_sub = self._parse_flow_element(sub_elem)
                if parsed_sub:
                    subprocess.flowElements.append(parsed_sub)

            element_obj = subprocess

        elif tag_enum == BPMNTag.SEQUENCE_FLOW:
            source = elem.get("sourceRef")
            target = elem.get("targetRef")
            element_obj = SequenceFlow(
                id=elem_id, sourceRef=source, targetRef=target, name=name, documentation=documentation
            )

        elif tag_enum in TAG_TO_CLASS:
            element_obj = TAG_TO_CLASS[tag_enum](id=elem_id, name=name, documentation=documentation)

        if element_obj:
            self._parse_extension_elements(elem, target=element_obj)

        return element_obj

    def _parse_script(self, elem: Element) -> Optional[str]:
        script_el = elem.find("bpmn:script", namespaces=BPMN_NS)
        return script_el.text if script_el is not None else None

    def _parse_service_task_extensions(self, elem: Element, service_task: ServiceTask):
        ext_el = elem.find("bpmn:extensionElements", namespaces=BPMN_NS)
        if ext_el is None:
            return

        # -- taskDefinition --
        task_def_el = ext_el.find("zeebe:taskDefinition", namespaces=BPMN_NS)
        if task_def_el is not None:
            job_type = task_def_el.get("type")
            retries = task_def_el.get("retries")
            if job_type:
                service_task.taskDefinition = ZeebeTaskDefinition(
                    type=job_type,
                    retries=retries,
                )

        # -- inputs --
        for input_el in ext_el.findall(".//zeebe:input", namespaces=BPMN_NS):
            src = input_el.get("source") or ""
            tgt = input_el.get("target")
            if tgt:
                service_task.inputs.append(ZeebeInput(source=src, target=tgt))

        # -- outputs --
        for output_el in ext_el.findall(".//zeebe:output", namespaces=BPMN_NS):
            src = output_el.get("source") or ""
            tgt = output_el.get("target")
            if tgt:
                service_task.outputs.append(ZeebeOutput(source=src, target=tgt))

        # -- headers --
        for header_el in ext_el.findall(".//zeebe:header", namespaces=BPMN_NS):
            key = header_el.get("key")
            value = header_el.get("value")
            if key and value:
                service_task.headers.append(ZeebeHeader(key=key, value=value))

    def _parse_user_task_extensions(self, elem: Element, user_task: UserTask):
        ext_el = elem.find("bpmn:extensionElements", namespaces=BPMN_NS)
        if ext_el is None:
            return

        # -- form --
        form_el = ext_el.find("zeebe:formDefinition", namespaces=BPMN_NS)
        if form_el is not None:
            user_task.form = ZeebeFormDefinition(
                formKey=form_el.get("formKey") or form_el.get("formId"),
                binding=form_el.get("binding"),
                version=form_el.get("version"),
            )

        # -- assignment --
        assignment_el = ext_el.find("zeebe:assignmentDefinition", namespaces=BPMN_NS)
        assignee = candidate_groups = candidate_users = None
        if assignment_el is not None:
            assignee = assignment_el.get("assignee")
            candidate_groups = assignment_el.get("candidateGroups")
            candidate_users = assignment_el.get("candidateUsers")

        priority_el = ext_el.find("zeebe:priorityDefinition", namespaces=BPMN_NS)
        priority = priority_el.get("priority") if priority_el is not None else None

        if any([assignee, candidate_groups, candidate_users, priority]):
            user_task.assignment = ZeebeAssignment(
                assignee=assignee,
                candidateGroups=candidate_groups,
                candidateUsers=candidate_users,
                dueDate=None,
                followUpDate=None,
                priority=priority,
            )

        # -- inputs --
        for input_el in ext_el.findall(".//zeebe:input", namespaces=BPMN_NS):
            src = input_el.get("source") or ""
            tgt = input_el.get("target")
            if tgt:
                user_task.inputs.append(ZeebeInput(source=src, target=tgt))

        # -- outputs --
        for output_el in ext_el.findall(".//zeebe:output", namespaces=BPMN_NS):
            src = output_el.get("source") or ""
            tgt = output_el.get("target")
            if tgt:
                user_task.outputs.append(ZeebeOutput(source=src, target=tgt))

        # -- headers --
        for header_el in ext_el.findall(".//zeebe:header", namespaces=BPMN_NS):
            key = header_el.get("key")
            value = header_el.get("value")
            if key and value:
                user_task.headers.append(ZeebeHeader(key=key, value=value))

    def _parse_extension_elements(
        self,
        elem: Element,
        target: Optional[AtomicFlowElement] = None,
        ext_props: Optional[List[ExtensionProperty]] = None,
        exec_listeners: Optional[List[ExecutionListener]] = None,
    ):
        ext_el = elem.find("bpmn:extensionElements", namespaces=BPMN_NS)
        if ext_el is None:
            return

        # Assign to appropriate targets
        if target is not None:
            prop_list = target.extensionProperties
            listener_list = target.executionListeners
        else:
            prop_list = ext_props if ext_props is not None else []
            listener_list = exec_listeners if exec_listeners is not None else []

        for listener in ext_el.findall(
            ".//zeebe:executionListener", namespaces=BPMN_NS
        ):
            event_type = listener.get("eventType")
            listener_type = listener.get("type")
            retries = listener.get("retries")

            if not listener_type:
                logger.warning("ExecutionListener missing 'type' attribute")
                continue

            listener_list.append(
                ExecutionListener(
                    event_type=event_type, listener_type=listener_type, retries=retries
                )
            )

        for prop in ext_el.findall(".//zeebe:property", namespaces=BPMN_NS):
            name = prop.get("name")
            value = prop.get("value")
            if name and value:
                prop_list.append(ExtensionProperty(name=name, value=value))

        version_tag = ext_el.find("zeebe:versionTag", namespaces=BPMN_NS)
        if version_tag is not None:
            value = version_tag.get("value")
            if value:
                prop_list.append(
                    ExtensionProperty(name="zeebe:versionTag", value=value)
                )
