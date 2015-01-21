from django.db import models
from django.contrib.auth.models import User
from webapps2.settings import SERVER_EMAIL
import ldap, ldap.async

from generic.errors import Http401

FACTOR_LIST = [
  "admin",
  "senator",
  "finance",
  "appointments",
  "student",
  "fundingpoll",
  "faculty",
  "yearbook",
  "posts_mod",
  "elections",
]

FACTORS = {
  0 : "admin",
  "admin" : 0,
  1 : "senator",
  "senator" : 1,
  2 : "finance",
  "finance" : 2,
  3 : "appointments",
  "appointments" : 3,
  4 : "student",
  "student" : 4,
  5 : "fundingpoll",
  "fundingpoll" : 5,
  6 : "faculty",
  "faculty" : 6,
  7 : "yearbook",
  "yearbook" : 7,
  8 : "posts_mod",
  "posts_mod" : 8,
  9 : "elections",
  "elections" : 9,
}

class SinUser(User):
    '''User with custom SIN properties and methods.

    Attributes:
      attended_signator_trainging(bool): whether the student attended
        signator training. 
      username(str): the username, based on their Reed email
      first_name(str): the users first name
      last_name(str): the users last name
      email(str): the users email
    '''
    attended_signator_training = models.BooleanField(default = False)

    @classmethod
    def ldap_lookup_user(cls, username):
        server = "ldap://ldap.reed.edu:389/"
        query = 'uid=%s,ou=people,dc=reed,dc=edu' % username

        s = ldap.async.List(ldap.initialize(server))
        s.startSearch(query, ldap.SCOPE_SUBTREE, '(objectClass=*)')

        try:
            partial = s.processResults()
        except ldap.SIZELIMIT_EXCEEDED: pass

        return list(s.allResults)

    @classmethod
    def get_ldap_user(cls, username):
        results = SinUser.ldap_lookup_user(username)

        u = SinUser()

        user_dict = results[0][1][1]

        # Getting some data on the user
        u.username = user_dict['uid'][0]
        try:
            u.first_name = user_dict["displayName"][0]
        except KeyError:
            u.first_name = ' '
        u.last_name = user_dict['sn'][0]
        u.email = user_dict['mail'][0]
        u.factors = 0
        u.save()

        # Creating the authenticating factors
        factor_list = []
        affiliation = user_dict['eduPersonPrimaryAffiliation'][0]
        if affiliation in FACTORS:
            factor_list.append(affiliation)
        factor_list.append('student')
        u.set_factor_list(factor_list)
        u.save()

        return u
        
    def refresh_from_ldap(self):
        results = SinUser.ldap_lookup_user(self.username)
        user_dict = results[0][1][1]
        self.username = user_dict['uid'][0]
        try:
            self.first_name = user_dict['displayName'][0]
        except KeyError:
            try:
                self.first_name = user_dict['givenName'][0]
            except KeyError:
                self.first_name = ' '
        self.last_name = user_dict['sn'][0]

        # Checks if they have the "mail" attribute, which should filter out
        # alumni
        try:
            self.email = user_dict['mail'][0]
        except:
            pass

        # Creating authenticating factors
        affiliation = user_dict['eduPersonPrimaryAffiliation'][0]
        factor_list = []
        if affiliation in FACTORS:
            factor_list.append(affiliation)
        factor_list.append("student")
        self.add_factors(factor_list)
        self.save()
        return self

    def get_factor_list(self):
        # Returns a list of factors as strings
        return map(lambda x: str(x), self.factor_set.all())

    def set_factor_list(self, factor_list):
        for f in Factor.objects.all():
            if str(f) in factor_list:
                if not self in f.users.all():
                    f.users.add(self)
            else:
                if self in f.users.all():
                    f.users.remove(self)

    def add_factors(self, factor_list):
        for f in Factor.objects.all():
            if str(f) in factor_list:
                if not self in f.users.all():
                    f.users.add(self)

    def has_factor(self, factor_list):
        # Checks in the user has one of the given factors
        users_factors = self.get_factor_list()
        for f in factor_list:
            if f in users_factors:
                return True
        return False

    def is_admin(self):
        return self.factor_set.filter(name = 'admin') != []

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def send_mail(self, subject, message, sender = SERVER_EMAIL):
        self.mail.send_mail(subject, message, sender, [self.email], fail_silently = False)


class Factor(models.Model):
    name = models.CharField(max_length = 50)
    users = models.ManyToManyField(SinUser)
    
    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length = 100)
    signator = models.ForeignKey(SinUser, related_name = "signator_set")
    
    location = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 20)
    email = models.EmailField()
    website = models.CharField(max_length = 200)

    description = models.TextField()
    meeting_info = models.TextField()
    annual_events = models.TextField()
    associated_off_campus_organizations = models.TextField()

    enabled = models.BooleanField(default = True)
    archived = models.BooleanField(default = False)
    
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)

    def send_mail_to_signator(self, subject, message):
        self.signator.send_mail(subject, message)

    def __str__(self):
        return self.name

    disable_subject = """IMPORTANT - %s has been disabled"""
    disable_message = """<html><body><p>Dear %s,</p>
<p>As you may or may not know, the current policy of SIN is to disable all student organizations at the beginning of each semester. This is in order to maintain a fresh record of student organizations and remove student organizations that are no longer active.</p><p>To renew your organization please visit the following link: <a href="%s">%s</a></p></body></html>"""
    reenable_url = "http://sin.reed.edu/webapps2/organization-manager/orgs/%i/renew/"

    def disable(self):
        self.enabled = False
        self.save()
        # Send email to signator notifying them that their organization has been disabled. 
        url = Organization.reenable_url %self.id
        subject = disable_subject % self.name
        message = disable_message % (self.signator.get_full_name(), url, url)

        self.send_mail_to_signator(subject, message)
