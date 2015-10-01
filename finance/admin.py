from django.contrib import admin
from .models import Budget, BudgetItem


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
  list_display = ['organization', 'created_on', 'approved', 'finalized', 'allocated', 'requested']
