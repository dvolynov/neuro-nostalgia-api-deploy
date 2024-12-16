from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from uuid import uuid4
import os

from .dependences import api_key
from .modules import generate_css


router = APIRouter()


@router.post("/retroify")
def retroify(
    url: str,
    model_name: str        = "gemini-1.5-pro",
    max_output_tokens: int = 8_192,
    temperature: float     = 1,
    request: Request       = None
    ):
    css, html = generate_css(url, api_key, model_name, max_output_tokens, temperature)

    page_id = str(uuid4())

    html = html.replace("<body>", f"<body>{css}")

    os.makedirs("api/v4/cache", exist_ok=True)

    with open(f"api/v4/cache/{page_id}.html", "w") as file:
        file.write(html)

    base_url = f"{request.url.scheme}://{request.url.hostname}"
    return {
        "url": f"{base_url}/api/v4/webpage/{page_id}",
        "css": css
    }


@router.get("/webpage/{page_id}", response_class=HTMLResponse)
async def webpage(page_id: str):
    file_path = f"api/v4/cache/{page_id}.html"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Page not found")

    with open(file_path, encoding="utf-8") as file:
        html = file.read()

    return HTMLResponse(content=html)