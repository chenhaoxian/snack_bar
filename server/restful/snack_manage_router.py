import json
from logger.server_logger import ServerLogger
from flask import Blueprint, request
from services.snack_service import SnackService

snack_manage = Blueprint('snack_manage', __name__)


@snack_manage.route('/api/snack/<snack_code>', methods=['Get'])
@ServerLogger.log
def get_snack_info(snack_code):
    snack_service = SnackService()
    return json.dumps(snack_service.get_snack_by_code(snack_code))


@snack_manage.route('/api/snack', methods=['Post'])
@ServerLogger.log
def update_snack_info():
    snack_data = json.loads(request.data.decode())
    snack_service = SnackService()
    result = snack_service.update_snack(snack_data)
    if result.acknowledged:
        return json.dumps({"result": result.acknowledged})
    else:
        return json.dumps({"result": result.acknowledged}), 401


@snack_manage.route('/api/snack', methods=['Get'])
@ServerLogger.log
def get_snack_list():
    snack_service = SnackService()
    return json.dumps(snack_service.get_snack_list())


@snack_manage.route('/api/snack/<snack_id>', methods=['Post'])
@ServerLogger.log
def remove_snack_info(snack_id):
    snack_service = SnackService()
    result = snack_service.remove_snack(snack_id)
    if result.acknowledged:
        return json.dumps({"result": result.acknowledged})
    else:
        return json.dumps({"result": result.acknowledged}), 401
