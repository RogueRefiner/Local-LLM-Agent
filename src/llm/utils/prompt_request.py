from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str
    template_name: str
