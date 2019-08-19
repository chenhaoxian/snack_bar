from threading import Timer
from multiprocessing import Process
import requests
import json
from utils import store_snack
from config import config_option
from video_frame.window import msg_info_box

class OrderManager(object):
    def __init__(self):
        self.TIMEOUT = 5
        self.old_info = {}
        self.task = None

    def post_to_server(self, order, session_manger):
        url = config_option['BACKEND_URL']+config_option['POST_ORDER_API']
        try:
            r = requests.post(url, data=json.dumps(order))
            r.raise_for_status()
            session_manger.reset_user_session()
            msg_info_box.open_msg_info_box()
        except Exception as e:
            print(e)


    def create_order(self, user_session, session_manger):
        snack_info_to_server = store_snack.process_order_for_server(user_session['snack_info'])
        user_info = user_session['user_info']
        order_to_server = {
            'user':{
                "nickName":user_info['profile']['nickName'],
                "unionId":user_info['profile']['unionId'],
                'openId':user_info['profile']['openId']},
                "snack_list":snack_info_to_server['record'],
                'location':config_option['LOCATION']
        }
        post = Process(target=self.post_to_server, args=(order_to_server, session_manger))
        post.start()
        post.join()


    def run(self, global_dict):
        while (True):
            # print('order manager running')
            session_manager = global_dict.get('session_manager')
            user_session = session_manager.get_user_session().copy()
            if user_session['session_time'] is 1:
                print('order manager')
                print(user_session)
                self.create_order(user_session, session_manager)


if __name__ == '__main__':
    storage = {'snacks': [1, 2], 'user_infos': [1, 2]}
    order = OrderManager(storage)
    # print(order.validate_order())
    order.run()
    # order.backup_info()
    storage['snacks'] = [1, 3]
    # print(order.is_info_changed())
    order.run()
    # d    self.task = Timer(TIMEOUT, self.create_order)
