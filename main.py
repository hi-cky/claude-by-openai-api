from fastapi import FastAPI
from config import settings
from routers import openai, extras
from dependencies import streaming_perf_middleware

app = FastAPI(
    title="Claude to OpenAI API Adapter",
    description="API adapter for Claude models with OpenAI-style interface",
    version="1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 在创建app之后添加
app.middleware("http")(streaming_perf_middleware)

# 注册路由
app.include_router(openai.router, prefix="/api")
app.include_router(extras.router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "Claude to OpenAI API Adapter is running",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        'main:app', 
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )