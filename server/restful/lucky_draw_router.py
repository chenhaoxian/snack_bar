#coding:utf8

# coding=utf-8
import json
from flask import Blueprint, request
from logger.server_logger import ServerLogger
from services.lucky_draw_service import LuckyDrawService


lucky_draw = Blueprint('lucky_draw',__name__)


@lucky_draw.route('/api/luckydraw/prize/<unionid>', methods=['Get'])
@ServerLogger.log
def prize(unionid):
    prize_service = LuckyDrawService()
    response = prize_service.prize_drawing(unionid)
    return json.dumps(response)


@lucky_draw.route('/api/luckydraw/quota/<unionid>', methods=['Get'])
@ServerLogger.log
def quota(unionid):
    ld_service = LuckyDrawService()
    quota = ld_service.get_number_of_remaining_draw_by_unionid(unionid)

    return json.dumps({'quota': quota})


@lucky_draw.route('/api/luckydraw/prize', methods=['Get'])
@ServerLogger.log
def get_lucky_draw_result():
    prize_service = LuckyDrawService()
    response = prize_service.get_lucky_draw_result()
    return json.dumps(response, ensure_ascii=False)


@lucky_draw.route('/api/luckydraw/prize', methods=['Post'])
@ServerLogger.log
def update_redeem_result():
    lucky_draw_data = json.loads(request.data.decode())
    lucky_draw_service = LuckyDrawService()
    result = lucky_draw_service.update_redeem_result(lucky_draw_data['id'])
    if result.acknowledged:
        return json.dumps({"result": result.acknowledged})
    else:
        return json.dumps({"result": result.acknowledged}), 401
