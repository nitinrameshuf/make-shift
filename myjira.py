from falconpy import ImageAssessment

# Initialize FalconPy Client
falcon = ImageAssessment(client_id="your_client_id", client_secret="your_client_secret")

# Define parameters to filter by "latest" tag
params = {
    "filter": "tags:['latest']",  # Exact match for tag "latest"
    "limit": 100  # Adjust the limit as needed
}

# API Call to Fetch Container Images
response = falcon.GetCombinedImages(parameters=params)

# Check response status
if response["status_code"] == 200:
    images = response["body"]["resources"]
    print("Retrieved Container Images:", images)
else:
    print("Error:", response)
