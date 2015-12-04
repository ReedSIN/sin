import logging
import datetime

from django.shortcuts import render, render_to_response, redirect

# exceptions, errors, permissions
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages

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
  # for ifj's testing purposes
  'student', 
]

def index(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  try:
      grant_app = SOSGrantApp.objects.get(applicant=request.user)
  except:
      grant_app = None
  template_args = {"grant_app": grant_app}
  return render(request, 'sos_grant/index.html', template_args)

def admin_index(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  try:
      grant_app = SOSGrantApp.objects.get(applicant=request.user)
  except:
      grant_app = None
  template_args = {"grant_app": grant_app}
  return render(request, 'sos_grant/index.html', template_args)

def manage_application(request):
  authenticate(request, VALID_FACTORS)
  template_args = {}
  try:
    grant_app = SOSGrantApp.objects.get(applicant=request.user)
    print(grant_app)
  except:
    messages.error(request, "You don\'t have an application to manage! Create one here!");
    return redirect('sos_grant:create_application')
  template_args = {"grant_app": grant_app}
  return render(request, 'sos_grant/manage_application.html', template_args)

def view_application(request):
  authenticate(request, VALID_FACTORS)
  template_args = {}
  return render(request, 'sos_grant/view_application.html', template_args)

def create_application(request):
  authenticate(request, VALID_FACTORS)
  sos_form = SOSGrantAppForm()
  template_args = {"sos_form": sos_form}
  return render(request, 'sos_grant/edit_application.html', template_args)

def edit_application(request):
  authenticate(request, VALID_FACTORS)
  if request.method == 'GET':
    # try to get an existing app and prefill with old responses
    try:
      grant_app = SOSGrantApp.objects.get(applicant=request.user)
      sos_form = SOSGrantAppForm(instance=grant_app)
    except:
      sos_form = SOSGrantAppForm()
    template_args = {"sos_form": sos_form}
    return render(request, 'sos_grant/edit_application.html', template_args)
  elif request.method == 'POST':
    try:
      grant_app = SOSGrantApp.objects.get(applicant=request.user)
      sos_form = SOSGrantAppForm(request.POST, instance=grant_app)
      # to do: update modified on
      messages.success(request, 'Your application was updated successfully! Party on.')
      print("one existed?")
    except:
      sos_form = SOSGrantAppForm(request.POST)
      if sos_form.is_valid():
        grant_app = sos_form.save(commit=False)
        grant_app.applicant = request.user
        grant_app.save()
        messages.success(request, 'Your application was submitted successfully! Party on.')
    print("is this workin")
    print(grant_app)
    print(sos_form)
    print("?")
    template_args = {"sos_form": sos_form}
    return render(request, 'sos_grant/edit_application.html', template_args)
  else:
    raise HttpResponseForbidden

def delete_application(request):
  authenticate(request, VALID_FACTORS)
  template_args = {}
  try:
    grant_app = SOSGrantApp.objects.get(applicant=request.user)
    grant_app.delete()
    messages.success(request, "okay, we've deleted your application.");
  except:
    messages.error(request, "we couldn't find your application");
  return render(request, 'sos_grant/index.html', template_args)