from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied

import sys, os
import ldap, ldap.async

from webapps2.settings import TEST
from generic.errors import Http401, HttpResponse403
from generic.models import SinUser
from generic.models import FACTORS

# Import JSON api
from generic.api import *

def get_user(request):
    # Get username as passed along by cosign authentication
    if TEST:
        name = 'wjones'
    else:
        name = request.META.get('REMOTE_USER','')
    # Check if we already have a SinUser with that username
    try:
        user = SinUser.objects.get(username = name)
    # Otherwise, try to create a new SinUser object
    except SinUser.DoesNotExist:
        user = SinUser.get_ldap_user(username = name)
    # If that fails, raise an error
    except Exception:
        raise Http401('Something went wrong getting the user named %s' % name)
    return user
    

def authenticate(request, valid_factors):
    # Set the user if not already matching the cookie from Kerberos
    ru = request.META.get('REMOTE_USER', '')
    if ((request.user.username != ru) or (ru == '')):
        # Get the user and authenticating factors
        request.user = get_user(request).refresh_from_ldap()
        
    # If one of the users factors is valid, return True
    if request.user.has_factor(valid_factors):
        return True
    # Otherwise return a 401 error
    else:
        raise PermissionDenied


def logout(request):
    if request.method != 'GET':
        raise Http404
    else:
        forward_url = "https://weblogin.reed.edu/cgi-bin/logout?http://sin.reed.edu"
        response = redirect(forward_url, permanent=True)
        response.delete_cookie(key = 'cosign-sin')
        return response


