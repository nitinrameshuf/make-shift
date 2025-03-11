Oracle VirtualBox:
https://files.greenbone.net/download/delivery/website-trials-22.04-abdk-greenbone/Greenbone-Enterprise-TRIAL-22.04.27-VirtualBox.ova

SHA256 Checksum:
f9b33326689083ed82fb6706e1ab4053b5cf3364f8cda26ea2beb63397663ff4


from falconpy import ContainerSecurity
import time

# Initialize FalconPy Client
falcon = ContainerSecurity(client_id="your_client_id", client_secret="your_client_secret")

# Step 1: Request CSV Export with Filter for "latest" Tag
export_response = falcon.query_vulnerabilities_combined(
    parameters={
        "export": "true",
        "format": "csv",
        "filter": "tag:'latest'"  # Case-sensitive filter
    }
)

# Check if request was successful
if export_response["status_code"] == 202:
    # Extract export ID
    export_id = export_response["body"]["resources"][0]
    print(f"Export initiated, ID: {export_id}")

    # Step 2: Wait for the export to complete
    time.sleep(10)  # Adjust this if needed based on API response time

    # Step 3: Download the CSV
    download_response = falcon.get_vulnerability_export(
        ids=[export_id]
    )

    # Save to file
    csv_filename = "filtered_vulnerability_export.csv"
    with open(csv_filename, "wb") as file:
        file.write(download_response["body"])

    print(f"CSV Report saved as {csv_filename}")

else:
    print(f"Failed to initiate export: {export_response}")
