from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import settings

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def validate_api_key(authorization: str = Security(api_key_header)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key"
        )

    if authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        if token == settings.OPENAI_API_KEY:
            return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key"
    )
    
    
import time
from fastapi import Request

async def streaming_perf_middleware(request: Request, call_next):
    start_time = time.time()
    
    # 调用路由
    response = await call_next(request)
    
    # 如果是流式响应且包含Transfer-Encoding头部
    if "Transfer-Encoding" in response.headers and response.headers["Transfer-Encoding"] == "chunked":
        duration = time.time() - start_time
        print(f"Streaming request completed in {duration:.2f}s")
        
    return response