__author__ = 'tonycastronova'

import json
import yaml
import copy
import datetime

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
        self.isPrimaryOrganizationContact=isPrimaryOrganizationContact
        self.affiliationEnd=affiliationEnd
        self.personLink=personLink

    def ID(self):
        '''
        :return: A unique id for the user: lastname_organizationCode
        '''
        return self.person.lastname+' ['+self.organization.code+']'

    def _affilationToDict(self):
        import uuid

        aff_dict = copy.deepcopy(self.__dict__)
        aff_dict.pop('person')
        aff_dict.pop('organization')
        return {str(uuid.uuid4()):dict(person=self.person.__dict__,
                    organization=self.organization.__dict__,
                    affiliation=aff_dict)}

    def toJSON(self):
        return json.dumps(self._affilationToDict())

    def toYAML(self):
        return yaml.dump(self._affilationToDict())

def BuildAffiliationfromJSON(j):
    affiliations = []
    if not isinstance(j, list):
        j = list(j)

    for entry in j:
        json_dict = json.loads(entry)
        p = Person(**json_dict['person'])
        o = Organization(**json_dict['organization'])
        json_dict['affiliation'].update(dict(person=p,organization=o))
        a = Affiliation(**json_dict['affiliation'])
        affiliations.append(a)

    return affiliations

def BuildAffiliationfromYAML(y):
    affiliations = []
    yaml_dict = yaml.safe_load(y)

    for entry in yaml_dict.values():
        p = Person(**entry['person'])
        o = Organization(**entry['organization'])
        entry['affiliation'].update(dict(person=p,organization=o))
        a = Affiliation(**entry['affiliation'])
        affiliations.append(a)

    return affiliations




# NOTE: classes must inherit from object in order to be decoded properly
# NOTE: This doesn't work if the json serialized objects are unavailable, which will be most of the time.
# According to the JsonPickle documentation(http://jsonpickle.github.io/#module-jsonpickle),
#     the object must be accessible globally via a module and must inherit from object (AKA new-style classes).
if __name__ == "__main__":

    import jsonpickle
    import cPickle as pickle
    import dill
    import yaml
    import datetime

    p = Person('tony', 'castronova')
    o1 = Organization(typeCV='university',
                      name='Utah State University',
                      code='usu')
    o2 = Organization(typeCV='university',
                      name='Utah Water Research Laboratory',
                      code='uwrl',
                      description='description = research laboratory Affiliated with utah state university',
                      parent='usu')

    affilations = [Affiliation(email='tony.castronova@usu.edu', startDate=datetime.datetime(2014,03,10), organization=o1, person=p, phone='435-797-0853', address='8200 old main, logan ut, 84322'),
                   Affiliation(email='tony.castronova@usu.edu', startDate=datetime.datetime(2014,03,10), organization=o2, person=p, address='8200 old main, logan ut, 84322')]

    # test custom YAML dump
    with open('../../app_data/configuration/users.yaml', 'w') as f:
        for a in affilations:
            y = a.toYAML()
            f.write(y)

    # test fromYaml
    with open('../../app_data/configuration/users.yaml', 'r') as f:
        yobj = BuildAffiliationfromYAML(f.read())

    # write object to json
    # jp = jsonpickle.encode(affilations)
    # with open('../../app_data/configuration/users.json', 'w') as f:
    #     f.write(jp)

    # just using pickle
    # with open('../../app_data/configuration/users.pkl', 'wb') as f:
    #     f.write(pickle.dumps(affilations))

    # using dill
    # with open('../../app_data/configuration/users.pkl', 'wb') as f:
    #     dill.dump(affilations, f)
    #


    # # test custom JSON dump
    # with open('../../app_data/configuration/test.json', 'w') as f:
    #     for a in affilations:
    #         j = a.toJSON()
    #         f.write(j)


    # test fromJson
    # with open('../../app_data/configuration/test.json', 'r') as f:
    #     jobj = BuildAffiliationfromJSON(f.read())



