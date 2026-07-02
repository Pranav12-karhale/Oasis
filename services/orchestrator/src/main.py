"""
Oasis LangGraph Orchestrator — Agentic RAG Pipeline
The brain of Oasis: a stateful, cyclic workflow that classifies user intent,
fetches real-time data from MCP servers, retrieves relevant documents, generates
health advisories, self-critiques, translates, and renders for accessibility.
"""

import os
import logging
from typing import TypedDict, Optional

from fastapi import FastAPI
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage

logger = logging.getLogger("oasis.orchestrator")


# ═════════════════════════════════════════════════════════════════════════════
# STATE SCHEMA
# ═════════════════════════════════════════════════════════════════════════════

class OasisState(TypedDict):
    """Complete state carried through the LangGraph pipeline."""
    # Input
    messages: list[BaseMessage]
    input_text: str
    input_modality: str              # "text" | "voice"
    voice_input_audio: Optional[bytes]
    transcribed_text: str

    # User context
    user_location: dict              # {lat, lng, city, state, district}
    user_language: str               # ISO 639-1 code (hi, mr, bn, etc.)
    detected_language: str           # Language detected from voice
    accessibility_mode: str          # "standard" | "voice" | "isl" | "simplified"

    # Classification
    intent: str                      # "health_query" | "disaster_alert" | "general_info"

    # MCP context (fetched from real-time data sources)
    weather_context: dict            # Temperature, humidity, UV, forecast
    pollution_context: dict          # AQI, PM2.5, PM10, pollutants
    disaster_context: dict           # Active warnings, severity
    population_context: dict         # Density, demographics
    health_context: dict             # Regional disease patterns
    conflict_context: dict           # Active conflicts/unrest

    # RAG
    retrieved_documents: list        # RAG results with citations
    relevance_score: float           # Grading output (0.0–1.0)

    # Generation
    draft_response: str              # Pre-translation English response
    final_response: str              # Translated, formatted response
    citations: list[dict]            # Sources for the response

    # Voice output
    audio_response: Optional[bytes]  # TTS audio output
    audio_url: str                   # URL to audio response

    # Control flow
    iteration_count: int             # Self-correction loop counter (max 3)
    metadata: dict                   # Trace IDs, timestamps, node timings


# ═════════════════════════════════════════════════════════════════════════════
# LLM PROVIDER (Gemini Pro primary, Groq fallback)
# ═════════════════════════════════════════════════════════════════════════════

def get_llm():
    """Get the primary LLM — Google Gemini Pro via your subscription."""
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-pro"),
        temperature=0.3,           # Low temp for factual health advice
        max_output_tokens=4096,
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )


def get_fallback_llm():
    """Fallback LLM — Groq free tier (Llama 3.3 70B)."""
    try:
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY"),
        )
    except Exception:
        logger.warning("Groq fallback unavailable, using Gemini only")
        return get_llm()


# ═════════════════════════════════════════════════════════════════════════════
# GRAPH NODES
# ═════════════════════════════════════════════════════════════════════════════

async def speech_to_text_node(state: OasisState) -> OasisState:
    """Convert voice input to text via Bhashini ASR."""
    if state["input_modality"] != "voice":
        state["transcribed_text"] = state["input_text"]
        return state

    # TODO: Call Bhashini ASR service
    logger.info("ASR: Converting voice input to text")
    state["transcribed_text"] = state.get("input_text", "")
    state["detected_language"] = state.get("user_language", "en")
    return state


async def classify_intent_node(state: OasisState) -> OasisState:
    """Classify user query intent using Gemini structured output."""
    llm = get_llm()
    query = state["transcribed_text"] or state["input_text"]

    prompt = f"""Classify the following user query into one of these categories:
- health_query: Questions about health, safety, air quality, water quality, disease risks
- disaster_alert: Questions about natural disasters, earthquakes, floods, cyclones, emergencies
- general_info: General questions, greetings, or unrelated topics

User query: "{query}"

Respond with ONLY one of: health_query, disaster_alert, general_info"""

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    intent = response.content.strip().lower()

    if intent not in ("health_query", "disaster_alert", "general_info"):
        intent = "health_query"  # Default to health

    state["intent"] = intent
    logger.info(f"Intent classified: {intent}")
    return state


async def enrich_location_node(state: OasisState) -> OasisState:
    """Enrich location data with geocoding and regional context."""
    location = state.get("user_location", {})
    if not location:
        # Default to a general India context
        state["user_location"] = {
            "city": "Unknown",
            "state": "Unknown",
            "lat": 20.5937,
            "lng": 78.9629,
            "district": "Unknown",
        }
    logger.info(f"Location enriched: {state['user_location'].get('city', 'Unknown')}")
    return state


async def mcp_fetch_node(state: OasisState) -> OasisState:
    """Fetch real-time data from all MCP servers in parallel."""
    city = state["user_location"].get("city", "Delhi")
    state_name = state["user_location"].get("state", "")

    # TODO: Replace with actual MCP server calls
    # For now, set placeholder context
    state["weather_context"] = {"status": "pending_mcp_integration", "city": city}
    state["pollution_context"] = {"status": "pending_mcp_integration", "city": city}
    state["disaster_context"] = {"status": "pending_mcp_integration", "state": state_name}
    state["health_context"] = {"status": "pending_mcp_integration"}
    state["population_context"] = {"status": "pending_mcp_integration"}
    state["conflict_context"] = {"status": "pending_mcp_integration"}

    logger.info(f"MCP data fetched for {city}")
    return state


async def retrieve_node(state: OasisState) -> OasisState:
    """Retrieve relevant documents from Qdrant vector store."""
    # TODO: Integrate with RAG engine service
    query = state["transcribed_text"] or state["input_text"]
    state["retrieved_documents"] = []
    state["relevance_score"] = 0.0
    logger.info(f"RAG retrieval for: {query[:50]}...")
    return state


async def grade_relevance_node(state: OasisState) -> OasisState:
    """Grade the relevance of retrieved documents."""
    docs = state.get("retrieved_documents", [])
    if not docs:
        state["relevance_score"] = 0.0
    else:
        # TODO: Use LLM-based grading
        state["relevance_score"] = 0.8
    return state


async def rewrite_query_node(state: OasisState) -> OasisState:
    """Rewrite the query for better retrieval results."""
    llm = get_llm()
    query = state["transcribed_text"] or state["input_text"]

    prompt = f"""The following search query didn't return relevant results. 
Rewrite it to be more specific and search-friendly for a health/safety knowledge base.

Original query: "{query}"
Location context: {state['user_location'].get('city', 'India')}

Provide ONLY the rewritten query, nothing else."""

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    state["transcribed_text"] = response.content.strip()
    state["iteration_count"] = state.get("iteration_count", 0) + 1
    logger.info(f"Query rewritten (iteration {state['iteration_count']})")
    return state


async def generate_advisory_node(state: OasisState) -> OasisState:
    """Generate health/safety advisory using Gemini with full context."""
    llm = get_llm()
    query = state["transcribed_text"] or state["input_text"]

    context_parts = []
    if state.get("weather_context"):
        context_parts.append(f"Weather: {state['weather_context']}")
    if state.get("pollution_context"):
        context_parts.append(f"Air Quality: {state['pollution_context']}")
    if state.get("disaster_context"):
        context_parts.append(f"Disaster Alerts: {state['disaster_context']}")
    if state.get("health_context"):
        context_parts.append(f"Health Data: {state['health_context']}")
    if state.get("retrieved_documents"):
        context_parts.append(f"Knowledge Base: {state['retrieved_documents'][:3]}")

    context = "\n".join(context_parts) if context_parts else "No real-time data available yet."

    # Adjust prompt based on accessibility mode
    voice_instruction = ""
    if state.get("accessibility_mode") == "voice":
        voice_instruction = (
            "\nIMPORTANT: This response will be read aloud via text-to-speech. "
            "Use clear, simple sentences. Avoid complex formatting, bullet points, "
            "or special characters. Write as if speaking to someone."
        )

    prompt = f"""You are Oasis, an AI health and safety advisor for India.
Based on the user's location and real-time environmental data, provide a helpful,
accurate, and actionable health/safety advisory.

Location: {state['user_location'].get('city', 'India')}, {state['user_location'].get('state', '')}
Real-time Context:
{context}

User Question: {query}
{voice_instruction}

Guidelines:
- Be specific to the user's location and current conditions
- Provide actionable advice (what to do, what to avoid)
- Mention any active warnings or alerts
- If data is unavailable, say so honestly
- Keep response concise but comprehensive
- Include relevant precautions for vulnerable groups (children, elderly, pregnant women)
- Cite sources when possible"""

    try:
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        state["draft_response"] = response.content
    except Exception as e:
        logger.error(f"Gemini failed, trying Groq fallback: {e}")
        fallback = get_fallback_llm()
        response = await fallback.ainvoke([HumanMessage(content=prompt)])
        state["draft_response"] = response.content

    logger.info("Advisory generated")
    return state


async def critique_node(state: OasisState) -> OasisState:
    """Self-critique: check for hallucination, completeness, and safety."""
    # Simple heuristic critique for MVP
    draft = state.get("draft_response", "")

    # Check if response is too short
    if len(draft) < 50:
        state["relevance_score"] = 0.3
        return state

    # Pass — response looks reasonable
    state["relevance_score"] = 0.9
    return state


async def translate_node(state: OasisState) -> OasisState:
    """Translate response to user's preferred language via Bhashini."""
    target_lang = state.get("user_language", "en")

    if target_lang == "en":
        state["final_response"] = state["draft_response"]
        return state

    # TODO: Call Bhashini translation service
    # For now, return English with a note
    state["final_response"] = state["draft_response"]
    logger.info(f"Translation to {target_lang} — pending Bhashini integration")
    return state


async def text_to_speech_node(state: OasisState) -> OasisState:
    """Convert response to speech via Bhashini TTS (for voice/blind mode)."""
    if state.get("accessibility_mode") not in ("voice", "simplified"):
        return state

    # TODO: Call Bhashini TTS service
    state["audio_url"] = ""
    logger.info("TTS — pending Bhashini integration")
    return state


async def format_response_node(state: OasisState) -> OasisState:
    """Format the final response with citations and metadata."""
    state["final_response"] = state.get("final_response") or state.get("draft_response", "")
    state["citations"] = state.get("citations", [])
    return state


# ═════════════════════════════════════════════════════════════════════════════
# CONDITIONAL EDGES (Routing Logic)
# ═════════════════════════════════════════════════════════════════════════════

def route_by_intent(state: OasisState) -> str:
    """Route to different paths based on classified intent."""
    return state.get("intent", "health_query")


def route_by_relevance(state: OasisState) -> str:
    """Route based on document relevance score."""
    score = state.get("relevance_score", 0.0)
    iterations = state.get("iteration_count", 0)

    if score >= 0.6 or iterations >= 3:
        return "generate"
    return "rewrite"


def route_by_critique(state: OasisState) -> str:
    """Route based on self-critique results."""
    score = state.get("relevance_score", 0.0)
    iterations = state.get("iteration_count", 0)

    if score >= 0.7 or iterations >= 3:
        return "translate"
    return "regenerate"


def route_accessibility(state: OasisState) -> str:
    """Route based on accessibility mode."""
    mode = state.get("accessibility_mode", "standard")
    if mode in ("voice", "simplified"):
        return "tts"
    return "format"


# ═════════════════════════════════════════════════════════════════════════════
# BUILD THE GRAPH
# ═════════════════════════════════════════════════════════════════════════════

def build_oasis_graph() -> StateGraph:
    """Build the complete Oasis agentic RAG pipeline."""

    graph = StateGraph(OasisState)

    # Add nodes
    graph.add_node("speech_to_text", speech_to_text_node)
    graph.add_node("classify", classify_intent_node)
    graph.add_node("enrich", enrich_location_node)
    graph.add_node("mcp_fetch", mcp_fetch_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade", grade_relevance_node)
    graph.add_node("rewrite", rewrite_query_node)
    graph.add_node("generate", generate_advisory_node)
    graph.add_node("critique", critique_node)
    graph.add_node("translate", translate_node)
    graph.add_node("tts", text_to_speech_node)
    graph.add_node("format", format_response_node)

    # Set entry point
    graph.set_entry_point("speech_to_text")

    # Define edges
    graph.add_edge("speech_to_text", "classify")
    graph.add_edge("classify", "enrich")
    graph.add_edge("enrich", "mcp_fetch")
    graph.add_edge("mcp_fetch", "retrieve")
    graph.add_edge("retrieve", "grade")

    # Conditional: grade → generate or rewrite
    graph.add_conditional_edges(
        "grade",
        route_by_relevance,
        {"generate": "generate", "rewrite": "rewrite"},
    )
    graph.add_edge("rewrite", "retrieve")  # Loop back

    graph.add_edge("generate", "critique")

    # Conditional: critique → translate or regenerate
    graph.add_conditional_edges(
        "critique",
        route_by_critique,
        {"translate": "translate", "regenerate": "generate"},
    )

    # Conditional: accessibility mode
    graph.add_conditional_edges(
        "translate",
        route_accessibility,
        {"tts": "tts", "format": "format"},
    )
    graph.add_edge("tts", "format")
    graph.add_edge("format", END)

    return graph.compile()


# ═════════════════════════════════════════════════════════════════════════════
# FASTAPI SERVICE
# ═════════════════════════════════════════════════════════════════════════════

app = FastAPI(title="Oasis Orchestrator", version="0.1.0")
oasis_graph = build_oasis_graph()


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "orchestrator"}


@app.post("/process")
async def process_query(request: dict):
    """
    Process a user query through the full LangGraph pipeline.
    Accepts text or voice input, returns advisory with optional audio.
    """
    # Build initial state
    initial_state: OasisState = {
        "messages": [],
        "input_text": request.get("input_text", ""),
        "input_modality": request.get("input_modality", "text"),
        "voice_input_audio": None,
        "transcribed_text": "",
        "user_location": request.get("location", {}),
        "user_language": request.get("language", "en"),
        "detected_language": "",
        "accessibility_mode": request.get("accessibility_mode", "standard"),
        "intent": "",
        "weather_context": {},
        "pollution_context": {},
        "disaster_context": {},
        "population_context": {},
        "health_context": {},
        "conflict_context": {},
        "retrieved_documents": [],
        "relevance_score": 0.0,
        "draft_response": "",
        "final_response": "",
        "citations": [],
        "audio_response": None,
        "audio_url": "",
        "iteration_count": 0,
        "metadata": {},
    }

    # Run the graph
    result = await oasis_graph.ainvoke(initial_state)

    return {
        "response": result.get("final_response", ""),
        "intent": result.get("intent", ""),
        "language": result.get("user_language", "en"),
        "audio_url": result.get("audio_url", ""),
        "citations": result.get("citations", []),
        "location": result.get("user_location", {}),
        "context": {
            "weather": result.get("weather_context", {}),
            "pollution": result.get("pollution_context", {}),
            "disaster": result.get("disaster_context", {}),
        },
    }


@app.get("/alerts")
async def get_alerts(city: str, state: str = None):
    """Fetch active alerts for a city (direct MCP query, no full pipeline)."""
    # TODO: Direct calls to disaster, weather, pollution MCPs
    return {
        "city": city,
        "state": state,
        "alerts": [],
        "message": "Alert aggregation — pending MCP integration",
    }


@app.post("/assess")
async def health_risk_assessment(request: dict):
    """Full risk assessment — runs the pipeline with assessment-specific prompts."""
    request["input_text"] = (
        f"Give me a complete health and safety risk assessment for "
        f"{request.get('location', {}).get('city', 'my location')}"
    )
    return await process_query(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
