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

    def __init__(self, first, last):
        self.first_name = first
        self.last_name = last
        self.middle_name = ''

    def get_random_id(self):
        return str(uuid.uuid4())

    def object_to_dictionary(self):
        return self.__dict__


class Organization(object):
    def __init__(self, typeCV, name, code, description=None, link=None, parent=None):
        self.typeCV = typeCV
        self.name = name
        self.code = code
        self.description = description
        self.link = link
        self.parent = parent

class Organization2(object):
    def __init__(self, name):
        self.address = None
        self.affiliation_end = None
        self.code = None
        self.description = None
        self.email = None
        self.is_primary_organization_contact = False
        self.link = None
        self.name = name
        self.parent = None
        self.person_link = None
        self.phone = None
        self.start_date = None
        self.type_cv = None

    def object_to_dictionary(self):
        return self.__dict__

    def store_date_as_object(self, date_string):
        self.start_date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')

    def set_data(self, json):
        # This implementations allows this method to be reusable without breaking
        if "code" in json:
            self.code = json["code"]
        else:
            self.code = json["name"]

        if "is_primary_organization_contact" in json:
            self.is_primary_organization_contact = json["is_primary_organization_contact"]

        if "parent" in json:
            self.parent = json["parent"]

        if "affiliation_end" in json:
            self.affiliation_end = json["affiliation_end"]

        if "name" in json:
            self.name = json["name"]

        if "phone" in json:
            self.phone = json["phone"]

        if "type" in json:
            self.type_cv = json["type"]

        if "url" in json:
            self.link = json["url"]

        if "start_date" in json:
            self.start_date = json["start_date"]

        if "address" in json:
            self.address = json["address"]

        if "person_link" in json:
            self.person_link = json["person_link"]

        if "email" in json:
            self.email = json["email"]

        if "description" in json:
            self.description = json["description"]

class Affiliation(object):
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
        :return: A unique id for the user: lastname_organizationCode
        '''
        return self.person.last_name+' ['+self.organization.code+']'

    def _affilationToDict(self):

        aff_dict = copy.deepcopy(self.__dict__)
        aff_dict.pop('person')
        aff_dict.pop('organization')

        aff_dict['startDate'] = aff_dict['startDate'].strftime("%Y-%m-%dT%H:%M:%S")
        if aff_dict['affiliationEnd'] is not None:
            aff_dict['affiliationEnd'] = aff_dict['affiliationEnd'].strftime("%Y-%m-%dT%H:%M:%S")
        # return {str(uuid.uuid4()):dict(person=self.person.__dict__,
        #             organization=self.organization.__dict__,
        #             affiliation=aff_dict)}
        aff_dict.update(self.organization.__dict__)
        return aff_dict

    def toJSON(self):
        return json.dumps(self._affilationToDict(), sort_keys=True, indent=4, separators=(',', ': '))

    def toSerializableDict(self):
        return self._affilationToDict()

def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            #  Search string for keyword date
            if key.lower().find('date') != -1:
                # Convert only those that are dates otherwise you get unnecessary errors
                json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            elog.debug("Failed to convert date into datetime object")
            pass
    return json_dict


# def BuildAffiliationfromJSON(userinfo):
#     affiliations = []
#
#     # json_dict = json.loads(j, object_hook=date_hook)
#     for key, value in userinfo.iteritems():
#
#         p = Person(**value['person'])
#         o = Organization(**value['organizations'])
#         value['affiliation'].update(dict(person=p, organization=o))
#         a = Affiliation(**value['affiliation'])
#         affiliations.append(a)
#
#     return affiliations



def jsonToDict(user_filepath):

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

            # {'person':person,
            #                              'organization':organization,
            #                              'affiliation':affiliation}


    return user_obj


    #         organizations.append([organization, affiliation])


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
    settings_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../app_data/config/'))
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


