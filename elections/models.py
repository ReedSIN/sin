from django.db import models
from datetime import datetime
# UGHH.... timezones
from pytz import timezone


from generic.models import *
# Create your models here.

class Election(models.Model):
    # Name of the position 
    position = models.CharField(max_length = 50)
    # Number of seats for this position, pretty much one for anything but Senate
    numSeats = models.IntegerField(default=1)
    quorumOption = models.BooleanField(default=True)
    writeInOption = models.BooleanField(default=True)
    # When election is open
    start = models.DateTimeField(default = datetime(1994, 5, 29))
    end = models.DateTimeField(default = datetime(1994, 7, 29))
    results = models.ManyToManyField('Candidate', blank=True, related_name="winners")

    def __unicode__(self):
        return u'%s' %(self.position)

    def save_csv(self):
        '''Saves of CSV file of the election to be processed'''
        csv_path = 'election%s.csv' % (self.id)
        csv_file = open(csv_path, 'wb')
        # Cache the number of candidates
        cand_num = self.candidate_set.count()
        ranks = range(1, cand_num+1)
        # First row
        text = "Voter ID,"+ ','.join(ranks)
        # Iterate over rows
        for ballot in self.ballot_set:
            text += '\n' + ballot.voter.id + ','
            text += ballot.votes
        # Save file
        csv_file.write(text)
        csv_file.close()

    def is_open(self):
        '''Returns a boolean indicated whether the election is open.'''
        our_tz = timezone('US/Pacific')
        now = datetime.now(tz = our_tz)
        return now > self.start and now < self.end

    @classmethod
    def get_open(self):
        '''Returns a list of all open elections.'''
        all_elections = self.objects.all().select_related('candidate_set')
        elections_list = []
        for election in all_elections:
            if election.is_open():
                elections_list.append(election)
        return elections_list
        
        

class Candidate(models.Model):
    # Candidates will no longer be tied to SinUsers.
    # Why? So we can have Quest boards as candidates.
    name = models.CharField(max_length=50, blank=False)
    election = models.ForeignKey("Election", related_name="candidate_set")
    blurb = models.TextField(default='')
    # Will track whether candidate is write-in, which should be displayed
    # as a choice in the ballot view.
    write_in = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%s' %(self.name)

class Ballot(models.Model):
    # Ballot is the votes for a candidate.
    # Votes are stored In A List Of Candidate Object Ids
    election = models.ForeignKey("Election", related_name="ballot_set")
    voter = models.ForeignKey(SinUser, related_name="ballot_set")
    quorum = models.BooleanField(default=False)
    votes = models.CommaSeparatedIntegerField(max_length=150, blank=False)
    def __unicode__(self):
        # Prints out voter name and list of the votes
        output = 'Voter: ' + self.voter.first_name + ' ' + self.voter.last_name
        rank = 1
        # Cache the candidates
        candidates = self.list_candidates_by_rank()
        for candidate in candidates:
            output += '\n' + str(rank) + ':  ' + candidate.name
            rank += 1
        return output

    def list_candidates_by_rank(self):
        # Note: this funtion does a DB query per candidate. Cache it when possible.
        if str(self.votes) == '':
            return []
        # 1. Get the list of ids as a list of integers
        ids = map(int, self.votes.split(','))
        # 2. Define function to get candidates
        f = lambda x: Candidate.objects.get(id=x)
        # 3. Return the list of candidates
        return map(f, ids)

    def to_dict(self):
        '''Converts the ballot to a dictionary with candidate ID's as keys and
        their respective ranks as values.'''
        if self.votes == '':
            return {}
        votes = map(int, self.votes.split(','))
        output = {}

        # Get the write-in candidates
        wicands = self.election.candidate_set.filter(write_in = True)
        wiids = []
        for cand in wicands:
            wiids.append(cand.id)

        i = 1
        for vote in votes:
            if vote in wiids:
                output['w'] = i
                # Gotta save that name!!
                writeInName = Candidate.objects.get(id = vote).name
                output['writeInName'] = writeInName
            else:
                output[vote] = i
                i += 1
        return output
