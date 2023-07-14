import openai
import requests
import json

openai.api_key = "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"

# API call to the Freelance Writers API
def get_freelance_writers(position, niches, online, limit):
    # Define the API endpoint
    url = "https://app.staging.theurbanwriters.com/api/v1/freelancers/search"

    # Define the authorization header with bearer token
    headers = {
        "Authorization": "Bearer dc0_TQryOqO35oiBkUQq52If3n"
    }

    # Define the parameters for the request
    params = {
        "position": position,
        # "niches": niches,
        # "online": online,
        "limit": limit,
    }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)

    # Parse the response JSON
    data = response.json()

    # Return the data as a JSON string
    return json.dumps(data)


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "Get me some freelance writers who are currently online. Keep the answer as concise as possible"}]
    functions = [
        {
            "name": "get_freelance_writers",
            "description": "Get freelance writers based on the position, niches, online status, and limit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "position": {
                        "type": "string",
                        "description": "The position of the freelancers, e.g., 'writer'",
                    },
                    "niches": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "The niches of the freelancers, e.g., ['fiction']"
                    },
                    "online": {
                        "type": "boolean",
                        "description": "Whether the freelancers are currently online or not."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The maximum number of freelancers to return."
                    }
                },
                "required": ["position", "niches", "online", "limit"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_freelance_writers": get_freelance_writers,
        }  
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            position=function_args.get("position"),
            niches=function_args.get("niches"),
            online=function_args.get("online"),
            limit=function_args.get("limit"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        print(messages)

        return second_response


print(run_conversation())
