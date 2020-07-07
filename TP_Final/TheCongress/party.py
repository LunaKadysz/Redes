class Party:

    def __init__(self, id, text):
      self.id = id
      self.text = text
      self.representatives = {}


    def add_representative(self, representative, year, month):
        if month == 12 and self.representatives.get(year):
            if representative not in self.representatives[year]:
                actual = self.representatives.get(year + 1, set())
                actual.add(representative)
                self.representatives[year + 1] = actual
        else:
            actual = self.representatives.get(year, set())
            actual.add(representative)
            self.representatives[year] = actual
