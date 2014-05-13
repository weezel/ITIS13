class Person:
    def __init__(self, en, ru, url):
        self.en_name = en.decode("utf-8").encode("utf-8")
        self.ru_name = ru.decode("utf-8").encode("utf-8")
        self.url = url.decode("utf-8").encode("utf-8")
    def compare(self, p):
        pass
    def __repr__(self):
        return "%s = %s" % (self.en_name, self.ru_name)
