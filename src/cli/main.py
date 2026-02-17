from cli.controller.cli_controller import CliController
from utils.logger.app_logger import ApplicationLogger

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
            f"Response: {response}\nResponse.status_code: {response.status_code}\n"
        )
        endpoint, parfameters = cli_controller.parse_response(response)
