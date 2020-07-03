class Party:

    def __init__(self, id, text):
      self.id = id
      self.text = text
      self.representatives = {}


    def add_representative(self, representative, year):
        actual = self.representatives.get(year, set())
        actual.add(representative)
        self.representatives[year] = actual
