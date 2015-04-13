from django.shortcuts import render
from django.core.urlresolvers import reverse

from generic.views import *
from elections.models import *


# Create your views here.

VALID_FACTORS = [
    'student'
]

def index(request):
    authenticate(request, VALID_FACTORS)

    # Check if there are any open elections
    open_elections = bool(Election.get_open())

    template_args = {
        'open_elections': open_elections,
    }

    return render(request, 'elections/index.html', template_args)


def vote(request):
    authenticate(request, VALID_FACTORS)

    user = request.user

    # Try to get the users ballots if they have already
    # voted.
    voted = False
    ballots = Ballot.objects.filter(voter = user)

    if ballots:
        voted = True

    open_elections = Election.get_open()

    template_args = {
        'open_elections': open_elections
    }

    return render(request, 'elections/vote.html', template_args)

def submit_vote(request):
    authenticate(request, VALID_FACTORS)

    template_args = {
        'title': 'Vote Submitted',
        'message': '''Your vote has been recorded. If you would like to edit
        your votes, feel free to return to the voting page. Your votes should
        reappear there.''',
        'redirect': reverse('elections.views.index')
    }

    return render(request, 'generic/alert-redirect.phtml', template_args)
