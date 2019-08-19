import json
import requests
from logger.server_logger import ServerLogger
from flask import Blueprint, request, Response
from services.user_service import UserService
from services.wechat_service import WechatService
from services.face_service import FaceService
from util.read_config import ConfigReader

user_session = Blueprint('user_session', __name__)


@user_session.route('/api/user/<code>', methods=['Get'])
@ServerLogger.log
def get_user_session(code):
    config = ConfigReader().get_config()
    app_id = config.get("wechat", "app_id")
    secret = config.get("wechat", "secret")
    user_session_url = config.get("wechat", "user_session_url")
    url = user_session_url + app_id + '&secret=' + secret + '&grant_type=authorization_code&js_code=' + code
    user_session_from_wechat = requests.get(url)
    user_service = UserService()
    if user_session is not None:
        user_service.handle_user_session(json.loads(user_session_from_wechat.text).get('openid'))
        return Response(user_session_from_wechat.text)
    return Response('failed')


@user_session.route('/api/user', methods=['Post'])
@ServerLogger.log
def get_user_profile():
    config = ConfigReader().get_config()
    app_id = config.get("wechat", "app_id")
    try:
        data = json.loads(request.data.decode())
        encryptedData = data.get('encryptedData')
        iv = data.get('iv')
        sessionKey = data.get('sessionKey')
        pc = WechatService(app_id, sessionKey)
        user_profile = pc.decrypt(encryptedData, iv)
        face_service = FaceService()
        # user_profile['unionId'] = user_profile['unionId']
        face_service.handle_face_by_id(user_profile['unionId'], None, user_profile)
        return json.dumps(user_profile)

    except Exception as e:
        print(str(e))
        # app.logger.info(str(e))
        return Response('failed', 500)
