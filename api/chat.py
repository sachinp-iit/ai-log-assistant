# api/chat.py

from fastapi import APIRouter

from agents.log_agent import log_agent

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(query: str):
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
        }
    )
    
    return {
        "response": response["messages"][-1].content,
    }