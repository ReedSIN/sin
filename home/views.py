from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from generic.views import *
from generic.models import *
from generic.errors import *

# We need these so that we have template args for the conditional displays
from elections.models import *
from fundingpoll.models import *
from fundingpoll.views import *
from appointments.models import *
from sos_grant.models import SOSGrantDates, SOSGrantApp

# Create your views here.
VALID_FACTORS = ['student']


def index(request):
    authenticate(request, VALID_FACTORS)
    open_elections = bool(Election.get_open())
    fp = get_fp()
    open_positions = Position.objects.filter(
        expires_on__gt=datetime.today()).order_by('expires_on')
    try:
        grant_app = SOSGrantApp.objects.get(applicant=request.user)
        grant_dates = SOSGrantDates.objects.all()[0]
    except:
        grant_app = None
        grant_dates = None

    template_args = {
        'open_elections': open_elections,
        'reg_open': fp.during_registration(),
        'voting_open': fp.during_voting(),
        'open_positions': open_positions,
        "grant_open": bool(grant_dates),
        "grant_app": grant_app,
    }

    return render(request, 'home/index.html', template_args)
