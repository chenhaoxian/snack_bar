# coding=utf-8
from flask import Flask

from logger.server_logger import ServerLogger

from restful.lucky_draw_router import lucky_draw
from restful.message_post_router import message_post
from restful.face_recog_router import face_recog
from restful.user_session_router import user_session
from restful.snack_manage_router import snack_manage

app = Flask(__name__)

app.register_blueprint(face_recog)
app.register_blueprint(lucky_draw)
app.register_blueprint(message_post)
app.register_blueprint(user_session)
app.register_blueprint(snack_manage)


@app.route('/')
def index():
    return "Hello, World"


@app.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Origion"] = "*"
    response.headers["Access-Control-Allow-Method"] = "Get, Post"
    return response


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000
    )
