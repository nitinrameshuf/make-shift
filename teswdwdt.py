from falconpy import CloudPosture, ContainerImages, ContainerVulnerabilities, Assets
from collections import Counter
import os

# Replace with your actual credential retrieval
CLIENT_ID = os.getenv("CRWD_CLIENT_ID")
CLIENT_SECRET = os.getenv("CRWD_SECRET")

# Initialize Falcon modules
posture = CloudPosture(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
images = ContainerImages(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
vulns = ContainerVulnerabilities(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
assets = Assets(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

def get_misconfiguration_summary():
    # Query misconfigurations and count by severity
    query = posture.query_misconfigurations(filter="severity:['critical','high','medium','low']")
    ids = query.get("body", {}).get("resources", [])
    counts = Counter()
    if ids:
        details = posture.get_misconfigurations(ids=ids)
        for item in details["body"]["resources"]:
            counts[item["severity"]] += 1
    return dict(counts)

def get_container_findings():
    # Query container vulns and pull CVEs and severities
    query = vulns.query_combined_container_vulnerabilities(filter="severity:['critical','high','medium','low']")
    ids = query.get("body", {}).get("resources", [])
    findings = []
    if ids:
        details = vulns.get_container_vulnerabilities(ids=ids)
        for item in details["body"]["resources"]:
            findings.append({
                "cve": item.get("cve"),
                "severity": item.get("severity"),
                "image": item.get("image"),
                "status": item.get("status", "unknown")
            })
    return findings

def get_unassessed_container_images():
    # Pull images and find those missing vulnerability data or scan status
    response = images.get_combined_images(parameters={"limit": 500})
    unassessed = []
    for img in response.get("body", {}).get("resources", []):
        if not img.get("vulnerabilities") and not img.get("scan_status"):
            unassessed.append({
                "repository": img.get("repository"),
                "os": img.get("base_os", "unknown")
            })
    return unassessed

def get_unsupported_assets():
    # Pull assets marked with status: unsupported
    query = assets.query_combined_assets(filter="status:'unsupported'")
    ids = query.get("body", {}).get("resources", [])
    unsupported = []
    if ids:
        details = assets.get_assets(ids=ids)
        for asset in details["body"]["resources"]:
            unsupported.append({
                "hostname": asset.get("hostname"),
                "status": asset.get("status"),
                "platform": asset.get("platform_name", "unknown")
            })
    return unsupported

def main():
    result = {
        "misconfiguration_summary": get_misconfiguration_summary(),
        "container_findings": get_container_findings(),
        "unassessed_images": get_unassessed_container_images(),
        "unsupported_assets": get_unsupported_assets()
    }

    # Print or return this for integration into ShieldOne
    print(result)

if __name__ == "__main__":
    main()
