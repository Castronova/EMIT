class Affiliation:

    def __init__(self, affiliation=""):
        self.affiliations = []
        self.affiliations.append(affiliation)

    def add_affiliation(self, name):
        self.affiliations.append(name)

    def add_many_affiliation(self, affiliation_list):
        for affil in affiliation_list:
            self.affiliations.append(affil)

    def remove_all_affiliations(self):
        self.affiliations = []

    def remove_affiliation(self, name):
        self.affiliations.remove(name)
