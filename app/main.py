import env_setup; env_setup.setup()

from django.template import add_to_builtins
add_to_builtins('agar.django.templatetags')

from webapp2 import RequestHandler, Route, WSGIApplication

from agar.env import on_production_server
from agar.config import Config
from agar.django.templates import render_template


class MainApplicationConfig(Config):
    """
    :py:class:`~agar.config.Config` settings for the ``main`` `webapp2.WSGIApplication`_.
    Settings are under the ``main_application`` namespace.

    The following settings (and defaults) are provided::

        main_application_NOOP = None

    To override ``main`` `webapp2.WSGIApplication`_ settings, define values in the ``appengine_config.py`` file in the
    root of your project.
    """
    _prefix = 'main_application'

    #: A no op.
    NOOP = None

config = MainApplicationConfig.get_config()


class MainHandler(RequestHandler):
    def get(self):
        render_template(self.response, 'index.html')


application = WSGIApplication(
    [
        Route('/', MainHandler, name='main'),
    ],
    debug=not on_production_server
)
