import json
import os
from typing import Any

import _settings as settings
import chainlit as cl
from chainlit import ThreadDict, logger
from config.config import get_chat_settings
from constants import CHAT_PROFILES, DEFAULT_DOMAIN, DEFAULT_PASSWORD
from external.va_cskh import chat
from schemas.assistant_response import ChatResponse

settings.setup()


# Starters are suggestions to help users get started with the chat.
@cl.set_starters
async def set_starters() -> list[cl.Starter]:
    return [
        cl.Starter(
            label="Connection Error or Account Login Issue",
            message="Mình bị lỗi kết nối",
            icon="/public/1.svg",
        ),
        cl.Starter(
            label="Reset Password Request",
            message="Mình cần reset mật khẩu ạ",
            icon="/public/2.svg",
        ),
        cl.Starter(
            label="Change Linked Account Email",
            message="Mình cần hỗ trợ thay đổi email liên kết tài khoản",
            icon="/public/3.svg",
        ),
        cl.Starter(
            label="Transaction Error - Card Top-up Issue",
            message="Lỗi nạp thẻ card ạ",
            icon="/public/4.svg",
        ),
    ]


# Chat profiles are used to define the chat's appearance and behavior.
@cl.set_chat_profiles
async def chat_profile() -> list[cl.ChatProfile]:
    return [
        cl.ChatProfile(
            name=CHAT_PROFILES,
            markdown_description="Chào bạn, mình là chatbot hỗ trợ khách hàng. "
            "Mình có thể giúp bạn với các vấn đề liên quan đến tài khoản, giao dịch, và hỗ trợ kỹ thuật. "
            "Hãy chia sẻ vấn đề của bạn để mình có thể giúp bạn tốt hơn nhé",
            icon="/public/profile.png",
        ),
    ]


# Password authentication callback for user login.
@cl.password_auth_callback
def auth_callback(username: str, password: str) -> cl.User | None:
    # Environment variable for the password (use a secure method in production)
    valid_password = os.getenv("USER_CHAINLIT_PASSWORD", DEFAULT_PASSWORD)

    if username.endswith(DEFAULT_DOMAIN) and password == valid_password:
        return cl.User(identifier=username, metadata={"role": "user", "provider": "credentials"})

    return None


# Chat start event handler to initialize chat settings.
@cl.on_chat_start
async def start() -> None:
    _settings = await cl.ChatSettings(get_chat_settings()).send()

    cl.user_session.set("settings", _settings)


# Chat resume event handler to load chat history.
@cl.on_chat_resume
async def load_chat_history(thread: ThreadDict) -> None:
    # Extract primary messages from chat history
    primary_messages = [message for message in thread["steps"] if message.get("parentId") is None]

    # Store primary messages in user session under 'memory'
    cl.user_session.set("memory", primary_messages)


# Main message handler for incoming messages. and sends it to a specified API.
@cl.on_message
async def main(message: cl.Message) -> None:
    # Retrieve and update user settings
    cl_settings = cl.user_session.get("settings", {})
    cl_settings["domain"] = "cskh"

    # Prepare metadata for request construction
    metadata: dict[str, Any] = {"debug": cl_settings.get("debug"), "sender_name": cl.user_session.get("user").identifier, "message_id": message.id}
    clear_history = cl_settings.get("clear_history", False)
    sender_id = message.thread_id.replace("-", "")

    # Construct the request payload with metadata
    if cl_settings.get("intent") and cl_settings["intent"] != "None":
        metadata["text"] = message.content
        message.content = f"/.{cl_settings['intent']}"

    params = {"content": "clear" if clear_history else message.content, "sender_id": sender_id, "metadata": metadata}

    # Get response from the bot API
    bot_response: ChatResponse = await chat(**params)

    # Handle debug information if needed
    if cl_settings.get("debug"):
        for logs in bot_response.metadata.values():
            await show_step(logs)

    # Process and send the API response to the user
    await send_response(bot_response)


@cl.step(show_input="json", language="json")
async def show_step(logs: dict[str, Any]) -> None:
    if not logs:
        return None

    current_step = cl.context.current_step

    # Assigning step name based on 'message_id' or a default value
    current_step.name = "Log Session History"

    # Setting input and output to the formatted log entry
    formatted_log = json.dumps(logs, indent=4, ensure_ascii=False)
    current_step.input = {}
    current_step.output = formatted_log

    return None


async def send_response(assistant_message: ChatResponse) -> None:
    try:
        # Extract the response content
        reply_message = assistant_message.content[0].text if assistant_message.content else ""

        # Send an initial placeholder message
        msg = cl.Message("")
        await msg.send()
        await cl.sleep(1)  # Pause briefly to simulate typing or processing delay

        # Update the message with the actual content
        msg.content = reply_message
        await msg.update()
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error(f"Failed to process response: {str(e)}")
        await cl.Message("An error occurred while processing the response.").send()
