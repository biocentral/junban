from typing import TypeVar

class PipelineContext:
    """ Large struct to hold pipeline context during execution """
    pass

C = TypeVar("C", bound=PipelineContext)
