from cli.controller.cli_controller import CliController
from utils.logger.app_logger import ApplicationLogger
import json
import requests

if __name__ == "__main__":
    cli_controller = CliController()
    logger = ApplicationLogger()

    while True:
        template = cli_controller.choose_template()

        if template == "exit":
            exit()

        prompt_option = cli_controller.choose_prompt_option()
        prompt = cli_controller.enter_prompt(prompt_option)
        response = cli_controller.execute_prompt(prompt, template)
        logger.debug(
            f"Response: {response.content}\nResponse.status_code: {response.status_code}\n"
        )

        try:
            url, endpoint, headers, parameters = cli_controller.parse_response(
                json.loads(response.content)["response"]
            )

            response = requests.post(
                url=f"{url}{endpoint}", json=parameters, headers=headers
            )
            logger.debug(
                f"response.status_code: {response.status_code}, response.text: {response.text}"
            )

        except Exception as e:
            logger.error(f"Failed to parse parameters from llm response: {response}")
