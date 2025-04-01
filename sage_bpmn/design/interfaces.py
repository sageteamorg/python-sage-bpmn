from abc import ABC, abstractmethod
from typing import List


class AbstractExecutor(ABC):
    @abstractmethod
    def step(self) -> bool:
        """Advance the process by one execution step."""
        raise NotImplementedError

    @abstractmethod
    def visualize(self):
        """Render the current process state."""
        raise NotImplementedError

    @abstractmethod
    def print_execution_tree(self):
        """Print the current execution tree."""
        raise NotImplementedError


class ExecutionObserver(ABC):
    @abstractmethod
    def on_step(
        self,
        active_nodes: List[str],
        visited_nodes: List[str],
        execution_metadata: dict,
    ):
        pass
