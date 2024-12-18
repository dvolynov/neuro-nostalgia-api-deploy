from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
import os


router = APIRouter()


@router.get("/{page_id}", response_class=HTMLResponse)
async def webpage(page_id: str, request: Request):
    file_path = f"api/cache/{page_id}.html"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Page not found")

    with open(file_path, encoding="utf-8") as file:
        html = file.read()

    return HTMLResponse(content=html)