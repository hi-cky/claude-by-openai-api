from fastapi import APIRouter, Depends
from schemas import openai
from dependencies import validate_api_key
from services.openai_adapter import OpenAIAdapter
from fastapi.responses import StreamingResponse, Response

router = APIRouter()


@router.get("/v1/models", dependencies=[Depends(validate_api_key)])
async def list_models():
    pass
    # return OpenAIAdapter.list_models()


@router.options("/v1/chat/completions")
async def handle_options():
    """处理OPTIONS预检请求"""
    return Response(
        status_code=204,
        headers={
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Origin": "*"
        }
    )

@router.post("/v1/chat/completions", dependencies=[Depends(validate_api_key)])
async def create_chat_completion(request: openai.Request):
    """处理聊天完成请求（支持流式）"""

    # 非流式处理
    if not request.stream:
        pass
        
    # 流式处理
    async def event_stream():
        async for chunk in OpenAIAdapter.create_chat_completion_stream(request): # type: ignore
            # print("chunk:", chunk)
            # 将数据格式化为SSE事件
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Transfer-Encoding': 'chunked'
        }
    )
