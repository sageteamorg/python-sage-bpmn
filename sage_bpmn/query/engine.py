from typing import List, Optional

from sage_bpmn.design.interface import IBPMNRepository
from sage_bpmn.helpers.data_classes import BPMNGateway, BPMNTask
from sage_bpmn.helpers.enums import GatewayType, TaskType


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
