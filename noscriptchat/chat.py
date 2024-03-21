import datetime
import threading
import time
import uuid
import html
from typing import Generator, Optional, Dict, List

from noscriptchat import config


class ChatStorage:
    """
    singleton class that holds all chat messages in memory
    """
    _singleton = None

    @classmethod
    def singleton(cls):
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton

    def __init__(self):
        self._messages_per_room: Dict[str, List[dict]] = {}
        self._lock = threading.RLock()

    def post_message(self, room: str, message: str, user: Optional[str] = None):
        """
        Add a new message to a chat-room.
        """
        if user:
            user = user[:config.MAX_NAME_LENGTH]

        with self._lock:
            if room not in self._messages_per_room:
                self._messages_per_room[room] = []

            messages = self._messages_per_room[room]
            messages.append({
                "date": datetime.datetime.utcnow(),
                "uuid": uuid.uuid4(),
                "user": user or None,
                "message": message[:config.MAX_MESSAGE_LENGTH],
            })
            if len(messages) > config.MAX_MESSAGES:
                messages.pop(0)

    def iter_messages(self, room: str = "") -> Generator[dict, None, None]:
        """
        Loop infinitely until new messages arrive.

        :param room: str, the room name

        :return: generator of dict
        """
        # TODO: this set currently grows unlimited
        yielded_ids = set()
        while True:
            messages = None

            with self._lock:
                if room in self._messages_per_room:
                    messages = list(self._messages_per_room[room])

            if messages:
                for message in messages:
                    if message["uuid"] not in yielded_ids:
                        yielded_ids.add(message["uuid"])
                        yield message

            time.sleep(config.MESSAGE_CHECK_INTERVAL)
