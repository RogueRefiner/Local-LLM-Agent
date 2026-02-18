from dataclasses import dataclass, field
from utils.logger.app_logger import ApplicationLogger
import os
from pathlib import Path
from string import Template
from ollama import chat
import re
import json


@dataclass
class ApiService:
    """API service for handling prompts and running them.

    Attributes:
        api_logger (ApplicationLogger): Logger for API operations

    Methods:
        build_final_prompt(prompt: str, template_name: str) -> str: Builds the final prompt using a specified template.
        run_prompt(prompt: str) -> None: Runs the given prompt through a chat model and prints the response.
        extract_json(text: str) -> str: Extracts JSON from a text string by removing any surrounding code blocks or syntax.
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

    def run_prompt(self, prompt: str) -> str:
        """Runs the provided prompt through a chat model.

        Args:
            prompt (str): The prompt to be sent to the chat model.
        """
        ret = ""
        self.api_logger.debug("Running prompt")
        response = chat(
            model="qwen2.5-coder:7b",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            options={
                "num_thread": 4,
                "num_flash_attn": True,
                "num_batch": 128,
                "num_ctx": 4096,
                "f16_kv": True,
            },
        )
        for chunk in response:
            msg_chunk = chunk.message.content
            if type(msg_chunk) == str:
                ret += msg_chunk
            print(msg_chunk, end="", flush=True)
        print("\n")
        return ret

    def extract_json(self, text: str) -> str:
        """
        Extracts JSON from a text string by removing any surrounding code blocks or syntax.

        Args:
            text (str): The text string containing JSON data.

        Returns:
            str: The extracted JSON data as a string.
        """
        cleaned = re.sub(
            r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE
        )
        return json.loads(cleaned)
