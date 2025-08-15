import time
import json
from schemas import openai
from .claude import claude_service
import anthropic
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIAdapter:
    @staticmethod
    def list_models() -> dict:
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
    async def create_openai_stream_from_claude(stream: anthropic.AsyncStream, model_name: str):
        """创建OpenAI格式的流式响应生成器"""
        response_id = f"chatcmpl-{int(time.time()*1000)}"
        created_time = int(time.time())
        fingerprint = "fp_" + hex(int(time.time() * 1000))[2:]
        
        tool_used = False

        try:
            # Send role message first
            yield f"data: {json.dumps(openai.StreamResponse(
                id=response_id,
                created=created_time,
                model=model_name,
                choices=[openai.StreamChoice(
                    delta=openai.StreamChoiceDelta(role="assistant"),
                    finish_reason=None
                )],
                system_fingerprint=fingerprint
            ).model_dump(exclude_none=True))}\n\n"

            # Process the stream
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

                        match current_content_block.type:
                            case "text":
                                yield f"data: {json.dumps(openai.StreamResponse(
                                    id=response_id,
                                    created=created_time,
                                    model=model_name,
                                    choices=[openai.StreamChoice(
                                        delta=openai.StreamChoiceDelta(
                                            content=delta.text
                                        ),
                                    )],
                                    system_fingerprint=fingerprint
                                ).model_dump(exclude_none=True))}\n\n"

                            case "tool_use":
                                tool_call_input_buffer += delta.partial_json

                    case "content_block_stop":
                        if not current_content_block:
                            continue

                        match current_content_block.type:
                            case "tool_use":
                                tool_call = openai.ToolCall(
                                    id="call_" + current_content_block.id.split('_')[1],
                                    function=openai.ToolCallFunction(
                                        name=current_content_block.name,
                                        arguments=tool_call_input_buffer
                                    )
                                )
                                tool_used = True

                                yield f"data: {json.dumps(openai.StreamResponse(
                                    id=response_id,
                                    created=created_time,
                                    model=model_name,
                                    choices=[openai.StreamChoice(
                                        index=0,
                                        delta=openai.StreamChoiceDelta(
                                            tool_calls=[tool_call]
                                        ),
                                        finish_reason=None
                                    )],
                                    system_fingerprint=fingerprint
                                ).model_dump(exclude_none=True))}\n\n"

                        current_content_block = None

        except Exception as e:
            # Handle streaming errors gracefully
            logging.error(f"Streaming error: {e}")
            error_chunk = {
                "error": {
                    "type": "stream_error",
                    "message": "An error occurred during streaming"
                }
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"
            
        finally:
            # Send final chunk
            yield f"data: {json.dumps(openai.StreamResponse(
                id=response_id,
                created=created_time,
                model=model_name,
                choices=[openai.StreamChoice(
                    index=0,
                    delta=openai.StreamChoiceDelta(),
                    finish_reason="tool_calls" if tool_used else "stop"
                )],
                system_fingerprint=fingerprint
            ).model_dump(exclude_none=True))}\n\n"
            # 流结束时的清理
            yield "data: [DONE]\n\n"
