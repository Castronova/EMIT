class Organizations:

    def __init__(self, organization=""):
        self.organization = []
        self.organization.append(organization)

    def add_organization(self, organ):
        self.organization.append(organ)

    def remove_all_organization(self):
        self.organization = []

    def remove_organization(self, name):
        # remove by name
        self.organization.remove(name)
