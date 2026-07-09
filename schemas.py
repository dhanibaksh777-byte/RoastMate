from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message : str
    session_id : Optional[str] = None


class ChatResponse(BaseModel):
    response : str
    session_id : str


class MessageItem(BaseModel):
    role : str
    content : str


class HistoryResponse(BaseModel):
    session_id = str
    messages = list[MessageItem]







# from pydantic import BaseModel
# from typing import Optional


# class ChatRequest(BaseModel):
#     message : str
#     session_id : Optional[str] = None
    
# class ChatResponse(BaseModel):
#     response : str
#     session_id : str

    