from django import forms

# imports for modelform
from django.forms import ModelForm
from .models import SOSGrant, SOSGrantApp 


#form availaible to ADMINS
class SOSGrantForm(ModelForm):
    class Meta:
        model = SOSGrant
        exclude = ('created_on', 'modified_on')


#form availiable to applicants
class SOSGrantAppForm(ModelForm):
    class Meta:
      model = SOSGrantApp
      exclude = ('applicant','created_on','modified_on', 'sos_grant')

