import logging
import datetime

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

# exceptions, errors, permissions
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden

#generic imports
from generic.views import *
from generic.models import *

#app specific imports
from .forms import SOSGrantAppForm
from .models import SOSGrantApp

VALID_FACTORS = [
  'finance',
  'student',
  'senator',
]

ADMIN_FACTORS = [
  'finance',
  'senator',
]

# import csv
# import cStringIO
# import codecs
# from django.template.defaultfilters import striptags

def index(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  template_args = {}
  return render(request, 'sos_grant/index.html', template_args)

def manage_application(request):
  authenticate(request, VALID_FACTORS)
  # sos_app = SOSGrantApp.get(applicant=)
  template_args = {}
  return render(request, 'sos_grant/index.html', template_args)

def view_application(request):
  authenticate(request, VALID_FACTORS)
  template_args = {}
  return render(request, 'sos_grant/index.html', template_args)

def create_application(request):
  authenticate(request, VALID_FACTORS)
  sos_form = SOSGrantAppForm()
  template_args = {"sos_form": sos_form}
  return render(request, 'sos_grant/create_application.html', template_args)

def edit_application(request):
  authenticate(request, VALID_FACTORS)
  template_args = {}
  return render(request, 'sos_grant/index.html', template_args)

def save_application(request):
  authenticate(request, VALID_FACTORS)
  template_args = {}
  return render(request, 'sos_grant/index.html', template_args)

def submit_application(request):
  authenticate(request, VALID_FACTORS)
  template_args = {}
  return render(request, 'sos_grant/index.html', template_args)

def delete_application(request):
  authenticate(request, VALID_FACTORS)
  template_args = {}
  return render(request, 'sos_grant/index.html', template_args)