from selenium import selenium

class TestBase(object):

    def __init__(self, selenium):
        self.selenium = selenium
        super(TestBase, self).__init__()

