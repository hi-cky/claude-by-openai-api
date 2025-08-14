from pydantic import BaseModel
from typing import Literal, Optional
from . import openai
import json

class Tool(BaseModel):
    name: str
    description: str
    input_schema: dict
    
    @classmethod
    def from_openai(cls, func: openai.Function) -> "Tool":
        return cls(
            name=func.name, 
            description=func.description, 
            input_schema=func.parameters.model_dump()
        )


class Message(BaseModel):
    role: Literal["user", "assistant", "tool"]
    content: str | list[dict]
    
    @classmethod
    def from_openai(cls, msg: openai.Message) -> "Message":
        match msg.role:
            case "tool" if msg.tool_call_id:
                return cls(
                    role="user",
                    content=[
                        {
                            "type": "tool_result",
                            "tool_use_id": msg.tool_call_id.replace("call", "toolu"),
                            "content": msg.content
                        }
                    ]
                )

            case "assistant" if msg.tool_calls:
                    return cls(
                        role="assistant",
                        content=[
                            {
                                "id": tool_call.id.replace("call", "toolu"),
                                "input": json.loads(tool_call.function.arguments),
                                "name": tool_call.function.name,
                                "type": "tool_use"
                            }
                            for tool_call in msg.tool_calls
                        ]
                    )

            case _ : # user | system | assistant
                result = cls(
                    role="user",
                    content=[]
                )
                if msg.content:
                    if isinstance(msg.content, str):
                        result.content = msg.content
                        
                    else:
                        result.content = [context.model_dump() for context in msg.content]
                return result


class Request(BaseModel):
    model: str
    messages: list[Message]
    temperature: float = 0.7
    max_tokens: int = 4000
    tools: Optional[list[Tool]] = None
    
    @classmethod
    def from_openai(cls, request: openai.Request) -> "Request":
        return cls(
            model=request.model,
            messages=[Message.from_openai(msg) for msg in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens if request.max_tokens is not None else 4000,
            tools=[Tool.from_openai(tool.function) for tool in request.tools]
        )
