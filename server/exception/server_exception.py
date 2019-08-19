

class ServerException:

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "[Internal Logic Error:] %s" % (self.msg)