from typing import Generic
from abc import ABC, abstractmethod

from .pipeline_context import C


class PipelineStep(ABC, Generic[C]):

    @abstractmethod
    def _check_entry_assumptions(self, context: C) -> bool:
        """ You can use this method to check if the pipeline step can be executed.
        Depending on your use case, you can use assert statements, raise exceptions, or return a boolean.
        """
        return True

    @abstractmethod
    def _check_exit_assumptions(self, context: C) -> bool:
        """ You can use this method to check if the pipeline step executed successfully.
        Depending on your use case, you can use assert statements, raise exceptions, or return a boolean.
        """
        return True

    @abstractmethod
    def get_start_message(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_end_message(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def _execute(self, context: C) -> C:
        raise NotImplementedError

    def run(self, context: C) -> C:
        if not self._check_entry_assumptions(context):
            assert False, "Entry assumptions not met"

        context = self._execute(context)

        if not self._check_exit_assumptions(context):
            assert False, "Exit assumptions not met"

        return context
