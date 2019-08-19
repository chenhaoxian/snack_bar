from PyQt5.QtGui import (QPixmap,QImage)
from PyQt5.QtWidgets import QWidget,QLabel,QApplication,QPushButton,QMainWindow,QGridLayout, QHBoxLayout, QVBoxLayout, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

import cv2
import sys
import time

class OpenCvVideo(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        main_layout = QVBoxLayout()
        basic_info_layout = QVBoxLayout()
        info_layout = QFormLayout()
        basic_info_layout.addLayout(info_layout)
        camera_layout = QVBoxLayout()
        camera_layout.setAlignment(Qt.AlignTop)
        main_layout.addLayout(basic_info_layout)
        main_layout.addLayout(camera_layout)

        name_label = QLabel()
        weichat_label = QLabel()
        total_price_label = QLabel()
        statistic_table = QTableWidget()
        statistic_table.setColumnCount(4)
        statistic_table.setRowCount(2)
        statistic_table.setHorizontalHeaderLabels(('Snack', 'Quantity', 'Unit Price', 'Total Price'))
        statistic_table.setItem(0, 0, QTableWidgetItem("product 1"))
        statistic_table.setItem(0, 1, QTableWidgetItem("1"))
        statistic_table.setItem(0, 2, QTableWidgetItem("2.5"))
        statistic_table.setItem(0, 3, QTableWidgetItem("2.5"))

        statistic_table.setItem(1, 0, QTableWidgetItem("product 2"))
        statistic_table.setItem(1, 1, QTableWidgetItem("2"))
        statistic_table.setItem(1, 2, QTableWidgetItem("3"))
        statistic_table.setItem(1, 3, QTableWidgetItem("6"))

        name_label.setText('LINLA5')
        weichat_label.setText('Labin')
        total_price_label.setText('8.5')
        info_layout.addRow(QLabel('Domain Id:'), name_label)
        info_layout.addRow(QLabel('Weichat Name:'), weichat_label)
        info_layout.addRow(QLabel('Total Price:'), total_price_label)
        basic_info_layout.addWidget(statistic_table)

        self.cap = cv2.VideoCapture(0)
        self.label = QLabel()
        # self.label.showFullScreen()
        camera_layout.addWidget(self.label)

        self.setLayout(main_layout)



    def capture_image(self):
        ret, frame = self.cap.read()
        # cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        cv_img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        q_image = QImage(cv_img_rgb[:], cv_img_rgb.shape[1], cv_img_rgb.shape[0], cv_img_rgb.shape[1] * 3,
                         QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_image))


if(__name__ == '__main__'):
    app = QApplication(sys.argv)

    mainWin = OpenCvVideo()
    mainWin.show()

    while(True):
        mainWin.capture_image()
        app.processEvents()
        # mainWin.update()
        time.sleep(0.2)

    sys.exit(app.exec_())
