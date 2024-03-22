import datetime
import threading
import time
import uuid
import html
from typing import Generator, Optional, Dict, List

from . import config
from .emojify import emojify


class ConnectionCounter:
    """
    It basically counts if the message loops are still running.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self._room_connection_timestamps_map: Dict[str, Dict[str, float]] = {}
        self._last_check_timestamp = 0

    def num_connections(self, room: str = ""):
        return len(self._room_connection_timestamps_map.get(room, tuple()))

    def update_connection(self, room: str, request_uuid: str) -> int:
        timestamp_now = datetime.datetime.utcnow().timestamp()
        with self._lock:
            # store current timestamp for room/request
            if room not in self._room_connection_timestamps_map:
                self._room_connection_timestamps_map[room] = {}
            self._room_connection_timestamps_map[room][request_uuid] = timestamp_now

            # once and then let one of the threads remove old request ids
            if timestamp_now - self._last_check_timestamp >= config.MESSAGE_CHECK_INTERVAL_SECONDS:

                for uuid, timestamp in list(self._room_connection_timestamps_map[room].items()):
                    if timestamp_now - timestamp >= config.MESSAGE_CHECK_INTERVAL_SECONDS * 2:
                        del self._room_connection_timestamps_map[room][uuid]

                if not self._room_connection_timestamps_map[room]:
                    del self._room_connection_timestamps_map[room]

        return self.num_connections(room)


connection_counter = ConnectionCounter()


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

        Escaping of user input is done here and the escaped version
        is stored to memory.
        """
        if user:
            user = self._text_to_web(user[:config.MAX_NAME_LENGTH])

        with self._lock:
            if room not in self._messages_per_room:
                self._messages_per_room[room] = []

            messages = self._messages_per_room[room]
            messages.append({
                "date": datetime.datetime.utcnow(),
                "uuid": str(uuid.uuid4()),
                "user": user or None,
                "message": self._text_to_web(message[:config.MAX_MESSAGE_LENGTH]).replace("\n", "\n<br/>"),
            })
            self._clean_messages(messages)

    def iter_messages(self, request_uuid: str, room: str = "") -> Generator[dict, None, None]:
        """
        Loop infinitely until new messages arrive.

        :param request_uuid: str, id of the request/response stream
        :param room: str, the chat room name

        :return: generator of dict
            if there's a {"type": "info"} in there it's an info object,
            otherwise it's the message
        """
        # TODO: this set currently grows unlimited
        yielded_ids = set()
        last_yielded_connection_count = -1
        while True:
            messages = None

            with self._lock:
                if room in self._messages_per_room:
                    messages = self._messages_per_room[room]
                    self._clean_messages(messages)
                    messages = list(messages)

            if messages:
                for message in messages:
                    if message["uuid"] not in yielded_ids:
                        yielded_ids.add(message["uuid"])
                        yield message

            num_connections = connection_counter.update_connection(room, request_uuid)
            if num_connections != last_yielded_connection_count:
                yield {"type": "info", "num_connections": num_connections}
                last_yielded_connection_count = num_connections

            time.sleep(config.MESSAGE_CHECK_INTERVAL_SECONDS)

    def _clean_messages(self, messages: List[dict]) -> None:
        """
        Remove messages from the list according to config settings
        """
        while len(messages) > config.MAX_MESSAGES:
            messages.pop(0)

        now = datetime.datetime.utcnow()

        for idx in reversed(range(len(messages))):
            message = messages[idx]
            if (now - message["date"]).total_seconds() > config.MAX_MESSAGE_AGE_SECONDS:
                messages.pop(idx)

    def _text_to_web(self, text: str) -> str:
        return html.escape(emojify(text))
