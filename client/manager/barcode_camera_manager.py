# -*- coding: utf-8 -*-

import sys

from utils.logger.decorator import dec_logging
from video_frame import CameraController
from video_frame.barcode_decorator import BarcodeDetection
from video_frame.window import WindowProducer
from config import config_option

class BarcodeCameraManager(object):
    def __init__(self):
        self._window = WindowProducer.produce_window('CameraOnlyWindow')('Barcode Detection')
        self.old_frame = []
        def __window_close_call_back():
            sys.exit(0)

        self.barcode_detection = BarcodeDetection()
        self._window.set_window_close_callback(__window_close_call_back)


    @dec_logging
    def run(self, user_session):
        resolution_detect = (int(config_option['BARCODE_CAMERA_RESOLUTION_DETECT_WIDTH']), int(config_option['BARCODE_CAMERA_RESOLUTION_DETECT_HEIGHT']))
        resolution_display = (int(config_option['BARCODE_CAMERA_RESOLUTION_DISPLAY_WIDTH']), int(config_option['BARCODE_CAMERA_RESOLUTION_DISPLAY_HEIGHT']))

        self.camera = CameraController(int(config_option['BARCODE_CAMERA_PORT']),resolution=resolution_detect)
        self.user_session = user_session
        self.haveDetectBarcode = False
        count = 0
        while True:
            ret, frame = self.camera.capture()
            # if(not self.haveDetectBarcode):

            if(count == 25):
                self.haveDetectBarcode, frame = self.barcode_detection.barcode_decorator(frame, self.user_session)
                count = 0
            count = count+1

            self._window.display(frame=frame, resolution=resolution_display, pos=(0,0))
            self._window.wait_for_close()

        self._camera.release_capture()
        self._window.destroy()


