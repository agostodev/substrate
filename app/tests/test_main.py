import env_setup; env_setup.setup_tests(); env_setup.setup_django()

from agar.test import BaseTest, WebTest

import routes


class MainTest(BaseTest, WebTest):

    APPLICATION = routes.application

    def test_hello_world(self):
        response = self.get("/")
        self.assertOK(response)
