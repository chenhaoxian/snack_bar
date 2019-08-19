from abc import abstractmethod


class BasicWindow:

    @abstractmethod
    def display(self, resolution=(), **data):
        pass

    @abstractmethod
    def shut_down(self):
        pass

    @abstractmethod
    def set_window_close_callback(self):
        pass

    @abstractmethod
    def wait_for_close(self):
        pass
