import ckanext.dgutests.testbase as t

class LoginTests(t.TestBase):

    def test_basic(self):

        print self.config.get('username')
        print self.config.get('password')