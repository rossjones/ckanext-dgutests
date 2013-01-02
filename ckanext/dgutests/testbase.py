from selenium import selenium
from selenium.webdriver.support.wait import WebDriverWait

class TestBase(object):
    """ Provides a base class for tests which contains both the selenium
        object used to run the tests, and helper methods such as wait()

        Documentation on the selenium object can be found at:
        http://selenium.googlecode.com/svn/trunk/docs/api/py/selenium/selenium.selenium.html
        """

    def __init__(self, selenium):
        self.selenium = selenium
        super(TestBase, self).__init__()

    def wait(self, max_wait=10):
        self.selenium.wait_for_page_to_load(max_wait*1000)

    def fill_form(self, frm_locator, data):
        for k,v in data.iteritems():
            self.selenium.type("identifier=%s" % k, v)
        self.selenium.submit(frm_locator)
