from tools.ingest import ingest_data
from tools.clean import clean_data
from tools.transform import transform_data
from tools.validate import validate_data
from tools.store import store_data
from tools.anomaly import detect_anomalies   # ✅ NEW

from agent.self_heal import fix_error
from utils.logger import log


def execute_pipeline(plan, source):

    df = None
    anomalies = None  # ✅ store anomalies

    for step in plan:
        try:
            log(f"🚀 Running step: {step}")

            if step == "ingest":
                df = ingest_data(source)

                if df is None:
                    raise ValueError("Ingestion returned None")

            elif step == "clean":
                df = clean_data(df)

            elif step == "transform":
                df = transform_data(df)

            elif step == "validate":
                validate_data(df)

            elif step == "anomaly":
                df, anomalies = detect_anomalies(df)

            elif step == "store":
                store_data(df)

            log(f"✅ Completed step: {step}")

        except Exception as e:
            log(f"❌ Error in step '{step}': {e}")

            # Try to fix automatically
            fix_error(step, e)

    return df, anomalies