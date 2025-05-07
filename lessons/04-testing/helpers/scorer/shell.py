from inspect_ai.scorer import (
    Score,
    Target,
    accuracy,
    scorer,
    stderr,
)

from inspect_ai.solver._task_state import TaskState

from inspect_ai.util import sandbox
import logging

# setup logger for this source file
logger = logging.getLogger(__name__)

@scorer(metrics=[accuracy()])
def command_results(sandbox_name=None ,cwd=None,
                    cmd=None, cmd_args=None, cmd_output=None, exit_code=0,
                    exact=False, ignore_exit_code=False):

    async def score(state: TaskState, target: Target):

        nonlocal cmd, cmd_args, cmd_output, sandbox_name, cwd, exit_code, exact, ignore_exit_code

        # defaults
        expected_output = cmd_output
        output_ok = False
        exit_ok = False

        # calculate the full command
        complete_cmd = [cmd]
        if cmd_args is not None:
            complete_cmd.extend(cmd_args)

        # log each expected output
        logger.info("cmd_output : %s", cmd_output)
        explanation = []

        try:
            result = await sandbox(sandbox_name).exec(cwd=cwd, cmd=complete_cmd)

            # check for the expected exit code
            if not ignore_exit_code:
                if result.returncode == exit_code:
                    explanation.append(f"exit code {result.returncode} matches expected {exit_code}")
                    exit_ok = True
                else:
                    explanation.append(f"exit code {result.returncode} does not match expected {exit_code}")
                    exit_ok = False
            else:
                exit_ok = True

            # check for the expected output
            if cmd_output is not None:
                if exact:
                    if expected_output == result.stdout:
                        explanation.append(f"exact output matches expected {expected_output}")
                        output_ok = True
                else:
                    if expected_output.lower() in result.stdout.lower():
                        explanation.append(f"output matches expected {expected_output}")
                        output_ok = True
            else:
                output_ok = True

        except FileNotFoundError:
            explanation.append(f"command {cmd} not found")
            output_ok = False

        return Score(value=1 if output_ok and exit_ok else 0, explanation="\n".join(explanation))

    return score

# checks if a file exists
@scorer(metrics=[accuracy()])
def check_file_exists(filename=None, sandbox_name=None):

    async def score(state: TaskState, target: Target):
        nonlocal filename, sandbox_name
        if (filename is None):
            filename = state.metadata.get("filename")

        explanation = []
        # check for the expected output
        try:
            _ = await sandbox(sandbox_name).read_file(filename)
            exists = True
        except FileNotFoundError:
            explanation.append(f"file {filename} not found")
            exists = False
        return Score(value=1 if exists else 0, explanation="\n".join(explanation))

    return score

# looks at the output of the previous completion
@scorer(metrics=[accuracy(), stderr()])
def is_markdown():

    async def score(state: TaskState, target: Target):

        # check for correct
        answer = state.output.completion

        result = "I"  # incorrect
        explanation = "no markdown backticks found"

        if "```" in answer:
            result = "P"  # partial
            explanation = "we got some backticks"

        if answer.startswith("```"):
            result = "C"  # correct
            explanation = "we start with backticks"

        # return score
        return Score(
            value=result,
            answer=answer,
            explanation=explanation
        )
    return score
