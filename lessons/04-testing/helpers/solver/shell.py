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

from ._settings import BaseSettings

class ScriptSettings(BaseSettings):

    sandbox_name = None
    command = ""

    metadata_fields = {
        "sandbox_name": "sandbox_name",
        "command": "command",
    }

@solver
def script_exec(command=None, sandbox_name=None, cwd=None):

    async def solve(state: TaskState, generate: Generate) -> TaskState:

        # Configure settings
        nonlocal command, sandbox_name, cwd
        settings = ScriptSettings()
        settings.update({
            "sandbox_name": sandbox_name,
            "command": command,
        }, state)

        logger.info("command : **%s**", settings.command)

        answer = "We received no answer from script exec."
        try:
            result = await sandbox(settings.sandbox_name).exec(cwd=cwd, cmd=["sh", "-c", settings.command])

            if result.returncode != 0:
                answer = "We got an error from script exec."
                state.messages.append(
                    ChatMessageAssistant(
                        content=f"Error: {result.stderr}"
                    )
                )
                return state
            else:
                answer = result.stdout
                logger.info("script exec result : %s", answer)
                state.messages.append(
                    ChatMessageAssistant(
                        content=answer
                    )
                )

        except FileNotFoundError:
            answer = "We got an error from script exec"
            state.messages.append(
                ChatMessageAssistant(
                    content=answer
                )
            )

        return state

    return solve
