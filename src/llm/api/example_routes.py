from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from llm.controller.api_controller import get_api_controller, ApiControlller
from llm.utils.prompt_request import PromptRequest
from utils.logger.app_logger import ApplicationLogger, get_application_logger

router = APIRouter()


@router.post("/prompt")
async def execute_prompt(
    request: PromptRequest,
    api_controller: ApiControlller = Depends(get_api_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> None:
    """
    Executes a prompt using the provided request data.

    Args:
        request (PromptRequest): The request containing the prompt and template name.
        api_controller (ApiControlller, optional): Dependency for API controller logic. Defaults to the dependency injected instance.
        api_logger (ApplicationLogger, optional): Dependency for application logging. Defaults to the dependency injected instance.

    Returns:
        None
    """
    api_logger.debug(f"/prompt endpoint called with request: {request}")
    prompt = api_controller.build_final_prompt(request.prompt, request.template_name)
    api_controller.run_prompt(prompt)
    api_logger.debug(f"prompt execution finished")
