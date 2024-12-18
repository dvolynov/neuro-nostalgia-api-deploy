from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from endpoints.page import router as page_router


app = FastAPI(title="Neuro-Nostalgia-API")

app.include_router(api_router, prefix="/api")
app.include_router(page_router, prefix="")


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)