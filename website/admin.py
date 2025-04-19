
from .models import Admin, SuperAdmin 
from .__init__ import x


def add_formateur(formateur):
    try:
        firstname = formateur.firstname
        lastname = formateur.lastname
        age = formateur.age
        birthday = formateur.birthday
        state = formateur.state
        country = formateur.country
        number = formateur.number
        address = formateur.address
        email = formateur.email
        linkedin = formateur.linkedin

        conn = x.connect()
        cursor = conn.cursor()

        formateur_query = """
        INSERT INTO formateur (firstname, lastname, age, birthday, state, country, number, address, email, linkedin)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(formateur_query, (firstname, lastname, age, birthday, state, country, number, address, email, linkedin))
        conn.commit()

        formateur_id = cursor.lastrowid

        if Admin.admin:
            admin_id = Admin.admin.id
            action_query = """
            INSERT INTO action_admin (id_admin, action_name, date, id_formateur)
            VALUES (%s, %s, NOW(), %s)
            """
            cursor.execute(action_query, (admin_id, 'added_formateur', formateur_id))
            conn.commit()

        if SuperAdmin.super_admin:
            super_admin_id = SuperAdmin.super_admin.id
            action_query = """
            INSERT INTO action_superadmin (id_superadmin, action_name, date, id_formateur)
            VALUES (%s, %s, NOW(), %s)
            """
            cursor.execute(action_query, (super_admin_id, 'added_formateur', formateur_id))
            conn.commit()

        cursor.close()

        return True  
    except Exception as e:
        print("Error adding formateur:", e)
        return False

def add_request(formateur_id, privilege_name):
    try:
        conn = x.connect()
        cursor = conn.cursor()

        query_add_request = """
        INSERT INTO requests (id_formateur, id_admin, date, privilege_name)
        VALUES (%s, %s, NOW(), %s)
        """
        cursor.execute(query_add_request, (formateur_id, Admin.admin.id, privilege_name))
        conn.commit()

        cursor.close()

        print("Request added successfully.")
    except Exception as e:
        print("Error while adding request:", e)
