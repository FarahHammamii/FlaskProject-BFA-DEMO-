

from datetime import datetime


class Formateur:
    def __init__(self, firstname, lastname, age, birthday, state, country, number, address, formateur_id, email, linkedin,dateajout):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.birthday = birthday
        self.state = state
        self.country = country
        self.number = number
        self.address = address
        self.email = email
        self.linkedin = linkedin
        self.formateur_id = formateur_id
        self.domains = []
        self.dateajout = datetime.strptime(dateajout, '%Y-%m-%d') if isinstance(dateajout, str) else dateajout

class Admin:

    
    def __init__(self, id, email, password, firstName, lastName):
        self.id = id
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.privileges = []
        self.activity_level = 0
        self.actions = []
        self.requests = []
    def add_action(self, action_name, date, formateur_id):
        self.actions.append([action_name, date, formateur_id])

class SuperAdmin:
    super_admin = None
    
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password
        self.actions = []
        self.accept = []
        self.attribute = []
