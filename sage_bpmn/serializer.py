from pathlib import Path
from typing import Union

from lxml.etree import XMLParser, _ElementTree, parse

from sage_bpmn.design.interface import IBPMNRepository
from sage_bpmn.helpers.data_classes import (
    BPMNEvent,
    BPMNGateway,
    BPMNSequenceFlow,
    BPMNTask,
    BPMNProcess
)
from sage_bpmn.helpers.enums import EventType, GatewayType, TaskType
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

    def extract_events(self):
        """Extracts BPMN events (Start, End, Intermediate) and stores them in the repository."""
        for event_type in EventType:
            elements = self.root.findall(
                f".//bpmn:{event_type.value}", namespaces=BPMN_NAMESPACE
            )

            for element in elements:
                event = BPMNEvent(
                    event_id=element.get("id", "Unknown"),
                    name=element.get(
                        "name", f"{event_type.name}_{element.get('id', 'Unknown')}"
                    ),
                    event_type=event_type,
                )
                self.repository.add_event(event)

    def extract_processes(self):
        """Extracts processes and subprocesses from BPMN XML."""
        processes = self.root.findall(".//bpmn:process", namespaces=BPMN_NAMESPACE)
        
        print(f"Found {len(processes)} processes")  # DEBUGGING

        for process in processes:
            process_id = process.get("id", "Unknown")
            name = process.get("name", f"Process_{process_id}")
            is_executable = process.get("isExecutable", "false") == "true"

            print(f"Extracting process: ID={process_id}, Name={name}, Executable={is_executable}")  # DEBUGGING

            bpmn_process = BPMNProcess(
                process_id=process_id,
                name=name,
                is_executable=is_executable,
                elements=[]
            )
            self.repository.add_process(bpmn_process)

            # Extract subprocesses inside this process
            self.extract_subprocesses(process, process_id)

    def extract_subprocesses(self, parent, parent_process_id):
        """Recursively extracts subprocesses inside a process."""
        subprocesses = parent.findall(".//bpmn:subProcess", namespaces=BPMN_NAMESPACE)
        for subprocess in subprocesses:
            subprocess_id = subprocess.get("id", "Unknown")
            name = subprocess.get("name", f"Subprocess_{subprocess_id}")

            bpmn_process = BPMNProcess(
                process_id=subprocess_id,
                name=name,
                is_executable=True,  # Subprocesses are typically executable
                parent_process_id=parent_process_id,
                elements=[]
            )
            self.repository.add_process(bpmn_process)

    def extract_all(self):
        """Extracts all BPMN elements: gateways, tasks, and sequence flows."""
        self.extract_gateways()
        self.extract_tasks()
        self.extract_sequence_flows()
        self.extract_events()
        self.extract_processes()
