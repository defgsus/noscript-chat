import datetime
import threading
import time
import uuid
import html
from typing import Generator, Optional

import bottle

from noscriptchat import config


_index_template = (config.TEMPLATE_PATH / "index.html").read_text()
_message_template = (config.TEMPLATE_PATH / "message.html").read_text()


def render_chat(
        room: str,
        user: Optional[str] = None,
) -> str:
    """
    Renders the beginning of index.html for a specific room
    """
    url = config.URL
    if room:
        url = f"{url}/{room}"

    return bottle.template(
        _index_template,
        title=f"{room}@noscript-chat" if room else "noscript-chat",
        url=url,
        room=room or "",
        user=user or "",
    )


def render_message(message: dict):
    """
    Renders a single message
    """
    message = message.copy()
    is_new = (datetime.datetime.utcnow() - message["date"]).seconds <= config.MESSAGE_CHECK_INTERVAL * 3
    message["date"] = message["date"].strftime("%Y-%m-%d %H:%M UTC")
    message["user"] = message["user"] or "anonymous"
    message["classes"] = "new" if is_new else ""
    # bottle.template already escapes everything
    # message["message"] = html.escape(message["message"])
    return bottle.template(_message_template, **message)


class ChatStorage:
    """
    Class to be used a singleton that holds all chat messages in memory
    """
    _singleton = None

    @classmethod
    def singleton(cls):
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton

    def __init__(self):
        self._rooms = {}
        self._lock = threading.RLock()

    def post_message(self, room: str, message: str, user: Optional[str] = None):
        """
        Add a new message to a chat-room.
        """
        with self._lock:
            if room not in self._rooms:
                self._rooms[room] = []

            self._rooms[room].append({
                "date": datetime.datetime.utcnow(),
                "uuid": uuid.uuid4(),
                "user": user or None,
                "message": message[:config.MAX_MESSAGE_LENGTH],
            })

    def iter_messages(self, room: str = "") -> Generator[dict, None, None]:
        """
        Loop infinitely until new messages arrive.

        :param room: str, the room name

        :return: generator of dict
        """
        yielded_ids = set()
        while True:
            messages = None

            with self._lock:
                if room in self._rooms:
                    messages = list(self._rooms[room])

            if messages:
                for message in messages:
                    if message["uuid"] not in yielded_ids:
                        yielded_ids.add(message["uuid"])
                        yield message

            time.sleep(config.MESSAGE_CHECK_INTERVAL)
