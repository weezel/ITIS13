class Person:
    def __init__(self, en, ru, url):
        self.en_name = en
        self.ru_name = ru
        self.url = url
    def compare(self, p):
        pass
    def __repr__(self):
        return u"%s = %s" % (self.en_name, self.ru_name)
