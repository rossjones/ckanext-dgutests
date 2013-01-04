from selenium import selenium
from selenium.webdriver.support.wait import WebDriverWait

class TestBase(object):
    """ Provides a base class for tests which contains both the selenium
        object used to run the tests, and helper methods such as wait()

        Documentation on the selenium object can be found at:
        http://selenium.googlecode.com/svn/trunk/docs/api/py/selenium/selenium.selenium.html
        """

    def __init__(self, selenium, config):
        self.selenium = selenium
        self.config = config
        super(TestBase, self).__init__()

    def wait(self, max_wait=10):
        self.selenium.wait_for_page_to_load(max_wait*1000)

    def fill_form(self, frm_locator, data, submit=None):
        for k,v in data.iteritems():
            if '=' in k:
                self.selenium.type(k, v)
            else:
                self.selenium.type("identifier=%s" % k, v)
        if submit:
            self.selenium.click(submit)
            self.wait()
        else:
            self.selenium.submit(frm_locator)
