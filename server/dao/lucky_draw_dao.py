import time
from bson.objectid import ObjectId
from util import mongo_connection, read_config
from model.lucky_draw_result import LuckyDrawResult


class LuckyDrawDao:

    def __init__(self):
        config = read_config.ConfigReader().get_config()
        self.mongo_connector = mongo_connection.MongoConnector()
        self.snackbar_db = self.mongo_connector.init_db()
        self.lucky_draw_coll = self.snackbar_db[config.get("mongodb", "lucky_draw_coll")]
        self.face_coll = self.snackbar_db[config.get("mongodb", "face_coll")]
        self.prize_lowest_level = int(config.get("lucky_draw", "prize_lowest_level"))

    def count_prize_by_unionid(self, unionid):
        count = self.lucky_draw_coll.find({"unionid": unionid}).count()
        return count

    def add_lucky_draw(self, lucky_draw):
        result = self.lucky_draw_coll.insert_one(lucky_draw)
        return result.acknowledged

    def get_last_create_date_by_unionid(self, unionid):
        cursor = self.lucky_draw_coll.find({"unionId": unionid}, {"createDate": 1}).sort([('createDate', -1)])
        if cursor.count() >= 1:
            create_date = cursor.next().get('createDate')
        else:
            create_date = None
        return create_date

    def get_all_results_with_prize(self):
        cursor = self.lucky_draw_coll.find({"prize.prizeLevel": {"$lt": self.prize_lowest_level}}).sort(
            [('createDate', -1)])
        lucky_draw_result_with_prize = []
        if cursor is not None:
            for document in cursor:
                lucky_draw_result = LuckyDrawResult(document.get('_id').__str__(), document.get('prize'),
                                                    document.get('unionId'), document.get('isRedeem'),
                                                    document.get('createDate'), document.get('userInfo'))
                lucky_draw_result_with_prize.append(lucky_draw_result.__dict__)
        return lucky_draw_result_with_prize

    def update_redeem_result(self, id):
        result = self.lucky_draw_coll.update_one({"_id": ObjectId(id)}, {"$set": {"isRedeem": True}})
        return result


if __name__ == '__main__':
    ld = LuckyDrawDao()
    create_date = ld.get_last_create_date_by_unionid('ogQAs09RnlIsqtZ2CVa0VKurjUsw')
    print(create_date)
    print(type(create_date))
    time_test = time.strptime(create_date, "%Y-%m-%d %H:%M:%S")
    print(time_test)
    print(time.localtime())
    # now = time.strptime(time.localtime(), "%Y-%m-%d %H:%M:%S")#time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(time.localtime().tm_yday - time_test.tm_yday)
