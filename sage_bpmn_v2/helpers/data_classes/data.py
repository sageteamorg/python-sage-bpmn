from dataclasses import dataclass
from typing import Optional


@dataclass
class DataObject:
    """
    Represents a BPMN DataObject, which provides information about what data is required
    or produced by activities within the process. It is a snapshot of data at a specific time.

    XML Example:
    ------------
    <dataObject id="DataObject_1" name="Invoice" />

    Attributes:
    -----------
    id : str
        Unique identifier of the data object.
    name : Optional[str]
        Human-readable name for the data object (e.g., "Invoice", "Customer Record").
    """

    id: str
    name: Optional[str] = None


@dataclass
class DataStoreReference:
    """
    Represents a BPMN DataStoreReference, which links to a persistent data store,
    allowing activities to read or write long-lived data.

    XML Example:
    ------------
    <dataStoreReference id="DataStore_1" name="CustomerDB" />

    Attributes:
    -----------
    id : str
        Unique identifier of the data store reference.
    name : Optional[str]
        Human-readable name of the data store (e.g., database or storage system).
    """

    id: str
    name: Optional[str] = None
