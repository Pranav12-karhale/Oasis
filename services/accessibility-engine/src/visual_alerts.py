def map_severity_to_visuals(severity: str, context_type: str) -> dict:
    """
    Maps text severity to visual cues and vibration patterns for deaf users.
    """
    severity_lower = severity.lower()
    
    visuals = {
        "color_hex": "#22c55e", # default green
        "icon": "info",
        "vibration_pattern": [100] # ms
    }
    
    if severity_lower in ["critical", "high"]:
        visuals["color_hex"] = "#ef4444" # red
        visuals["icon"] = "alert-triangle"
        visuals["vibration_pattern"] = [500, 200, 500, 200, 500] # SOS-like
    elif severity_lower in ["moderate", "medium"]:
        visuals["color_hex"] = "#f97316" # orange
        visuals["icon"] = "alert-circle"
        visuals["vibration_pattern"] = [300, 100, 300]
    elif severity_lower == "low":
        visuals["color_hex"] = "#eab308" # yellow
        visuals["icon"] = "info"
        visuals["vibration_pattern"] = [200]
        
    return visuals
