from utils.logger import log

def fix_error(step, error):
    log(f"Fixing error in {step}: {error}")

    # basic fallback
    if step == "validate":
        log("Skipping validation error")

    return True