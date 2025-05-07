#import helpers
from helpers.reporter.pretty import pretty_results
from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import system_message, generate
from inspect_ai.scorer import includes, model_graded_fact
from textwrap import dedent

from helpers.solver.aider_coder import aider_coder
from helpers.solver.codex_coder import codex_coder
from helpers.solver.claude_coder import claude_coder

from helpers.scorer.shell import command_results
from helpers.solver.git_repo import repo_clone
from helpers.solver.shell import script_exec

@task
def coding_agent() -> Task:

    dataset=[
        Sample(
            input=dedent("""Generate a javascript file name hello-world.js that prints out hello. Also make a test for it and install any modules if you need to.
The test should be in a file called hello-world.test.js. The test should check that the output of the hello-world.js file is hello. The test should use the jest framework. The test should be in a folder called tests. The tests folder should be in the same directory as the hello-world.js file. The hello-world.js file should be in a folder called src. The src folder should be in the same directory as the tests folder. The tests folder should be in the same directory as the src folder.
                         """),
            target="The generated code should have the filename hello-world.js",
        )
    ]

    repo_dir = "/my-repo/workshop"
    repo_url = "https://github.com/jedi4ever/from-prompt-to-mcp.git"

    return Task(
        dataset=dataset,
        solver=[
            script_exec(command=f"rm -rf {repo_dir}"),
            script_exec(command=f"mkdir -p {repo_dir}"),
            #repo_clone(repo_url=repo_url, repo_dir=repo_dir),
            #aider_coder(repo_dir=repo_dir),
            codex_coder(repo_dir=repo_dir),
            #claude_coder(repo_dir=repo_dir),
            script_exec(command=f"ls -l {repo_dir}"),
        ],
        scorer=[
            # model_graded_fact(), 
            command_results(cwd=repo_dir, cmd="node", cmd_args=["src/hello-world.js"], cmd_output="hello"),
            command_results(cwd=repo_dir, cmd="npm", cmd_args=["run","test"]),
        ],
        sandbox="docker"
    )

if __name__ == "__main__":
    # Run the task
    results = eval(coding_agent, max_steps=10,log_level="info", display="rich")

    # Print the results
    #pretty_results(results)