from dataclasses import dataclass, field
from typing import Any

import requests
from cli.service.cli_service import CliService


@dataclass
class CliController:
    """
    Attributes:
        cli_service (CliService): The service for handling CLI operations.

    Methods:
        choose_template() -> str: Choose a template from available options.
        choose_prompt_option() -> str: Choose a prompt option from available options.
        enter_prompt(prompt_option: str) -> str: Enter a prompt based on the selected option.
        execute_prompt(prompt: str, template: str) -> requests.Response: Execute a prompt using the specified template and return the response.
    """

    cli_service: CliService = field(default_factory=lambda: CliService())

    def choose_template(self) -> str:
        """
        Choose a template from available options.

        Args:
            None

        Returns:
            str: Selected template.

        """
        return self.cli_service.choose_template()

    def choose_prompt_option(self) -> str:
        """
        Choose a prompt option from available options.

        Args:
            None

        Returns:
            str: Selected prompt option.
        """
        return self.cli_service.choose_prompt_option()

    def enter_prompt(self, prompt_option: str) -> str:
        """
        Enter a prompt based on the selected option.

        Args:
            prompt_option (str): The option for entering the prompt.

        Returns:
            str: The entered prompt.
        """
        return self.cli_service.enter_prompt(prompt_option)

    def execute_prompt(self, prompt: str, template: str) -> requests.Response:
        """
        Execute a prompt using the specified template and return the response.

        Args:
            prompt (str): The prompt to execute.
            template (str): The template to use for executing the prompt.

        Returns:
            requests.Response: The response from the prompt execution.
        """
        return self.cli_service.execute_prompt(prompt, template)

    def parse_response(self, response: requests.Response) -> tuple[str, dict[str, Any]]:
        # TODO:
        return self.cli_service.parse_response(response)
