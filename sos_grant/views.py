import logging
import datetime

from django.shortcuts import render, render_to_response, redirect

# exceptions, errors, permissions
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib import messages

#generic imports
from generic.views import *
from generic.models import *

#app specific imports
from .forms import SOSGrantForm, SOSGrantAppForm
from .models import SOSGrant, SOSGrantApp

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
  try:
      grant_app = SOSGrantApp.objects.get(applicant=request.user)
  except:
      grant_app = None
  template_args = {"grant_app": grant_app}
  return render(request, 'sos_grant/index.html', template_args)

def admin_index(request):
  authenticate(request, ADMIN_FACTORS)
  #return the sos grant seasons
  try:
    grants = SOSGrant.objects.order_by('end_date')
  except ObjectDoesNotExist:
    grants = None
  print("hi")
  print(grants)

  template_args = {"grant_periods": grants}

  return render(request, 'sos_grant/admin_index.html', template_args)

def admin_create_grant_season(request):
  '''
  allows a user with the valid factors to define a new grant period
  FINISH THIS
  '''
  authenticate(request, ADMIN_FACTORS)
  grant_form = SOSGrantForm()
  template_args = {"grant_form": grant_form}
  return render(request, 'sos_grant/admin_edit_grant.html')

def admin_edit_grant_season(request, grant_id):
  '''
  given a grant season (SOSGrant), allow a user to edit the start and end dates
  '''
  authenticate(request, ADMIN_FACTORS)
  if request.method == 'GET':
    try:
      grant_season = SOSGrant.objects.get(pk=grant_id)
      grant_form = SOSGrantForm(instance=grant_season)
    except:
      #uh oh
      grant_form = SOSGrantForm()
      messages.error("We couldn\'t find an open grant period, please create one here.")
    template_args = {"grant_form": grant_form}
  elif request.method == 'POST':
    try:
      grant_season = SOSGrant.objects.get(pk=grant_id)
      grant_form = SOSGrantForm(request.POST, instance=grant_season)
      # to do: update modified on
      messages.success(request, 'The SOS Grant was updated successfully! Party on.')
    except:
      grant_form = SOSGrantForm(request.POST)
      if grant_form.is_valid():
        grant_app = grant_form.save(commit=False)
        grant_app.save()
        messages.success(request, 'Your application was submitted successfully! Party on.')
    template_args = {"sos_form": sos_form}


  return render(request, 'sos_grant/admin_edit_grant.html', template_args)

def admin_grant_list(request):
  '''
  allows a user to see a list of the applications for the current season
  of SOS grant
  ''' 
  authenticate(request, ADMIN_FACTORS)
  return render(request, 'sos_grant/admin_application_list_view.html')

def admin_grant_detail(request, grant_app_id):
  '''
  allows a user to view a grant app in detail
  '''
  authenticate(request, ADMIN_FACTORS)
  grant_app = get_object_or_404(SOSGrantApp, pk=grant_app_id)
  template_args = {'grant_app': grant_app }

  return render(request, 'sos_grant/admin_application_detail_view.html', template_args)


def manage_application(request):
  authenticate(request, VALID_FACTORS)
  template_args = {}
  try:
    grant_app = SOSGrantApp.objects.get(applicant=request.user)
  except:
    messages.error(request, "You don\'t have an application to manage! Create one here!");
    return redirect('sos_grant:create_application')
  template_args = {"grant_app": grant_app}
  return render(request, 'sos_grant/manage_application.html', template_args)

#not sure if we need this
def create_application(request):
  '''
  if there is no application, the user will be sent here to create one
  '''
  authenticate(request, VALID_FACTORS)
  sos_form = SOSGrantAppForm()
  template_args = {"sos_form": sos_form}
  return render(request, 'sos_grant/edit_application.html', template_args)

def edit_application(request):
  authenticate(request, VALID_FACTORS)
  if request.method == 'GET':
    # try to get an existing app and prefill with old responses
    # otherwise, return an empty application 
    try:
      grant_app = SOSGrantApp.objects.get(applicant=request.user )
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
    except:
      sos_form = SOSGrantAppForm(request.POST)
      if sos_form.is_valid():
        grant_app = sos_form.save(commit=False)
        grant_app.applicant = request.user
        grant_app.save()
        messages.success(request, 'Your application was submitted successfully! Party on.')
    template_args = {"sos_form": sos_form}
    return render(request, 'sos_grant/edit_application.html', template_args)
  else:
    return HttpResponseForbidden()

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