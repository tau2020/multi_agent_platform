# agents/message.py

class Message:
    def __init__(self, sender, receiver, msg_type, content):
        self.sender = sender
        self.receiver = receiver
        self.msg_type = msg_type  # 'task', 'output', 'terminate', etc.
        self.content = content
