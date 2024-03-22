import scss
from bottle import route, error, request, HTTPResponse, redirect

from .chat import ChatStorage
from .render import render_chat, render_message, render_disclaimer
from . import config

_compiler = scss.Compiler()
_base_style = _compiler.compile_string((config.STATIC_PATH / "style.scss").read_text())
_dark_colors_style = _compiler.compile_string((config.STATIC_PATH / "dark-colors.scss").read_text())

STATICS = {
    "style-light.css": _base_style,
    "style-dark.css": "\n".join([_base_style, _dark_colors_style]),
    "style-auto.css": "\n".join([_base_style, f"@media (prefers-color-scheme: dark) {{{_dark_colors_style}}}"]),
    "favicon.ico": (config.STATIC_PATH / "favicon.ico").read_bytes(),
}


@error(404)
def error404(error):
    redirect("/")


@route("/style-<colors:re:[a-z]+>.css")
def style_view(colors: str):
    return HTTPResponse(
        STATICS.get(f"style-{colors}.css", STATICS["style-auto.css"]),
        headers={"Content-Type": "text/css"},
    )


@route("/favicon.ico")
def icon_view():
    return HTTPResponse(
        STATICS["favicon.ico"],
        headers={"Content-Type": "image/x-icon"},
    )


@route("/disclaimer")
def disclaimer_view():
    return render_disclaimer(colors=get_style_colors())


@route(f"/<room:re:{config.ROOM_REGEX}>")
def chat_view(room: str):
    yield from render_chat_endless(room=room)


@route(f"/<room:re:{config.ROOM_REGEX}>", method="POST")
def chat_post_view(room):
    if request.forms.get("message"):
        ChatStorage.singleton().post_message(
            room=room,
            message=request.forms.getunicode("message"),
            user=request.forms.getunicode("user"),
        )

    yield from render_chat_endless(room=room, user=request.forms.getunicode("user"))


def render_chat_endless(room: str = "", user: str = ""):
    yield render_chat(room=room, user=user, colors=get_style_colors())

    for message in ChatStorage.singleton().iter_messages(room):
        yield render_message(message)


def get_style_colors():
    colors = "auto"
    if "light" in request.query:
        colors = "light"
    elif "dark" in request.query:
        colors = "dark"
    return colors
