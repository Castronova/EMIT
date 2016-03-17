from gui.models.Affiliations import Affiliation
from gui.models.Person import Person
from gui.models.Organizations import Organizations

class User:

    def __init__(self, first, last, organ, phone, email):

        self.new_person = Person(first=first, last=last)
        self.organization = Organizations(organization=organ)



