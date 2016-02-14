import logging
import datetime

from django.shortcuts import render, render_to_response, redirect

# exceptions, errors, permissions
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.forms.models import model_to_dict

#generic imports
from generic.views import *
from generic.models import *

#app specific imports
from .forms import SOSGrantDatesForm, SOSGrantAppForm
from .models import SOSGrantDates, SOSGrantApp

VALID_FACTORS = [
  'finance',
  'student',
  'senator',
]

ADMIN_FACTORS = [
  'sos_com', 
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
  #return the sos grant dates
  try:
    grant_dates = SOSGrantDates.objects.get(end_date__gt=timezone.now())
  except ObjectDoesNotExist:
    grant_dates = None
    messages.info(request, "There isn't an open grant period right now. You can set the start and end dates for this round of SOS grant applications")
  except MultipleObjectsReturned:
    grant_dates = SOSGrantDates.objects.get(end_date__gt=timezone.now())[0]
    messages.warning(request, "We found multiple grant periods that are open right now. Please contact a webmaster about this.")
  template_args = {"grant_period": grant_dates}

  return render(request, 'sos_grant/admin_index.html', template_args)

def admin_create_grant_date(request):
  '''
  allows a user with the valid factors to define a new grant period
  FINISH THIS
  '''
  authenticate(request, ADMIN_FACTORS)
  if request.method == 'GET':
    grant_form = SOSGrantDatesForm()
    template_args = {"grant_form": grant_form}
    return render(request, 'sos_grant/admin_edit_grant_date.html', template_args)
  elif request.method == 'POST':
      grant_form = SOSGrantDatesForm(request.POST)
      if grant_form.is_valid():
        grant_app = grant_form.save(commit=False)
        grant_app.save()
        messages.success(request, 'We created a grant period with the dates you suggested. Thanks!')
        return redirect('sos_grant:index')
      else:
        messages.error(request, 'We weren\'t able to use those dates, please fix them and resubmit.')
        template_args = {"grant_form": grant_form}
        return render(request, 'sos_grant/admin_edit_grant_date.html', template_args)
  else:
    return HttpResponseForbidden()


def admin_edit_grant_date(request):
  '''
  given a grant date (SOSGrant), allow a user to edit the start and end dates
  '''
  authenticate(request, ADMIN_FACTORS)
  if request.method == 'GET':
    try:
      grant_date = SOSGrantDates.objects.get(end_date__gt=timezone.now())
      grant_form = SOSGrantDatesForm(instance=grant_date)
    except:
      #uh oh
      grant_form = SOSGrantDatesForm()
      messages.error(request, "We couldn\'t find an open grant period, please create one here.")

  elif request.method == 'POST':
    try:
      grant_date = SOSGrantDates.objects.get(end_date__gt=timezone.now())
      grant_form = SOSGrantDatesForm(request.POST, instance=grant_date)
      # to do: some kind of validation to make sure the dates are not weird or set to sometime
      #in the past
      if grant_form.is_valid():
        grant_app = grant_form.save(commit=False)
        grant_app.modified_on = timezone.now()
        grant_app.save()
        messages.success(request, 'The SOS Grant Dates were updated successfully! Party on.')
        return redirect('sos_grant:index')
      else:
        messages.error(request, 'We weren\'t able to update those dates, please fix them and resubmit.')
    except:
      messages.error(request, "We couldn\'t find an open grant period, please create one here.")
      # return render(request, 'sos_grant/admin_edit_grant_date.html', template_args)
  else:
    return HttpResponseForbidden()

  template_args = {"grant_form": grant_form}
  return render(request, 'sos_grant/admin_edit_grant_date.html', template_args)

def admin_grant_app_list(request):
  '''
  allows a user to see a list of the applications for the current date
  of SOS grant
  ''' 
  authenticate(request, ADMIN_FACTORS)
  #get all of the objects for the current open grant app
  try:
    grant_date = SOSGrantDates.objects.get(end_date__gt=timezone.now())
  #otherwise, return the object that most recently ended
  except ObjectDoesNotExist:
    grant_date = SOSGrantDates.objects.filter(end_date_lte=timezone.now()).order_by('end_date')[0]
  #maybe there are no grant dates at all right now
  except:
    grant_date = None
    messages.info("There are no grant dates which are open or have recently ended.")
  grant_apps = SOSGrantApp.objects.filter(sos_grant_dates__pk=grant_date.id)
  template_args = {"grant_apps":grant_apps, "grant_date": grant_date}
  return render(request, 'sos_grant/admin_application_list_view.html', template_args)

def admin_grant_app_detail(request, grant_app_id):
  '''
  allows a user to view a grant app in detail
  '''
  authenticate(request, ADMIN_FACTORS)
  grant_app = get_object_or_404(SOSGrantApp, pk=grant_app_id)
  template_args = {'sos_app': grant_app}

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

  try:
    grant_date = SOSGrantDates.objects.get(end_date__gt=timezone.now())
  except ObjectDoesNotExist:
    grant_date = None
    messages.error(request, "Sorry, but the SOS grant isn't accepting applications at this time.")
    return redirect('sos_grant:index')

  if request.method =="GET":
    sos_form = SOSGrantAppForm()
    template_args = {"sos_form": sos_form, "grant_date":grant_date}

  elif request.method == "POST":
    sos_form = SOSGrantAppForm(request.POST)
    if sos_form.is_valid():
      grant_app = sos_form.save(commit=False)
      grant_app.applicant = request.user
      grant_app.sos_grant_dates = grant_date
      grant_app.save()
      messages.success(request, 'Your application was submitted successfully! Party on.')
      return redirect('sos_grant:index')
    else:
      messages.error(request, 'There were some errors in your application, please fix them and resubmit.')
    template_args = {"sos_form": sos_form, "grant_date": grant_date}

  return render(request, 'sos_grant/edit_application.html', template_args)

def edit_application(request):
  authenticate(request, VALID_FACTORS)
  try:
    grant_date = SOSGrantDates.objects.get(end_date__gt=timezone.now())
  except ObjectDoesNotExist:
    grant_date = None
    messages.error(request, "Sorry, but the SOS grant isn't accepting applications at this time.")
    return redirect('sos_grant:index')

  if request.method == 'GET':
    # try to get an existing app and prefill with old responses
    try:
      grant_app = SOSGrantApp.objects.get(applicant=request.user)
      sos_form = SOSGrantAppForm(instance=grant_app)
    # otherwise, return an empty application 
    except:
      sos_form = SOSGrantAppForm()
    template_args = {"sos_form": sos_form}
    return render(request, 'sos_grant/edit_application.html', template_args)

  elif request.method == 'POST':
    try:
      grant_app = SOSGrantApp.objects.get(applicant=request.user)
      sos_form = SOSGrantAppForm(request.POST, instance=grant_app)
      if sos_form.is_valid():
        grant_app = sos_form.save(commit=False)
        grant_app.applicant = request.user
        grant_app.sos_grant_dates = grant_date
        grant_app.modified_on = timezone.now()
        grant_app.save()
        # to do: update modified on
        messages.success(request, 'Your application was updated successfully! Party on.')
        return redirect('sos_grant:index')
      else:
        messages.error(request, 'There were some errors in your application, please fix them and resubmit.')
    except:
      messages.error(request, 'We couldn\'t find an application associated with you... maybe something has gone terribly wrong.')
    #   sos_form = SOSGrantAppForm(request.POST)
    #   if sos_form.is_valid():
    #     grant_app = sos_form.save(commit=False)
    #     grant_app.applicant = request.user
    #     grant_app.sos_grant_dates = grant_date
    #     grant_app.save()
    #     messages.success(request, 'Your application was submitted successfully! Party on.')
    #     return redirect(request, 'sos_grant/index.html')
    #   else:
    #     messages.error(request, 'There were some errors in your application, please fix them and resubmit.')
    template_args = {"sos_form": sos_form, "grant_date": grant_date}
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
    messages.error(request, "we couldn't find your application, sorry 'bout that");
  return render(request, 'sos_grant/index.html', template_args)