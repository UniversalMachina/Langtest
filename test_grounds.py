import requests
import json

url = "https://app.staging.theurbanwriters.com/api/v1/freelancers/search?position=writer&niches=[\"fiction\"]&limit=10"
headers = {
    "Authorization": "Bearer dc0_TQryOqO35oiBkUQq52If3"
}

response = requests.get(url, headers=headers)

# Now you can access the response body as a json with the following line
response_json = response.json()

print(json.dumps(response_json, indent=4))
