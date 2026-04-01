from scheduler import start_scheduler, stop_scheduler, get_scheduler_status

st.subheader("⏱ Schedule Pipeline")

schedule_minutes = st.number_input("Run every (minutes)", min_value=1, value=1)

if st.button("Start Scheduler") and file_path:
    start_scheduler(file_path, schedule_minutes)
    st.success(f"✅ Pipeline scheduled every {schedule_minutes} minutes")

if st.button("Stop Scheduler"):
    stop_scheduler()
    st.warning("🛑 Scheduler stopped")

st.write("Scheduler running:", get_scheduler_status())