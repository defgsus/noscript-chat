import datetime
from typing import Generator, Optional, Dict, List

import bottle

from noscriptchat import config


_index_template = (config.TEMPLATE_PATH / "index.html").read_text()
_message_template = (config.TEMPLATE_PATH / "message.html").read_text()
_disclaimer_template = (config.TEMPLATE_PATH / "disclaimer.html").read_text()


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

    return bottle.template(
        _index_template,
        title=f"{room}@{url}" if room else url,
        url=url,
        room=room or "",
        user=user or "",
        style=f"style-{colors}.css",
    )


def render_disclaimer(colors: str = "auto"):
    return bottle.template(
        _disclaimer_template,
        title="Disclaimer",
        url=config.WEBSITE_URL,
        style=f"style-{colors}.css",
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
    # bottle.template already escapes everything
    # message["message"] = html.escape(message["message"])
    return bottle.template(_message_template, **message)

