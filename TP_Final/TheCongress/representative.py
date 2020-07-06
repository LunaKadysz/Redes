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

    def add_party(self, party, year):
        self.parties[year] = party

    def get_attributes(self, year):
        return {'party': self.parties[year]}

    def was_in_year(self, year):
        if self.parties.get(year):
            return True

    def __eq___(self, other):
        self._validate(other)
        return self.id == other.id

    def __lt__(self, other):
        self._validate(other)
        return self.id < other.id

    def __gt__(self, other):
        self._validate(other)
        return self.id > other.id

    def _validate(self, other):
        assert type(self) == type(other), f'{type(other)} is not a Representative!'
