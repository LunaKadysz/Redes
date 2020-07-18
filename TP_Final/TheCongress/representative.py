from collections import defaultdict
class Representative:

    def __init__(self, id, name, last_name, state):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.state = state
        self.parties = {}
        self.votes = {}

    def add_vote(self, voting, vote):
        self.votes[voting] = vote

    def add_party(self, party, year, month):
        if month == 12:
            if party not in self.parties.get(year, set()):
                self.parties[year + 1] = set()
                self.parties[year + 1].add(party)
            else:
                self.parties[year] = set()
                self.parties[year].add(party)

        else:
            self.parties[year] = set()
            self.parties[year].add(party)

    def get_attributes(self, year):
        return {'party': self.parties.get(year)}

    def was_in_year(self, year):
        if self.parties.get(year):
            return True

    def __hash__(self):
        return hash((self.id, self.name, self.last_name))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id and self.name == other.name and self.last_name == other.last_name and self.votes == other.votes

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id
