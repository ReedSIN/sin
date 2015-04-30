from django.test import TestCase
from elections.models import Election, Ballot, Candidate
from generic.models import SinUser
from datetime import datetime
import random
# Create your tests here.

class testElection:
	elections = []
	candidates = []
	ballots = []

	def __init__(self):
		#define the user
		try:
			self.usr = SinUser.objects.get(username="wjones")
		except SinUser.DoesNotExist:
			self.usr = SinUser.get_ldap_user('wjones')

		#create two elections
		e0 = Election.objects.create(position="ElectionTest3", vanity=True, end=datetime(2015, 4, 28))
		e1 = Election.objects.create(position="ElectionTest4", numSeats = 3, end=datetime(2015, 4, 28))
		self.elections.append(e0)
		self.elections.append(e1)

	def testCandidates(self):
		#create 2*numseats candidates per election
		for election in self.elections:
			for i in range(election.numSeats*2):
				c = Candidate.objects.create(election = election, name=str(election.id) + "testingCand"+ str(i), blurb = "c" + str(i) + "blurb for" + str(election.position) + ".")
				self.candidates.append(c)		

	def testBallots(self):
		#create 15 ballots for every election
		for election in self.elections:
			numSeats = election.numSeats
			for i in range(15):
				#form the (random) votes and vote string
				elecCands = Candidate.objects.filter(election=election)
				votes = random.sample([c.id for c in elecCands], numSeats)
				#map the votes to valid candidate ids
				votestr = ''.join(str(x)+ ',' for x in votes)
				votestr = votestr[0:-1]

				#save the ballot
				b = Ballot.objects.create(election=election, voter=self.usr, votes=votestr)
				self.ballots.append(b)