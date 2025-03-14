from typing import List, Optional

from sage_bpmn.design.interface import IBPMNRepository
from sage_bpmn.helpers.data_classes import (
    BPMNEvent,
    BPMNGateway,
    BPMNProcess,
    BPMNSequenceFlow,
    BPMNTask,
)
from sage_bpmn.helpers.enums import EventType, GatewayType, TaskType


class BPMNQueryEngine:
    """Handles searching and filtering of BPMN Gateways."""

    def __init__(self, repository: IBPMNRepository):
        self.repository = repository

    def get_gateway_by_id(self, gateway_id: str) -> Optional[BPMNGateway]:
        """Finds a BPMN gateway by its ID."""
        return self.repository.get_gateways().get(gateway_id, None)

    def get_gateways_by_type(self, gateway_type: GatewayType) -> List[BPMNGateway]:
        """Filters and returns BPMN gateways of a specific type."""
        return [
            gw
            for gw in self.repository.get_gateways().values()
            if gw.gateway_type == gateway_type
        ]

    def search_gateways_by_name(
        self, name_query: str, exact_match: bool = False
    ) -> List[BPMNGateway]:
        """Searches for BPMN gateways by name."""
        if exact_match:
            return [
                gw
                for gw in self.repository.get_gateways().values()
                if gw.name == name_query
            ]
        return [
            gw
            for gw in self.repository.get_gateways().values()
            if name_query.lower() in gw.name.lower()
        ]

    def get_task_by_id(self, task_id: str) -> Optional[BPMNTask]:
        return self.repository.get_tasks().get(task_id, None)

    def get_tasks_by_type(self, task_type: TaskType) -> List[BPMNTask]:
        return [
            task
            for task in self.repository.get_tasks().values()
            if task.task_type == task_type
        ]

    def search_tasks_by_name(
        self, name_query: str, exact_match: bool = False
    ) -> List[BPMNTask]:
        if exact_match:
            return [
                task
                for task in self.repository.get_tasks().values()
                if task.name == name_query
            ]
        return [
            task
            for task in self.repository.get_tasks().values()
            if name_query.lower() in task.name.lower()
        ]

    def get_sequence_flow_by_id(self, flow_id: str) -> Optional[BPMNSequenceFlow]:
        return self.repository.get_sequence_flows().get(flow_id, None)

    def get_sequence_flows_by_source(self, source_id: str) -> List[BPMNSequenceFlow]:
        return [
            flow
            for flow in self.repository.get_sequence_flows().values()
            if flow.source_ref == source_id
        ]

    def get_sequence_flows_by_target(self, target_id: str) -> List[BPMNSequenceFlow]:
        return [
            flow
            for flow in self.repository.get_sequence_flows().values()
            if flow.target_ref == target_id
        ]

    def get_all_sequence_flows(self) -> List[BPMNSequenceFlow]:
        """Returns all BPMN sequence flows."""
        return list(self.repository.get_sequence_flows().values())

    def get_event_by_id(self, event_id: str) -> Optional[BPMNEvent]:
        """Finds an event by its ID."""
        return self.repository.get_events().get(event_id, None)

    def get_events_by_type(self, event_type: EventType) -> List[BPMNEvent]:
        """Filters and returns BPMN events of a specific type."""
        return [
            event
            for event in self.repository.get_events().values()
            if event.event_type == event_type
        ]

    def get_all_events(self) -> List[BPMNEvent]:
        """Returns all BPMN events."""
        return list(self.repository.get_events().values())

    def get_process_by_id(self, process_id: str) -> Optional[BPMNProcess]:
        """Finds a BPMN process by its ID."""
        return self.repository.get_processes().get(process_id, None)

    def get_subprocesses(self, parent_process_id: str) -> List[BPMNProcess]:
        """Returns all subprocesses of a given process."""
        return [
            p
            for p in self.repository.get_processes().values()
            if p.parent_process_id == parent_process_id
        ]
