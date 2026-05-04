# Junban (順番) – Simple Sequential Python Workflows

Junban (english: order) is a lightweight library for defining and executing sequential (scientific) workflows in Python.

## Installation

Junban is available via [pypi](https://pypi.org/project/junban/):

```shell
pip install junban
```

## Quick Example

Here is a simple example showing how to define a context and two steps. It showcases how context is passed between steps
and how entry/exit assumptions (verification) are handled.

```python
from dataclasses import dataclass
from junban.pipeline import Pipeline
from junban.pipeline_step import PipelineStep
from junban.pipeline_context import PipelineContext


# 1. Define your context by inheriting from PipelineContext
@dataclass
class MyContext(PipelineContext):
    value: int = 0
    is_processed: bool = False


# 2. Create pipeline steps by inheriting from PipelineStep
class IncrementStep(PipelineStep[MyContext]):
    def _check_entry_assumptions(self, context: MyContext) -> bool:
        # Verification before step execution
        return context.value == 0

    def _execute(self, context: MyContext) -> MyContext:
        # Core logic of the step
        context.value += 1
        return context

    def _check_exit_assumptions(self, context: MyContext) -> bool:
        # Verification after step execution
        return context.value == 1

    def get_start_message(self) -> str:
        return "Incrementing value..."

    def get_end_message(self) -> str:
        return "Value incremented."


class ProcessStep(PipelineStep[MyContext]):
    def _check_entry_assumptions(self, context: MyContext) -> bool:
        return context.value > 0

    def _execute(self, context: MyContext) -> MyContext:
        context.is_processed = True
        return context

    def _check_exit_assumptions(self, context: MyContext) -> bool:
        return context.is_processed is True

    def get_start_message(self) -> str:
        return "Processing..."

    def get_end_message(self) -> str:
        return "Processed."


# 3. Initialize and execute the pipeline
if __name__ == "__main__":
    context = MyContext()
    pipeline = Pipeline(
        steps=[IncrementStep(), ProcessStep()],
        name="ExamplePipeline"
    )

    final_context = pipeline.execute(context)
    print(f"Final value: {final_context.value}, Processed: {final_context.is_processed}")
```
