from agent.planner import plan_pipeline
from agent.executor import execute_pipeline

def run_pipeline(source):

    plan = plan_pipeline(source)
    result = execute_pipeline(plan, source)

    return result