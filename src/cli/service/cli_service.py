from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import cutie
import requests
from llm.utils.prompt_request import PromptRequest
from dotenv import load_dotenv
from utils.logger.app_logger import ApplicationLogger

load_dotenv()


@dataclass
class CliService:
    """
    Attributes:
        llm_url (str): The URL for language model operations.
        cli_logger (ApplicationLogger): The logger for CLI operations.

    Methods:
        choose_template() -> str: Choose a template from available options.
        choose_prompt_option() -> str: Choose a prompt option from available options.
        enter_prompt(prompt_option: str) -> str: Enter a prompt based on the selected option.
        execute_prompt(prompt: str, template: str) -> requests.Response: Execute a prompt using the specified template and return the response.
    """

    llm_url: str = field(
        default_factory=lambda: os.getenv("LLM_URL", "http://localhost:8000/prompt")
    )
    cli_logger: ApplicationLogger = field(default_factory=lambda: ApplicationLogger())

    def choose_template(self) -> str:
        """
        Choose a template from available options.

        Args:
            None

        Returns:
            str: Selected template.

        """
        templates = json.loads(os.getenv("TEMPLATES", '["Templates:", "generate_docstring", "example", "exit"]'))  # type: ignore
        return templates[
            cutie.select(templates, caption_indices=[0], selected_index=len(templates))  # type: ignore
        ]

    def choose_prompt_option(self) -> str:
        """
        Choose a prompt option from available options.

        Args:
            None

        Returns:
            str: Selected prompt option.
        """
        prompt_options = json.loads(
            os.getenv("PROMPT_OPTIONS", '["Prompt Options:", "file", "enter prompt"]')
        )
        return prompt_options[
            cutie.select(
                prompt_options, caption_indices=[0], selected_index=len(prompt_options)
            )
        ]

    def enter_prompt(self, prompt_option: str) -> str:
        """
        Enter a prompt based on the selected option.

        Args:
            prompt_option (str): The option for entering the prompt.

        Returns:
            str: The entered prompt.
        """
        match prompt_option:
            case "file":
                file_path = Path(
                    f'files/{input("Enter the file name without file ending (e.g. example):\n")}.txt'
                )
                try:
                    assert os.path.exists(
                        file_path
                    ), f"Error {file_path} does not exist in {Path('files')}"
                except AssertionError as e:
                    error_msg = f"Error when fetching file containing prompt: {e}"
                    self.cli_logger.error(error_msg)
                    raise AssertionError(error_msg)

                with open(file_path) as file:
                    prompt = "\n".join(file.readlines())
            case "enter prompt":
                prompt = input("Enter your prompt:\n")
            case _:
                prompt = input("Enter your prompt:\n")
        return prompt

    def execute_prompt(self, prompt: str, template: str) -> requests.Response:
        """
        Execute a prompt using the specified template and return the response.

        Args:
            prompt (str): The prompt to execute.
            template (str): The template to use for executing the prompt.

        Returns:
            requests.Response: The response from the prompt execution.
        """
        prompt_request = PromptRequest(prompt=prompt, template_name=template)
        return requests.post(self.llm_url, prompt_request.toJSON())
