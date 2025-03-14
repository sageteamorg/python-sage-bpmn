import pytest
from enum import StrEnum
from sage_bpmn.helpers.enums import GatewayType, TaskType
from sage_bpmn.helpers.data_classes import BPMNGateway, BPMNTask


# Tests for sage_bpmn.helpers.enums
def test_gateway_type_enum_values():
    """Test that GatewayType enum has the correct values."""
    expected_values = {
        GatewayType.EXCLUSIVE: "exclusiveGateway",
        GatewayType.PARALLEL: "parallelGateway",
        GatewayType.INCLUSIVE: "inclusiveGateway",
        GatewayType.EVENT_BASED: "eventBasedGateway",
    }
    for gateway, value in expected_values.items():
        assert gateway.value == value
        assert isinstance(gateway, GatewayType)
        assert isinstance(gateway, StrEnum)


def test_task_type_enum_values():
    """Test that TaskType enum has the correct values."""
    expected_values = {
        TaskType.GENERIC: "task",
        TaskType.USER: "userTask",
        TaskType.MANUAL: "manualTask",
        TaskType.SERVICE: "serviceTask",
        TaskType.SCRIPT: "scriptTask",
        TaskType.BUSINESS_RULE: "businessRuleTask",
        TaskType.SEND: "sendTask",
        TaskType.RECEIVE: "receiveTask",
    }
    for task, value in expected_values.items():
        assert task.value == value
        assert isinstance(task, TaskType)
        assert isinstance(task, StrEnum)


def test_gateway_type_enum_length():
    """Test the number of GatewayType enum members."""
    assert len(GatewayType) == 4  # EXCLUSIVE, PARALLEL, INCLUSIVE, EVENT_BASED


def test_task_type_enum_length():
    """Test the number of TaskType enum members."""
    assert len(TaskType) == 8  # GENERIC, USER, MANUAL, SERVICE, SCRIPT, BUSINESS_RULE, SEND, RECEIVE


# Tests for sage_bpmn.helpers.data_classes
def test_bpmn_gateway_instantiation():
    """Test BPMNGateway instantiation with valid data."""
    gateway = BPMNGateway(
        gateway_id="g1",
        name="Decision Point",
        gateway_type=GatewayType.EXCLUSIVE,
    )
    assert gateway.gateway_id == "g1"
    assert gateway.name == "Decision Point"
    assert gateway.gateway_type == GatewayType.EXCLUSIVE


def test_bpmn_gateway_immutability():
    """Test that BPMNGateway is immutable."""
    gateway = BPMNGateway(
        gateway_id="g1",
        name="Decision Point",
        gateway_type=GatewayType.EXCLUSIVE,
    )
    with pytest.raises(AttributeError):
        gateway.gateway_id = "g2"
    with pytest.raises(AttributeError):
        gateway.name = "New Name"
    with pytest.raises(AttributeError):
        gateway.gateway_type = GatewayType.PARALLEL


def test_bpmn_task_instantiation():
    """Test BPMNTask instantiation with valid data."""
    task = BPMNTask(
        task_id="t1",
        name="Process Order",
        task_type=TaskType.USER,
    )
    assert task.task_id == "t1"
    assert task.name == "Process Order"
    assert task.task_type == TaskType.USER


def test_bpmn_task_immutability():
    """Test that BPMNTask is immutable."""
    task = BPMNTask(
        task_id="t1",
        name="Process Order",
        task_type=TaskType.USER,
    )
    with pytest.raises(AttributeError):
        task.task_id = "t2"
    with pytest.raises(AttributeError):
        task.name = "New Task"
    with pytest.raises(AttributeError):
        task.task_type = TaskType.SERVICE


def test_bpmn_task_repr():
    """Test the __repr__ method of BPMNTask."""
    task = BPMNTask(
        task_id="t1",
        name="Process Order",
        task_type=TaskType.USER,
    )
    expected_repr = "<USER Task id=t1 name=Process Order>"
    assert repr(task) == expected_repr

    # Test with a different task type
    task2 = BPMNTask(
        task_id="t2",
        name="Send Email",
        task_type=TaskType.SEND,
    )
    assert repr(task2) == "<SEND Task id=t2 name=Send Email>"


def test_bpmn_gateway_type_validation():
    """Test that BPMNGateway only accepts GatewayType enum values."""
    with pytest.raises(TypeError) as exc_info:
        BPMNGateway(
            gateway_id="g1",
            name="Invalid Gateway",
            gateway_type="not_an_enum",  # Invalid type
        )
    assert "gateway_type must be a GatewayType" in str(exc_info.value)


def test_bpmn_task_type_validation():
    """Test that BPMNTask only accepts TaskType enum values."""
    with pytest.raises(TypeError) as exc_info:
        BPMNTask(
            task_id="t1",
            name="Invalid Task",
            task_type="not_an_enum",  # Invalid type
        )
    assert "task_type must be a TaskType" in str(exc_info.value)