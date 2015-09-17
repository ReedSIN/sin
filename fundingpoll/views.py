import demjson
import logging
import datetime

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from generic.views import *
from fundingpoll.models import *
# from generic.errors import HttpResponse403, Http403
from generic.models import *

import csv
import cStringIO
import codecs
from django.template.defaultfilters import striptags

class UnicodeWriter:
  """
  A CSV writer which will write rows to CSV file "f",
  which is encoded in the given encoding.
  """
  
  def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
    # Redirect output to a queue
    self.queue = cStringIO.StringIO()
    self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
    self.stream = f
    self.encoder = codecs.getincrementalencoder(encoding)()
    
  def writerow(self, row):
    self.writer.writerow([striptags(s).encode("utf-8") for s in row])
    # Fetch UTF-8 output from the queue ...
    data = self.queue.getvalue()
    data = data.decode("utf-8")
    # ... and reencode it into the target encoding
    data = self.encoder.encode(data)
    # write to the target stream
    self.stream.write(data)
    # empty queue
    self.queue.truncate(0)
    
  def writerows(self, rows):
    for row in rows:
      self.writerow(row)

VALID_FACTORS = [
  'admin',
  'fundingpoll',
  'student'
]

ADMIN_FACTORS = [
  'admin',
  'fundingpoll'
]

TREASURER_FACTORS = [
  'fundingpoll',
  'student'
]

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/var/log/django/django.log',
                    filemode='a')

def debug(msg):
    logging.error(msg)

def index(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
 
  try:
    fp = get_fp()
    fp_exists = True
  except ObjectDoesNotExist:
    fp_exists = False
 
  num_orgs = len(request.user.signator_set.all())

  has_org = (num_orgs > 0)

  template_args = {
    'admin': admin,
    'num_orgs': num_orgs,
    'has_org': has_org,
    'reg_open': None
  }

  if fp_exists and fp.during_registration():
    template_args['reg_open'] = True
    
    def get_org(o):
      return o.organization

    fp_reg_orgs = [o for o in fp.fundingpollorganization_set.filter(funding_poll = fp, organization__signator = request.user)]
    reg_orgs = [get_org(o) for o in fp_reg_orgs]
    unreg_orgs = filter(lambda o: o not in reg_orgs,request.user.signator_set.all())
    fp_unreg = len(unreg_orgs) > 0
    template_args['need_to_reg'] = fp_unreg
  else:
    template_args['reg_open'] = False

  return render(request, 'fundingpoll/index.html', template_args)

def decamelcase(s):
  i = s.index('_')
  new_s = s[:1].upper() + s[1:i] + " " + s[i+1:i+2].upper() + s[i+2:]
  return new_s

def schedule(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  
  fp = get_fp()
  
  current_time = datetime.now()
  template_args = {
    'admin' : admin,
    'fp' : fp,
    'reg_open' : fp.during_registration(),
    'voting_open' : fp.during_voting(),
    'budgets_open' : fp.during_budgets(),
    'time' : current_time
  }
  
  return render(request, 'fundingpoll/schedule.html', template_args)

def registered(request):
  authenticate(request, VALID_FACTORS)

  fp = get_fp()
  forgs = FundingPollOrganization.objects.select_related().filter(funding_poll = fp).order_by('organization__name')

  template_args = {
    'forgs' : forgs
  }

  return render(request, 'fundingpoll/registered.html', template_args)

def vote_main(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  
  fp = get_fp()
  
  if not fp.during_voting() and not admin:
    raise PermissionDenied

  # Check if they have already voted
  vote_set = FundingPollVote.objects.filter(voter = request.user,
                                     funding_poll = fp)
  if vote_set.exists():
    r = HttpResponseForbidden()
    r.write('''
    <h1>Sorry</h1>
    <p>You may not vote twice in Funding Poll.</p>
    ''')
    return r
    
  
  forgs = FundingPollOrganization.objects.filter(funding_poll = fp).order_by('?') #Randomize order
  
  template_args = {
    'forgs' : forgs
  }
  
  return render(request, 'fundingpoll/vote_main.html', template_args)


def admin_voting(request):
  authenticate(request, ADMIN_FACTORS)
  
  fp = get_fp()
  
  forgs = FundingPollOrganization.objects.select_related().filter(funding_poll = fp).order_by('?')
  
  template_args = {
    'forgs' : forgs
  }
  
  return render(request, 'fundingpoll/vote_main.html', template_args)

def submit_vote(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  
  if request.method != 'POST':
    raise Http404()
  
  fp = get_fp()
  
  if not fp.during_voting() and not admin:
    raise PermissionDenied
  
  d = request.POST
  query = d.copy()
  del query['csrfmiddlewaretoken']
  
  voter = request.user
  try:
    FundingPollVote.objects.save_fp_data_list(FundingPollOrganization, fp, voter, query)
  except IntegrityError:
    if not admin:
      r = HttpResponseForbidden()
      r.write('<p>Error, you may not vote twice in fundingpoll.</p>')
      return r
  
  return render(request, 'fundingpoll/voting_success.html')

def organize_orgs(request):
  authenticate(request, ADMIN_FACTORS)

  fp = get_fp()
  orgs = FundingPollOrganization.objects.filter(funding_poll = fp)
  names = []
  r = ''
  
  for o in orgs:
    names = names + [o.organization.name]

  names.sort()

  for o in orgs:
    for n in names:
      if o.organization.name == n:
        o.ordering = names.index(n)

    o.save()
    r = r + o.organization.name + " " + str(o.ordering) +"\n"

  return HttpResponse(r, mimetype='text/plain')

def partition(fun, iter):
    result = {}
    for i in iter:
        result.setdefault(fun(i), []).append(i) 
    return result

def get_top_40():
  fp = get_fp()
  return fp.fundingpollorganization_set.select_related().order_by('-total_votes')[:40]

def in_top_40(forg):
  fp = get_fp()
  forg40 = fp.fundingpollorganization_set.order_by('-total_votes')[40:41][0]
  return forg.total_votes > forg40.total_votes

def top_40_emails(request):
  authenticate(request, ADMIN_FACTORS)
  topforty = get_top_40()

  r = ""

  for forg in topforty:
    r += forg.organization.signator.username + "@reed.edu, "

  return HttpResponse(r, mimetype="text/plain")

def my_registrations(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  
  fp = get_fp()

  current_fp = fp.during_registration() or fp.during_voting() or fp.during_budgets()
  
  if not current_fp  and not admin:
    raise PermissionDenied
  
  if request.user.attended_signator_training == False:
    template_args = {
      'title' : 'Error!',
      'message' : 'You cannot register an organization because you have not attended Signator Training.',
      'redirect' : reverse('fundingpoll.views.index')
    }
    return render(request, 'generic/alert-redirect.phtml', template_args)
  
  
  if fp.during_registration():
    def get_org(o):
      return o.organization
    fundingpoll_registered_orgs = [o for o in fp.fundingpollorganization_set.filter(funding_poll = fp, organization__signator = request.user)]
    registered_orgs = [get_org(o) for o in fundingpoll_registered_orgs]
    unregistered_orgs = filter(lambda o: o not in registered_orgs,request.user.signator_set.all())
    
    template_args = {
      'admin' : admin,
      'user' : request.user,
      'reg_orgs' : fundingpoll_registered_orgs,
      'unreg_orgs' : unregistered_orgs,
    }
    
    return render(request, 'fundingpoll/my_registrations.html', template_args)    
  else:
    registered_orgs = filter(lambda x: x.organization.signator == request.user,get_top_40())
     
    if registered_orgs == [] and not admin:
      raise PermissionDenied
    
    template_args = {
      'admin' : admin,
      'user' : request.user,
      'reg_orgs' : registered_orgs,
    }
    
    return render(request, 'fundingpoll/my_registrations_budget.html', template_args)

def save_registration(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(['admin'])
  
  if request.method != 'POST':
    raise Http404
  
  fp = get_fp()
  
  if not fp.during_registration() and not admin:
    raise PermissionDenied
  
  query = demjson.decode(request.POST['query_string'])
  
  all_orgs = list(request.user.signator_set.all())
  
  def update_org(d):
    org_id = d['id']
    org = Organization.objects.get(id = org_id)
    try:
      f_org = fp.fundingpollorganization_set.select_related().get(organization__id = org_id)
    except Exception:
      f_org = FundingPollOrganization(organization = org,
                                      funding_poll = fp,
                                      total_votes = 0,
                                      top_six = 0,
                                      approve = 0,
                                      no_opinion = 0,
                                      disapprove = 0,
                                      deep_six = 0)
    
    f_org.other_signators = d.get('other_signators','')
    f_org.comment = d.get('comments','')
    
    a = d.get('other_signators','')
    b = d.get('comments','')
    
    f_org.save()
    
    return org
  query_orgs = [update_org(d) for d in query]
  delete_orgs = [o for o in all_orgs if not o in query_orgs]
  for o in delete_orgs:
    try:
      fp.fundingpollorganization_set.get(organization = o).delete()
    except: pass
  
  template_args = {
    'title' : 'Success!',
    'message' : 'Your organization has been registered for funding poll.',
    'redirect' : reverse('fundingpoll.views.index')
  }
  return render(request, 'generic/alert-redirect.phtml', template_args)

class counter(object):
  def __init__(self):
    self.count = 1
  def next(self):
    c = self.count
    self.count = self.count + 1
    return c


def view_all_budgets(request):
  authenticate(request, TREASURER_FACTORS)
  
  def budget_mapper(o):
    l = o.fundingpollbudget_set.all()
    if len(l) == 0:
      return []
    else:
      return l[0]
  
  budgets = filter(lambda x: x != [], map(budget_mapper,get_top_40()))
  
  template_args = {
    'admin' : True,
    'budgets' : budgets,
    'counter' : counter()
  }
  
  return render(request, 'fundingpoll/view_all_budgets.html', template_args)

def view_one_budget(request, budget_id):
  authenticate(request, TREASURER_FACTORS)
  
  budget = FundingPollBudget.objects.get(id = budget_id)
  items = budget.fundingpollbudgetitem_set.all()
  
  template_args = {
    'admin' : True,
    'budget' : budget,
    'items' : items
  }
  
  return render(request, 'fundingpoll/view_one_budget.html', template_args)

def view_results(request):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  
  fp = get_fp()
  
  if not fp.after_voting() and not admin:
    raise PermissionDenied
  
  if fp.fundingpollorganization_set.all().count() > 0:
    total_votes = fp.fundingpollorganization_set.all()[:1][0].fundingpollvote_set.count()
    total_voters = SinUser.objects.count()
    ratio = float(total_votes)/float(total_voters)
  else:
    total_votes = 0
    total_voters = SinUser.objects.count()
    ratio = 0
  
  template_args = {
    'admin' : admin,
    'forgs' : fp.fundingpollorganization_set.order_by('-total_votes'),
    'total_votes' : total_votes,
    'total_users' : total_voters,
    'ratio' : ratio,
    'counter' : counter()
  }
  
  return render(request, 'fundingpoll/results.html', template_args)


def admin_view_results(request):
  authenticate(request, ADMIN_FACTORS)
  
  fp = get_fp()
    
  template_args = {
    "forgs" : fp.fundingpollorganization_set.select_related().order_by('-total_votes'),
    "counter" : counter()
  }
  
  return render(request, 'fundingpoll/results.html',template_args)

def preview_budget(request, budget_id):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  
  if not admin:
    budget = FundingPollBudget.objects.get(organization__organization__signator = request.user, id = budget_id)
  else:
    budget = FundingPollBudget.objects.get(id = budget_id)
  items = budget.fundingpollbudgetitem_set.all()
  
  template_args = {
    'admin' : admin,
    'budget' : budget,
    'items' : items
  }
  
  return render(request, 'fundingpoll/view_one_budget.html', template_args)

def edit_budget(request, org_id):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  
  if request.method != 'GET':
    raise Http404()
  
  fp = get_fp()
  
  if not fp.during_budgets() and not admin:
    raise PermissionDenied
  
  if not admin and request.user.signator_set.filter(id = org_id).count() == 0:
    raise PermissionDenied
  
  org = FundingPollOrganization.objects.select_related().get(funding_poll = fp, organization__id = org_id)
  
  # Lazy Budget Creation
  if len(org.fundingpollbudget_set.all()) == 0:
    b = FundingPollBudget()
    b.signator_user = org.organization.signator 
    b.organization = org
    b.description = ""
    b.response = ""
    b.requested = 0
    b.allocated = 0
    b.save()
  
  budget = org.fundingpollbudget_set.all()[0]
  budget_items = budget.fundingpollbudgetitem_set.all()
  
  template_args = {
    'admin' : admin,
    'user' : request.user,
    'org' : org,
    'budget' : budget,
    'items' : budget_items
  }
  
  return render(request, 'fundingpoll/edit_budget.html', template_args)

import re

BUDGET_ITEM_RE= 'budget_item\[(\d+)\]\["(\w+)"\]'
RE = re.compile(BUDGET_ITEM_RE)


MONEY_RE = re.compile('^\$?((?:(?:\d+)|(?:\d{1,3}(?:,\d{3})*))(?:\.\d{0,2})?)$')

class InvalidCurrencyFormatException(Exception):
  def __str__(self):
    return "You have inputted an improperly formatted decimal number. Please go back and correct any errors."

def escape_money(input):
  if input == '':
    return '0'
  m = MONEY_RE.match(input)
  if m == None:
    raise InvalidCurrencyFormatException()
  return m.group(1).replace(',','')

def save_budget(request, budget_id):
  authenticate(request, VALID_FACTORS)
  admin = request.user.has_factor(ADMIN_FACTORS)
  
  if request.method != 'POST':
    raise Http404()
  
  fp = get_fp()
  
  if not fp.during_budgets():
    raise PermissionDenied
  
  if not admin:
    budget = FundingPollBudget.objects.get(organization__organization__signator = request.user, id = budget_id)
  else:
    budget = FundingPollBudget.objects.get(id = budget_id)
  query = demjson.decode(request.POST['query_string'])
  
  budget.description = query['description']
  budget.save()
  current_items = budget.fundingpollbudgetitem_set.all()
  for i in current_items:
    i.delete()  
  
  total_requested = 0
  for i in query['budget_items']:
    item = FundingPollBudgetItem()
    item.budget = budget
    item.name = i['name']
    item.description = i['description']
    requested = escape_money(i['requested'])
    item.requested = requested
    item.allocated = 0
    total_requested = total_requested + float(requested)
    item.save()
  budget.requested = str(total_requested)
  budget.save()
  
  url = reverse('fundingpoll.views.edit_budget',
                args=[budget.organization.organization.id]) 
  
  template_args = {
    'title' : 'Success!',
    'message' : 'Your budget has successfully been saved. You can edit it until budget editing ends at %s' % str(fp.end_budgets),
    'redirect' : url
  }
  return render(request, 'generic/alert-redirect.phtml', template_args)
  
def __process_budget_post(user, budget, total_requested, dictionary, create = True):  
  organization = None
  description = None
  requested = None
  email = None
  
  budget_items = {}
  
  for k in dictionary:
    
    m = RE.match(k)
    
    if m != None:
      budget_number = m.group(1)
      budget_field = m.group(2)
      
      if not budget_number in budget_items:
        item = {}
        budget_items[budget_number] = item
    
      budget_items[budget_number][budget_field] = dictionary[k]
    else:
      if k == 'description':
        description = dictionary[k]
      elif k == 'requested':
        requested = float(dictionary[k])
      elif k == 'email':
        email = dictionary[k]
      elif k == 'organization':
        organization = dictionary[k]
      elif k == 'submit':
        pass
      else:
        raise Http400
  
  item_list = []
  
  for i in budget_items:
    item = budget_items[i]
    
    i = FundingPollBudgetItem()
    i.name = item["name"]
    i.description = item["description"]
    i.response = ""
    i.requested = item["requested"]
    i.allocated = '0'
    
    total_requested = total_requested + float(i.requested)
    item_list.append(i)
  
  budget.requested = str(total_requested)
  budget.save()
  
  for i in item_list:
    i.budget = budget
    i.save()

def csv_budget_list(request):
  authenticate(request, TREASURER_FACTORS)
  
  def get_budget(fp_org):
    try:
      budget = fp_org.fundingpollbudget_set.select_related().latest('created_on')
      return {
        'org':fp_org.organization,
        'fp_org':fp_org,
        'budget':budget,
      }
    except FundingPollBudget.DoesNotExist:
      return {
        'org':fp_org.organization,
        'fp_org':fp_org,
        'budget':None
        }
  
  budgets = map(get_budget,get_top_40())
  
  response = HttpResponse(content_type = "text/csv")
  response['Content-Disposition'] = 'attachment; filename=fundingpoll_budget_list.csv'
  
  writer = UnicodeWriter(response)
  
  writer.writerow(['Organization',
                   'Signator',
                   'Administration Desc',
                   'Administration Costs',
                   'Refreshments Desc',
                   'Refreshments Cost',
                   'Entertainment Desc',
                   'Entertainment Cost',
                   'Capital Improvments Desc',
                   'Capital Improvments Cost',
                   'Frozen Desc',
                   'Frozen Cost',
                   'Miscellaneous Desc',
                   'Miscellaneous Cost'])
  for b in budgets:
    if b.get('budget',False):
      if b.get('budget').fundingpollbudgetitem_set.count() == 6:
        admin_item = b['budget'].fundingpollbudgetitem_set.get(name = 'Administration Costs')
        refresh_item = b['budget'].fundingpollbudgetitem_set.get(name = 'Refreshments')
        enter_item = b['budget'].fundingpollbudgetitem_set.get(name = 'Entertainment')
        capi_item = b['budget'].fundingpollbudgetitem_set.get(name = 'Capital Improvements')
        froz_item = b['budget'].fundingpollbudgetitem_set.get(name = 'Frozen')
        misc_item = b['budget'].fundingpollbudgetitem_set.get(name = 'Miscellaneous')
        writer.writerow([ b['org'].name,
                          unicode(b['org'].signator),
                          unicode(admin_item.description),
                          unicode(admin_item.requested),
                          unicode(refresh_item.description),
                          unicode(refresh_item.requested),
                          unicode(enter_item.description),
                          unicode(enter_item.requested),
                          unicode(capi_item.description),
                          unicode(capi_item.requested),
                          unicode(froz_item.description),
                          unicode(froz_item.requested),
                          unicode(misc_item.description),
                          unicode(misc_item.requested)
                          ])
      else:
        writer.writerow([b['org'].name,
                         unicode(b['org'].signator)])
    else:
      writer.writerow([b['org'].name,
                       unicode(b['org'].signator)])
  return response
