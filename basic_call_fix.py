import requests
import json

# Define the API endpoint
url = "https://app.staging.theurbanwriters.com/api/v1/freelancers/search"

# Define the authorization header with bearer token
headers = {
    "Authorization": "Bearer dc0_TQryOqO35oiBkUQq52If3"
}

# Define the parameters for the request
params = {
    "position": "writer",
    "niches": '["fiction"]',
    "limit": 10,
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Check if request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()
    print(response.request.url)
    # Print the data
    print(json.dumps(data, indent=4))
else:
    data = response.json()
    print(response.request.url)
    # Print the data
    print(json.dumps(data, indent=4))
    print(f"Request failed with status code {response.status_code}")


