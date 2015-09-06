from django.contrib import admin
from models import FundingPoll, FundingPollOrganization, FundingPollBudget, FundingPollBudgetItem, FundingPollVote
# Register your models here.

admin.site.register(FundingPoll)
admin.site.register(FundingPollOrganization)
admin.site.register(FundingPollBudget)
admin.site.register(FundingPollBudgetItem)
admin.site.register(FundingPollVote)

