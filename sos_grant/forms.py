from django import forms

# imports for modelform
from django.forms import ModelForm
from .models import SOSGrantDates, SOSGrantApp 
from django.forms.widgets import DateTimeInput, SplitDateTimeWidget
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset
from crispy_forms.bootstrap import PrependedText
# def validate_date():
#form availaible to ADMINS

# def validate_date(self):
#   print(self)
#   print("validate_date")

class SOSGrantDatesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SOSGrantDatesForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout = Layout(
            Field('name'),
            PrependedText('start_date', '<span class=\"glyphicon glyphicon-time\" aria-hidden=\"true\"></span>', placeholder="mm-dd-yyyy hr:min"),
            PrependedText('end_date', '<span class=\"glyphicon glyphicon-time\" aria-hidden=\"true\"></span>', placeholder="mm-dd-yyyy hr:min"),
        )
        self.helper.layout.append(Submit('submit', 'Submit', css_class="btn btn-lg btn-primary btn-block form-control"))

    class Meta:
        model = SOSGrantDates
        fields = ('name', 'start_date', 'end_date')
        localized_fields = ('start_date', 'end_date')
#form availiable to applicants
class SOSGrantAppForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SOSGrantAppForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-sm-2'
        # self.helper.field_class = 'col-sm-10'
        self.helper.form_id="sos_grant_form"
        self.helper.layout = Layout(
            Fieldset(
              '(tell us about you)',
              'name',
              'preferred_pron',
              'major',
              'year',
              'address',
              'phone',
              'email',
            ),
            Fieldset('Opportunity Type','opp_choice'),
            Fieldset(
              'Internship or Employment Opportunity',
              'pos_title',
              'comp_name',
              'hours',
              'salary',
              'supervisor',
              id="intern_section"
            ),
            Fieldset(
              'Conference or Activity-Based Opportunity',
              'conf_title',
              'role',
              PrependedText('start_date', '<span class=\"glyphicon glyphicon-calendar\" aria-hidden=\"true\"></span>', placeholder="mm-dd-yyyy, or whatever you know"),
              'contact',
              id="conf_section",
            ),
            Fieldset(
              'Tell us more',
              'description'
            ),
            Fieldset(
              'Funding',
              'acad_fund',
              'ss_fund',
              'clbr_fund',
              'other_fund',
              PrependedText('funds', '$'),
              'explain'
            ),
            'proposal'
        )
        self.helper.layout.append(Submit('Save & Submit', 'Save & Submit', css_class="btn btn-lg btn-primary btn-block form-control"))
    class Meta:
      model = SOSGrantApp
      exclude = ('applicant','created_on','modified_on', 'sos_grant_dates')

      # self.fields['mydate'].widget = widgets.AdminDateWidget()
      # self.fields['mytime'].widget = widgets.AdminTimeWidget()
      # self.fields['mydatetime'].widget = widgets.AdminSplitDateTime()