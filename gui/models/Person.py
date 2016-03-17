class Person:

    def __init__(self, first=None, last=None):
        self.first_name = first
        self.last_name = last
        self.email = None
        self.phone = -1
        self.address = None

    def print_person(self):
        print self.first_name
        print self.last_name
        print self.email
        print self.phone
        print self.address

    def set_address(self, address):
        self.address = address

    def set_email(self, email):
        self.email = email

    def set_first_name(self, first):
        self.first_name = first

    def set_last_name(self, last):
        self.last_name = last

    def set_phone(self, number):
        self.phone = number





