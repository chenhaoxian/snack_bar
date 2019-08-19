
def produce_window(window_type):
    window = __import__('video_frame').window
    return getattr(window,window_type)
