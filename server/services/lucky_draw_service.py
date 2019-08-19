import time
from dao.lucky_draw_dao import LuckyDrawDao
from dao.face_dao import FaceDao
from util import random_util
from util import date_util


class LuckyDrawService:
    def __init__(self):
        self.lucky_draw_dao = LuckyDrawDao()
        self.face_dao = FaceDao()
        self.date_util = date_util.date_util()
        self.prize_tua = [(['a0', 4, '谢谢参与'], 85), (['a1', 1, '神秘大奖'], 1), (['a2', 2, '百醇饼干一盒'], 2),
                          (['a3', 3, '卫龙辣条一包'],6), (['a4', 3, 'QQ糖一包'], 6)]

    def prize_drawing(self, unionid):
        last_prize_date_str = self.lucky_draw_dao.get_last_create_date_by_unionid(unionid)
        date_interval = self.date_util.get_day_interval_with_sysdate_by_time_str(last_prize_date_str)

        if date_interval is None or date_interval >= 1:
            userInfo = self.face_dao.get_profile_by_union_id(unionid)
            if userInfo is not None:
                lucky_draw = {}
                lucky_draw['unionId'] = unionid
                lucky_draw['userInfo'] = userInfo
                lucky_draw['createDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                lucky_draw['isRedeem'] = False
                prize_result = random_util.random_util(self.prize_tua)()
                prize = {}
                prize['code'] = prize_result[0]
                prize['prizeLevel'] = prize_result[1]
                prize['prizeName'] = prize_result[2]
                lucky_draw['prize'] = prize
                self.lucky_draw_dao.add_lucky_draw(lucky_draw)
                lucky_draw['_id'] = None
                return lucky_draw
            else:
                return None
        else:
            return None

    def get_number_of_remaining_draw_by_unionid(self, unionid):
        last_prize_date_str = self.lucky_draw_dao.get_last_create_date_by_unionid(unionid)
        if last_prize_date_str is None:
            return 1

        date_interval = self.date_util.get_day_interval_with_sysdate_by_time_str(last_prize_date_str)
        if date_interval >= 1:
            return 1
        else:
            return 0

    def get_lucky_draw_result(self):
        return self.lucky_draw_dao.get_all_results_with_prize()

    def update_redeem_result(self, id):
        return self.lucky_draw_dao.update_redeem_result(id)

#
# if __name__ == '__main__':
#     ld_service = LuckyDrawService()
#     ld = ld_service.prize_drawing('ogQAs09RnlIsqtZ2CVa0VKurjUsw')
#     print(ld)
