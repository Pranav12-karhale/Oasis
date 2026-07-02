import logging

logger = logging.getLogger("oasis.voice.navigator")

def process_voice_command(command: str) -> dict:
    """
    Parses voice commands for app navigation (hands-free operation).
    e.g., "Go to settings", "Read alerts"
    """
    cmd_lower = command.lower()
    
    if "setting" in cmd_lower:
        action = "navigate"
        target = "/settings"
    elif "alert" in cmd_lower:
        action = "navigate"
        target = "/alerts"
    elif "map" in cmd_lower:
        action = "navigate"
        target = "/map"
    elif "weather" in cmd_lower:
        action = "trigger_query"
        target = "weather"
    else:
        action = "unknown"
        target = None
        
    logger.info(f"Parsed voice command '{command}' -> {action} {target}")
    
    return {
        "action": action,
        "target": target
    }
