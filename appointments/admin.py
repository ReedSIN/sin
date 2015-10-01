from django.contrib import admin
from .models import Position, Application

admin.site.site_header = "SIN Administration"
admin.site.site_title = "SIN Administration"


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
  list_display = ['name', 'contact', 'created_on', 'expires_on']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
  list_display = ['position', 'applicant', 'year', 'email', 'modified_on']