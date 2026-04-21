from dataclasses import dataclass
from junban.pipeline import Pipeline
from junban.pipeline_step import PipelineStep
from junban.pipeline_context import PipelineContext

@dataclass
class MyContext(PipelineContext):
    data: int = 0
    processed: bool = False

class IncrementStep(PipelineStep[MyContext]):
    def _check_entry_assumptions(self, context: MyContext) -> bool:
        return context.data == 0

    def _check_exit_assumptions(self, context: MyContext) -> bool:
        return context.data == 1

    def get_start_message(self) -> str:
        return "Incrementing data..."

    def get_end_message(self) -> str:
        return "Data incremented."

    def _execute(self, context: MyContext) -> MyContext:
        context.data += 1
        return context

class ProcessStep(PipelineStep[MyContext]):
    def _check_entry_assumptions(self, context: MyContext) -> bool:
        return context.data > 0

    def _check_exit_assumptions(self, context: MyContext) -> bool:
        return context.processed is True

    def get_start_message(self) -> str:
        return "Processing data..."

    def get_end_message(self) -> str:
        return "Data processed."

    def _execute(self, context: MyContext) -> MyContext:
        context.processed = True
        return context

def main():
    ctx = MyContext()
    pipeline = Pipeline(steps=[IncrementStep(), ProcessStep()], name="MySimplePipeline")
    final_ctx = pipeline.execute(ctx)
    print(f"Final context: {final_ctx}")

if __name__ == "__main__":
    main()
