from pathlib import Path

from decouple import config


SOURCE_PATH = Path(__file__).resolve().parent

# point to a different set of templates
TEMPLATE_PATH = config("TEMPLATE_PATH", default=SOURCE_PATH / "templates", cast=Path)
# point to different static files
STATIC_PATH = config("STATIC_PATH", default=SOURCE_PATH / "static", cast=Path)

# the network host on which to serve
HOST = config("HOST", default="localhost")
# the network port on which to serve
PORT = config("PORT", default=8000, cast=int)
# turn on debugging with "true"
DEBUG = config("DEBUG", default=False, cast=lambda x: str(x).lower() == "true")
# maximum visitors to serve at once. this translates to the number of required threads
MAX_VISITORS = config("MAX_VISITORS", default=1024, cast=int)

# the complete public url of the website, with protocol
WEBSITE_URL = config("WEBSITE_URL", default="http://localhost:8000")

# messages will be truncated to this length
MAX_MESSAGE_LENGTH = config("MAX_MESSAGE_LENGTH", default=4096, cast=int)
# user names will be truncated to this length
MAX_NAME_LENGTH = config("MAX_NAME_LENGTH", default=100, cast=int)
# sleep time per server thread before delivering new messages
MESSAGE_CHECK_INTERVAL_SECONDS = config("MESSAGE_CHECK_INTERVAL_SECONDS", default=1, cast=float)
# maximum number of messages that are kept in memory
MAX_MESSAGES = config("MAX_MESSAGES", default=20, cast=int)
# maximum number of seconds that messages are kept in memory
MAX_MESSAGE_AGE_SECONDS = config("MAX_MESSAGE_AGE_SECONDS", default=60 * 60 * 2, cast=float)

# regular expression to parse the chat room from the url
ROOM_REGEX = config("ROOM_REGEX", default=r"[a-zA-Z_\-0-9]*")
