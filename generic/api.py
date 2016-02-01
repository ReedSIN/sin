from generic.models import SinUser, Organization

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

def check_user(request):
    '''Receives a request with parameter username, returning a boolean
    indicating whether the user exists and the name of the user.'''
    username = request.GET.get('username', '')
    exists = True
    name = ''
    try:
        the_user = SinUser.objects.get(username = username)
        name = the_user.first_name + ' ' + the_user.last_name
    except SinUser.DoesNotExist:
        exists = False

    return JsonResponse({'valid' : str(exists).lower(),
                         'name' : name})

def search_orgs(request):
    '''Recieves a request with search parameters and returns a list of
    organizations fitting the search.'''
    s = request.GET.get('s', '')

    if s == '':
        orgs = Organization.objects.all()
    else:
        orgs = Organization.objects.filter(name__contains=s)

    org_list = [{'name': org.name,
                 'signator': (org.signator.first_name + ' ' + org.signator.last_name),
                 'email': org.signator.email,
                 'id': org.id }
                for org in orgs]

    return JsonResponse({
        'orgs' : org_list
        })
