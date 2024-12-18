from fastapi import APIRouter

from api.v1 import router as v1_router
from api.v2 import router as v2_router
from api.v3 import router as v3_router
from api.v4 import router as v4_router


router = APIRouter()

router.include_router(v1_router, prefix="/v1", tags=["v.1.0 (Schema + Webpage Gemini)"])
router.include_router(v2_router, prefix="/v2", tags=["v2.0 (CSS Gemini)"])
router.include_router(v3_router, prefix="/v3", tags=["v3.0 (Fine-tuned GPT-4o)"])
router.include_router(v4_router, prefix="/v4", tags=["v4.0 (beta)"])