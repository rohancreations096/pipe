from tools.ingest import ingest_data
from tools.clean import clean_data
from tools.transform import transform_data
from tools.validate import validate_data
from tools.store import store_data
from agent.self_heal import fix_error
from utils.logger import log

def execute_pipeline(plan, source):

    df = None

    for step in plan:
        try:
            log(f"Running step: {step}")

            if step == "ingest":
                df = ingest_data(source)

            elif step == "clean":
                df = clean_data(df)

            elif step == "transform":
                df = transform_data(df)

            elif step == "validate":
                validate_data(df)

            elif step == "store":
                store_data(df)

        except Exception as e:
            fix_error(step, e)

    return df