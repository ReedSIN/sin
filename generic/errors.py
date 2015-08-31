from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.template.loader import render_to_string
import sys

"""
    sudo chmod 666 to give everyone read/write permissions but no executable permissions

    https://docs.djangoproject.com/en/1.7/ref/request-response/
    - definitions of HttpResponse Subclasses

    - HttpRequest verse HttpResponse
    - HttpResponse objects are your responsibility. Each view you write is responsible for instantiating, populating and returning an HttpResponse"
    - HttpRequest objects are created automatically by django

    - emails being sent: https://docs.djangoproject.com/en/1.7/howto/error-reporting/

TODO:
    - let's clean up the templates directory in general. Get rid of what isn't being used.
        - like "old-old-tempaltes"
    - 400 errors
        - What's the difference between Http400 and HttpResponse400?
        - when is each used?
    - 403 errors
        - What's the difference between Http403 and HttpResponse403?
        - when is each used?
    - 404 errors
        - currently serving up 404.html in templates directory
        - make a nice, generic 404 html template
"""

class Http400(Exception):
    def __str__(self):
        return "Bad Request"

class HttpResponse400(HttpResponseBadRequest):
    def __init__(self):
        # TODO There's a type here. Not fixing yet
        # check and it's not in the original webapps
        HttpResponseBadRequeest.__init__(self)
        self.write('<p>Bad request. Please check your query and try again.</p>')

class Http401(Exception):
    pass

class Http403(Exception):
    def __str__(self):
        return "You don't have permission to be here."

class HttpResponse403(HttpResponseForbidden):
    def __init__(self, text):
        HttpResponseForbidden.__init__(self)
        self.write(render_to_string('errors/http_forbidden.phtml'))
        self.write("You don't have permission to access the requested object.\n")
        self.write(text)

def server_error(request):
    template_name = 'errors/http_500.phtml'
    excinfo = sys.exc_info()[1]
    is401 = isinstance(excinfo,Http401)
    template_args = {
        'path': request.path,
        'excinfo': excinfo,
        'is401': is401
        }
    return render_to_response(template_name,
                              tempate_args,
                              context_instance = RequestContext(request))

