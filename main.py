from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import router as v1_router
from api.v2 import router as v2_router
from api.v3 import router as v3_router
from api.v4 import router as v4_router


app = FastAPI(title="Neuro-Nostalgia-API")
app.include_router(v1_router, prefix="/api/v1", tags=["v1.0 (schema + webpage)"])
app.include_router(v2_router, prefix="/api/v2", tags=["v2.0 (css only)"])
app.include_router(v3_router, prefix="/api/v3", tags=["v3.0 (GPT-40 based)"])
app.include_router(v4_router, prefix="/api/v4", tags=["v4.0 (Article)"])

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)