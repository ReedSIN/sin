from django.db import models
from datetime import datetime
import json

from generic.models import *

# Create your models here.


class Election(models.Model):
    # Name of the position 
    position = models.CharField(max_length=50)
    vanity = models.BooleanField(default=False)
    # Number of seats for this position, pretty much one for anything but Senate
    numSeats = models.IntegerField(default=1)
    quorumOption = models.BooleanField(default=True)
    writeInOption = models.BooleanField(default=True)
    # Student Body Size
    sbSize = models.IntegerField(default=1354)
    # When election is open
    start = models.DateTimeField(default=datetime(1994, 5, 29))
    end = models.DateTimeField(default=datetime(1994, 7, 29))
    results = models.ManyToManyField(
        'Candidate', blank=True, related_name="winners")
    summary_json = models.TextField(default='', blank=True, editable=False)

    def __unicode__(self):
        return u'%s' % (self.position)

    @property
    def percent_voted(self):
        '''Returns the percent of the student body that has voted'''
        voter_count = Ballot.objects.filter(election=self).count()
        return int(float(voter_count) / float(self.sbSize) * 100.0)

    @property
    def reached_potential_quorum(self):
        '''Tests whether quorum could be reached based on number of voters'''
        return self.percent_voted >= 25

    @property
    def percent_quorum(self):
        '''Returns the percent of the student body that voted quorum'''
        ballot_count = self.ballot_set.filter(quorum=True).count()
        return int(float(ballot_count) / float(self.sbSize) * 100.0)

    @property
    def reached_quorum(self):
        '''Tests whether quorum has been reached'''
        return self.percent_quorum >= 25

    def save_csv(self):
        '''Saves of CSV file of the election to be processed'''
        csv_path = 'election%s.csv' % (self.id)
        csv_file = open(csv_path, 'wb')
        # Cache the number of candidates
        cand_num = self.candidate_set.count()
        ranks = range(1, cand_num + 1)
        # First row
        text = "Voter ID," + ','.join(ranks)
        # Iterate over rows
        for ballot in self.ballot_set:
            text += '\n' + ballot.voter.id + ','
            text += ballot.votes
        # Save file
        csv_file.write(text)
        csv_file.close()

    def is_open(self):
        '''Returns a boolean indicated whether the election is open.'''
        now = datetime.today()
        return now > self.start and now < self.end

    def is_closed(self):
        '''Returns a boolean indicated whether the election is closed.'''
        return self.end < datetime.today()

    @property
    def summary(self):
        '''Returns an object with a summary of voting pattern'''
        candidates = Candidate.objects.filter(election=self).order_by('-name')
        if self.summary_json != '':
            table = json.loads(self.summary_json)
        else:
            ballots = Ballot.objects.filter(election=self)

            row_count = candidates.filter(write_in=False).count() + 1
            # Create index lookup dictionary
            cand_dict = {}
            for i, cand in enumerate(candidates):
                cand_dict[cand.id] = i

            ballots = [b.get_votes() for b in ballots]
            # initialize the array
            # Each column is a candidate, each row is a rank
            table = [[0 for x in range(candidates.count())]
                     for y in range(row_count)]

            for ballot in ballots:
                for i, c_id in enumerate(ballot):
                    table[i][cand_dict[c_id]] += 1

            # save for future use
            self.summary_json = json.dumps(table)

        return {'candidates': candidates, 'table': table}

    @classmethod
    def get_open(self):
        '''Returns a list of all open elections.'''
        all_elections = self.objects.all().select_related('candidate_set')
        elections_list = []
        for election in all_elections:
            if election.is_open():
                elections_list.append(election)
        return elections_list

    @classmethod
    def get_closed(self):
        '''Returns a list of all closed elections.'''
        return self.objects.filter(end__lt=datetime.today())


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
        return u'%s' % (self.name)


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

    def get_votes(self):
        '''Returns the votes as a list of integers'''
        if str(self.votes) == '':
            return []
        else:
            return map(int, self.votes.split(','))

    def list_candidates_by_rank(self):
        # 1. Get the list of ids as a list of integers
        ids = self.get_votes()
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
        wicands = self.election.candidate_set.filter(write_in=True)
        wiids = []
        for cand in wicands:
            wiids.append(cand.id)

        i = 1
        for vote in votes:
            if vote in wiids:
                output['w'] = i
                # Gotta save that name!!
                writeInName = Candidate.objects.get(id=vote).name
                output['writeInName'] = writeInName
            else:
                output[vote] = i
                i += 1
        return output
