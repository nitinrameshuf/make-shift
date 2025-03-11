from falconpy import ContainerImages

# Initialize the FalconPy client
falcon = ContainerImages(client_id='your_client_id', client_secret='your_client_secret')

# Define parameters to filter images with the tag 'latest'
params = {
    'filter': "tag:'latest'",  # Filter to retrieve images with the 'latest' tag
    'limit': 100               # Limit the number of results to 100
}

# Fetch image assessment results
response = falcon.get_combined_images(parameters=params)

# Check if the request was successful
if response['status_code'] == 200:
    images = response['body']['resources']
    if images:
        print(f"Retrieved {len(images)} container images with the 'latest' tag:")
        for img in images:
            print(f"- Image ID: {img.get('image_id')}, Repository: {img.get('repository')}, "
                  f"Tags: {img.get('tags')}, Vulnerabilities: {img.get('vulnerability_count', 0)}")
    else:
        print("No images found with the 'latest' tag.")
else:
    print(f"Error fetching images: {response['status_code']} - {response.get('errors', 'Unknown error')}")
