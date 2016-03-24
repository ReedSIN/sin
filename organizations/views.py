from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from generic.views import authenticate
from generic.models import Organization
from generic.models import SinUser
from webapps2.settings import TEST
from fundingpoll.models import FundingPollOrganization
from finance.models import Budget

from django.core.urlresolvers import reverse

VALID_FACTORS = [
    'student'
]

ADMIN_FACTORS = [
    'admin'
]

VALID_POST_FIELDS = [
    'name',
    'location',
    'phone_number',
    'email',
    'website',
    'description',
    'meeting_info',
    'annual_events',
    'associated_off_campus_organizations',
    'referral_info',
]

VALID_FIELDS = VALID_POST_FIELDS
VALID_FIELDS.insert(1,'signator')

SAO = ['holmberk', 'websterka', 'duranr', 'mkincaid', 'ramirezc', 'marcoma']

def isSAO(request):
    if not TEST:
        username = request.META['REMOTE_USER']
        if username in SAO:
            return True
        else:
            return False
    else:
        return False

def index(request):
    authenticate(request, VALID_FACTORS)
    
    orgs = request.user.signator_set.all()

    template_args = {
        'organizations' : orgs
    }
    return render(request, 'organizations/index.html', template_args)

    
def organization_detail(request, org_id):
    authenticate(request, VALID_FACTORS)

    org = Organization.objects.get(id = org_id)
    try:
        fp_org = FundingPollOrganization.objects.get(organization = org)
        in_fp = True
        fp_is_closed = fp_org.funding_poll.after_voting()
    except FundingPollOrganization.DoesNotExist:
        fp_org = None
        in_fp = False
        fp_is_closed = False


    budgets = Budget.objects.filter(organization = org)
        
    template_args = {
        'org' : org,
        'in_fp' : in_fp,
        'fp_org': fp_org,
        'fp_is_closed': fp_is_closed,
        'budgets': budgets
        }
    return render_to_response('organizations/organization_detail.html',
                              template_args,
                              context_instance=RequestContext(request))

def escape(s):
    '''Gets unicode represenation of objects and puts quotes around it'''
    if type(s) != str and type(s) != unicode:
        return '"' + unicode(s).replace('"','') + '"'
    return '"' + s.replace('"','') + '"'

def decamelcase(s):
    '''Takes a string and replaces underscores with spaces
    and capitalizes the words in the string'''
    r = s[0].capitalize()
    i = 1
    while i < len(s):
        if s[i] == '_':
            r = r + ' '
            r = r + s[i+1].capitalize()
            i = i + 1
        else:
            r = r + s[i]
        i += 1
    return r
    
def csv_list(request):
    authenticate(request, VALID_FACTORS)
    resultant = ",".join(map(decamelcase,VALID_FIELDS)) + ",public_post_ok\n"

    if isSAO(request):
        orgs = Organization.objects.select_related().order_by('name').filter(archived = 0)
    else:
        orgs = Organization.objects.select_related().order_by('name')

    for o in orgs:
        for f in VALID_FIELDS:
            resultant = resultant + "%s," % (escape(o.__getattribute__(f)))
        resultant = resultant + "%s\n" % (str(str(o.public_post_ok) == '1'))
    resultant = HttpResponse(resultant, content_type = "text/csv")
    resultant['Content-Disposition'] = 'attachment; filename=organization_list.csv'
    return resultant    

def new_org(request):
    return edit_org(request, '')

def edit_org(request, org_id):
    authenticate(request, VALID_FACTORS)
    username = request.user.username
    user = SinUser.objects.get(username=username)

    if not request.user.attended_signator_training:
        template_args = {
            'title' : 'You have not attended signator training',
            'message' : 'You can not create an organization on SIN since you did not attend signators training. If you have been to signator training and believe this is an error, contact the SIN webmasters.',
            'redirect' : reverse('organizations.views.index')
        }
        return render_to_response('generic/alert-redirect.phtml', template_args, context_instance=RequestContext(request))


    if org_id != '':
        # If there is an org_id, get that organization's data
        o = request.user.signator_set.get(id = org_id)
        # Don't want to give option for fp reg
        fp_reg = False
    else:
        # Otherwise, create a blank org
        if user.attended_signator_training == False:
            raise PermissionDenied
        o = Organization()
        o.name = ""
        o.signator = request.user
        o.location = ""
        o.phone_number = ""
        o.email = request.user.email
        o.website = ""
        o.description = ""
        o.public_post_ok = True
        # We also want to give option to register for funding poll
        fp_reg = True

    # However, in the case that registration is not open, we can't let
    # them register for funding poll
    from fundingpoll.models import FundingPoll, FundingPollOrganization, get_fp
    fp = get_fp()
    
    if not fp.during_registration():
        fp_reg = False


    template_args = {
        'user' : request.user,
        'org' : o,
        'fp_reg' : fp_reg,
        }

    return render_to_response('organizations/edit_org.html',
                              template_args,
                              context_instance=RequestContext(request))

def delete_org(request, org_id):
    authenticate(request, VALID_FACTORS)

    # Make sure we only let them delete their own organizations!
    try:
        organization = request.user.signator_set.get(id = org_id)
    except Organization.DoesNotExist:
        raise PermissionDenied

    organization.delete()

    messages.add_message(request, messages.SUCCESS, 'Organization deleted.')

    return redirect('organizations.views.index')


def save_org(request, org_id):
    # Saves an organization
    authenticate(request, VALID_FACTORS)
    
    if request.method != "POST":
        raise PermissionDenied

    post_dict = request.POST

    name = post_dict['name']

    def org_with_name_exists_redirect(n):
        try:
            Organization.objects.get(name = n)
            template_args = {
                'title' : 'Error!',
                'message' : "An organization with the name `%s` already exists. Please choose another name." % n,
                'redirect' : reverse('organizations.views.new_org')
                }
            return render_to_response('generic/alert-redirect.phtml',
                                      template_args,
                                      context_instance=RequestContext(request))
        except Organization.DoesNotExist:
            return None

    if (org_id != ''):
        try: 
            # Check if the organization with that id already exists
            organization = request.user.signator_set.get(id = org_id)
            # If it does not...
        except Organization.DoesNotExist:
            # Make sure there isn't another org with the same name
            test = org_with_name_exists_redirect(name)
            if test != None:
                # If there is one with the same name, tell them that
                return test
            # Otherwise, create a new organiation
            organization = Organization()
    else:
        # If there is no id supplied
        # Check if there is another org with same name
        test = org_with_name_exists_redirect(name)
        if test != None:
            return test
        # if not, create a new organization
        organization = Organization()
    
    organization.signator = request.user

    # Set all the properties of the organization
    for n in post_dict:
        if n in VALID_POST_FIELDS:
            organization.__setattr__(n, post_dict[n])
    organization.public_post_ok = ('on' == post_dict.get('public_post_ok', 'off'))

    organization.save()

    # Now if they also wanted to register for funding poll
    from fundingpoll.models import FundingPoll, FundingPollOrganization, get_fp
    fp = get_fp()


    fp_reg = post_dict.get('fp_reg') == u'on'
    if (fp.during_registration() and fp_reg):

        fpo = FundingPollOrganization(organization = organization,
                                        funding_poll = fp,
                                        total_votes = 0,
                                        top_six = 0,
                                        approve = 0,
                                        no_opinion = 0,
                                        disapprove = 0,
                                        deep_six = 0)
        
        fpo.other_signators = post_dict.get('other_signators', '')
        fpo.comment = post_dict.get('comments', '')

        fpo.save()

    messages.add_message(request, messages.SUCCESS, 'Organization saved.')

    return redirect('organizations.views.index')


def change_signator_get(request, org_id):
    authenticate(request, VALID_FACTORS)
    o = Organization.objects.get(id = org_id, signator = request.user)
    template_args = {
        'o' : o
        }
    return render(request, 'organizations/change_signator.html',
                  template_args)

def change_signator_post(request, org_id):
    authenticate(request, VALID_FACTORS)

    new_username = request.POST.get('signator')
    try:
        new_signator = SinUser.objects.get(username = new_username)
    except SinUser.DoesNotExist:
        failure_message = '''That user does not exist in our database. Please
            check that you entered the correct username and that the user has
            logged onto SIN before. (Users are added to our database the first
            time they log in.)'''
    
        messages.add_message(request, messages.ERROR, failure_message)

        return change_signator_get(request, org_id)

    o = Organization.objects.get(id = org_id, signator = request.user)
    o.signator = new_signator
    o.email = new_signator.email
    o.save()

    success_message = '''The Signator of organization &ldquo;%s&rdquo; was successfully
    changed from &ldquo;%s&rdquo; to &ldquo;%s.&rdquo;''' % (o.name, request.user.get_full_name(), new_signator.get_full_name())
    
    messages.add_message(request, messages.SUCCESS, success_message)
    
    return index(request)


def ajax_show_all(request):
    authenticate(request, VALID_FACTORS)

    if request.method != 'GET':
        raise PermissionDenied

    query = request.GET

    s = query.get('start')
    e = query.get('end')

    if s == None:
        s = 0
    else:
        s = int(s)

    if e == None:
        e = Organization.objects.count()
    else:
        e = int(e)

    def serialize(o):
        return {
            'id' : o.id,
            'name' : o.name,
            'signator' : str(o.signator),
            'email' : o.email
            }

    orgs = [serialize(o) for o in Organization.objects.all()[s:e]]

    return HttpResponse(demjson.encode(orgs), mimetype = 'text/javascript')

def ajax_organization_details(request, org_id):
    authenticate(request, VALID_FACTORS)

    o = Organization.objects.get(id = org_id)
    resultant = demjson.encode({
            'id' : o.id,
            'name' : o.name,
            'signator' : str(o.signator),
            'signator_sin_id' : o.signator.id,
            'location' : o.location,
            'email' : o.email,
            'phone_number' : o.phone_number,
            'website' : o.website,
            'description' : o.description,
            'meeting_info' : o.meeting_info,
            'annual_events' : o.annual_events,
            'partner_orgs' : o.associated_off_campus_organizations,
            })

    return HttpResponse(resultant, mimetype = 'text/javascript')

def ajax_my_organization(request):
    authenticate(request, VALID_FACTORS)
    
    orgs = request.user.signator_set.all()

    resultant = []

    for o in orgs:
        resultant.append({
                'name' : o.name,
                'id' : o.id,
                'signator' : str(request.user),
                'email' : o.email,
                'location' : o.location,
                'phone_number' : o.phone_number,
                'website' : o.website,
                'description' : o.description
                })
    return HttpResponse(demjson.encode(resultant), mimetype = 'text/javascript')

def manage_signators(request):
    authenticate(request, ADMIN_FACTORS)

    signators = SinUser.objects.filter(attended_signator_training = True)

    template_args = {
        'signators' : signators
    }

    return render(request, 'organizations/manage-signators.html', template_args)

def remove_signator(request, sig_id):
    authenticate(request, ADMIN_FACTORS)

    try:
        signator = SinUser.objects.get(id = sig_id)
    except SinUser.DoesNotExist:
        messages.add_message(request, messages.ERROR,
                             "User not found; could not remove from signators list.")
        return redirect("organizations.views.manage_signators")

    signator.attended_signator_training = False
    signator.save()

    messages.add_message(request, messages.SUCCESS,
                         "Successfully removed %s from signator list." % signator.get_full_name())
    
    return redirect("organizations.views.manage_signators")

def add_signators(request):
    authenticate(request, ADMIN_FACTORS)
    
    if request.method == 'POST':
        return add_signators_post(request)
        
    return render_to_response('organizations/add_signators.html',
                              {},
                              context_instance=RequestContext(request))
        
    
def add_signators_post(request):
    authenticate(request, ADMIN_FACTORS)

    # Get the list of signators
    usernames = request.POST['signators']
    usernames = usernames.split(' ')

    users = [get_user_from_username(username) for username in usernames]

    users = [user for user in users if user is not None]

    for user in users:
        add_signator(user)
    
    messages.add_message(request, messages.SUCCESS,
                             "Successfully added %d of %d given users to signator list." % (len(users), len(usernames)))

    return redirect("organizations.views.manage_signators")

def add_signator(user):
    user.attended_signator_training = True
    user.save()

# This really needs to be added to generic
def get_user_from_username(username):
    try:
        user = SinUser.objects.get(username = username)
    except SinUser.DoesNotExist:
        try:
            user = SinUser.get_ldap_user(username = username)
        except Exception:
            user = None
    return user
