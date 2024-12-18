from fastapi import APIRouter, Request
from uuid import uuid4

from .dependences import *
from ..dependences import *

from .modules import generate_css
from ..tools import bot


router = APIRouter()


@router.post("/generate")
def generate(
    url: str,
    model_name: str        = "gemini-1.5-flash",
    max_output_tokens: int = 8_192,
    creativity: int        = 100,
    request: Request       = None
    ):

    temperature = 2 * creativity / 100
    css, html = generate_css(url, api_key, model_name, max_output_tokens, temperature)
    page_id = str(uuid4())
    html = html.replace("<body>", f"<body>{css}")

    with open(f"api/cache/{page_id}.html", "w") as file:
        file.write(html)

    base_url = f"{request.url.scheme}://{request.url.hostname}"
    generated_url = f"{base_url}/{page_id}"

    bot.send_message(
        text=f"""
Url:  {url}
Version:  `API v2.0`
Creativity:  `{creativity}`
Model:  `{model_name}`
Max Output Tokens:  `{max_output_tokens}`
Status:  `{"success ✅" if html else "error ❌"}`
Result:  {generated_url}
        """,
        chat_id=telegram_chat_id,
        token=telegram_bot_token,
    )

    return {"url": generated_url}