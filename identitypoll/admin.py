from django.contrib import admin
from models import IdentityFundingPeriod, IdentityFundingOrg


@admin.register(IdentityFundingPeriod)
class IdentityFundingPeriodAdmin(admin.ModelAdmin):
    list_display = [
        'start_registration', 'end_registration', 'start_budgets',
        'end_budgets'
    ]


@admin.register(IdentityFundingOrg)
class FundingPollOrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'identity_funding_period', 'signator_user', 'mission_statement',
        'requested', 'description', 'allocated', 'response'
    ]
