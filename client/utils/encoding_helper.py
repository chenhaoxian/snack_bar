# -*-coding:utf-8-*-
def encoding_validation(data):
    # New user register will trigger a record not contain the "faceCode" be
    # sent to the Redis
    if not (data and type(data) is dict and ("profile" in data or "unionId" in data) and "faceCode" in data):
        raise EncodingIncorrect("encoding", data)


def profile_validation(data):
    to_check = data["profile"]
    # Pic update will trigger a record not contain the "profile" be
    # sent to the Redis
    if not to_check:
        return

    if not (to_check and type(to_check) is dict and ("nickName" in to_check or "unionId" in to_check)):
        raise EncodingIncorrect("profile", data)


class EncodingIncorrect(Exception):
    # NOTICE: "data" may have sensitive data
    def __init__(self, incorrect_type, data):
        super(EncodingIncorrect, self).__init__(
            "Encoding data incorrect(type: {type}): {data}".format(type=incorrect_type, data=data)
        )
