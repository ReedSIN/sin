from generic.models import SinUser, Organization
from fundingpoll.models import *
from generic.views import *

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

def view_results_json(request):
    '''Returns JSON of funding poll results.'''

    fp = get_fp()
    forgs = fp.fundingpollorganization_set.all()

    fp_org_out = [{ 'name' : org.name,
                    'signator' : f.organization.signator.get_full_name,
                    'points' : org.total_votes,
                    'topsix' : org.top_six,
                    'approve' : org.approve,
                    'noopinion' : org.no_opinion,
                    'disapprove' : org.disapprove,
                    'deepsix' : org.deep_six}
                  for org in forgs]
    
    return JsonResponse({'fp_orgs': fp_org_out})
