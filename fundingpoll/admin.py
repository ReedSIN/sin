from django.contrib import admin
from models import FundingPoll, FundingPollOrganization, FundingPollBudget, FundingPollBudgetItem, FundingPollVote
# Register your models here.

# admin.site.register(FundingPoll)
# admin.site.register(FundingPollOrganization)
# admin.site.register(FundingPollBudget)
# admin.site.register(FundingPollBudgetItem)
# admin.site.register(FundingPollVote)

@admin.register(FundingPoll)
class FundingPollAdmin(admin.ModelAdmin):
  list_display = ['start_registration', 'end_registration', 'start_voting', 'end_voting', 'start_budgets', 'end_budgets']



@admin.register(FundingPollOrganization)
class FundingPollOrganizationAdmin(admin.ModelAdmin):
  list_display = ['organization', 'created_on', 'ordering', 'total_votes']

@admin.register(FundingPollBudget)
class FundingPollBudgetAdmin(admin.ModelAdmin):
  list_display = ['organization', 'signator_user', 'requested', 'allocated', 'modified_on']
