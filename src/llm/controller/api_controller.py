from dataclasses import dataclass, field
from llm.service.api_service import ApiService
from utils.logger.app_logger import ApplicationLogger


@dataclass
class ApiControlller:
    """
    A class for managing API requests and handling prompts.

    Attributes:
        template_dict (dict[str, str]): A dictionary of template names to their file paths.
            Defaults to a lambda function that returns `{"example": "example.txt"}`.
        api_service (ApiService): An instance of the ApiService class used for building and running prompts.
            Defaults to a lambda function that returns an instance of ApiService.

    Methods:
        build_final_prompt(prompt: str, template_name: str) -> str:
            Builds the final prompt by combining the input prompt with the specified template.
        run_prompt(prompt: str) -> None: Runs the provided prompt using the api_service.
    """

    template_dict: dict[str, str] = field(
        default_factory=lambda: {"example": "example.txt"}
    )
    api_service: ApiService = field(default_factory=lambda: ApiService())

    def build_final_prompt(self, prompt: str, template_name: str) -> str:
        """
        Builds the final prompt by combining the input prompt with the specified template.

        Args:
            prompt (str): The input prompt to be combined with the template.
            template_name (str): The name of the template to use for building the prompt.

        Returns:
            str: The final prompt built using the input prompt and the specified template.
        """
        return self.api_service.build_final_prompt(prompt, template_name)

    def run_prompt(self, prompt: str) -> None:
        """
        Runs the provided prompt using the api_service.

        Args:
            prompt (str): The prompt to be run.
        """
        self.api_service.run_prompt(prompt)


def get_api_controller() -> ApiControlller:
    """
    Returns a new instance of ApiControlller.

    Returns:
        ApiControlller: A new instance of ApiControlller with default values for its attributes.
    """
    return ApiControlller()
