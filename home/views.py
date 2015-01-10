from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from generic.views import *
from generic.models import *
from generic.errors import *

# Create your views here.
VALID_FACTORS = [
    'student'
]

def index(request):
    authenticate(request, VALID_FACTORS)
    return render_to_response('home/index.html',
                              context_instance = RequestContext(request))
