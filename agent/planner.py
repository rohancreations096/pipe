def plan_pipeline(user_input):
    """
    Simple planner (can upgrade with LLM later)
    """
    plan = [
        "ingest",
        "clean",
        "transform",
        "validate",
        "store"
    ]
    return plan