def generate_aria(text: str, severity: str, context_type: str) -> dict:
    """
    Generates ARIA attributes and screen-reader optimized text.
    """
    role = "alert" if severity in ["high", "critical"] else "status"
    
    # Optimize text for screen readers (e.g., expanding abbreviations)
    sr_text = text.replace("AQI", "Air Quality Index").replace("PM2.5", "Particulate Matter 2.5")
    
    return {
        "role": role,
        "aria-live": "assertive" if role == "alert" else "polite",
        "aria-atomic": "true",
        "screen_reader_text": f"{severity} severity {context_type} advisory: {sr_text}"
    }
