import openai
import json
import requests

openai.api_key = "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"

def search_freelancers(position, niches, online=True, availableAfter=None, limit=10, page=0):

    """Search for freelancers given a set of search parameters"""

    # Define the endpoint and the headers
    url = "https://app.staging.theurbanwriters.com/api/v1/freelancers/search"
    headers = {
        "Authorization": "Bearer dc0_TQryOqO35oiBkUQq52If3"
    }

    # Define the parameters
    params = {
        "position": position,
        "niches": niches,
        "online": online,
        "availableAfter": availableAfter,
        "limit": limit,
        "page": page
    }

    # Make the request and parse the response
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return json.dumps(data)
    else:
        return json.dumps({"error": f"Request failed with status code {response.status_code}"})

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "Search for online writers specialized in health & fitness and self-help."}]
    functions = [
        {
            "name": "search_freelancers",
            "description": "Search for freelancers given a set of search parameters",
            "parameters": {
                "type": "object",
                "properties": {
                    "position": {"type": "string"},
                    "niches": {"type": "array", "items": {"type": "string"}},
                    "online": {"type": "boolean", "default": True},
                    "availableAfter": {"type": "string", "default": None},
                    "limit": {"type": "number", "default": 10},
                    "page": {"type": "number", "default": 0}
                },
                "required": ["position", "niches"]
            }
            ,
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        available_functions = {
            "search_freelancers": search_freelancers,
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(**function_args)

        print(function_response)


        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )
        print(messages)
        return second_response


print(run_conversation())
