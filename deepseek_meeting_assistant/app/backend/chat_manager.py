import json
from datetime import datetime


class ChatHistory:
    def __init__(self):
        self.chat_history = []

    def add_message(self, user_input, ai_response):
        self.chat_history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "user": user_input,
            "assistant": ai_response
        })

    def get_history(self, limit=None):
        if limit:
            return self.chat_history[-limit:]
        return self.chat_history

    def clear(self):
        self.chat_history = []

    def to_dict(self):
        return self.chat_history
