def simplify_for_isl(text: str) -> str:
    """
    Simplifies text into Subject-Object-Verb (SOV) structure commonly used in ISL.
    Removes complex conjunctions and metaphors.
    """
    # TODO: Implement NLP model for proper ISL gloss generation
    # MOCK implementation for MVP
    return text.replace("It is recommended to", "You should") \
               .replace("sensitive groups", "sick people") \
               .replace("prolonged heavy exertion", "hard work outside")
