# -*- coding: utf-8 -*-

import cv2

from utils.logger.decorator import dec_logging


@dec_logging(exit=True, trace=True)
class CameraController(object):
    def __init__(self, webcam_handle=0, resolution=(640, 480)):
        # Get a reference to webcam #0 (the default one)
        self._video_capture = cv2.VideoCapture(webcam_handle)
        if not self._video_capture.isOpened():
            raise Exception("Camera #{handle} is not opened.".format(handle=webcam_handle))
        self._video_capture.set(3, int(resolution[0]))
        self._video_capture.set(4, int(resolution[1]))

    def capture(self):
        # Grab a single frame of video
        ret, frame = self._video_capture.read()
        if not ret:
            raise Exception("Read frame from camera failed.")
        return ret, frame

    def release_capture(self):
        # Release handle to the webcam
        self._video_capture.release()
