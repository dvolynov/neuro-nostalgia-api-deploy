from fastapi import APIRouter, Request
from uuid import uuid4

from .dependences import *
from ..dependences import *

from .modules import generate_retro_website
from ..tools import bot


router = APIRouter()


@router.post("/generate")
def generate(
        url: str,
        creativity: int = 100,
        accuracy: int = 100,
        request: Request = None
    ):
    os.makedirs("api/cache", exist_ok=True)

    temperature = 2 * (creativity / 100)
    topP = (100 - accuracy) / 100

    html = generate_retro_website(url, api_key, html_assistant_id, topP, temperature)
    page_id = str(uuid4())

    with open(f"api/cache/{page_id}.html", "w") as file:
        file.write(html)

    base_url = f"{request.url.scheme}://{request.url.hostname}"
    generated_url = f"{base_url}/{page_id}"

    bot.send_message(
        text=f"""
Url:  {url}
Version:  `API v3.0`
Creativity:  `{creativity}`
Accuracy:  `{accuracy}`
Status:  `{"success ✅" if html else "error ❌"}`
Result:  {generated_url}
        """,
        chat_id=telegram_chat_id,
        token=telegram_bot_token,
    )

    return {"url": generated_url}