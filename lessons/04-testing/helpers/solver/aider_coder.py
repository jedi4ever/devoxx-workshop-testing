from inspect_ai.solver import (solver, Generate)
from inspect_ai.solver._task_state import TaskState
from inspect_ai.util import sandbox

from inspect_ai.model import (
    ChatMessageAssistant,
    ModelOutput,
)

import os
import logging
# setup logger for this source file
logger = logging.getLogger(__name__)
from datetime import datetime
from uuid import uuid4

from ._settings import BaseSettings

class AiderSettings(BaseSettings):

    agent_name = "aider"

    cwd = None
    sandbox_name = None
    cmd =  "aider"
    prompt_filename = "prompt.txt"
    repo_dir = "."

    metadata_fields = {
        "sandbox_name": "sandbox_name",
        "cmd": "cmd",
        "repo_dir": "repo_dir",
        "prompt_filename": "prompt_filename",
    }


@solver
def aider_coder(sandbox_name=None, cmd=None, repo_dir=None, prompt_filename=None, cwd=None):
 
    async def solve(state: TaskState, generate: Generate) -> TaskState:

        # Configure settings
        nonlocal repo_dir, sandbox_name, cmd, prompt_filename, cwd
        settings = AiderSettings()
        settings.update({
            "sandbox_name": sandbox_name,
            "cmd": cmd,
            "repo_dir": repo_dir,
            "prompt_filename": prompt_filename,
            "cwd": cwd
        },state)

        # question=state.input_text #initial request
        question = state.user_prompt.content  # updated prompt via promptemplate solver
        logger.info("question to %s : %s", settings.agent_name, question)

        # completion = state.output.completion  # last completion

        # generate unique prompt filename
        eventid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        # logger.info("eventid: %s", eventid)
        full_prompt_filename = os.path.join("/tmp", settings.prompt_filename + "-" + eventid)
        logger.info("prompt filename: %s", full_prompt_filename)

        # default reply
        answer = f"We received no answer from {settings.agent_name}."

        try:
            # https://aider.chat/docs/scripting.html
            # We write the prompt into a file to avoid stdin issues
            await sandbox(settings.sandbox_name).write_file(
                full_prompt_filename, contents=question)

            # We add it to the safe directory
            #full_repo_dir = os.path.join(cwd, repo_dir)

            _ = await sandbox(settings.sandbox_name).exec(cmd=["git","config","--global","--add","safe.directory", settings.repo_dir])

            # Run aider
            result = await sandbox(settings.sandbox_name).exec(cwd=settings.repo_dir,
                            cmd=[settings.cmd, "--yes", "--message-file", full_prompt_filename])

            if result.returncode != 0:
                answer = f"We got an error from {settings.agent_name}."
                logger.error("error : %s", result)

                state.messages.append(
                    ChatMessageAssistant(
                        content=f"Error: {result.stderr}"
                    )
                )
                return state
            
            # We set the answer
            answer = result.stdout
            logger.info("%s result : %s", settings.agent_name, answer)
        except (ValueError, IsADirectoryError, PermissionError) as ex:
            answer = f"Something went wrong with {settings.agent_name}: {ex}"

        # We add the answer to the chat history
        state.messages.append(
            ChatMessageAssistant(
                content=answer
            )
        )

        # state.output is not a string
        # gives error : 'A custom validator is returning a value other than `self`.\n'
        # also can pass along errors here
        model_answer = ModelOutput.from_content(settings.agent_name, content=answer)
        state.output = model_answer

        return state

    return solve
