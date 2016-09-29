from util import must_get


class Model:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        return must_get(self.data, name)


class Brand(Model):
    pass
