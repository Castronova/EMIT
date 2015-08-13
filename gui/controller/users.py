__author__ = 'tonycastronova'


'''
 These are a set of classes for encapsulating user/affiliation data.  This should replace the preferences.txt file and
 enable us to store multiple user's information.
'''

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

# isPrimaryOrganizationContact
# affiliationEnd
# address
# personLink
class Affiliation(object):
    def __init__(self, email, startDate, organization, person, phone=None, address=None):

        self.email = email
        self.startDate = startDate
        self.phone = phone
        self.organization = organization
        self.person = person


# def user_load(str):
#     import cPickle
#     import dill
#
#     d = dill.loads(str)
#     print d
#
#     d = cPickle.loads(str)
#     print d


# NOTE: classes must inherit from object in order to be decoded properly
# NOTE: This doesn't work if the json serialized objects are unavailable, which will be most of the time.
# According to the JsonPickle documentation(http://jsonpickle.github.io/#module-jsonpickle),
#     the object must be accessible globally via a module and must inherit from object (AKA new-style classes).
if __name__ == "__main__":

    import jsonpickle
    import cPickle as pickle
    import dill

    p = Person('tony', 'castronova')
    o1 = Organization(typeCV='university',
                      name='Utah State University',
                      code='usu')
    o2 = Organization(typeCV='university',
                      name='Utah Water Research Laboratory',
                      code='uwrl',
                      description='description = research laboratory Affiliated with utah state university',
                      parent='usu')

    affilations = [Affiliation(email='tony.castronova@usu.edu', startDate='03-10-2014', organization=o1, person=p, phone='435-797-0853', address='8200 old main, logan ut, 84322'),
                   Affiliation(email='tony.castronova@usu.edu', startDate='03-10-2014', organization=o2, person=p, address='8200 old main, logan ut, 84322')]

    # write object to json
    # jp = jsonpickle.encode(affilations)
    # with open('../../app_data/configuration/users.json', 'w') as f:
    #     f.write(jp)

    # just using pickle
    # with open('../../app_data/configuration/users.pkl', 'wb') as f:
    #     f.write(pickle.dumps(affilations))

    # using dill
    with open('../../app_data/configuration/users.pkl', 'wb') as f:
        dill.dump(affilations, f)

    # recreate object
    # with open('../../app_data/configuration/users.json', 'r') as f:
    #     json_text = f.read()
    #     data = jsonpickle.decode(json_text)

        # print data