import datetime
import pymongo
from bson.objectid import ObjectId
from util import mongo_connection, read_config
from model.order import Order


class OrderDao:
    def __init__(self):
        config = read_config.ConfigReader().get_config()
        self.order_coll_name = config.get("mongodb", "order_coll")
        self.face_coll_name = config.get("mongodb", "face_coll")
        self.mongo_connector = mongo_connection.MongoConnector()

        self.snackbar_db = self.mongo_connector.init_db()
        self.order_coll = self.snackbar_db[self.order_coll_name]
        self.face_coll = self.snackbar_db[self.face_coll_name]

    def get_order_by_user(self, user):
        cursor = self.order_coll.find({"user.unionId": user}).sort("created_date", pymongo.DESCENDING)
        order_list = []
        if cursor is not None:
            for document in cursor:
                order_utc_time_str = document.get('created_date')
                order_east_eight_zone_time = datetime.datetime.strptime(order_utc_time_str, "%Y/%m/%d %H:%M:%S") + datetime.timedelta(hours=8)
                order_east_eight_zone_time_str = order_east_eight_zone_time.strftime("%Y/%m/%d %H:%M:%S")
                order = Order(document.get('_id').__str__(), document.get('user'), document.get('snack_list'),
                              document.get('total_price'),
                              document.get('total_amount'), order_east_eight_zone_time_str, document.get('location'))
                order_list.append(order.__dict__)
        return order_list

    def add_order(self, user, snack_list, location):
        total_price = 0
        total_amount = 0
        utc_time = datetime.datetime.utcnow()
        utc_time_with_format = utc_time.strftime("%Y/%m/%d %H:%M:%S")
        for snack in snack_list:
            total_price += float(snack['snack_price']) * float(snack['amount'])
            total_amount += snack['amount']
        order = {
            "user": user,
            "total_price": total_price,
            "snack_list": snack_list,
            "total_amount": total_amount,
            "created_date": utc_time_with_format,
            "location": location
        }
        result = self.order_coll.insert_one(order)
        return result

    def remove_order(self, order_id):
        result = self.order_coll.delete_one({"_id": ObjectId(order_id)})
        return result
