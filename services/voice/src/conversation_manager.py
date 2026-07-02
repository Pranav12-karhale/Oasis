import logging
from typing import Dict, List

logger = logging.getLogger("oasis.voice.conversation")

class ConversationManager:
    """
    Manages multi-turn voice interaction contexts.
    """
    def __init__(self):
        # session_id -> list of previous contexts
        self.sessions: Dict[str, List[dict]] = {}

    def get_context(self, session_id: str) -> List[dict]:
        return self.sessions.get(session_id, [])

    def add_turn(self, session_id: str, user_query: str, system_response: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            
        self.sessions[session_id].append({
            "query": user_query,
            "response": system_response
        })
        
        # Keep only last 5 turns to prevent context bloat
        if len(self.sessions[session_id]) > 5:
            self.sessions[session_id].pop(0)
            
        logger.debug(f"Added turn to session {session_id}. Total turns: {len(self.sessions[session_id])}")
