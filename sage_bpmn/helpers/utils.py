from .exceptions import BPMNFileTypeError


def validate_bpmn_file(file_path):
    """Checks if the given file has a .bpmn extension."""
    if not file_path.lower().endswith(".bpmn"):
        raise BPMNFileTypeError(file_path)
    print(f"File '{file_path}' is a valid BPMN file.")
