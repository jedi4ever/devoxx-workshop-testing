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

class ClaudeSettings(BaseSettings):

    agent_name = "claude"

    # defaults
    cwd = None
    sandbox_name = None
    cmd =  "claude"
    prompt_filename = "prompt.txt"
    repo_dir = "."

    metadata_fields = {
        "sandbox_name": "sandbox_name",
        "cmd": "cmd",
        "repo_dir": "repo_dir",
        "prompt_filename": "prompt_filename",
    }

@solver
def claude_coder(sandbox_name=None, cmd=None, repo_dir=None, prompt_filename=None, cwd=None):

    async def solve(state: TaskState, generate: Generate) -> TaskState:

        # Configure settings
        nonlocal repo_dir, sandbox_name, cmd, prompt_filename, cwd
        settings = ClaudeSettings()
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

        # default reply
        answer = f"We received no answer from {settings.agent_name}."

        try:
            # Codex does not have a way to accept a prompt from a file
            # We write the prompt into a file to avoid stdin issues
            # await sandbox(sandbox_name).write_file(
            #    default_prompt_filename, contents=question)

            # https://github.com/anthropics/claude-code/issues/581
            # "--dangerously-skip-permissions" 
            # https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview#tools-available-to-claude
            result = await sandbox(sandbox_name).exec(cwd=settings.repo_dir, cmd=[
                settings.cmd, "-p", question, "--allowedTools", "WebFetch(domain:*)", "Edit", "Write"])


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
            logger.info("%s coder result : %s",settings.agent_name, answer)
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
