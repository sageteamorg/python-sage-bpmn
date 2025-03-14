from typing import Dict, List

from sage_bpmn.design.interface import IBPMNRepository
from sage_bpmn.helpers.data_classes import BPMNGateway, BPMNSequenceFlow, BPMNTask


class InMemoryBPMNRepository(IBPMNRepository):
    """Stores BPMN gateways and tasks in memory."""

    def __init__(self):
        self._gateways: Dict[str, BPMNGateway] = {}
        self._tasks: Dict[str, BPMNTask] = {}
        self._sequence_flows: Dict[str, BPMNSequenceFlow] = {}

    def add_gateway(self, gateway: BPMNGateway):
        self._gateways[gateway.gateway_id] = gateway

    def get_gateways(self) -> Dict[str, BPMNGateway]:
        return self._gateways

    def add_task(self, task: BPMNTask):
        self._tasks[task.task_id] = task

    def get_tasks(self) -> Dict[str, BPMNTask]:
        return self._tasks

    def add_sequence_flow(self, flow: BPMNSequenceFlow):
        self._sequence_flows[flow.flow_id] = flow

    def get_sequence_flows(self) -> Dict[str, BPMNSequenceFlow]:
        return self._sequence_flows
