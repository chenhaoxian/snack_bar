# coding:utf8

import json
from flask import Blueprint, request
from logger.server_logger import ServerLogger
from services.face_service import FaceService
from util.read_config import ConfigReader
face_recog = Blueprint('face_recog', __name__)


@face_recog.route('/api/faces')
@ServerLogger.log
def get_all():
    face_service = FaceService()

    all_faces = face_service.get_all_faces()

    return json.dumps(all_faces, ensure_ascii=False)


@face_recog.route('/api/faces/<union_id>', methods=['Post'])
@ServerLogger.log
def handle_image(union_id):
    face_service = FaceService()
    config = ConfigReader().get_config()
    face_exception_code = int(config.get("face", "face_exception_code"))
    if union_id is None:
        return None

    file = None
    profile = None
    if 'file' in request.files:
        file = request.files['file']
    if 'profile' in request.form:
        profile = json.loads(request.form['profile'])

    res = face_service.handle_face_by_id(union_id, file, profile)
    if res == face_exception_code:
        return json.dumps({"status": res}), 401

    return json.dumps({"status": res})


@face_recog.route('/api/face', methods=['Post'])
@ServerLogger.log
def recognize_face():
    face_service = FaceService()
    if 'file' in request.files:
        file = request.files['file']
        result = face_service.recognize_face_by_image(file)
        return json.dumps({"isRecognized": True, "result": result}, ensure_ascii=False)
    else:
        return json.dumps({"isRecognized": False, "errmsg": "Please upload a image!"}), 400
