class Memory:
    def __init__(self):
        self.history = []

    def store_user_message(self, message: str):
        self.history.append(f"User: {message}")

    def store_bot_response(self, response: str):
        self.history.append(f"Bot: {response}")

    def get_history(self) -> list[str]:
        return self.history[-10:]  # Limit to last 10 for brevity
