from pathlib import Path

from decouple import config


SOURCE_PATH = Path(__file__).resolve().parent

TEMPLATE_PATH = SOURCE_PATH / "templates"
STATIC_PATH = SOURCE_PATH / "static"

HOST = config("HOST", default="localhost")
PORT = config("PORT", default=8000, cast=int)
DEBUG = config("DEBUG", default=False, cast=lambda x: str(x).lower() == "true")
MAX_THREADS = config("MAX_THREADS", default=16, cast=int)

URL = config("URL", default="noscript-chat.de")

MAX_MESSAGE_LENGTH = config("MAX_MESSAGE_LENGTH", default=1000, cast=int)
MESSAGE_CHECK_INTERVAL = config("MESSAGE_CHECK_INTERVAL", default=1, cast=float)
