from fastapi import APIRouter, Depends, HTTPException
from schemas import openai, claude
from dependencies import validate_api_key
from services.openai_adapter import OpenAIAdapter
from services.claude import claude_service
from fastapi.responses import StreamingResponse, Response

router = APIRouter()


@router.get("/v1/models", dependencies=[Depends(validate_api_key)])
async def list_models():
    return OpenAIAdapter.list_models()


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
        raise HTTPException(status_code=400, detail="Non-streaming requests are not supported.")

    try:
        # 初始化阶段可能抛出的异常应该直接raise，让外层处理
        claude_stream = await claude_service.stream_complete(
            **claude.Request.from_openai(request)
            .model_dump()
        )
        # 获取第一个 chunk 查看是否正常
        first_chunk = await claude_stream.__anext__()
        print(first_chunk)

        return StreamingResponse(
            OpenAIAdapter.create_openai_stream_from_claude(claude_stream, first_chunk.message.model),
            media_type="text/event-stream",
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Transfer-Encoding': 'chunked'
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
