import env_setup; env_setup.setup()

# DO NOT REMOVE
# Importing deferred is a work around to this bug.
# https://groups.google.com/forum/?fromgroups=#!topic/webapp2/sHb2RYxGDLc
from google.appengine.ext import deferred

from webapp2 import Route, WSGIApplication

# from agar.django.templates import render_template
from agar.env import on_production_server


# from django.template import add_to_builtins
# add_to_builtins('agar.django.templatetags')
# add_to_builtins('custom_tags.custom_tags')


# def handle_403(request, response, exception):
#     logging.exception(exception)
#     # response.write('You are not authorized to view this page!')
#     response.set_status(403)
#     render_template(response, '403_error.html')


# def handle_404(request, response, exception):
#     logging.exception(exception)
#     # response.write('Oops! I could swear this page was here!')
#     response.set_status(404)
#     render_template(response, '404_error.html')


# def handle_500(request, response, exception):
#     logging.exception(exception)
#     # response.write('A server error occurred!')
#     response.set_status(500)
#     render_template(response, '500_error.html')


# config = {
#    'webapp2_extras.auth': {
#        'user_model': 'models.YourUser',
#        'cookie_name': 'session'
#    }
# }


application = WSGIApplication(
    [
        ############################################################
        # main screen
        ############################################################
        Route(r'/',
                 handler='handlers.main.MainHandler',
                 name='main',
        ),
        ############################################################
        # warmup
        ############################################################
        Route(r'/_ah/warmup',
                 handler='handlers.warmup.WarmupHandler',
                 name='warmup',
        ),
    ], #config=config,
    debug=not on_production_server
)

# if not on_development_server:
#     application.error_handlers[403] = handle_403
#     application.error_handlers[404] = handle_404
#     application.error_handlers[500] = handle_500

