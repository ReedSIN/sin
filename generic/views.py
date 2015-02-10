from django.shortcuts import render
import sys, os
import ldap, ldap.async

from webapps2.settings import TEST
from generic.errors import Http401
from generic.models import SinUser
from generic.models import FACTORS

def get_user(request):
    # Get username as passed along by cosign authentication
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
    # Get the user and authenticating factors
    user = get_user(request).refresh_from_ldap()
    # If one of the users factors is valid, return True
    if not TEST:
        if user.has_factor(valid_factors):
            # Set user
            request.user = user
            return True
        # Otherwise return a 401 error
        else:
            request.user = SinUser()
            raise Http401(valid_factors)

    else:
        return True

def logout(request):
    if request.method != 'GET':
        raise Http404
    else:
        forward_url = request.GET.get('forward_url',
                                      'https://weblogin.reed.edu/cgi-bin/logout?http://sin.reed.edu')
        response = HttpResponsePermanentRedirect(forward_url)
        response.delete_cookie(key = 'cosign-sin')
        return response

