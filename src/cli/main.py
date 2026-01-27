from pathlib import Path
import requests
from llm.utils.prompt_request import PromptRequest
import cutie
import os
from utils.logger.app_logger import ApplicationLogger
from dotenv import load_dotenv
import json

load_dotenv()
URL = os.getenv("LLM_URL", "http://localhost:8000/prompt")
cli_logger = ApplicationLogger()


def choose_template() -> str:
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


def choose_prompt_option() -> str:
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


def enter_prompt(prompt_option: str) -> str:
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
                cli_logger.error(error_msg)
                raise AssertionError(error_msg)

            with open(file_path) as file:
                prompt = "\n".join(file.readlines())
        case "enter prompt":
            prompt = input("Enter your prompt:\n")
        case _:
            prompt = input("Enter your prompt:\n")
    return prompt


def execute_prompt(prompt: str, template: str) -> requests.Response:
    """
    Execute a prompt using the specified template and return the response.

    Args:
        prompt (str): The prompt to execute.
        template (str): The template to use for executing the prompt.

    Returns:
        requests.Response: The response from the prompt execution.
    """
    prompt_request = PromptRequest(prompt=prompt, template_name=template)
    return requests.post(URL, prompt_request.toJSON())


if __name__ == "__main__":
    while True:
        template = choose_template()

        if template == "exit":
            exit()

        prompt_option = choose_prompt_option()
        prompt = enter_prompt(prompt_option)
        response = execute_prompt(prompt, template)
        print(f"\nResponse.status_code: {response.status_code}\n")
