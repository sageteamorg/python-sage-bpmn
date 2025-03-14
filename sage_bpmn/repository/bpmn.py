from typing import Dict

from sage_bpmn.design.interface import IBPMNRepository
from sage_bpmn.helpers.data_classes import BPMNGateway, BPMNTask


class InMemoryBPMNRepository(IBPMNRepository):
    """Stores BPMN gateways and tasks in memory."""

    def __init__(self):
        self._gateways: Dict[str, BPMNGateway] = {}
        self._tasks: Dict[str, BPMNTask] = {}

    def add_gateway(self, gateway: BPMNGateway):
        self._gateways[gateway.gateway_id] = gateway

    def get_gateways(self) -> Dict[str, BPMNGateway]:
        return self._gateways

    def add_task(self, task: BPMNTask):
        self._tasks[task.task_id] = task

    def get_tasks(self) -> Dict[str, BPMNTask]:
        return self._tasks
