import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from video_frame.camera import CameraController


class CameraQWidget(QLabel):
    def __init__(self, frame=None):
        QWidget.__init__(self)
        self.camera_frame = frame
        # self.camera = CameraController()

    def set_frame(self, frame):
        self.camera_frame = frame

    def render(self, camera=None):
        if(camera is not None):
            self.camera_frame = camera

        if(self.camera_frame is None):
            return
        else:
            cv_img_rgb = cv2.cvtColor(self.camera_frame, cv2.COLOR_BGR2RGB)
            q_image = QImage(cv_img_rgb[:], cv_img_rgb.shape[1], cv_img_rgb.shape[0], cv_img_rgb.shape[1] * 3,
                             QImage.Format_RGB888)
            self.setPixmap(QPixmap.fromImage(q_image))

