import env_setup; env_setup.setup()

from webapp2 import WSGIApplication, RequestHandler, Route

from agar.env import on_production_server


class WarmupHandler(RequestHandler):
    def get(self):
        self.response.out.write("Warmed Up")


application = WSGIApplication(
    [
        Route('/_ah/warmup', WarmupHandler, name='warmup'),
    ],
    debug=not on_production_server
)
