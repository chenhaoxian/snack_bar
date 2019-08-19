import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication

from .basic_window import BasicWindow
from video_frame.camera_qt import CameraQWidget
from video_frame.user_info import UserInfo
from utils.store_snack import StoreSnack
from utils import  parsers
import cv2

class MoreUserInfoWindow(QWidget, BasicWindow):
    def __init__(self, name):
        self.app = QApplication(sys.argv)
        super(QWidget, self).__init__()
        super(BasicWindow, self).__init__()
        self.setLayout(self.define_page_element())
        self._name = name
        self.close_callback = None

    def define_page_element(self):
        main_layout = QVBoxLayout()
        self.user_info = UserInfo()
        self.camera = CameraQWidget()
        main_layout.addWidget(self.user_info)
        main_layout.addWidget(self.camera)
        return main_layout

    def get_app(self):
        return self.app

    def update_frame(self, frame):
        self.camera.render(frame)

    def update_user_info(self, user_info):
        wechatName = parsers.get_nick_name(user_info)
        self.user_info.set_weichat_name(wechatName)
        # self.user_info.set_domain_id(user_info['domainId'])

    def display(self, resolution=(), pos=(), **data):
        # Display the resulting image
        frame = data['frame']
        if (any(resolution)):
            frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_CUBIC)

        self.show()
        self.update_frame(frame)
        self.update_user_info(data.get('user_session')['user_info'])
        order_data  = data.get('user_session')['snack_info']
        # if(any(order_data)):
        self.user_info.set_snack(order_data)
        self.app.processEvents()

    def set_window_close_callback(self,func):
        self.close_callback = func


    def keyPressEvent(self, e):
        if(e.key() == Qt.Key_Q and self.close_callback is not None):
            self.close_callback()
            # sys.exit()


