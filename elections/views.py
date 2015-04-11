from django.shortcuts import render

from generic.views import *
from elections.models import *


# Create your views here.

VALID_FACTORS = [
    'student'
]

def index(request):
    authenticate(request, VALID_FACTORS)
    return render(request, 'elections/index.html')


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
