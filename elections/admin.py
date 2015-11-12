from django.contrib import admin
from .models import Election, Candidate, Ballot

# Register your models here.
@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
  list_display = ['position', 'numSeats', 'vanity', 'start', 'end']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
  list_display = ['name', 'election', 'write_in']

@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin):
  list_display = ['election', 'voter', 'quorum']
