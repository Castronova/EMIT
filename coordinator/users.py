__author__ = 'tonycastronova'

import os
import json
import copy
import uuid
import datetime
from coordinator.emitLogging import elog

'''
 These are a set of classes for encapsulating user/affiliation data.  This should replace the preferences.txt file and
 enable us to store multiple user's information.
'''

# todo: move outside of gui folder, possibly into engine

class Person(object):

    def __init__(self, firstname, lastname, middlename=None):
        self.firstname = firstname
        self.lastname  = lastname
        self.middlename = middlename


class Organization(object):

    def __init__(self, typeCV, name, code, description=None, link=None, parent=None):
        self.typeCV = typeCV
        self.name = name
        self.code = code
        self.description = description
        self.link = link
        self.parent = parent

class Affiliation(object):
    def __init__(self, email=None, startDate=None, organization=None, person=None, phone=None, address=None, isPrimaryOrganizationContact=False, affiliationEnd=None, personLink=None):

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
        :return: A unique id for the user: lastname_organizationCode
        '''
        return self.person.lastname+' ['+self.organization.code+']'

    def _affilationToDict(self):

        aff_dict = copy.deepcopy(self.__dict__)
        aff_dict.pop('person')
        aff_dict.pop('organization')

        aff_dict['startDate'] = aff_dict['startDate'].strftime("%Y-%m-%dT%H:%M:%S")
        if aff_dict['affiliationEnd'] is not None:
            aff_dict['affiliationEnd'] = aff_dict['affiliationEnd'].strftime("%Y-%m-%dT%H:%M:%S")
        return {str(uuid.uuid4()):dict(person=self.person.__dict__,
                    organization=self.organization.__dict__,
                    affiliation=aff_dict)}

    def toJSON(self):
        return json.dumps(self._affilationToDict(), sort_keys=True, indent=4, separators=(',', ': '))

def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.datetime.strptime(value, "%m/%d/%Y %H:%M:%S")
        except:
            elog.debug("Failed to convert date into datetime object")
    return json_dict

def BuildAffiliationfromJSON(j):
    affiliations = []

    json_dict = json.loads(j, object_hook=date_hook)  # json_dict is a list with dictionaries, like this [{}]
    for item in json_dict:
        for key, value in item.iteritems():

            p = Person(**value['person'])
            o = Organization(**value['organization'])
            value['affiliation'].update(dict(person=p, organization=o))
            a = Affiliation(**value['affiliation'])
            affiliations.append(a)

    return affiliations


# NOTE: classes must inherit from object in order to be decoded properly
# NOTE: This doesn't work if the json serialized objects are unavailable, which will be most of the time.
# According to the JsonPickle documentation(http://jsonpickle.github.io/#module-jsonpickle),
#     the object must be accessible globally via a module and must inherit from object (AKA new-style classes).
if __name__ == "__main__":



    # p = Person('tony', 'castronova')
    # o1 = Organization(typeCV='university',
    #                   name='Utah State University',
    #                   code='usu')
    # o2 = Organization(typeCV='university',
    #                   name='Utah Water Research Laboratory',
    #                   code='uwrl',
    #                   description='description = research laboratory Affiliated with utah state university',
    #                   parent='usu')
    #
    # affilations = [Affiliation(email='tony.castronova@usu.edu', startDate=datetime.datetime(2014,03,10), organization=o1, person=p, phone='435-797-0853', address='8200 old main, logan ut, 84322'),
    #                Affiliation(email='tony.castronova@usu.edu', startDate=datetime.datetime(2014,03,10), organization=o2, person=p, address='8200 old main, logan ut, 84322')]
    #

    # # write object to json
    settings_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../app_data/configuration/'))
    # with open(settings_path + '/users.json', 'w') as f:
    #     j = {}
    #     for a in affilations:
    #         affil = a._affilationToDict()
    #         j.update(affil)
    #     j = json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))
    #     f.write(j)

    # test fromJson
    with open(settings_path + '/users.json', 'r') as f:
        jobj = BuildAffiliationfromJSON(f.read())


