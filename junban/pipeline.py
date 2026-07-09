import logging

from typing import List, Generic, Optional

from .pipeline_context import C
from .pipeline_step import PipelineStep


class Pipeline(Generic[C]):
    def __init__(self, steps: List[PipelineStep[C]], name: Optional[str] = "PIPELINE",
                 logger: Optional[logging.Logger] = None):
        """
        Main junban pipeline class.

        :param steps: Pipeline steps to be executed.
        :param name: Name of the pipeline, defaults to "PIPELINE".
        :param logger: Optional logger to log pipeline steps, defaults to None.
        If no logger is provided, logs will be printed to stdout.
        """
        self.steps: List[PipelineStep[C]] = steps
        self.name = name
        self._log_info = lambda msg: self._log_info_func(msg, logger)
        self._log_error = lambda msg: self._log_error_func(msg, logger)

    @staticmethod
    def _log_info_func(message: str, logger: logging.Logger = None):
        if logger is None:
            print(message)
        else:
            logger.info(message)

    @staticmethod
    def _log_error_func(message: str, logger: logging.Logger = None):
        if logger is None:
            print(message)
        else:
            logger.error(message)

    def execute(self, context: C) -> C:
        """ Run the pipeline steps with the given initial context."""
        current_context = context
        for step in self.steps:
            try:
                skip = step.maybe_skip(context)
                if skip:
                    self._log_info(f"[{self.name}] Skipping..")
                else:
                    self._log_info(f"[{self.name}] {step.get_start_message()}")
                    current_context = step.run(current_context)
                    self._log_info(f"[{self.name}] {step.get_end_message()}")
            except AssertionError as e:
                self._log_error(f"[{self.name}] Assertion error in step {step.__class__.__name__}: {str(e)}")
                raise
            except Exception as e:
                self._log_error(f"[{self.name}] Error in step {step.__class__.__name__}: {str(e)}")
                raise
        return current_context
