from django.contrib import admin
from generic.models import *
# Register your models here.

class FactorAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)

admin.site.register(SinUser)
admin.site.register(Factor, FactorAdmin)
admin.site.register(Organization)
