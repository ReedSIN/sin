from django.db import models
from generic.models import SinUser
# Create your models here.

YEARS = (
  (0, 'Freshman'),
  (1, 'Sophomore'),
  (2, 'Junior'),
  (3, 'Senior')
)

class SOSGrantApp(models.Model):
    applicant = models.ForeignKey(SinUser, null=True)
    name = models.CharField(max_length=100)
    preferred_pron = models.CharField(max_length = 30, blank=True)
    major = models.CharField(max_length = 30)
    year = models.IntegerField(max_length = 1, choices = YEARS)

    #contact info
    address = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 15)
    email = models.EmailField()

    #app info
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)

    #questions...