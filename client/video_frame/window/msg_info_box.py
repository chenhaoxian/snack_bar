from PyQt5.QtWidgets import QMessageBox, QApplication
import sys

def open_msg_info_box():
    app = QApplication(sys.argv)
    info_box= QMessageBox()  ##Message Box that doesn't run
    info_box.setIcon(QMessageBox.Information)
    info_box.setText("Success Create Order! Please check in wechat.")
    info_box.setWindowTitle("Information")
    info_box.setStandardButtons(QMessageBox.Ok)
    info_box.button(QMessageBox.Ok).animateClick(4 * 1000)  # 3秒自动关闭
    info_box.exec_()


if __name__ == "__main__":
    open_msg_info_box()