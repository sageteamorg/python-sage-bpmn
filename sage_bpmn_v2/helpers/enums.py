from enum import StrEnum


class BPMNTag(StrEnum):
    START_EVENT = "startEvent"
    END_EVENT = "endEvent"
    USER_TASK = "userTask"
    SCRIPT_TASK = "scriptTask"
    SERVICE_TASK = "serviceTask"
    EXCLUSIVE_GATEWAY = "exclusiveGateway"
    PARALLEL_GATEWAY = "parallelGateway"
    SEQUENCE_FLOW = "sequenceFlow"
    SUB_PROCESS = "subProcess"
