from falconpy import ScheduledReports, ReportExecutions

scheduled = ScheduledReports(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
executions = ReportExecutions(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Step 1: Get report ID by name
report = scheduled.query_reports(filter='name:"My Weekly Report"', limit=1)
scheduled_report_id = report["body"]["resources"][0]

# Step 2: Get latest execution ID for that report
execution = executions.query_reports(filter=f"scheduled_report_id:'{scheduled_report_id}'", limit=1)
execution_id = execution["body"]["resources"][0]

# Step 3: Wait for execution to complete (if needed)

# Step 4: Download CSV
csv_bytes = executions.get_download(ids=execution_id, stream=True)
with open("report.csv", "wb") as f:
    f.write(csv_bytes)
