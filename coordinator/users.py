import copy
import datetime
import json
import uuid

'''
 These are a set of classes for encapsulating user/affiliation data.  This should replace the preferences.txt file and
 enable us to store multiple user's information.
'''

# todo: move outside of gui folder, possibly into engine

class Person(object):
    """
    Person object, mimics odm2 person table
    """

    def __init__(self, first, last):
        self.first_name = first
        self.last_name = last
        self.middle_name = ''

    def get_random_id(self):
        """
        Genenerates a unique id for the user object
        Returns: a 36 character unique identifier
        """

        return str(uuid.uuid4())


class Organization(object):
    """
    Organization object, mimics odm2 organization table
    """
    def __init__(self, typeCV, name, code, description=None, link=None, parent=None):
        self.typeCV = typeCV
        self.name = name
        self.code = code
        self.description = description
        self.link = link
        self.parent = parent


class Affiliation(object):
    """
    Afflilation Object, mimics odm2 affiliations table
    """
    def __init__(self, email, startDate, organization, person, phone, address=None, isPrimaryOrganizationContact=False, affiliationEnd=None, personLink=None):

        if None in [email, startDate, organization, person]:
            raise Exception('Required parameter not given')


        if not isinstance(startDate, datetime.datetime) and (not isinstance(affiliationEnd, datetime.datetime) or affiliationEnd is None):
            raise Exception('startDate and affiliationEnd must be python datetimes')

        self.email = email
        self.startDate = startDate
        self.phone = phone
        self.address = address
        self.organization = organization
        self.person = person
        self.isPrimaryOrganizationContact = isPrimaryOrganizationContact
        self.affiliationEnd = affiliationEnd
        self.personLink = personLink

    def ID(self):
        '''
        Generates an id for the affiliation object using the Person.last_name and Organization.code
        Returns: a unique id for the user: Person.last_name [Organization.code]
        '''
        return self.person.last_name+' ['+self.organization.code+']'

    def toSerializableDict(self):
        """
        Gets a json serializable representation of the Affiliation Class
        Returns: dictionary of the Affiliation class members without Person or Organization objects

        """
        aff_dict = copy.deepcopy(self.__dict__)
        aff_dict.pop('person')
        aff_dict.pop('organization')

        aff_dict['startDate'] = aff_dict['startDate'].strftime("%Y-%m-%dT%H:%M:%S")
        if aff_dict['affiliationEnd'] is not None:
            aff_dict['affiliationEnd'] = aff_dict['affiliationEnd'].strftime("%Y-%m-%dT%H:%M:%S")
        aff_dict.update(self.organization.__dict__)
        return aff_dict


def jsonToDict(user_filepath):
    """
    Creates a json serializable dictionary from the EMIT users.json file
    Args:
        user_filepath: path the the EMIT users.json file

    Returns: a json serializable dictionary of the Person, Organization, and Affiliations defined by users.py

    """

    with open(user_filepath, 'r') as f:
        data = json.load(f)

    user_obj = {}
    for key in data.iterkeys():

        obj = data[key]
        persondict = obj['person']
        person = Person(first=persondict["first_name"], last=persondict["last_name"])

        for orgname in obj['organizations'].iterkeys():
            org = obj['organizations'][orgname]
            organization = Organization(typeCV=org['typeCV'],
                                           name=org['name'],
                                           code=org['name'],
                                           description=org['description'],
                                           link=org['link'],
                                           parent=None)


            affiliation = Affiliation(email=org['email'],
                                         startDate=datetime.datetime.strptime(org['startDate'],'%Y-%m-%dT%H:%M:%S'),
                                         organization=organization,
                                         person=person,
                                         phone=org['phone'],
                                         address=None,
                                         isPrimaryOrganizationContact=False,
                                         affiliationEnd=None,
                                         personLink=None)

            user_obj[affiliation.ID()] = affiliation

    return user_obj

