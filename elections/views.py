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

    open_elections = Election.get_open()

    if not bool(open_elections):
        # If there are no elections, return them back to the elections index
        template_args = {
            'title' : 'No open elections',
            'message' : 'Sorry, there are no open elections for which you canvote in.',
            'redirect' : reverse('elections.views.index')
        }
        return render(request, 'generic/alert-redirect.phtml',
                      template_args)

    user = request.user

    # Try to get the users ballots if they have already
    # voted.
    voted = False
    ballots = Ballot.objects.filter(voter = user)

    if ballots:
        voted = True

    template_args = {
        'ballots' : ballots,
        'open_elections': open_elections
    }

    return render(request, 'elections/vote.html', template_args)

def submit_vote(request):
    authenticate(request, VALID_FACTORS)
    
    d = request.POST

    open_elections = Election.get_open()
    
    for election in open_elections:
        # Create a ballot for this election
        ballot = Ballot.objects.create(election = election,
                                       voter = request.user)
        
        # First, check if they checked quorum
        quorum = ''
        try:
            quorum = d['quorum-' + str(election.id)]
        except KeyError:
            ballot.quorum = True
        if quorum == 'noquorum':
            ballot.quorum = False
        
        # Now record their votes, but only if they can
        if ballot.quorum == True and quorum != 'quorum':
            
            votes = []

            for candidate in election.candidate_set.all():
                votes.append([candidate,
                              d[str(election.id) + '-' + str(candidate.id)]])

            def get_rank(vote):
                return vote[1]

            votes.sort(key = get_rank)
            
            vote_string = ""

            for vote in votes:
                vote_string += str(votes.pop(0)[0].id)
                vote_string += ","

            ballot.votes = vote_string

        ballot.save()
    

    return render(request, 'elections/submitted_vote.html')
