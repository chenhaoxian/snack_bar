import cv2
import sys
import time
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QApplication,QLabel
from PyQt5.QtCore import Qt
from video_frame.user_info import UserInfo
from video_frame.camera_qt import CameraQWidget
import json

class WindowController(QWidget):
    def __init__(self, name):
        super(QWidget, self).__init__()
        main_layout = QVBoxLayout()
        self.label = QLabel('Domain Id:')
        main_layout.addWidget(self.label)


    def update_text(self, i):
        self.label.setText(i)




if(__name__ == '__main__'):
    app = QApplication(sys.argv)
    mainWin = WindowController('opecv video')

    mainWin.show()

    i = 0
    while(True):
        mainWin.update_text(json.dumps(i))
        i = i+1
        app.processEvents()
        # mainWin.update()
        time.sleep(0.2)

    sys.exit(app.exec_())