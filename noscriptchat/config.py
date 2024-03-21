from pathlib import Path

from decouple import config


SOURCE_PATH = Path(__file__).resolve().parent

TEMPLATE_PATH = SOURCE_PATH / "templates"
STATIC_PATH = SOURCE_PATH / "static"

HOST = config("HOST", default="localhost")
PORT = config("PORT", default=8000, cast=int)
DEBUG = config("DEBUG", default=False, cast=lambda x: str(x).lower() == "true")
MAX_VISITORS = config("MAX_VISITORS", default=1024, cast=int)

WEBSITE_URL = config("WEBSITE_URL", default="https://noscript-chat.de")

MAX_MESSAGE_LENGTH = config("MAX_MESSAGE_LENGTH", default=1000, cast=int)
MAX_NAME_LENGTH = config("MAX_NAME_LENGTH", default=100, cast=int)
MESSAGE_CHECK_INTERVAL = config("MESSAGE_CHECK_INTERVAL", default=1, cast=float)
MAX_MESSAGES = config("MAX_MESSAGES", default=20, cast=int)

ROOM_REGEX = config("ROOM_REGEX", default=r"[a-z_\-0-9]*")
