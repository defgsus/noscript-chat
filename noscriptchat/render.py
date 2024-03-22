import datetime
import html
import secrets
from typing import Generator, Optional, Dict, List

import bottle
from jinja2.loaders import FileSystemLoader
from jinja2 import Template, Environment

from . import config, emojify


_template_environment = Environment(
    loader=FileSystemLoader(config.TEMPLATE_PATH),
)

_index_template = _template_environment.get_template("index.html")
_message_template = _template_environment.get_template("message.html")
_disclaimer_template = _template_environment.get_template("disclaimer.html")
_emojis_template = _template_environment.get_template("emojis.html")

_short_emoji_map = {
    name: chr(code)
    for name, code in emojify.singleton.emoji_map.items()
    if len(name) <= 20
}


def render_chat(
        room: str,
        user: Optional[str] = None,
        colors: str = "auto",
) -> str:
    """
    Renders the beginning of index.html for a specific room
    """
    url = config.WEBSITE_URL.split("://", 1)[-1]
    if room:
        url = f"{url}/{room}"

    return _index_template.render(
        page="chat",
        query=f"?{bottle.request.query_string}" if bottle.request.query_string else "",
        style=f"style-{colors}.css",
        random_room=get_random_room_name(),

        title=f"{room}@{url}" if room else url,
        url=url,
        room=room or "",
        user=user or "",
    )


def render_disclaimer(colors: str = "auto"):
    return _disclaimer_template.render(
        page="disclaimer",
        query=f"?{bottle.request.query_string}" if bottle.request.query_string else "",
        style=f"style-{colors}.css",
        random_room=get_random_room_name(),

        title="Disclaimer",
        url=config.WEBSITE_URL,
    )


def render_emoji_page(colors: str = "auto"):
    return _emojis_template.render(
        page="emojis",
        query=f"?{bottle.request.query_string}" if bottle.request.query_string else "",
        style=f"style-{colors}.css",
        random_room=get_random_room_name(),

        title="Emojis",
        url=config.WEBSITE_URL,
        emoji_map=_short_emoji_map,
    )


def render_message(message: dict):
    """
    Renders a single message
    """
    message = message.copy()
    is_new = (datetime.datetime.utcnow() - message["date"]).total_seconds() <= config.MESSAGE_CHECK_INTERVAL_SECONDS * 3

    message["date"] = message["date"].strftime("%Y-%m-%d %H:%M UTC")
    message["user"] = message["user"] or "anonymous"
    message["classes"] = "new" if is_new else ""

    return _message_template.render(**message)


def get_random_room_name():
    return secrets.token_urlsafe(16)
