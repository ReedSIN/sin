from django.db import models
from generic.models import SinUser
from django.utils.safestring import mark_safe
# Create your models here.

from datetime import datetime, timedelta
from pytz import timezone

YEARS = (
  (0, 'Freshman'),
  (1, 'Sophomore'),
  (2, 'Junior'),
  (3, 'Senior')
)

class SOSGrant(models.Model):
    '''
    a model to hold the start and end dates for a "season" of SOS Grants
    '''
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)

    @property
    def can_apply(self):
      '''
      returns true if the application period is open
      '''
      today = datetime.now()
      return self.start_date < today and self.end_date < today



class SOSGrantApp(models.Model):
    '''
    the individual SOS Grant application
    '''
    applicant = models.OneToOneField(SinUser, null=True)
    name = models.CharField(max_length=100)
    preferred_pron = models.CharField(max_length = 30, blank=True, verbose_name="Preferred Pronouns")
    major = models.CharField(max_length = 30)
    year = models.IntegerField(max_length = 1, choices=YEARS)

    #contact info
    address = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 15)
    email = models.EmailField()

    #app info
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)
    sos_grant = models.ForeignKey(SOSGrant)

    #questions...
    #Internships / Short Term Employment OR Conference/Activity Based
    INTERN = 'I'
    CONF = 'C'
    OPP_CHOICES = (
      (INTERN, 'Internship or short term employment'),
      (CONF, "Conference or activity-based opportunity")
      )
    opp_choice = models.CharField(max_length=1, choices=OPP_CHOICES, \
                                  verbose_name="For what type of opportunity are you applying for assistance?",\
                                  help_text=mark_safe("If you aren't sure, contact <a href=\"sos-committee@reed.edu\">sos-committee@reed.edu</a>."))

    #internship or short employment section
    #questions if the user chooses INTERN/ 'I'
    pos_title = models.CharField(blank=True, max_length=140, verbose_name="What is the title of your position?",\
                                 help_text="(for all of these questions, if you don't know yet, give us your best guess)")
    comp_name = models.CharField(blank=True, max_length=140, verbose_name="What is the name of your company/employer?")
    hours = models.CharField(blank=True, max_length=140, verbose_name="What is the hourly commitment of the internship or short-term employment?")
    salary = models.CharField(blank=True, max_length=140, verbose_name="What is your (expected) salary for the position?")
    supervisor = models.TextField(blank=True, verbose_name="Who is your supervior for the position? Please provide relevant contact information.", \
                                  help_text="This can also be your point of contact if you don't know who your supervisor would be yet")

    #questions if the user chooses CONF/'C'
    conf_title = models.CharField(blank=True, max_length=140, verbose_name="What is the name of the conference or activity?",\
                                 help_text="(for all of these questions, if you don't know yet, give us your best guess)")
    role = models.TextField(blank=True, verbose_name="What is your role/involvement in the conference or activity?")
    start_date = models.TextField(blank=True, verbose_name="What is the starting date and duration of the conference or activity?")
    contact = models.TextField(blank=True, verbose_name="Who is your contact person for this conference or activity-based opportunity?"\
                                              " Please provide relevant contact information.")
    
    #question for both choices I/C
    description = models.TextField(blank=True, verbose_name="Please describe your tasks and responsibilities in your summer role," \
                                          " how this role might influence your Reed education," \
                                          " and other reasons why the committee should recommend allocating grant" \
                                          " money towards your summer opportunity. In your application, the SOS committee" \
                                          " will also consider whether or not there are pre-existing sources of funding" \
                                          " in pursuing similar opportunities. If there are other sources of financial" \
                                          " support for this opportunity that you have chosen to not explore, please elaborate on that choice here.",\
                                          help_text="(If you haven't looked for money, go do that! Contact career services!"\
                                          " We don't have very much money, and a lot of people want our money-" \
                                          " the more money you take from other sources, the more people we can help!)")


    # #funding section
    acad_fund = models.TextField(verbose_name="Have you sought funding from an academic department?", \
                                  help_text="If so, what was the outcome? (let us know if you're waiting to hear back, also!)")
    ss_fund = models.TextField(verbose_name="Have you sought funding from Student Services?", \
                                  help_text="If so, what was the outcome? (let us know if you're waiting to hear back, also!)")
    clbr_fund = models.TextField(verbose_name="Have you sought funding from The Center for Life Beyond Reed (Career Services)?",\
                                  help_text="If so, what was the outcome? (let us know if you're waiting to hear back, also!)")
    other_fund = models.TextField(verbose_name="Have you sought funding from other resources on campus?",\
                                  help_text="If so, what was the outcome? (let us know if you're waiting to hear back, also!)")
    funds = models.DecimalField(verbose_name="What is the total amount of funding you have received from other sources at Reed?",\
                                  max_digits = 8, decimal_places = 2)
    explain = models.TextField(blank=True, verbose_name="The SOS Committee will be in contact with the Business Office about your financial status." \
                                            " If you have financial need that would not necessarily be reflected in this information,"\
                                            " please explain the circumstances below.",\
                               help_text=mark_safe("If you have any questions, please email <a href=\"sos-committee@lists.reed.edu\">sos-committee@lists.reed.edu</a>"))
    proposal = models.TextField(blank=True, verbose_name=mark_safe("If you'd prefer to write your proposal directly in the application, you may do so here."\
                                            " If not, please send it to <a href=\"sos-committee@reed.edu\">sos-committee@reed.edu</a>."))


    #ensure that only one application can be submitted per student
    class Meta:
      unique_together = ("applicant", "sos_grant")