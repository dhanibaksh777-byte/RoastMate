from fastapi import FastAPI,Depends
from groq_client import get_roast
from sqlalchemy.orm import Session
from models import Message
from database import engine,get_db
from system_prompt import SYSTEM_PROMPT
from schemas import ChatRequest,ChatResponse,MessageItem,HistoryResponse
from fastapi import HTTPException
import uuid



app = FastAPI()





@app.post("/chat")
def chat(request : ChatRequest,db : Session = Depends(get_db)):
    session_id = request.session_id
    if session_id is None:
        session_id = str(uuid.uuid4())

    else:
        session_id = request.session_id


    old_messages = db.query(Message).filter(Message.session_id == session_id).all()

    conversation = []
    conversation.append({"role" : "system", "content":SYSTEM_PROMPT})

    for msgs in old_messages:
        conversation.append({"role" : "user ", "content" : request.message})

        conversation.append({"role" : msgs.role, "content" : msgs.content})

        try:
            bot_reply = get_roast(conversation)

            UserMsg = Message(session_id = session_id, role = "user", content = request.message)
            BotMsg = Message(session_id = session_id,role = "assistant", content = bot_reply)
            db.add(UserMsg)
            db.add(BotMsg)
            db.commit()
            return ChatResponse(session_id = session_id,response = bot_reply)

        except Exception as e:
            raise HTTPException(status_code=500,detail="bot is currently unavailable")
        


@app.get("/history/{session_id}")
def chat(session_id : str, db : Session = Depends(get_db)):
    fetch_db = db.query(Message).filter(Message.session_id == session_id).all()
    messages_list = []
    for msgs in fetch_db:
        messages_list.append(MessageItem(role=msgs.role,content = msgs.content))

    return HistoryResponse(session_id = session_id,messages = messages_list)

@app.delete("/history/{session_id}")
def chat(session_id : str, db : Session = Depends(get_db)):
    message = db.query(Message).filter(Message.session_id == session_id).all()
    for msgs in message:
        db.delete(msgs)
    db.commit()

    return {"message": "chat is deleted!"}




        



































# from fastapi import FastAPI,Depends
# from sqlalchemy.orm import Session
# from database import engine,get_db
# from system_prompt import SYSTEM_PROMPT
# from groq_client import get_roast
# from models import Message
# from schemas import ChatRequest,ChatResponse
# from fastapi import HTTPException
# import uuid


# app = FastAPI()


# @app.post("/chat")
# def chat(request : ChatRequest, db : Session = Depends(get_db)):
#     session_id = request.session_id
#     if session_id is None:
#         session_id = str(uuid.uuid4())

#     else:
#         session_id = request.session_id

#     old_messages = db.query(Message).filter(Message.session_id == session_id).all()

#     conversation = []
#     conversation.append({"role": "system", "content": SYSTEM_PROMPT})

#     for msgs in old_messages:
#         conversation.append({"role": msgs.role, "content": msgs.content})

#         conversation.append({"role": "user", "content": request.message})
#     try:
#         bot_reply = get_roast(conversation)

#         UserMsg = Message(session_id = session_id,role = "user",content = request.message)
#         BotReply = Message(session_id = session_id, role = "assistant",content = bot_reply)
#         db.add(UserMsg)
#         db.add(BotReply)
#         db.commit()
#         return ChatResponse(session_id = session_id ,  response = bot_reply)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Bot is currently not available!")
    
