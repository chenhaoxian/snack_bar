from util import mongo_connection, read_config
from model.face import *


class FaceDao:
    def __init__(self):
        config = read_config.ConfigReader().get_config()
        self.face_coll_name = config.get("mongodb", "face_coll")
        self.mongo_connector = mongo_connection.MongoConnector()
        self.snackbar_db = self.mongo_connector.init_db()
        self.face_coll = self.snackbar_db[self.face_coll_name]

    def add_face(self, face):
        result = self.face_coll.insert_one(face.__dict__)
        return result.acknowledged

    def update_face_by_id(self, face):
        if face.faceCode is not None and face.profile is not None:
            result = self.face_coll.update_one(
                {"unionId": face.unionId},
                {"$set": {"faceCode": face.faceCode, "profile": face.profile}}
            )
            return result.acknowledged
        elif face.faceCode is None:
            result = self.face_coll.update_one(
                {"unionId": face.unionId},
                {"$set": {"profile": face.profile}}
            )
            return result.acknowledged
        else:
            result = self.face_coll.update_one(
                {"unionId": face.unionId},
                {"$set": {"faceCode": face.faceCode}}
            )
            return result.acknowledged

    def update_face_by_open_id(self, face):
        if face.faceCode is not None and face.profile is not None:
            result = self.face_coll.update_one(
                {"openId": face.openId},
                {"$set": {"faceCode": face.faceCode, "profile": face.profile, "unionId": face.unionId}}
            )
            return result.acknowledged
        elif face.faceCode is None:
            result = self.face_coll.update_one(
                {"openId": face.openId},
                {"$set": {"profile":face.profile, "unionId": face.unionId}}
            )
            return result.acknowledged
        else:
            result = self.face_coll.update_one(
                {"openId": face.openId},
                {"$set": {"faceCode": face.faceCode, "unionId": face.unionId}}
            )
            return result.acknowledged

    def find_all(self):
        cursor = self.face_coll.find({})
        face_list=[]
        for document in cursor:
            if document['faceCode'] is not None:
                face=Face(openId=document['openId'],faceCode=document['faceCode']
                          ,unionId=document['unionId'],profile=document['profile'])
                face_list.append(face.__dict__)
        return face_list

    def get_profile_by_union_id(self,unionId):
        document = self.face_coll.find_one({"unionId":unionId},{"profile":1})
        if document is not None:
            return document.get('profile')
        else:
            return None




    def count_face_by_id(self, id):
        count = self.face_coll.find({"unionId":id}).count()
        return count

    def count_face_by_open_id(self, domain_id):
        count = self.face_coll.find({"openId":domain_id}).count()
        return count

