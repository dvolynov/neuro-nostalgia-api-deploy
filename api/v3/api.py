from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from uuid import uuid4
import os

from .dependences import api_key, html_assistant_id
from .modules import generate_retro_website


router = APIRouter()


@router.post("/retroify")
def retroify(url: str, request: Request):
    os.makedirs("api/v3/cache", exist_ok=True)
    
    html = generate_retro_website(url, api_key, html_assistant_id)

    page_id = str(uuid4())

    with open(f"api/v3/cache/{page_id}.html", "w") as file:
        file.write(html)

    base_url = f"{request.url.scheme}://{request.url.hostname}"
    return {
        "url": f"{base_url}/api/v3/webpage/{page_id}",
        "html": html
    }


@router.get("/webpage/{page_id}", response_class=HTMLResponse)
async def webpage(page_id: str):
    file_path = f"api/v3/cache/{page_id}.html"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Page not found")

    with open(file_path, encoding="utf-8") as file:
        html = file.read()

    return HTMLResponse(content=html)