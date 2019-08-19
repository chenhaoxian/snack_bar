import json, requests
from logger.server_logger import ServerLogger
from flask import Blueprint, request
from services.form_service import FormService
from services.order_service import OrderService
from util.read_config import ConfigReader
message_post = Blueprint('message_post', __name__)


@message_post.route('/api/access_token', methods=['Get'])
@ServerLogger.log
def get_access_token():
    config = ConfigReader().get_config()
    app_id = config.get("wechat", "app_id")
    secret = config.get("wechat", "secret")
    access_token_url = config.get("wechat", "access_token_url")
    url = access_token_url + app_id + '&secret=' + secret
    access_token = requests.get(url)
    return access_token.content.decode()


@message_post.route('/api/form_info', methods=['Post'])
@ServerLogger.log
def save_form_info():
    form_data = json.loads(request.data.decode())
    form_service = FormService()
    id = form_data['unionId']
    form_id = form_data['formId']
    expire_date = form_data['expire']
    is_useful = True
    result = form_service.save_form(id, form_id, expire_date, is_useful)
    if result.acknowledged:
        return json.dumps({"result": result.acknowledged})
    else:
        return json.dumps({"result": result.acknowledged}), 401


@message_post.route('/api/form_info/<union_id>', methods=['Get'])
@ServerLogger.log
def examine_available_form_by_union_id(union_id):
    form_service = FormService()
    result = form_service.examine_available_form_by_union_id(union_id)
    return json.dumps({"result": result})


@message_post.route('/api/order/<user>', methods=['Get'])
@ServerLogger.log
def get_order_by_user(user):
    order_service = OrderService()
    return json.dumps(order_service.get_order_by_user(user))


@message_post.route('/api/order', methods=['Post'])
@ServerLogger.log
def add_order():
    order_data = json.loads(request.data.decode())
    order_service = OrderService()
    user = order_data['user']
    snack_list = order_data['snack_list']
    location = order_data['location']
    result = order_service.add_order(user, snack_list, location)
    add_order_result_status = result.acknowledged
    if add_order_result_status:
        form_service = FormService()
        access_token = get_access_token()
        form_service.post_order_info(user, json.loads(access_token)['access_token'])
        return json.dumps({"result": add_order_result_status})
    else:
        return json.dumps({"result": add_order_result_status}), 401

