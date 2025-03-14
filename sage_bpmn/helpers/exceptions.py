class BPMNError(Exception):
    """Base exception for all BPMN-related errors."""

    def __init__(self, message, element=None):
        self.message = message
        self.element = element  # Optional BPMN element reference
        super().__init__(message)


class BPMNParseError(BPMNError):
    """Raised when BPMN XML parsing fails."""

    def __init__(self, message, line=None):
        super().__init__(message)
        self.line = line  # Line number in the BPMN XML file


class BPMNValidationError(BPMNError):
    """Raised when BPMN model is invalid (e.g., missing start event)."""

    def __init__(self, message, element=None):
        super().__init__(message, element)


class BPMNExecutionError(BPMNError):
    """Raised during BPMN execution errors (e.g., missing task data)."""

    def __init__(self, message, task_id=None):
        super().__init__(message)
        self.task_id = task_id  # ID of the failed BPMN task


class BPMNGraphError(BPMNError):
    """Raised when BPMN graph contains inconsistencies."""

    def __init__(self, message, node=None):
        super().__init__(message)
        self.node = node  # Node in the BPMN graph


class BPMNSerializationError(BPMNError):
    """Raised when exporting BPMN fails."""

    def __init__(self, message, format_type=None):
        super().__init__(message)
        self.format_type = format_type  # XML, JSON, etc.


class BPMNFileTypeError(BPMNError):
    """Raised when a non-.bpmn file is loaded."""

    def __init__(self, file_path):
        message = f"Invalid file type: '{file_path}'. Expected a .bpmn file."
        super().__init__(message, file_path)
