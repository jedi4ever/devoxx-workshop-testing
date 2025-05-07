from multiprocessing import ProcessError
from inspect_ai.scorer import (
    CORRECT,
    INCORRECT,
    AnswerPattern,
    Score,
    Target,
    accuracy,
    scorer,
    stderr,
)
from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import match
from inspect_ai.solver import generate

from inspect_ai.scorer import Target
from inspect_ai.solver import (solver)
from inspect_ai.solver._task_state import TaskState

from inspect_ai.tool import bash
from inspect_ai.util import sandbox

from inspect_ai.model import (
    ChatMessage,
    ChatMessageUser,
    ChatMessageAssistant,
    ModelName,
    ModelOutput,
    get_model
)

from inspect_ai.solver import generate, system_message, Generate
import logging
import os

# setup logger for this source file
logger = logging.getLogger(__name__)

@solver
def repo_clone(cwd=None, repo_url=None, sandbox_name=None, repo_dir=None, ignore_errors=True):

    async def solve(state: TaskState, generate: Generate) -> TaskState:

        # defaults
        default_cwd = "."
        nonlocal cwd, repo_url, repo_dir
        if cwd is  None:
            cwd = default_cwd

        # construct full path to repo_dir
        full_repo_dir = os.path.join(cwd, repo_dir)
        logger.info("repo %s", full_repo_dir)

        # by default we assume the repo_dir is not a directory
        is_dir = False
        try:
            _ = await sandbox(sandbox_name).read_file(full_repo_dir)
        except FileNotFoundError:
            pass
        except IsADirectoryError:
            logger.info("repo_dir %s is a directory", full_repo_dir)
            is_dir = True
            # We need to clone the repo

        # Repo already exists
        if is_dir:
            state.messages.append(
                ChatMessageAssistant(
                    content=f"Directory {full_repo_dir} already exists. No need to clone."
                )
            )
            return state

        # Repo does not yet exist(directory)
        answer = "We received no answer from git clone."
        try:
            result = await sandbox(sandbox_name).exec(cwd=cwd, cmd=["git", "clone", repo_url, full_repo_dir])

            if result.returncode != 0:
                answer = "We got an error from git clone repo."
                state.messages.append(
                    ChatMessageAssistant(
                        content=f"Error: {result.stderr}"
                    )
                )
                return state
            else:
                answer = result.stdout
                state.messages.append(
                    ChatMessageAssistant(
                        content=answer
                    )
                )


            # We add it to the safe directory
            _ = await sandbox(sandbox_name).exec(cmd=["git","config","--global","--add","safe.directory", full_repo_dir])

        except FileNotFoundError:
            answer = "We got an error from git clone repo."
            state.messages.append(
                ChatMessageAssistant(
                    content=answer
                )
            )

        return state

    return solve
