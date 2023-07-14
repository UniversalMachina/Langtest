import openai
import json
import requests

openai.api_key = "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"


def search_freelancers(position=None, niches=None, online=None, availableAfter=None, limit=None, page=None):
    """Search for freelancers given a set of search parameters"""

    base_url = "https://app.staging.theurbanwriters.com/api/v1/freelancers/search"
    headers = {
        "Authorization": "Bearer dc0_TQryOqO35oiBkUQq52If3"
    }

    params = []

    if position is not None:
        params.append(f"position={position}")

    if niches is not None:
        niches_string = ','.join([f"'{str(niche)}'" for niche in niches])
        params.append(f"niches=[{niches_string}]")

    if online is not None:
        params.append(f"online={str(online).lower()}")

    if availableAfter is not None:
        params.append(f"availableAfter={availableAfter}")

    if limit is not None:
        params.append(f"limit={limit}")

    if page is not None:
        params.append(f"page={page}")

    # Combine all parameters and form the final URL
    url = f"{base_url}?{'&'.join(params)}"
    print(url)
    # Make the request and parse the response
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return json.dumps(data)
    else:
        return json.dumps({"error": f"Request failed with status code {response.status_code}"})


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    # messages = [{"role": "user", "content": "Search for online writers specialized in fiction."}]
    messages = [{"role": "user", "content": "Search for online writers who specialize in fiction."}]
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
        fuction_to_call = available_functions[function_name]

        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_args)
        function_response = fuction_to_call(
            position=function_args.get("position"),
            niches=function_args.get("niches"),
            online=function_args.get("online"),
            availableAfter=function_args.get("availableAfter"),
            limit=function_args.get("limit"),
            page=function_args.get("page"),
        )

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
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
        )
        print(messages)
        return second_response




print(run_conversation())
