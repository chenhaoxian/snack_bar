from bson.objectid import ObjectId
from util import mongo_connection, read_config
from model.snack import Snack


class SnackDao:
    def __init__(self):
        config = read_config.ConfigReader().get_config()
        self.snack_coll_name = config.get("mongodb", "snack_coll")
        self.mongo_connector = mongo_connection.MongoConnector()

        self.snackbar_db = self.mongo_connector.init_db()
        self.snack_coll = self.snackbar_db[self.snack_coll_name]

    def update_snack(self, snack):
        result = self.snack_coll.update_one(
            {"_id": ObjectId(snack.get('id'))},
            {"$set": {"snack_code": snack.get('snack_code'), "snack_name": snack.get('snack_name'),
                      "snack_price": snack.get('snack_price'), "location": snack.get('location')}},
            upsert=True
        )
        return result

    def get_snack_list(self, criteria):
        cursor = self.snack_coll.find(criteria)
        snack_list = []
        if cursor is not None:
            for document in cursor:
                snack = Snack(document.get('_id').__str__(), document.get('snack_code'), document.get('snack_name'), document.get('snack_price'), document.get('location'))
                snack_list.append(snack.__dict__)
        return snack_list

    def remove_snack(self, snack_id):
        result = self.snack_coll.delete_one({"_id": ObjectId(snack_id)})
        return result
