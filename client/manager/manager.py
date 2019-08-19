# -*- coding: utf-8 -*-

import sys
from queue import Empty as queueEmpty

from config import logger, config_option
from face_rec import face_rec
from utils import parsers
from utils.encoding_helper import encoding_validation, profile_validation
from utils.logger.decorator import dec_logging
from utils.server_connector import load_all_encoding
from video_frame import CameraController, frame_editor
from video_frame.window import WindowProducer


class Manager(object):
    """The manager for controlling the windows and request to the server"""

    def __init__(self, queue):
        """Initial the environment

        :env: Runtime environmentDISPLAY_CATEGARY
        """
        super(Manager, self).__init__()
        self._known_faces = []
        self._window = None
        self._queue = queue

        self._PROCESS_LEVEL = int(config_option["CAPTURE_LEVEL"])
        self._STRATEGY = str(config_option["STRATEGY"])
        self._TOLERANCE = float(config_option["TOLERANCE"])
        self._DECT_SCALE = float(config_option["DECT_SCALE"])
        self._RESULT_SCALE = float(config_option["RESULT_SCALE"])
        self._DEBUG = bool(eval(config_option["DEBUG"]))

    def config(self, key=None):
        """The config the manager used"""
        if key is None:
            raise Exception("Key for the config must be set")
        # val = self._config.get(self._env, key)
        val = config_option[key]
        return val

    @dec_logging(exit=True)
    def set_known_faces(self, faces):
        """Get encodings from the server

        """
        for face in faces:
            encoding_validation(face)
            profile_validation(face)
        self._known_faces = faces

    @dec_logging
    def run(self, global_dict):
        """Works for the whole face recognition business

        """
        resolution_detect = (int(config_option['FACE_CAMERA_RESOLUTION_DETECT_WIDTH']), int(config_option['FACE_CAMERA_RESOLUTION_DETECT_HEIGHT']))
        resolution_display = (int(config_option['FACE_CAMERA_RESOLUTION_DISPLAY_WIDTH']), int(config_option['FACE_CAMERA_RESOLUTION_DISPLAY_HEIGHT']))
        self._camera = CameraController(int(config_option['FACE_CAMERA_PORT']),resolution=resolution_detect)
        self.set_known_faces(load_all_encoding())
        count = 0
        location_user_infos = []


        self._window = WindowProducer.produce_window(config_option["DISPLAY_STRATEGY"])('Snack Bar')

        def __window_close_call_back():
            sys.exit(0)

        self._window.set_window_close_callback(__window_close_call_back)
        while True:
            self.user_session = global_dict.get('session_manager').get_user_session()

            self._get_new_encoding()

            ret, frame = self._camera.capture()
            frame = frame_editor.pre_adjust(frame, flip=True)
            adjusted_frame = frame_editor.pre_adjust_for_dect(frame, scale=self._DECT_SCALE)

            # Only process every `process_level` frame of video to save time
            if count == self._PROCESS_LEVEL:
                face_encodings_to_check, face_locations = face_rec.detect_face(adjusted_frame)
                known_faces_filtered = list(filter(lambda x: x["faceCode"], self._known_faces))
                location_user_infos = face_rec.recognition(known_faces_filtered,
                                                           zip(face_encodings_to_check, face_locations),
                                                           self._STRATEGY, self._TOLERANCE)
                global_dict.get('session_manager').user_control(location_user_infos)
                count = 0
            else:
                count = count + 1


            frame = frame_editor.draw_info_on_frame(frame, location_user_infos, scale=self._DECT_SCALE,
                                                    show_distance=self._DEBUG)
            frame = frame_editor.post_adjust(frame, scale=self._RESULT_SCALE, debug=self._DEBUG)
            self._window.display(resolution=resolution_display, frame=frame,  user_info=parsers.build_user_info(location_user_infos), user_session=self.user_session)
            self._window.wait_for_close()

        self._camera.release_capture()
        self._window.destroy()

    @dec_logging(exit=False, trace=False)
    def _get_new_encoding(self):
        try:
            new_encoding = self._queue.get(False, timeout=1)
            self._handle_new_encoding(new_encoding)
        except queueEmpty:
            # ignore if no any new encoding
            pass

    def _update_encoding(self, index, encoding):
        if encoding["faceCode"]:
            self._known_faces[index]["faceCode"] = encoding["faceCode"]
            logger.info("Encoding for \"%s\" updated." % (encoding["unionId"],))
        if encoding["profile"]:
            self._known_faces[index]["profile"] = encoding["profile"]
            logger.info("Profile for \"%s\" updated." % (encoding["unionId"],))

    def _insert_encoding(self, encoding):
        self._known_faces.append(encoding)
        logger.info("New user \"%s\" registered." % (encoding["unionId"],))

    def _trace_encoding(self, id):
        for known_face in self._known_faces:
            if known_face["unionId"] == id:
                return self._known_faces.index(known_face)
        return -1

    def _handle_new_encoding(self, encoding):
        encoding_validation(encoding)
        profile_validation(encoding)

        encoding_index = self._trace_encoding(encoding["unionId"])
        if encoding_index == -1:
            self._insert_encoding(encoding)
        else:
            self._update_encoding(encoding_index, encoding)
