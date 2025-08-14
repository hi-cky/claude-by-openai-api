from fastapi import APIRouter
import random
from services.openai_adapter import OpenAIAdapter

router = APIRouter()

@router.get("/v1/health")
def health_check():
    pass
    # return {
    #     "status": "ok",
    #     "version": "1.0",
    #     "models_available": len(OpenAIAdapter.list_models().data)
    # }

@router.get("/v1/system/status")
def system_status():
    return {
        "load": random.uniform(0.1, 0.7),
        "memory": random.uniform(30, 80),
        "active_connections": random.randint(5, 50)
    }