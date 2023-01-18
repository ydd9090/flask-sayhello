import unittest
import os
from sayhello import app

class TestSettings(unittest.TestCase):

    def setUp(self,):
        self.app = app

    def tearDown(self):
        pass

    def test_avatars_save_path(self,):
        assert app.config["AVATARS_SAVE_PATH"] == os.path.join(os.path.join(os.path.dirname(app.root_path),"uploads"),"avatars")

    def test_debug_tb_intercept_redirects(self):
        assert app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] is False