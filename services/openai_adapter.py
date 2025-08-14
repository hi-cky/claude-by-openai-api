import time
from schemas import openai, claude
from .claude import claude_service
import anthropic

class OpenAIAdapter:
    @staticmethod
    def list_models():
        """获取可用模型列表"""
        return {
            "data": [
                {
                    "id": model_id,
                    "created": int(time.time()),
                    "owned_by": "anthropic"
                } for model_id in claude_service.available_models
            ]
        }


    @staticmethod
    async def create_chat_completion_stream(request: openai.Request):
        """创建OpenAI格式的流式响应生成器"""
        # 生成唯一的ID和时间戳
        response_id = f"chatcmpl-{int(time.time()*1000)}"
        created_time = int(time.time())
        fingerprint = "fp_" + hex(int(time.time() * 1000))[2:]

        try:
            stream = await claude_service.stream_complete(
                **claude.Request.from_openai(request).model_dump()
            )

            # 先发送角色消息
            yield openai.StreamResponse(
                id=response_id,
                created=created_time,
                model=request.model,
                choices=[openai.StreamChoice(
                    delta=openai.StreamChoiceDelta(role="assistant"),
                    finish_reason=None
                )],
                system_fingerprint=fingerprint
            ).model_dump_json()

            # 处理内容流
            tool_used = False  # 存储工具调用
            tool_call_input_buffer = ""
            current_content_block = None
            async for chunk in stream:
                match chunk.type:
                    case "content_block_start":
                        current_content_block = chunk.content_block

                    case "content_block_delta":
                        delta = chunk.delta
                        if not current_content_block:
                            continue
                        match current_content_block.type: # type: ignore
                            case "text":
                                # 发送文本块
                                yield openai.StreamResponse(
                                    id=response_id,
                                    created=created_time,
                                    model=request.model,
                                    choices=[openai.StreamChoice(
                                        delta=openai.StreamChoiceDelta(
                                            content=delta.text
                                        ),
                                    )],
                                    system_fingerprint=fingerprint
                                ).model_dump_json()

                            case "tool_use":
                                tool_call_input_buffer += delta.partial_json

                    case "content_block_stop":
                        if not current_content_block:
                            continue
                        match current_content_block.type: # type: ignore
                            case "tool_use":
                                # 工具调用请求
                                tool_call = openai.ToolCall(
                                    id="call_" + current_content_block.id.split('_')[1], # type: ignore
                                    function=openai.ToolCallFunction(
                                        name=current_content_block.name, # type: ignore
                                        arguments=tool_call_input_buffer
                                    )
                                )
                                tool_used = True

                                # 立即发送工具调用
                                yield openai.StreamResponse(
                                    id=response_id,
                                    created=created_time,
                                    model=request.model,
                                    choices=[openai.StreamChoice(
                                        index=0,
                                        delta=openai.StreamChoiceDelta(
                                            tool_calls=[tool_call]
                                        ),
                                        finish_reason=None
                                    )],
                                    system_fingerprint=fingerprint
                                ).model_dump_json()

                        current_content_block = None

            yield openai.StreamResponse(
                id=response_id,
                created=created_time,
                model=request.model,
                choices=[openai.StreamChoice(
                    index=0,
                    delta=openai.StreamChoiceDelta(),
                    finish_reason="tool_calls" if tool_used else "stop"
                )],
                system_fingerprint=fingerprint
            ).model_dump_json()

        except Exception as e:
            # 错误处理
            error_type = "api_error" if isinstance(e, anthropic.APIError) else "internal_error"
            code = e.status_code if hasattr(e, "status_code") else 500 # type: ignore

            error_response = {
                "id": response_id,
                "created": created_time,
                "model": request.model,
                "choices": [],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                },
                "error": {
                    "message": str(e),
                    "type": error_type,
                    "code": code
                }
            }
            print("error!!!!!", error_response)
            yield error_response
