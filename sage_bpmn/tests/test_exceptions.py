import pytest

from sage_bpmn.helpers.exceptions import (
    BPMNError,
    BPMNExecutionError,
    BPMNFileTypeError,
    BPMNGraphError,
    BPMNParseError,
    BPMNSerializationError,
    BPMNValidationError,
)


def test_bpmn_error_base():
    """Test the base BPMNError class with and without an element."""

    error = BPMNError("Base error")
    assert str(error) == "Base error"
    assert error.message == "Base error"
    assert error.element is None

    mock_element = {"id": "gateway1"}
    error_with_element = BPMNError("Base error with element", element=mock_element)
    assert str(error_with_element) == "Base error with element"
    assert error_with_element.element == mock_element


def test_bpmn_parse_error():
    """Test BPMNParseError with and without line number."""

    parse_error = BPMNParseError("XML parsing failed")
    assert str(parse_error) == "XML parsing failed"
    assert parse_error.line is None
    assert isinstance(parse_error, BPMNError)

    parse_error_with_line = BPMNParseError("XML parsing failed", line=42)
    assert str(parse_error_with_line) == "XML parsing failed"
    assert parse_error_with_line.line == 42
    assert isinstance(parse_error_with_line, BPMNError)


def test_bpmn_validation_error():
    """Test BPMNValidationError with and without element."""

    validation_error = BPMNValidationError("Missing start event")
    assert str(validation_error) == "Missing start event"
    assert validation_error.element is None
    assert isinstance(validation_error, BPMNError)

    mock_element = {"id": "task1"}
    validation_error_with_element = BPMNValidationError(
        "Invalid task", element=mock_element
    )
    assert str(validation_error_with_element) == "Invalid task"
    assert validation_error_with_element.element == mock_element
    assert isinstance(validation_error_with_element, BPMNError)


def test_bpmn_execution_error():
    """Test BPMNExecutionError with and without task_id."""

    execution_error = BPMNExecutionError("Execution failed")
    assert str(execution_error) == "Execution failed"
    assert execution_error.task_id is None
    assert isinstance(execution_error, BPMNError)

    execution_error_with_task = BPMNExecutionError("Task failed", task_id="task123")
    assert str(execution_error_with_task) == "Task failed"
    assert execution_error_with_task.task_id == "task123"
    assert isinstance(execution_error_with_task, BPMNError)


def test_bpmn_graph_error():
    """Test BPMNGraphError with and without node."""

    graph_error = BPMNGraphError("Graph inconsistency")
    assert str(graph_error) == "Graph inconsistency"
    assert graph_error.node is None
    assert isinstance(graph_error, BPMNError)

    mock_node = {"id": "node1"}
    graph_error_with_node = BPMNGraphError("Node error", node=mock_node)
    assert str(graph_error_with_node) == "Node error"
    assert graph_error_with_node.node == mock_node
    assert isinstance(graph_error_with_node, BPMNError)


def test_bpmn_serialization_error():
    """Test BPMNSerializationError with and without format_type."""

    serialization_error = BPMNSerializationError("Serialization failed")
    assert str(serialization_error) == "Serialization failed"
    assert serialization_error.format_type is None
    assert isinstance(serialization_error, BPMNError)

    serialization_error_with_format = BPMNSerializationError(
        "JSON export failed", format_type="JSON"
    )
    assert str(serialization_error_with_format) == "JSON export failed"
    assert serialization_error_with_format.format_type == "JSON"
    assert isinstance(serialization_error_with_format, BPMNError)


def test_bpmn_file_type_error():
    """Test BPMNFileTypeError with a file path."""
    file_path = "process.txt"
    file_type_error = BPMNFileTypeError(file_path)
    expected_message = f"Invalid file type: '{file_path}'. Expected a .bpmn file."
    assert str(file_type_error) == expected_message
    assert file_type_error.element == file_path
    assert isinstance(file_type_error, BPMNError)

    with pytest.raises(BPMNFileTypeError) as exc_info:
        raise BPMNFileTypeError("invalid.xml")
    assert (
        str(exc_info.value)
        == "Invalid file type: 'invalid.xml'. Expected a .bpmn file."
    )


def test_exception_hierarchy():
    """Test that all exceptions inherit from BPMNError."""
    assert issubclass(BPMNParseError, BPMNError)
    assert issubclass(BPMNValidationError, BPMNError)
    assert issubclass(BPMNExecutionError, BPMNError)
    assert issubclass(BPMNGraphError, BPMNError)
    assert issubclass(BPMNSerializationError, BPMNError)
    assert issubclass(BPMNFileTypeError, BPMNError)


def test_raise_and_catch_exceptions():
    """Test that each exception can be raised and caught."""
    exceptions = [
        (BPMNParseError, "Parse error", {"line": 10}, "Parse error"),
        (
            BPMNValidationError,
            "Validation error",
            {"element": {"id": "e1"}},
            "Validation error",
        ),
        (BPMNExecutionError, "Execution error", {"task_id": "t1"}, "Execution error"),
        (BPMNGraphError, "Graph error", {"node": {"id": "n1"}}, "Graph error"),
        (
            BPMNSerializationError,
            "Serialization error",
            {"format_type": "XML"},
            "Serialization error",
        ),
        (
            BPMNFileTypeError,
            "wrong_file.txt",
            {},
            "Invalid file type: 'wrong_file.txt'. Expected a .bpmn file.",
        ),
    ]

    for exception_class, message, kwargs, expected_str in exceptions:
        with pytest.raises(exception_class) as exc_info:
            raise exception_class(message, **kwargs)
        assert str(exc_info.value) == expected_str
