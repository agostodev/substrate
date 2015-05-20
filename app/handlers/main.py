import env_setup; env_setup.setup()

from webapp2 import RequestHandler

from django.template import add_to_builtins
add_to_builtins('agar.django.templatetags')

from agar.django.templates import render_template


class MainHandler(RequestHandler):
    def get(self):
        render_template(self.response, 'index.html')

