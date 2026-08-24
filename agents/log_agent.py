# agents/log_agent.py

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from config.settings import settings
from services.retrieval_service import RetrievalService

from agents.anomaly_agent import detect_anomalies
from agents.root_cause_agent import analyze_root_cause
from agents.summary_agent import summarize_incident
from agents.alert_agent import generate_alert

# ==========================================================
# JINJA2 PROMPT
# ==========================================================

prompt_environment = Environment(
    loader = FileSystemLoader (
        Path("prompts")
    )
)

prompt_template = prompt_environment.get_template("retrieval_agent.j2")


# ==========================================================
# RETRIEVAL TOOL
# ==========================================================

retrieval_service = RetrievalService()
checkpointer = InMemorySaver()

@tool
def search_infrastructure_logs(query: str) -> list[dict]:
    """
    Search infrastructure logs using semantic retrieval and reranking.
    """
    
    return retrieval_service.search(query = query)


# ==========================================================
# LLM
# ==========================================================

llm = ChatOpenAI(
    model = settings.OPENROUTER_MODEL,
    api_key = settings.OPENROUTER_API_KEY,
    base_url = settings.OPENROUTER_BASE_URL
)


# ==========================================================
# AGENT
# ==========================================================

log_agent = create_agent(
    model = llm,
    tools = [search_infrastructure_logs, 
             detect_anomalies, 
             analyze_root_cause,
             summarize_incident,
             generate_alert],
    system_prompt = prompt_template.render(),
    checkpointer = checkpointer,
)