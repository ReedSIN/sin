from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from generic.views import authenticate
from identitypoll.models import IdentityFundingPeriod, IdentityFundingOrg
from generic.models import SinUser

VALID_FACTORS = ['student', 'admin']

ADMIN_FACTORS = ['admin']


def get_current_funding_period():
    return IdentityFundingPeriod.objects.latest('created_on')


def get_current_models_for_user(user):
    period = get_current_funding_period()

    try:
        org = user.identity_orgs.filter(identity_funding_period=period)[0]
    except IndexError:
        org = None

    return (period, org)


def index(request):
    authenticate(request, VALID_FACTORS)

    period, org = get_current_models_for_user(request.user)

    if period:
        period_active = period.during_registration() or period.during_budgets()
    else:
        period_active = False

    if org:
        has_registered = True
        has_budgeted = org.description is not None and org.description != ''
    else:
        has_registered = False
        has_budgeted = False

    SinUser.objects.get(username=request.user.username)  # Populate backref
    attended_signator_training = request.user.attended_signator_training

    orgs = IdentityFundingOrg.objects.filter(signator_user=request.user)

    context = {
        'identity_funding_period': period,
        'funding_period_active': period_active,
        'attended_signator_training': attended_signator_training,
        'can_register': attended_signator_training and period.during_registration() and not has_registered,
        'can_budget': attended_signator_training and period.during_budgets() and not has_budgeted,
        'has_registered': has_registered,
        'has_budgeted': has_budgeted,
        'has_orgs': len(orgs) > 0,
        'orgs': orgs
    }

    return render(request, 'identitypoll/index.html', context)


def create_org(request):
    authenticate(request, VALID_FACTORS)

    org = IdentityFundingOrg(
        identity_funding_period=get_current_funding_period(),
        signator_user=request.user
    )

    org.save()

    return redirect('identitypoll.views.read_or_update_org', org.id)


def read_or_update_org(request, org_id):
    if request.method == 'GET':
        return read_org(request, org_id)
    elif request.method == 'POST':
        return update_org(request, org_id)
    else:
        raise PermissionDenied


def read_or_update_budget(request, org_id):
    if request.method == 'GET':
        return read_budget(request, org_id)
    elif request.method == 'POST':
        return update_budget(request, org_id)
    else:
        raise PermissionDenied


def admin_index_orgs(request):
    authenticate(request, ADMIN_FACTORS)

    period = get_current_funding_period()
    orgs = IdentityFundingOrg.objects.filter(identity_funding_period=period)

    context = {
        'identity_funding_period': period,
        'orgs': orgs
    }

    return render(request, 'identitypoll/admin_index_orgs.html', context)


def admin_read_or_update_org(request, org_id):
    if request.method == 'GET':
        return admin_read_org(request, org_id)
    elif request.method == 'POST':
        return admin_update_org(request, org_id)
    else:
        raise PermissionDenied


def admin_read_org(request, org_id):
    authenticate(request, ADMIN_FACTORS)

    org = IdentityFundingOrg.objects.get(id=org_id)

    context = {
        'org': org
    }

    return render(request, 'identitypoll/admin_read_org.html', context)


def read_org(request, org_id):
    authenticate(request, VALID_FACTORS)

    if not request.user.attended_signator_training:
        messages.add_message(request, messages.ERROR, 'You must attend signator training before apply for identity-based funding.')

        return redirect('identitypoll.views.index')

    # TODO: if approved, lock
    # TODO: must be during registration

    org = IdentityFundingOrg.objects.get(id=org_id)

    if org.signator_user != request.user:
        raise PermissionDenied

    if org.approved:
        messages.add_message(request, messages.ERROR, 'An organization cannot be changed after it has been approved.')

        return redirect('identitypoll.views.index')

    context = {
        'user': request.user,
        'org': org
    }

    return render(request, 'identitypoll/read_org.html', context)


def update_org(request, org_id):
    authenticate(request, VALID_FACTORS)

    # TODO: reject if org already exists with name

    org = IdentityFundingOrg.objects.get(id=org_id)

    if not org.signator_user == request.user or org.approved:
        raise PermissionDenied

    if len(IdentityFundingOrg.objects.filter(name=request.POST['name'])) > 0:
        messages.add_message(request, messages.ERROR, 'An organization with this name already exists.')

    org.name = request.POST['name']
    org.mission_statement = request.POST['mission_statement']
    org.save()

    messages.add_message(request, messages.SUCCESS, 'Organization saved.')

    return redirect('identitypoll.views.index')


def read_budget(request, org_id):
    authenticate(request, VALID_FACTORS)

    period = get_current_funding_period()

    if not period.during_budgets():
        messages.add_message(request, messages.ERROR, "Budgets are not currently open. They will be open from {} to {}".format(period.start_budgets, period.end_budgets))

        return redirect('identitypoll.views.index')

    org = IdentityFundingOrg.objects.get(id=org_id)

    if org.signator_user != request.user:
        raise PermissionDenied

    if not org.approved:
        messages.add_message(request, messages.ERROR, 'Senate must approve your organization before you can submit a budget.')

        return redirect('identitypoll.views.index')

    context = {'org': org}

    return render(request, 'identitypoll/read_budget.html', context)


def update_budget(request, org_id):
    authenticate(request, VALID_FACTORS)

    org = IdentityFundingOrg.objects.get(id=org_id)

    if not org.signator_user == request.user:
        raise PermissionDenied

    org.requested = request.POST['requested']
    org.description = request.POST['description']
    org.save()

    messages.add_message(request, messages.SUCCESS, 'Budget saved.')

    return redirect('identitypoll.views.index')


def admin_update_org(request, org_id):
    authenticate(request, ADMIN_FACTORS)

    org = IdentityFundingOrg.objects.get(id=org_id)

    org.approved = request.POST['approved'] == 'yes'
    org.response = request.POST['response']

    if request.POST['allocated'] != '':
        org.allocated = request.POST['allocated']

    org.save()

    messages.add_message(request, messages.SUCCESS, 'Response saved.')

    return redirect('identitypoll.views.admin_index_orgs')
