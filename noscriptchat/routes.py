import scss
from bottle import route, error, request, HTTPResponse, redirect

from .chat import render_chat, render_message, ChatStorage
from . import config


STATICS = {
    "style": scss.Compiler().compile_string((config.STATIC_PATH / "style.scss").read_text()),
}


@error(404)
def error404(error):
    return redirect("/")


@route('/style.css')
def style_view():
    return HTTPResponse(
        STATICS["style"],
        headers={"Content-Type": "text/css"}
    )


@route('/')
def index_view():
    yield render_chat("")
    for message in ChatStorage.singleton().iter_messages(""):
        yield render_message(message)


@route('/<room:path>')
def chat_view(room):
    yield render_chat(room)
    for message in ChatStorage.singleton().iter_messages(room):
        yield render_message(message)


@route('/<room:path>', method="POST")
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
