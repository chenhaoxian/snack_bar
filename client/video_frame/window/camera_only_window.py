import cv2

from .basic_window import BasicWindow


class CameraOnlyWindow(BasicWindow):
    def __init__(self, name):
        BasicWindow.__init__(self)
        self._name = name
        self.window_close_callback = None

    def display(self, resolution=(), pos=(), **data):
        frame = data['frame']
        if(any(resolution)):
            frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_CUBIC)
        cv2.imshow(self._name, frame)
        if (pos):
            cv2.moveWindow(self._name, pos[0], pos[1])

    def listener_key_board(self):
        pass

    def shut_down(self):
        cv2.destroyWindow(self._name)

    def set_window_close_callback(self,func):
        self.window_close_callback = func

    def wait_for_close(self):
        if (cv2.waitKey(30) & 0xFF == ord('q') and self.window_close_callback is not None):
            self.window_close_callback()



