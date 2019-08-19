import time
import pymongo
from util import mongo_connection, read_config
from model.form import Form


class FormDao:
    def __init__(self):
        config = read_config.ConfigReader().get_config()
        self.form_coll_name = config.get("mongodb", "form_coll")
        self.mongo_connector = mongo_connection.MongoConnector()

        self.snackbar_db = self.mongo_connector.init_db()
        self.form_coll = self.snackbar_db[self.form_coll_name]

    def add_form(self, id, form_id, expire_date, is_useful):
        form = {
            "union_id": id,
            "form_id": form_id,
            "expire_date": expire_date,
            "is_useful": is_useful
        }
        result = self.form_coll.insert_one(form)
        return result

    def get_available_form_id(self, id):
        now_time = time.time()
        cursor = self.form_coll.find({"union_id": id, "expire_date": {"$gt": now_time}, "is_useful": True}).sort(
            "expire_date", pymongo.ASCENDING)
        form_list = []
        if cursor.count() is not 0:
            for document in cursor:
                form = Form(document.get('union_id'), document.get('form_id'),
                            document.get('expire_date'),
                            document.get('is_useful'))
                form_list.append(form.__dict__)
            return form_list
        else:
            return None

    def update_form_unavailable(self, form_id):
        result = self.form_coll.update_one({"form_id": form_id}, {"$set": {"is_useful": False}})
        return result

    def remove_form_by_id(self, form_id):
        result = self.form_coll.delete_one({"form_id": form_id})
        return result
