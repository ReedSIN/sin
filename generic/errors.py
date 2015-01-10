from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.template.loader import render_to_string
import sys

class Http400(Exception):
    def __str__(self):
        return "Bad Request"

class Http403(Exception):
    def __str__(self):
        return "You don't have permission to be here."

class Http401(Exception): pass

class HttpResponse403(HttpResponseForbidden):
    def __init__(self):
        HttpResponseForbidden.__init__(self)
        self.write(render_to_string('errors/http_forbidden.phtml'))
        self.write("You don't have permission to access the requested object.")

class HttpResponse400(HttpResponseBadRequest):
    def __init__(self):
        HttpResponseBadRequeest.__init__(self)
        self.write('<p>Bad request. Please check your query and try again.</p>')

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
                   
