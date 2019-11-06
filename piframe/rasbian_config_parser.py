import socket


class RpiConfigParser(object):

    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.host_name = None
        self.host_ip = None
        self.get_host_name_ip()

    def read(self, filename):
        result = {}
        try:
            lines = open(filename).read().splitlines()
        except FileNotFoundError:
            return result

        for idx, line in enumerate(lines):
            if line:
                if not line.startswith('#'):
                    if not line.startswith('['):
                        line = line.split("#")[0]
                        line = line.split("=")
                        if len(line) >= 2:
                            result[line[0]] = line[1]
                            setattr(self, line[0], line[1])
        return result

    def get(self, name, default=None):
        try:
            value = getattr(self, name)
        except:
            value = default
        return value

    def get_host_name_ip(self):
        try:

            self.host_name = socket.gethostbyname(socket.gethostname())
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.host_ip = s.getsockname()[0]
            s.close()

            return(self.host_name, self.host_ip)
        except:
            return(None, None)
