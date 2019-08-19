import logging
from datakeeper.data_notifier import DataNotifier
from model.face import *
from dao.face_dao import FaceDao
from util.image_util import image_util
from util.read_config import ConfigReader


class FaceService:

    def __init__(self):
        self.face_dao = FaceDao()
        self.image_util = image_util()
        self.ConfigReader = ConfigReader()
        self.config = self.ConfigReader.get_config()
        self.DataNotifier = DataNotifier()
        self.face_exception_code = int(self.config.get("face", "face_exception_code"))

    def get_all_faces(self):
        all_faces = self.face_dao.find_all()
        return all_faces

    def handle_face_by_id(self, id, file, profile):

        try:
            if file is not None:
                face_code = self.image_util.handle_image(file)
                if face_code is self.face_exception_code:
                    return self.face_exception_code
            else:
                face_code = None

            if profile is not None:
                open_id = profile['openId']
            else:
                open_id = None

            face = Face(unionId=id, faceCode=face_code, profile=profile, openId=open_id)

            if self.face_dao.count_face_by_id(id) is 0:
                if self.face_dao.count_face_by_open_id(open_id) is not 0:
                    res = self.face_dao.update_face_by_open_id(face)
                else:
                    res = self.face_dao.add_face(face)
            else:
                res = self.face_dao.update_face_by_id(face)
            if res is True:
                DataNotifier.publish_change_to_redis_chanel(self.config, face)
            return res

        except Exception as e:
            print("Happen:" + str(e))
            logging.error(str(e))

    def recognize_face_by_image(self, file):
        all_face_list = self.face_dao.find_all()
        known_face_list = []
        profile_list = []
        if len(all_face_list) > 0:
            for face_info in all_face_list:
                if face_info.get('faceCode') is not None:
                    known_face_list.append(face_info.get('faceCode'))
                    profile_list.append(face_info.get('profile'))
        result = self.image_util.recognize_image(known_face_list, file, 0.4, profile_list)
        return result
