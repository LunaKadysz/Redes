from voting import Voting
from representative import Representative
from party import Party

from collections import defaultdict

class TheCongress:

    def __init__(self):
        self.representatives = []
        self.votings = {}
        self.parties = []
        self.validated = False

    def add_votes(self, vote_json, year, month):
        id = vote_json['id']
        voting_title = vote_json['titulo']
        voting_type = vote_json['tipo_mayoria_texto']
        result = vote_json['resultado_texto']
        voting = Voting(year, month, id, voting_title, voting_type, result)
        actual = self.votings.get(year, [])
        actual.append(voting)
        self.votings[year] = actual
        for a_vote in vote_json['votos']:
            person_id = a_vote['diputado_id']
            if person_id is not None:
                name = a_vote['diputado_nombre']
                last_name = a_vote['diputado_apellido']
                state = a_vote['provincia_texto']

                representative = self._get_representative(person_id, name, last_name, state)

                party_id = a_vote['bloque_id']
                party_text = a_vote['bloque_texto']
                party = self._get_party(party_id, party_text)

                representative.add_party(party, year, month)
                party.add_representative(representative, year, month)

                vote = a_vote['voto_texto']
                representative.add_vote(voting, vote)
                voting.add_representative(representative, vote)

    def get_yearly_representatives(self, year):
        return [repr for repr in self.representatives if repr.was_in_year(year)]


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

    def validate(self):
        self._reloc_votings()
        self.validated = True

    def _votings_to_change(self, year):
        votings_to_change = []
        old = self.votings[year][0].get_voters(ausentes = True)
        for voting in self.votings[year]:
            new = voting.get_voters(ausentes = True)
            diff = set(new).difference(set(old))
            if len(diff) > 20:
                votings_to_change.append(voting)
            else:
                old = new
        return votings_to_change

    def _reloc_votings(self):
        to_change = []
        for year, voting_list in self.votings.items():
            votings_to_change = self._votings_to_change(year)
            for voting in votings_to_change:
                print(f'Changing vote {voting.id} in {year} to {year + 1}')
                voting.set_legislative_year(voting, year + 1)
                self.votings[year].remove(voting)
                to_change.append(voting)
        if not self.votings.get(year + 1):
            self.votings[year + 1] = votings_to_change
        else:
            self.votings[year + 1].extend(to_change)
