from src._schemas import Message
from src.components import booking_handler
from src.store import BaseTrackerStore


class Application:
    def __init__(self, tracker_store: BaseTrackerStore = None):
        self.tracker_store = tracker_store

    async def chat(
        self,
        sender_id: str,
        text: str,
    ):
        history = await self.tracker_store.get_messages(sender_id)
        history = self.convert_to_openai_format(history)

        message = [{"role": "user", "content": text}]
        messages = history + message
        # TODO: Current setup is for a single agent handling flight bookings and general travel inquiries.
        # In the future, consider expanding to a multi-agent system for navigation to different agents.
        answer = await booking_handler(messages)

        message = {
            "query": text,
            "answer": answer,
            "sender_id": sender_id,
        }
        await self.tracker_store.insert_message(Message(**message))

        return answer

    @staticmethod
    def convert_to_openai_format(messages: list[Message]):
        formatted_messages = []
        for message in messages:
            user = {"role": "user", "content": message.query}
            assistant = {"role": "assistant", "content": message.answer}
            formatted_messages.append(user)
            formatted_messages.append(assistant)
        return formatted_messages
