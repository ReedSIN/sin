##-----------------------------------------------------------------------------#
# STV Election Tabulation
##-----------------------------------------------------------------------------#

# Each ballot is stored as a list of candidate ids, ordered by the rank the
# voter has assigned the candidate. Instead of working with individual ballots
# during calculations, this algorithm creates a tree structure that represents
# possible ways of voting and how many people voted in that particular way.
#
# Each node will have a count and candidate associated with it. It will also
# have a dictionary of child nodes, each of which represent the count of voters
# who chose a particular candidate as their next choice.
#
# In the process of keeping track of ballots, we can just merge different trees.

import math

from elections.models import Candidate, Ballot

class CandidateNode:
    """A node to form a tree structure representing voting patterns.

    Attributes:
        candidate (Candidate): the Candidate this node is associated with.
        count (int): the number of votes for this candidate given they voted for
                     the parents of this node.
    """
    def __init__(self, cand, count=0):
        """Loads the candidate and count"""
        self.cand = cand
        self.count = count
        self.children = {}

    def __repr__(self):
        """Prints the candidate name and their count"""
        return "<CandidateNode: " + self.cand.name + " (" + str(self.count) + ")>"

    def __add__(self, other):
        """Adds the counts of parents nodes and their corresponding children."""
        if isinstance(other, CandidateNode):
            # 1. Add the counts of the root nodes
            self.count += other.count
            # 2. Add the counts of the corresponding children
            # 2(a) Add nodes with zero counts to correspond with nodes for
            # Candidates present in other but not in self
            for key, child in other.children.iteritems():
                if key not in self.children:
                    new_cand = child.cand
                    self.children[key] = CandidateNode(cand = new_cand,
                                                       count = 0)
            # 2(b) Now add the nodes recursively
            for key, child in self.children.iteritems():
                # Need to be careful and check for missing keys
                if key in other.children:
                    child.__add__(other.children[key])
            return self
        else:
            raise TypeError('CandidateNodes may only be added to other CandidateNodes.')

    def __radd__(self, other):
        """Implements commutivity of addition."""
        self.__add__(self, other)

    def __rmul__(self, other):
        """Multiply a node and its children's counts by a scalar."""
        if type(other) == float:
            self.count = other * self.count
            for key, child in self.children.iteritems():
                child.__rmul__(other)
            return self
        else:
            raise TypeError('Only multiplication by floats supported.')

    def add_child(self, candidate, count=0):
        """Adds a child to the give node."""
        the_key = candidate.id
        new_node = CandidateNode(candidate, count)
        self.children[the_key] = new_node


def calculateSTV(election):
    ballots = Ballot.objects.filter(election = election)
    seats = election.numSeats

    # 1. Create a tree out of the votes.

    # First need to convent the ballots 
    ballot_list = []
    for ballot in ballots:
        ballot_list.append(ballot.votes.encode('ascii', 'ignore'))

    def get_candidate(key):
        return Candidate.objects.get(election = election, id = key)

    # Load tree dictionary
    trees = {}

    for ballot in ballot_list:
        if ballot == '':
            continue
        vote_list = ballot.split(",")
        vote_list = map(int, vote_list)


        vote_list = map(get_candidate, vote_list)

        # Create tree root, if necessary
        if vote_list[0].id not in trees:
            trees[vote_list[0].id] = CandidateNode(vote_list[0])

        node = trees[vote_list[0].id]

        for i, vote in enumerate(vote_list):
            # Add one to the count of the current node
            node.count += 1
            # If there is no next vote, break
            if i == len(vote_list):
                break
            # If the next vote has no node to go to, create it
            if i < len(vote_list)-1:
                if vote_list[i+1].id not in node.children:
                    node.add_child(vote_list[i+1])
                # Now select the new node
                node = node.children[vote_list[i+1].id]

    # 2. Define quota
    quota = math.floor( len(ballots) / (seats + 1) + 1 )
    print "The quota for this election is " + str(quota)

    # 3. Do STV Rounds
    finalists = []
        
    while len(finalists) < seats:
        print trees
        # First, check for candidates with surpluses
        for key, tree in trees.iteritems():
            if tree.count > quota:
                print "Surplus: " + tree.cand.name
                if tree.cand not in finalists:
                    finalists.append(tree.cand)
                surplus(key, trees, quota)
        # Then, eliminate the candidates with the fewest first place votes
        running_min_key = trees.keys()[0]
        for key, tree in trees.iteritems():
            if tree.count < trees[running_min_key].count:
                running_min_key = key

        print "Eliminating: " + trees[running_min_key].cand.name
        eliminate(running_min_key,trees)

    return finalists


def distribute(tree_list, trees):
    """Takes a dictionary of trees and merges them to the appropriate
    other trees."""
    for key, tree in tree_list.iteritems():
        # If the tree we need to merge to does not exist, just
        # distribute the children.
        if key not in trees:
            children = tree.children
            distribute(children, trees)
        # Otherwise merge the trees with addition
        else:
            trees[key] + tree

def surplus(key, trees, quota):
    """Redistributes the extra votes from a candidate who has more votes
    than needed for the quota."""
    total_votes = trees[key].count
    surplus = total_votes - quota
    surplus_prop = surplus / total_votes

    children = trees[key].children

    # Need to reduce votes in current tree so we don't redistribute votes twice.
    (1 - surplus_prop) * trees[key]

    for child in children:
        surplus_prop * child

    distribute(children, trees)

def eliminate(key, trees):
    """Eliminates a given candidate and redistributes their votes."""
    tree = trees[key]
    try:
        del trees[key]
    except KeyError:
        return
    children = tree.children
    distribute(children, trees)
