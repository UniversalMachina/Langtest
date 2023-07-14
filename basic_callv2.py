import requests
import json

url = "https://app.staging.theurbanwriters.com/api/v1/freelancers/search?niches=['fiction']&limit=10"

headers = {
    "Authorization": "Bearer dc0_TQryOqO35oiBkUQq52If3"
}

params = {
    "position": "writer",
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))
else:
    print(f"Request failed with status code {response.status_code}")