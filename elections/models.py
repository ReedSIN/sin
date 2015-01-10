from django.db import models

from generic.models import *
# Create your models here.

class Election(models.Model):
    # Name of the position 
    position = models.CharField(max_length = 50)
    # Number of seats for this position, pretty much one for anything but Senate
    numSeats = models.IntegerField(default=1)
    quorumOption = models.BooleanField(default=True)
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
        
        

class Candidate(models.Model):
    # Candidates will no longer be tied to SinUsers.
    name = models.CharField(max_length=50, blank=False)
    election = models.ForeignKey("Election", related_name="candidate_set")
    # Will track whether candidate is write-in, which should be displayed
    # as a choice in the ballot view.
    write_in = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%s' %(self.name)

class Ballot(models.Model):
    # Ballot is the votes for a candidate.
    # Votes are stored in a list of candidate object ids
    election = models.ForeignKey("Election", related_name="ballot_set")
    voter = models.ForeignKey(SinUser, related_name="ballot_set")
    quorum = models.BooleanField(default=False)
    votes = models.CommaSeparatedIntegerField(max_length=150, blank=False)
    def __unicode__(self):
        # Prints out voter name and list of the votes
        output = 'Voter: ' + voter.first_name + ' ' + voter.last_name
        rank = 1
        # Cache the candidates
        candidates = self.list_candidates_by_rank()
        for candidate in candidates:
            output += '\n' + rank + ':  ' + candidate.name
        return output

    def list_candidates_by_rank(self):
        # Note: this funtion does a DB query per candidate. Cache it when possible.
        # 1. Get the list of ids as a list of integers
        ids = map(int, self.votes.split(','))
        # 2. Define function to get candidates
        f = lambda x: Candidate.objects.get(id=x)
        # 3. Return the list of candidates
        return map(f, ids)
    
