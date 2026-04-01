from apscheduler.schedulers.background import BackgroundScheduler
from main import run_pipeline
from utils.logger import log

# Create global scheduler instance
scheduler = BackgroundScheduler()


def start_scheduler(file_path, minutes=1):
    """
    Start or update the pipeline scheduler
    """

    try:
        # Remove existing job if already running
        if scheduler.get_job("pipeline_job"):
            scheduler.remove_job("pipeline_job")
            log("🔄 Existing scheduler job removed")

        # Add new job
        scheduler.add_job(
            func=lambda: run_pipeline(file_path),
            trigger="interval",
            minutes=minutes,
            id="pipeline_job",
            replace_existing=True
        )

        # Start scheduler if not already running
        if not scheduler.running:
            scheduler.start()
            log("🚀 Scheduler started")

        log(f"⏱ Pipeline scheduled every {minutes} minutes")

    except Exception as e:
        log(f"❌ Scheduler error: {e}")


def stop_scheduler():
    """
    Stop the scheduler safely
    """
    try:
        if scheduler.running:
            scheduler.shutdown()
            log("🛑 Scheduler stopped")
    except Exception as e:
        log(f"❌ Error stopping scheduler: {e}")


def get_scheduler_status():
    """
    Check if scheduler is running
    """
    return scheduler.running