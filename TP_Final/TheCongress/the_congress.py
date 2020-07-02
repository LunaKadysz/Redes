from voting import Voting
from representative import Representative
from party import Party

class TheCongress:

    def __init__(self):
        self.representatives = []
        self.years = {}
        self.parties = []

    def add_votes(self, vote_json, year, month):
        id = vote_json['id']
        voting_title = vote_json['titulo']
        voting_type = vote_json['tipo_mayoria_texto']
        voting = Voting(year, month, id, voting_title, voting_type)
        actual = self.years.get(year, [])
        actual.append(voting)
        self.years[year] = actual
        for a_vote in vote_json['votos']:
            person_id = a_vote['diputado_id']
            name = a_vote['diputado_nombre']
            last_name = a_vote['diputado_apellido']
            state = a_vote['provincia_texto']

            representative = self._get_representative(person_id, name, last_name, state)

            party_id = a_vote['bloque_id']
            party_text = a_vote['bloque_texto']
            party = self._get_party(party_id, party_text)

            representative.add_party(party, year)
            party.add_representative(representative, year)

            vote = a_vote['voto_texto']
            representative.add_vote(voting, vote)
            voting.add_representative(representative, vote)

    def _get_representative(self, person_id,name, last_name, state):
        for representative in self.representatives:
            if representative.id == person_id:
                return representative
        new_representative = Representative(person_id,name, last_name, state)
        self.representatives.append(new_representative)
        return new_representative

    def _get_party(self, party_id, party_text):
        for party in self.parties:
            if party.id == party_id:
                return party
        new_party = Party(party_id, party_text)
        self.parties.append(new_party)
        return new_party
