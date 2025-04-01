from typing import List, Optional, Type

from sage_bpmn.models import AtomicFlowElement, Process, SubProcess


class BPMNQuery:
    def __init__(self, process: Process):
        self.process = process

    def find_by_id(self, element_id: str) -> Optional[AtomicFlowElement]:
        return self._search_by_id(self.process.flowElements, element_id)

    def find_by_type(
        self, element_type: Type[AtomicFlowElement]
    ) -> List[AtomicFlowElement]:
        return self._search_by_type(self.process.flowElements, element_type)

    def filter_by_attributes(
        self, element_type: Optional[Type[AtomicFlowElement]] = None, **attrs
    ) -> List[AtomicFlowElement]:
        return self._filter_by_attrs(self.process.flowElements, element_type, attrs)

    def _search_by_id(
        self, elements: List[AtomicFlowElement], element_id: str
    ) -> Optional[AtomicFlowElement]:
        for el in elements:
            if el.id == element_id:
                return el
            if isinstance(el, SubProcess):
                found = self._search_by_id(el.flowElements, element_id)
                if found:
                    return found
        return None

    def _search_by_type(
        self, elements: List[AtomicFlowElement], element_type: Type[AtomicFlowElement]
    ) -> List[AtomicFlowElement]:
        results = []
        for el in elements:
            if isinstance(el, element_type):
                results.append(el)
            if isinstance(el, SubProcess):
                results.extend(self._search_by_type(el.flowElements, element_type))
        return results

    def _filter_by_attrs(
        self,
        elements: List[AtomicFlowElement],
        element_type: Optional[Type[AtomicFlowElement]],
        attrs: dict,
    ) -> List[AtomicFlowElement]:
        results = []
        for el in elements:
            if element_type and not isinstance(el, element_type):
                continue

            match = all(getattr(el, attr, None) == val for attr, val in attrs.items())
            if match:
                results.append(el)

            if isinstance(el, SubProcess):
                results.extend(
                    self._filter_by_attrs(el.flowElements, element_type, attrs)
                )

        return results
