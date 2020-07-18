class Voting:

    """ 'AFIRMATIVO' = 'AFIRMATIVO'
    'NEGATIVO' = 'NEGATIVO'
    'ABSTENCION' = 'ABSTENCION'
    'AUSENTE' = 'AUSENTE' """

    def __init__(self, year, month, id, vote_title, voting_type, result):
        self.year = year
        self.month = month
        self.id = id
        self.vote_title = vote_title
        self.voting_type = voting_type
        self.result = result
        self.legislative_year = year
        self.legislative_month = month
        self._create_vote_dict()

    def _create_vote_dict(self):
        self.votos = {'AFIRMATIVO': [], 'NEGATIVO': [], 'ABSTENCION': [], 'AUSENTE': []}

    def add_representative(self, representative, vote):
        self.votos[vote].append(representative)

    def get_voters(self, ausentes = False):
        voters = self.votos['AFIRMATIVO'] + self.votos['NEGATIVO'] + self.votos['ABSTENCION']
        if ausentes:
            all_voters = voters + self.votos['AUSENTE']
            return all_voters
        else:
            return voters

    def set_legislative_year(self, voting, year):
        self.legislative_year = year
        self.legislative_month = 0

    def __hash__(self):
        return hash((self.id, self.year))

    def __eq__(self, other):
        return self.id == other.id and self.year == other.year and len(self.votos['AFIRMATIVO']) == len(other.votos['AFIRMATIVO']) and len(self.votos['NEGATIVO']) == len(other.votos['NEGATIVO']) and len(self.votos['AUSENTE']) == len(other.votos['AUSENTE']) and len(self.votos['ABSTENCION']) == len(other.votos['ABSTENCION'])
