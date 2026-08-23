# api/chat.py

from fastapi import APIRouter

from agents.log_agent import log_agent

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(query: str, thread_id: str = "default",):
    """
    Send a user query to the infrastructure log agent.
    """
    
    response = await log_agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        },
        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }
    )
    
    return {
        "thread_id": thread_id,
        "response": response["messages"][-1].content,
    }