import httpx
import json

# 流式调用
async def stream_chat():
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": "Bearer sk-REPLACE_ME",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }

        payload = {
            "model": "claude-sonnet-4-20250514",
            "messages": [{"role": "user", "content": "quick sort"}],
            "stream": True
        }

        async with client.stream(
            "POST",
            "http://localhost:8000/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30.0
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    data_str = line.split("data: ", 1)[1].strip()
                    if data_str == "[DONE]":
                        print("\n\nStream completed")
                        break

                    try:
                        data = json.loads(data_str)
                        if "choices" in data:
                            for choice in data["choices"]:
                                if "delta" not in choice:
                                    continue
                                if "content" in choice["delta"] and choice["delta"]["content"]:
                                    print(choice["delta"]["content"], end="", flush=True)
                                    
                                if "reasoning_content" in choice["delta"] and choice["delta"]["reasoning_content"]:
                                    print(choice["delta"]["reasoning_content"], end="", flush=True)
                    except json.JSONDecodeError:
                        print(f"Invalid JSON: {data_str}")

# 运行
import asyncio
asyncio.run(stream_chat())
