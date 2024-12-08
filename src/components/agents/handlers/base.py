import json
import logging
from collections.abc import Callable
from typing import Any

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from src._settings import settings

GPT_MODEL = settings.GPT_MODEL
client = OpenAI(api_key=settings.OPENAI_API_KEY)


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
async def chat_completion_request(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] = None,
    model=GPT_MODEL,
):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )
        return response
    except Exception as e:
        logging.warning("Unable to generate ChatCompletion response")
        logging.error(f"Exception: {e}")
        return e


async def handler(messages: list[dict[str, Any]], tools: list[dict[str, Any]] = None, functions: dict[str, Callable] = None):
    assistant_message = await chat_completion_request(messages, tools)
    answer = assistant_message.choices[0].message.content
    if answer is None:
        messages.append(assistant_message.choices[0].message)
    tool_calls = assistant_message.choices[0].message.tool_calls

    if tool_calls:
        print("Calling tool")
        tool_call_id = tool_calls[0].id
        tool_function_name = tool_calls[0].function.name
        tool_query_string = json.loads(tool_calls[0].function.arguments)

        func = functions[tool_function_name]
        result = func(**tool_query_string)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_function_name,
            "content": result,
        })

        assistant_message_with_function_call = await chat_completion_request(messages)
        answer = assistant_message_with_function_call.choices[0].message.content

    return answer
