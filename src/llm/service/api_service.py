from dataclasses import dataclass, field
from utils.logger.app_logger import ApplicationLogger
import os
from pathlib import Path
from string import Template
from ollama import chat


@dataclass
class ApiService:
    """API service for handling prompts and running them.

    Attributes:
        api_logger (ApplicationLogger): Logger for API operations

    Methods:
        build_final_prompt(prompt: str, template_name: str) -> str: Builds the final prompt using a specified template.
        run_prompt(prompt: str) -> None: Runs the given prompt through a chat model and prints the response.

    """

    api_logger: ApplicationLogger = field(default_factory=lambda: ApplicationLogger())

    def build_final_prompt(self, prompt: str, template_name: str) -> str:
        """Builds the final prompt by substituting the template with the provided prompt.

        Args:
            prompt (str): The input prompt to be substituted.
            template_name (str): The name of the template file.

        Returns:
            str: The final prompt after substitution.

        Raises:
            AssertionError: If the template does not exist in the templates directory.
        """
        file_path = Path(f"templates/{template_name}.txt")

        try:
            assert os.path.exists(
                file_path
            ), f"Error {template_name} does not exists in {Path('templates/')}"
        except AssertionError as e:
            error_msg = f"Error when building final prompt template: {e}"
            self.api_logger.error(error_msg)
            raise AssertionError(error_msg)

        with open(file_path) as file:
            template = Template("\n".join(file.readlines()))
            prompt = template.safe_substitute(prompt=prompt)

        self.api_logger.debug("Fetched prompt tempate and injected the prompt")

        return prompt

    def run_prompt(self, prompt: str) -> None:
        """Runs the provided prompt through a chat model.

        Args:
            prompt (str): The prompt to be sent to the chat model.
        """
        self.api_logger.debug("Running prompt")
        response = chat(
            model="qwen2.5-coder:7b",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            options={
                "num_thread": 4,  # Match physical cores, not logical threads
                "num_flash_attn": True,  # Highly recommended for speed
                "num_batch": 128,  # Lowering from default 512 can help mobile CPUs
                "num_ctx": 4096,  # Keep this as small as your task allows
                "f16_kv": True,  # Uses half-precision for key/value cache
            },
        )
        for chunk in response:
            print(chunk.message.content, end="", flush=True)
        print("\n")
