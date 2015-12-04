from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.SOSGrantApp)
class SOSGrantAppModelAdmin(admin.ModelAdmin):
  list_display = ['name', 'created_on', 'modified_on']