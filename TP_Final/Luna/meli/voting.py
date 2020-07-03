class Voting:

    def __init__(self, year, month, id, vote_title, voting_type, session_num):
        self.session = session_num
        self.year = year
        self.month = month
        self.id = id
        self.vote_title = vote_title
        self.voting_type = voting_type
        self._create_vote_dict()

    def _create_vote_dict(self):
        self.votos = {'AFIRMATIVO': [], 'NEGATIVO': [], 'ABSTENCION': [], 'AUSENTE': []}

    def add_representative(self, representative, vote):
        self.votos[vote].append(representative)
