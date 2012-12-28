import time
import ckanext.dgutests.testbase as t

class NavigationTests(t.TestBase):

    def test_basic_nav(self):
        self.selenium.open('http://localhost:5000/data')
        self.selenium.click("link=Publishers")
        time.sleep(1)
        assert 'Publishers' in self.selenium.get_title(), "Title was %s and not Publishers" % self.selenium.get_title()

        self.selenium.click("link=Tags")
        time.sleep(1)
        assert 'Tags' in self.selenium.get_title(), "Title was %s and not Tags" % self.selenium.get_title()
