from dao.face_dao import FaceDao

from model.face import Face


class UserService:

    def __init__(self):
        self.face_dao = FaceDao()

    def handle_user_session(self, id):

        try:
            face = Face(unionId=None, faceCode=None, profile=None, openId=id)
            if self.face_dao.count_face_by_open_id(id) is 0 :
                return self.face_dao.add_face(face)

        except Exception as e:
            print("Happen:" + str(e))
            # logging.error(str(e))