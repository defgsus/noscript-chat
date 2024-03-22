import random
import threading
import time
from functools import partial

import requests


WORDS = [
    "in", "for", "this", "is",
    "i", "you", "it",
    "glorious", "wonderful", "excellent", "real",
]

PHRASES = [
    "uh", "ar", "bo", "um", "le", "ba", "ki", "da", "mo",
]


def run_mock(
        host: str,
        port: int,
        users: int = 3,
        room: str = "mock",
):
    threads = []
    for i in range(users):
        user = "".join(random.choices(PHRASES, k=random.randrange(3, 7))).capitalize()
        threads.append(threading.Thread(
            target=partial(_mock_mainloop, host, port, room, user)
        ))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def _mock_mainloop(
        host: str,
        port: int,
        room: str,
        user: str,
):
    while True:

        message = " ".join(random.choices(WORDS, k=random.randrange(2, 6))).capitalize() + random.choice(".!?")

        try:
            requests.post(
                f"http://{host}:{port}/{room}",
                data={"user": user, "message": message},
                timeout=1.,
            )
        except requests.ConnectionError:
            pass

        time.sleep(random.uniform(1, 7))
