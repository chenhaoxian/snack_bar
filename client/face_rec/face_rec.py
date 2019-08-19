import face_recognition


def detect_face(frame):
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    # TODO: Add a structure to maintain the encoding-location relationship
    return face_encodings, face_locations


def recognition(known_face_objs, encoding_locations, strategy, tolerance=0.4):
    """Using different strategy to recognize faces
    :param known_face_objs:
    :param encoding_locations:
    :param strategy:
    :param tolerance:
    :return: [{'face_location': face_location, 'user_info': face_obj, 'distance': distance}]
    """
    location_user_infos = []

    for face_encoding, face_location in encoding_locations:
        # See if the face is a match for the known face(s)
        # if did't match any face, the _get*** will return ({}, 0)
        if strategy == "FIRST_MATCH":
            face_obj, distance = _get_first_match_face(known_face_objs, face_encoding, tolerance)
        elif strategy == "BEST_MATCH":
            face_obj, distance = _get_best_match(known_face_objs, face_encoding, tolerance)
        else:
            raise Exception("Unknown strategy")
        location_user_infos.append({'face_location': face_location, 'user_info': face_obj, 'distance': distance})

    return location_user_infos


def extract_encodings(face_objs):
    known_encodings = [x['faceCode'] for x in face_objs]
    return known_encodings


def _get_first_match_face(known_face_objs, face_encoding, tolerance):
    """
    :param known_face_objs: Include the user info, sample: {"faceCode": "","openId": "", "profile": {}}"
    :param face_encoding: The encoding to compare
    :param tolerance:
    :return: the match face object, sample: {"faceCode": "", "openId": "", "profile": {}}
    """
    result = {}
    known_encodings = extract_encodings(known_face_objs)
    matches = face_recognition.compare_faces(known_encodings, face_encoding, float(tolerance))

    # If a match was found in known_face_encodings, just use the first one.
    if True in matches:
        first_match_index = matches.index(True)
        result = known_face_objs[first_match_index]
    return result, 0


def _get_best_match(known_face_objs, face_encoding, tolerance):
    """
    :param known_face_objs: Include the user info, sample: {"faceCode": "","openId": "", "profile": {}}"
    :param face_encoding: The encoding to compare
    :param tolerance:
    :return: the match face object, sample: {"faceCode": "", "openId": "", "profile": {}}
    """
    best_match_distance = 0
    result = {}
    known_encodings = extract_encodings(known_face_objs)
    distances = face_recognition.face_distance(known_encodings, face_encoding)

    if len(distances):
        best_match_distance = distances.min()
        if best_match_distance < float(tolerance):
            best_match_index = distances.tolist().index(best_match_distance)
            result = known_face_objs[best_match_index]
    return result, best_match_distance
