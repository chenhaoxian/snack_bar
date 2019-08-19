import face_recognition
import pickle
import base64
import json
FACE_EXCEPTION_CODE = 2


class image_util:

    def __init__(self) -> None:
        super().__init__()

    def handle_image(self, file):
        image = face_recognition.load_image_file(file)
        face_locations = face_recognition.face_locations(image)
        if len(face_locations) is not 1:
            return FACE_EXCEPTION_CODE

        image_encoding = face_recognition.face_encodings(image, face_locations)[0]

        return image_encoding.tolist()

    def recognize_image(self, known_face_list, unknown_face_file, tolerance, profile_list):
        unknown_face_image = face_recognition.load_image_file(unknown_face_file)
        unknown_face_locations = face_recognition.face_locations(unknown_face_image)
        unknown_face_encodings = face_recognition.face_encodings(unknown_face_image, unknown_face_locations)
        result = []
        for unknown_face_encoding, unknown_face_location in zip(unknown_face_encodings, unknown_face_locations):
            distances = face_recognition.face_distance(known_face_list, unknown_face_encoding)
            if len(distances):
                best_match_distance = distances.min()
                if best_match_distance < float(tolerance):
                    best_match_index = distances.tolist().index(best_match_distance)
                    face_info = {
                        "face_location": unknown_face_location,
                        "name": profile_list[best_match_index].get("nickName")
                    }
                    result.append(face_info)
                else:
                    face_info = {
                        "face_location": unknown_face_location,
                        "name": "unknown"
                    }
                    result.append(face_info)
        return result
