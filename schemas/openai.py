from pydantic import BaseModel
from typing import Literal, Optional

class Parameters(BaseModel):
    type: Literal["object"]
    properties: dict
    required: Optional[list[str]] = None

class Function(BaseModel):
    name: str
    description: str
    parameters: Parameters

class Tool(BaseModel):
    type: Literal["function"] = "function"
    function: Function


class ToolCallFunction(BaseModel):
    name: str
    arguments: str

class ToolCall(BaseModel):
    id: str
    index: int = 0
    type: Literal["function"] = "function"
    function: ToolCallFunction

class Context(BaseModel):
    type: Literal["text"] = "text"
    text: str

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str | list[Context] | None
    tool_calls: Optional[list[ToolCall]] = None
    tool_call_id: Optional[str] = None


class Request(BaseModel):
    model: str
    messages: list[Message]
    temperature: float
    tools: list[Tool]
    tool_choice: Optional[Literal["auto"]] = "auto"
    max_tokens: Optional[int] = None
    stream: bool = True



# response
class StreamChoiceDelta(BaseModel):
    role: Optional[Literal["assistant", "tool"]] = None
    content: Optional[str] = None
    tool_calls: Optional[list[ToolCall]] = None


class StreamChoice(BaseModel):
    index: int = 0
    delta: StreamChoiceDelta
    finish_reason: Optional[Literal["stop", "tool_calls"]] = None


class StreamResponse(BaseModel):
    id: str
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int
    model: str
    choices: list[StreamChoice]
    system_fingerprint: str
