#import helpers
from helpers.reporter.pretty import pretty_results
from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import system_message, generate 
from inspect_ai.scorer import includes, model_graded_fact, match ,includes
from textwrap import dedent


@task
def example_task() -> Task:

    dataset=[
        Sample(
            input=dedent("""Generate a javascript file name hello-world.js that prints out hello. Also make a test for it and install any modules if you need to.
The test should be in a file called hello-world.test.js. The test should check that the output of the hello-world.js file is hello. The test should use the jest framework. The test should be in a folder called tests. The tests folder should be in the same directory as the hello-world.js file. The hello-world.js file should be in a folder called src. The src folder should be in the same directory as the tests folder. The tests folder should be in the same directory as the src folder.
                         """),
            target="The generated code should have the filename hello-world.js",
        )
    ]


    return Task(
        dataset=dataset,
        solver=[
            generate(),
        ],
        scorer=[
            match()
        ],
    )


if __name__ == "__main__":
    # Run the task
    results = eval(example_task, log_level="info", display="conversation")

    # Print the results
    print(pretty_results(results))
