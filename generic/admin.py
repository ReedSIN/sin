from django.contrib import admin
from generic.models import SinUser, Organization, Factor
# Register your models here.

@admin.register(SinUser)
class SinUserAdmin(admin.ModelAdmin):
  list_display = ['username', 'attended_signator_training']

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
  list_display = ['name', 'signator', 'created_on', 'modified_on', 'enabled']

@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
  filter_horizontal = ['users']
