def build_user_info(locatin_user_infos):
    wechat_name = 'Unknown'
    # TODO: display domain_id after the server binding the info
    domain_id = 'Unknown'

    if len(locatin_user_infos) > 0:
        user_info = locatin_user_infos[0]["user_info"]
        # Only display one person info on the GUI
        wechat_name = get_nick_name(user_info)

    return {'wechatName': wechat_name, 'domainId': domain_id}


def get_nick_name(user_info):
    nick_name = ""
    if user_info:
        if user_info["profile"].get("customizedNickName") != None and user_info["profile"].get("customizedNickName") != "":
            nick_name = user_info["profile"]["customizedNickName"]
        else:
            nick_name = user_info["profile"]["nickName"]
    return nick_name


def parser_camera_display_info(face_obj) -> str:
    """
    :param face_obj: the face_obj from server, and the distance tuple, sample: (face_obj, distance)
    :return: a string to display on the frame
    """
    if not face_obj:
        return "Unknown"
    elif face_obj["profile"].get("customizedNickName") != None and face_obj["profile"].get("customizedNickName") != "":
        return face_obj['profile']['customizedNickName']
    else:
        return face_obj['profile']['nickName']
