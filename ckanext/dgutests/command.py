
import logging
import os
import sys
import urllib2
import requests
import subprocess
import inspect
import pkgutil
import atexit
import collections

from optparse import OptionParser
from selenium import webdriver, selenium
from ckan.lib.cli import CkanCommand

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s: %(message)s')
log = logging.getLogger('ckanext-dgutests')

class TestRunner(CkanCommand):
    """
    Runs selenium tests

    Prepares selenium for running tests by starting up
    the selemiun server (if necessary) and running all
    of the tests in the tests folder.

    Available commands are:
        install - fetches the selenium jar and installs it locally
        run - runs all of the tests, starting selenium as necessary
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 1
    min_args = 1

    def __init__(self, name):
        super(TestRunner, self).__init__(name)
        self.selenium_process = None
        self.parser.add_option("-s", "--selenium",
                  type="string", dest="selenium_url",
                  help="Specify the selenium url")
        self.parser.add_option("-t", "--target",
                  type="string", dest="target_url",
                  help="Specify the server url")

    def command(self):
        log.info("Created TestRunner")
        cmd = self.args[0]
        if cmd not in ['install', 'run']:
            log.error("Unknown command [%s]" % cmd)
            sys.exit(1)

        root = os.path.abspath(os.path.join(__file__,
            os.path.pardir, os.path.pardir, os.path.pardir))
        self.selenium_home = os.path.join(root, 'selenium')
        if not os.path.exists(self.selenium_home):
            log.info("Creating selenium home directory")
            os.makedirs(self.selenium_home)

        getattr(self, '%s_task' % cmd)()

    def install_task(self):
        """ Installs selenium jar file """
        log.info("Running install task")
        url = "http://selenium.googlecode.com/files/selenium-server-standalone-2.28.0.jar"

        log.info("Downloading selenium")
        self._download(url, os.path.join(self.selenium_home,
            "selenium-server-standalone-2.28.0.jar"))

    def run_task(self):
        import urlparse

        selenium_url = self.options.selenium_url or self._run_selenium()
        target_url = self.options.target_url or "http://localhost:5000/data"
        obj = urlparse.urlparse(selenium_url)


        # For all functions in ckanext/dgutests/tests we should run them and pass
        # in the browser
        self.selenium = selenium(obj.hostname, obj.port, "*firefox", target_url)
        self.selenium.start()

        error_dict = collections.defaultdict(list)

        import ckanext.dgutests.tests
        for name,cls in inspect.getmembers(sys.modules["ckanext.dgutests.tests"], inspect.isclass):
            #if not name == 'MapPreviewTests':
            #    continue
            methods = [nm for (nm,_) in
                inspect.getmembers(cls, predicate=inspect.ismethod) if nm.startswith('test_')]
            if not methods:
                continue

            instance = cls(self.selenium)
            for method_name in methods:
                try:
                    getattr(instance, method_name)()
                except Exception as e:
                    error_dict["%s.%s" % (name,method_name)].append(e)
                    log.error(e)
                except AssertionError as b:
                    error_dict["%s.%s" % (name,method_name)].append(b)
                    log.error(b)


        # Cleanup
        self.selenium.stop()
        if self.selenium_process:
            log.info("Closing down our local selenium server")
            self.selenium_process.kill()

        for k,v in error_dict.iteritems():
            print k
            print '*' * 30
            for i in v:
                print i

    def _run_selenium(self):
        """ command is self._run_selenium() """
        # Check if selenium is already running locally, can we get any sort of response
        # from http://127.0.0.1:4444/
        running = True
        try:
            r = requests.get('http://127.0.0.1:4444/')
        except:
            running = False

        log.info("A local selenium is running? %s" % running)
        if not running:
            log.info("Creating our own local selenium instance")
            args = ['java', '-jar', os.path.join(self.selenium_home, "selenium-server-standalone-2.28.0.jar")]
            self.selenium_process = subprocess.Popen(args)
        return 'http://127.0.0.1:4444/'


    def _download(self, url, target):
        log.info("Downloading selenium to %s" % target)
        u = urllib2.urlopen(url)
        with open(target, 'wb') as f:
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,


