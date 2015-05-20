import env_setup; env_setup.setup()

from webapp2 import RequestHandler


class WarmupHandler(RequestHandler):
    def get(self):
        self.response.out.write("Warmed Up")

