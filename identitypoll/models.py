from django.db import models
from datetime import datetime

from generic.models import SinUser


class IdentityFundingPeriod(models.Model):
    start_registration = models.DateTimeField()
    end_registration = models.DateTimeField()
    start_budgets = models.DateTimeField()
    end_budgets = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def during_registration(self):
        today = datetime.now()

        return self.start_registration < today and today < self.end_registration

    def during_budgets(self):
        today = datetime.now()

        return self.start_budgets < today and today < self.end_budgets


class IdentityFundingOrg(models.Model):
    identity_funding_period = models.ForeignKey(IdentityFundingPeriod)
    signator_user = models.ForeignKey(SinUser, related_name='identity_orgs')
    name = models.TextField(default='')
    mission_statement = models.TextField(default='')
    approved = models.NullBooleanField()
    requested = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    description = models.TextField(default='')
    allocated = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    response = models.TextField(default='')

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def human_is_approved(self):
        if self.approved is True:
            return 'Yes'
        elif self.approved is False:
            return 'No'
        elif self.approved is None:
            return 'Pending'
