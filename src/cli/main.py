from cli.controller.cli_controller import CliController

if __name__ == "__main__":
    cli_controller = CliController()
    while True:
        template = cli_controller.choose_template()

        if template == "exit":
            exit()

        prompt_option = cli_controller.choose_prompt_option()
        prompt = cli_controller.enter_prompt(prompt_option)
        response = cli_controller.execute_prompt(prompt, template)
        print(f"\nResponse.status_code: {response.status_code}\n")
