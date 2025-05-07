from inspect_ai.solver import (solver, Generate)
from inspect_ai.solver._task_state import TaskState
from inspect_ai.util import sandbox

from inspect_ai.model import (
    ChatMessageAssistant,
    ModelOutput,
)

import logging
# setup logger for this source file
logger = logging.getLogger(__name__)

from ._settings import BaseSettings

class CodexSettings(BaseSettings):

    agent_name = "codex"
    cwd = None
    sandbox_name = None
    cmd =  "codex"
    prompt_filename = "prompt.txt"
    repo_dir = "."

    metadata_fields = {
        "sandbox_name": "sandbox_name",
        "cmd": "cmd",
        "repo_dir": "repo_dir",
        "prompt_filename": "prompt_filename",
    }

@solver
def codex_coder(sandbox_name=None, cmd=None, repo_dir=None, prompt_filename=None):

    async def solve(state: TaskState, generate: Generate) -> TaskState:

        # completion = state.output.completion  # last completion
        settings = CodexSettings()
        nonlocal repo_dir, prompt_filename,  cmd, sandbox_name
        settings.update({
            "sandbox_name": sandbox_name,
            "cmd": cmd,
            "repo_dir": repo_dir,
            "prompt_filename": prompt_filename
        }, state)

        # question=state.input_text #initial request
        question = state.user_prompt.content  # updated prompt via promptemplate solver
        logger.info("question to %s : %s", settings.agent_name, question)

        # default reply
        answer = f"We received no answer from {settings.agent_name}."

        try:
            # Codex does not have a way to accept a prompt from a file
            # We write the prompt into a file to avoid stdin issues
            # await sandbox(sandbox_name).write_file(
            #    default_prompt_filename, contents=question)

            logger.info("making sure ~/.codex exists")
            _ = await sandbox(settings.sandbox_name).exec(cmd = ["mkdir", "-p", "~/.codex"])
            last_update = '{"lastUpdateCheck": "Wed, 07 May 2025 20:24:34 GMT"}'
            logger.info("writing ~/.codex/update-check.json")
            _ = await sandbox(settings.sandbox_name).write_file("~/.codex/update-check.json", contents=last_update)
            # -q trigger json mode
            # but on first run it will notify us
            # {"lastUpdateCheck": "Tue, 06 May 2025 20:24:34 GMT"}
            # ~/.codex/update-check.json
            # ~/.codex/instructions.md extra instructions

            logger.info("cwd =  %s", settings.repo_dir)

            result = await sandbox(settings.sandbox_name).exec(cwd=settings.repo_dir, cmd=[
                settings.cmd, "-q", "--approval-mode", "full-auto", question])

            # We set the answer
            answer = result.stdout

            if (result.returncode != 0) or (answer == ""):
                answer = f"We got an error from {settings.agent_name}."
                logger.error("error : %s", result)
                state.messages.append(
                    ChatMessageAssistant(
                        content=f"Error: {result.stderr}"
                    )
                )
                return state

            logger.info("%s result : %s", settings.agent_name, answer)
        except FileNotFoundError:
            answer = f"Something went wrong with {settings.agent_name}."

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
