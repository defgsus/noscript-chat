import scss
from bottle import route, error, request, HTTPResponse, redirect

from .chat import ChatStorage
from .render import render_chat, render_message, render_disclaimer
from . import config


STATICS = {
    "style": scss.Compiler().compile_string((config.STATIC_PATH / "style.scss").read_text()),
}


@error(404)
def error404(error):
    return redirect("/")


@route("/style.css")
def style_view():
    return HTTPResponse(
        STATICS["style"],
        headers={"Content-Type": "text/css"}
    )


@route("/disclaimer")
def disclaimer_view():
    return render_disclaimer()


@route(f"/<room:re:{config.ROOM_REGEX}>")
def chat_view(room):
    yield render_chat(room)
    for message in ChatStorage.singleton().iter_messages(room):
        yield render_message(message)


@route(f"/<room:re:{config.ROOM_REGEX}>", method="POST")
def chat_view(room):
    if request.forms.get("message"):
        ChatStorage.singleton().post_message(
            room=room,
            message=request.forms.get("message"),
            user=request.forms.get("user"),
        )

    yield render_chat(room, user=request.forms.get("user"))
    for message in ChatStorage.singleton().iter_messages(room):
        yield render_message(message)
