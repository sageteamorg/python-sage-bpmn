from pathlib import Path
from typing import Dict, List, Union

from lxml.etree import XMLParser, _Element, _ElementTree, parse

from sage_bpmn.design.interface import IBPMNRepository
from sage_bpmn.helpers.data_classes import BPMNGateway, BPMNSequenceFlow, BPMNTask
from sage_bpmn.helpers.enums import GatewayType, TaskType
from sage_bpmn.helpers.exceptions import BPMNFileTypeError

BPMN_NAMESPACE = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"}


class BPMNParser:
    """BPMN XML Parser to extract BPMN elements."""

    def __init__(self, file_path: Union[Path, str], repository: IBPMNRepository):
        if isinstance(file_path, str):
            file_path = Path(file_path)

        if file_path.suffix.lower() != ".bpmn":
            raise BPMNFileTypeError(file_path)

        self.file_path = file_path
        self.xml_parser = XMLParser(remove_blank_text=True)
        self.tree: _ElementTree = parse(file_path, self.xml_parser)
        self.root = self.tree.getroot()
        self.repository = repository

    def extract_gateways(self):
        for gateway_type in GatewayType:
            elements = self.root.findall(
                f".//bpmn:{gateway_type.value}", namespaces=BPMN_NAMESPACE
            )
            for element in elements:
                gateway = BPMNGateway(
                    gateway_id=element.get("id", "Unknown"),
                    name=element.get(
                        "name", f"{gateway_type.name}_{element.get('id', 'Unknown')}"
                    ),
                    gateway_type=gateway_type,
                )
                self.repository.add_gateway(gateway)

    def extract_tasks(self):
        """Extracts all BPMN tasks and stores them in the repository."""
        for task_type in TaskType:
            elements = self.root.findall(
                f".//bpmn:{task_type.value}", namespaces=BPMN_NAMESPACE
            )
            for element in elements:
                task = BPMNTask(
                    task_id=element.get("id", "Unknown"),
                    name=element.get(
                        "name", f"{task_type.name}_{element.get('id', 'Unknown')}"
                    ),
                    task_type=task_type,
                )
                self.repository.add_task(task)

    def extract_sequence_flows(self):
        """Extracts sequence flows and stores them in the repository."""
        elements = self.root.findall(".//bpmn:sequenceFlow", namespaces=BPMN_NAMESPACE)

        for element in elements:
            sequence_flow = BPMNSequenceFlow(
                flow_id=element.get("id", "Unknown"),
                source_ref=element.get("sourceRef", "Unknown"),
                target_ref=element.get("targetRef", "Unknown"),
            )
            self.repository.add_sequence_flow(sequence_flow)

    def extract_all(self):
        """Extracts all BPMN elements: gateways, tasks, and sequence flows."""
        self.extract_gateways()
        self.extract_tasks()
        self.extract_sequence_flows()
