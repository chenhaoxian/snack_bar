import json
import requests
import time
from dao.form_dao import FormDao
from services.order_service import OrderService
from util import read_config


class FormService:
    def __init__(self):
        self.form_dao = FormDao()
        self.order_service = OrderService()
        self.config = read_config.ConfigReader().get_config()

    def save_form(self, id, form_id, expire_date, is_useful):
        result = self.form_dao.add_form(id, form_id, expire_date, is_useful)
        return result

    def get_available_form_id(self, id):
        available_form = self.form_dao.get_available_form_id(id)
        return available_form

    def update_form_unavailable(self, form_id):
        result = self.form_dao.update_form_unavailable(form_id)
        return result

    def examine_available_form_by_union_id(self, union_id):
        result = self.form_dao.get_available_form_id(union_id)
        if result is None:
            return False
        else:
            return True

    def post_order_info(self, user, access_token):
        available_form_list = self.get_available_form_id(user['unionId'])
        post_message_url = self.config.get("wechat", "post_message_url")
        post_message_template_id = self.config.get("wechat", "post_message_template_id")
        keyword_color = self.config.get("wechat", "post_message_keyword_color")
        post_message_mark = self.config.get("wechat", "post_message_mark")
        if available_form_list is not None:
            order_list_by_user = self.order_service.get_order_by_user(user['unionId'])
            if order_list_by_user.__len__() > 0:
                latest_order = order_list_by_user[0]
                available_form = available_form_list[0]
                time_show_str = time.strftime("%Y年%m月%d日 %H:%M:%S", time.strptime(latest_order.get('created_date'), "%Y/%m/%d %H:%M:%S"))
                location_show_str = latest_order.get('location')
                total_price_show_str = "￥" + str(latest_order.get('total_price'))
                post_url = post_message_url + access_token
                post_data = {
                    'page': 'pages/order/order',
                    'touser': user['openId'],
                    'template_id': post_message_template_id,
                    'form_id': available_form['form_id'],
                    'data': {
                        'keyword1': {'value': time_show_str, 'color': keyword_color},
                        'keyword2': {'value': location_show_str, 'color': keyword_color},
                        'keyword3': {'value': total_price_show_str, 'color': keyword_color},
                        'keyword4': {'value': post_message_mark, 'color': keyword_color}
                    }
                }
                requests.post(post_url, json.dumps(post_data))
                result = self.update_form_unavailable(available_form['form_id'])
                return result
            return None
        else:
            return None
