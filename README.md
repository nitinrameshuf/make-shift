from zapv2 import ZAPv2
import time

# Configuration
api_key = 'your_api_key_here'  # Replace this with your actual API key from ZAP
target = 'http://demo.testfire.net'  # Target website
zap_address = 'localhost'
zap_port = '8080'

# Initialize the ZAP API
zap = ZAPv2(apikey=api_key, proxies={'http': f'http://{zap_address}:{zap_port}', 'https': f'http://{zap_address}:{zap_port}'})

# Start the Spider
print("Starting Spider against target: " + target)
scan_id = zap.spider.scan(target)
time.sleep(2)  # Pause to let the spider start
while int(zap.spider.status(scan_id)) < 100:
    # Periodically check the spider's progress
    print("Spider progress %: " + zap.spider.status(scan_id))
    time.sleep(5)
print("Spider scan completed")

# Start the Active Scanner
print("Starting Active Scan against target: " + target)
scan_id = zap.ascan.scan(target)
while int(zap.ascan.status(scan_id)) < 100:
    # Periodically check the scan's progress
    print("Active Scan progress %: " + zap.ascan.status(scan_id))
    time.sleep(5)
print("Active Scan completed")

# Retrieve and print alerts
alerts = zap.core.alerts(baseurl=target)
print("Alerts:")
for alert in alerts:
    print(alert['alert'], alert['risk'], alert['url'])
