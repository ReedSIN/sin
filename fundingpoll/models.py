from django.db import models
from datetime import datetime, timedelta
from pytz import timezone

from generic.models import *
from generic.errors import Http400
from finance.models import Budget, BudgetItem

from fundingpoll.manager import FundingPollVoteManager

class FundingPoll(models.Model):
  start_registration = models.DateTimeField()
  end_registration = models.DateTimeField()
  start_voting = models.DateTimeField()
  end_voting = models.DateTimeField()
  start_budgets = models.DateTimeField()
  end_budgets = models.DateTimeField()

  created_on = models.DateTimeField(auto_now_add = True)
  modified_on = models.DateTimeField(auto_now = True)

  def during_registration(self):
    today = datetime.now()
    return self.start_registration < today and today < self.end_registration

  def during_voting(self):
    today = datetime.now()
    return self.start_voting < today and today < self.end_voting

  def after_voting(self):
    today = datetime.now()
    return self.end_voting < today

  def during_budgets(self):
    today = datetime.now()
    return self.start_budgets < today and today < self.end_budgets

def get_fp():
  if not FundingPoll.objects.exists():
    # Just in case there isn't one, create one
    today = datetime.now()
    FundingPoll.objects.create(
      start_registration = today, 
      end_registration = today,
      start_voting = today,
      end_voting = today,
      start_budgets = today,
      end_budgets = today
      )
  return FundingPoll.objects.latest('created_on')

SCALAR_CHOICES = [
  (8, 'Top Six'),
  (2, 'Approve'),
  (0, 'No Opinion'),
  (-1, 'Disapprove'),
  (-4, 'Deep Six')
]

class FundingPollOrganization(models.Model):
  funding_poll = models.ForeignKey(FundingPoll)
  organization = models.ForeignKey(Organization)
  other_signators = models.CharField(max_length = 150)
  comment = models.TextField()
  total_votes = models.IntegerField(default = 0)
  top_six = models.IntegerField(default = 0)
  approve = models.IntegerField(default = 0)
  no_opinion = models.IntegerField(default = 0)
  disapprove = models.IntegerField(default = 0)
  deep_six = models.IntegerField(default = 0)

  ordering = models.FloatField(default = 0.0)
  created_on = models.DateTimeField(auto_now_add = True)
  modified_on = models.DateTimeField(auto_now = True)

  @property
  def controversy(self):
    N = float(self.top_six + self.deep_six + self.approve + self.disapprove + self.no_opinion)
    mean_score = (4 * self.top_six - 4 * self.deep_six + self.approve - self.disapprove) / float(N)
    return (self.top_six * (4 - mean_score)**2 +
            self.deep_six * (-4 - mean_score)**2 +
            self.approve * (1 - mean_score)**2 +
            self.disapprove * (-1 - mean_score)**2 +
            self.no_opinion * (mean_score)**2) / N


  def save(self, force_insert = False, force_update = False):
    if self.ordering == 0.0:
      import random
      self.ordering = random.random()
    models.Model.save(self, force_insert, force_update)

  def __unicode__(self):
    return u'%s' % (self.organization.name)

# dont forget when you syncdb to make a large unique index
class FundingPollBudget(models.Model):
  signator_user = models.ForeignKey(SinUser)
  # organization should be a one to one field
  organization = models.ForeignKey(FundingPollOrganization)
  description = models.TextField()
  response = models.TextField()
  requested = models.DecimalField(max_digits = 8, decimal_places = 2)
  allocated = models.DecimalField(max_digits = 8, decimal_places = 2)

  created_on = models.DateTimeField(auto_now_add = True)
  modified_on = models.DateTimeField(auto_now = True)

class FundingPollBudgetItem(models.Model):
  name = models.CharField(max_length = 50)
  description = models.TextField()
  response = models.TextField()
  budget = models.ForeignKey(FundingPollBudget)
  requested = models.DecimalField(max_digits = 8, decimal_places = 2)
  allocated = models.DecimalField(max_digits = 8, decimal_places = 2)

  created_on = models.DateTimeField(auto_now_add = True)
  modified_on = models.DateTimeField(auto_now = True)

class FundingPollVote(models.Model):
  objects = FundingPollVoteManager()
  funding_poll = models.ForeignKey(FundingPoll)
  organization = models.ForeignKey(FundingPollOrganization)
  voter = models.ForeignKey(SinUser)
  scalar = models.IntegerField(choices = SCALAR_CHOICES)

  created_on = models.DateTimeField(auto_now_add = True)
  modified_on = models.DateTimeField(auto_now = True)



## MK 1/30/10 stopgap hack to make it easier to manually reg orgs for fp
def manual_reg_org(org_id):
 fp = get_fp()

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
     f_org.save()
 return f_org

def is_registered(org_id):
  fp = get_fp()
  org = Organization.objects.get(id = org_id)
  try:
    f_org = fp.fundingpollorganization_set.select_related().get(organization__id = org_id)
    return True
  except:
    return False

def fetch_not_registered_orgs(signator):
  """ Returns a queryset of organizations, signated by a given signator, that are not yet registered for the current funding poll.  """
  need_registration = []
  try:
    orgs = signator.signator_set.all()
    for i in orgs:
      if (not is_registered(i.id)):
        need_registration.append(i)
    return need_registration
  except:
    #RECURSIVELY FIX THIS - Intend to raise exception, but forget syntax ATM
    return []





