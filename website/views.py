from io import BytesIO
from flask import  url_for
import os
from flask import Blueprint, flash, jsonify, redirect, render_template, request, send_file, url_for
from  .models import Admin, Formateur
from . import x
import base64
from datetime import datetime
from collections import defaultdict
from flask import session

def calculate_privilege_percentages(admins):
    try:
        aj_count = 0
        del_count = 0
        modf_count = 0

        total_admins = len(admins)
        total=0

        for admin in admins:
            for privilege in admin.privileges:
                if privilege == 'aj':
                    aj_count += 1
                elif privilege == 'del':
                    del_count += 1
                elif privilege == 'mod':
                    modf_count += 1
                total=total+1


        return [aj_count, del_count, modf_count]

    except Exception as e:
        print("Error calculating privilege percentages:", e)
        return [0, 0, 0]  
views = Blueprint('views', __name__)
@views.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(views.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@views.route('/')
def home():
    if 'admin' not in session:
        session['admin'] = None

    return render_template("index.html")

def get_formateurs_with_domains():
    try:
        conn = x.connect()
        cursor = conn.cursor()

        query = """
        SELECT firstname, lastname, age, birthday, state, country, number, address, id AS formateur_id, email, linkedin, dateAjout
        FROM formateur
        """

        cursor.execute(query)
        results = cursor.fetchall()

        formateurs_dict = {}
        for row in results:
            formateur_id = row[8]
            if formateur_id not in formateurs_dict:
                formateurs_dict[formateur_id] = Formateur(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],row[11])
        query = """
        SELECT formateur_id, domain_name
        FROM domain
        """
        cursor.execute(query)
        domain_results = cursor.fetchall()

        for domain_row in domain_results:
            formateur_id = domain_row[0]
            if formateur_id in formateurs_dict:
                formateurs_dict[formateur_id].domains.append(domain_row[1])

        cursor.close()

        formateurs = list(formateurs_dict.values())
        return formateurs

    except Exception as e:
        print("Error while retrieving formateurs:", e)
        return []

@views.route('/dashboard')
def dashboard():
    admins = get_admins()  
    formateurs = get_formateurs_with_domains()
    domains = []
    countries = [formateur.country for formateur in formateurs if formateur.country]
    countries = list(set(country.capitalize() for country in countries))
    for formateur in formateurs:
        for domain in formateur.domains:
            normalized_domain = domain.strip().lower()
            if normalized_domain not in domains:
                domains.append(normalized_domain)
    formateurs_count = len(formateurs)
    formateurs_by_month = count_formateurs_by_month(formateurs)
    

    activities_data = calculate_activities_per_month(admins)
    top_admins = get_top_active_admins(admins, n=3) 
    privi=calculate_privilege_percentages(admins)


    return render_template('dashboard.html',admins=admins,activities_data=activities_data,top_admins=top_admins,privi=privi,number=formateurs_count, formateurs_by_month=formateurs_by_month,domains=domains,countries=countries)

@views.route('/profile')
def profile():
    return render_template('profile.html')

@views.route('/settings')
def settings():
    return render_template('settings.html')

@views.route('/notification')
def notification():
    notifications=get_admin_notifications()
    return render_template('notification.html',notifications=notifications)

@views.route('/formateurs')
def formateurs():
    formateurs = get_formateurs_with_domains()
    return render_template('formateurs.html',formateurs=formateurs)
@views.route('/about.html')
def about():
    return render_template('about.html')

@views.route('/form.html')
def form():
    return render_template('form.html')

def get_image_data_from_database(formateur_id):
    try:
        conn = x.connect()
        cursor = conn.cursor()

        query = "SELECT image FROM formateur WHERE id = %s"
        cursor.execute(query, (formateur_id,))

        image_data = cursor.fetchone()[0]

        return image_data

    except Exception as e:
        print("Error fetching image data:", e)
        return None

@views.route('/get_image/<int:formateur_id>')
def get_image(formateur_id):
    image_data = get_image_data_from_database(formateur_id)
    if image_data:
        return send_file(BytesIO(image_data), mimetype='image/png')
    return "Image not found", 404

@views.route('/formateur/<int:formateur_id>')
def formateur_detail(formateur_id):
    formateur = get_formateur_by_id(formateur_id)
    return render_template('oneTrainer.html', formateur=formateur)

def get_formateur_by_id(formateur_id):
    try:
        conn = x.connect()
        cursor = conn.cursor()

        query = """
        SELECT f.firstname, f.lastname, f.age, f.birthday, f.state, f.country, f.number, f.address, f.id AS formateur_id, f.email, f.linkedin, f.dateajout, d.domain_name
        FROM formateur AS f
        LEFT JOIN domain AS d ON f.id = d.formateur_id
        WHERE f.id = %s
        """


        cursor.execute(query, (formateur_id,))
        results = cursor.fetchall()

        formateur = None
        for row in results:
            if formateur is None:
                formateur = Formateur(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],row[11])
            formateur.domains.append(row[12])

        cursor.close()

        return formateur
    except Exception as e:
        print("Error while retrieving formateur by ID:", e)
        return None

@views.route('/modifier_formateur/<int:formateur_id>', methods=['GET', 'POST'])
def modifier_formateur(formateur_id):
    formateur = get_formateur_by_id(formateur_id)
    if not formateur:
        flash('Formateur not found', 'error')
        return redirect(url_for('views.formateurs'))
    return render_template('modifier.html', formateur=formateur)

from datetime import datetime

@views.route('/update_formateur/<int:formateur_id>', methods=['POST'])
def update_formateur(formateur_id):
    try:
        conn = x.connect()
        cursor = conn.cursor()

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        birthday = request.form['birthday']
        country = request.form['country']
        state = request.form['state']
        address = request.form['address']
        email = request.form['email']
        linkedin = request.form['linkedin']

        image = None
        if 'image' in request.files and request.files['image'].filename != '':
            image_file = request.files['image']
            image = image_file.read()

        if image:
            query = """
            UPDATE formateur
            SET firstname = %s, lastname = %s, age = %s, birthday = %s, country = %s,
                state = %s, address = %s, email = %s, linkedin = %s, image = %s
            WHERE id = %s
            """
            cursor.execute(query, (firstname, lastname, age, birthday, country, state, address, email, linkedin, image, formateur_id))
        else:
            query = """
            UPDATE formateur
            SET firstname = %s, lastname = %s, age = %s, birthday = %s, country = %s,
                state = %s, address = %s, email = %s, linkedin = %s
            WHERE id = %s
            """
            cursor.execute(query, (firstname, lastname, age, birthday, country, state, address, email, linkedin, formateur_id))

        conn.commit()

        # Add action to the action_admin table if the session has admin info and privileges
        if 'admin' in session and isinstance(session['admin'], dict):
            admin_info = session['admin']
            if 'privileges' in admin_info and admin_info['privileges']:
                action_name = 'mod'  # Assuming 'mod' represents modification
                date = datetime.now()
                id_admin = admin_info.get('id')

                # Insert action into action_admin table
                action_query = """
                INSERT INTO action_admin (id_admin, action_name, date, id_formateur)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(action_query, (id_admin, action_name, date, formateur_id))
                conn.commit()

        flash('Formateur modifié', 'success')
        return redirect(url_for('views.formateur_detail', formateur_id=formateur_id))
    except Exception as e:
        flash(f'Error updating formateur: {e}', 'error')
        return redirect(url_for('views.modifier_formateur', formateur_id=formateur_id))
    finally:
        cursor.close()
        conn.close()

def get_cv_data_from_database(formateur_id):
    try:
        conn = x.connect()
        cursor = conn.cursor()

        query = "SELECT cv FROM formateur WHERE id = %s"
        cursor.execute(query, (formateur_id,))

        cv_data = cursor.fetchone()[0]

        return cv_data

    except Exception as e:
        print("Error fetching CV data:", e)
        return None

@views.route('/get_cv/<int:formateur_id>')
def get_cv(formateur_id):
    cv_data = get_cv_data_from_database(formateur_id)
    if cv_data:
        return send_file(BytesIO(cv_data), mimetype='application/pdf')
    return "CV not found", 404
def delete_formateur_and_domains(formateur_id):
    try:
        conn = x.connect()
        cursor = conn.cursor()

        delete_domain_query = "DELETE FROM domain WHERE formateur_id = %s"
        cursor.execute(delete_domain_query, (formateur_id,))

        delete_formateur_query = "DELETE FROM formateur WHERE id = %s"
        cursor.execute(delete_formateur_query, (formateur_id,))

        conn.commit()
        cursor.close()

        return True 
    except Exception as e:
        print("Error deleting formateur and domains:", e)
        return False  

@views.route('/supprimer_formateur/<int:formateur_id>', methods=['DELETE'])
def supprimer_formateur(formateur_id):
    if delete_formateur_and_domains(formateur_id):
        if 'admin' in session:
            conn = x.connect()
            cursor = conn.cursor()
            admin_info = session['admin']
            query_action = """
            INSERT INTO action_admin (id_admin, action_name, date, id_formateur)
            VALUES (%s, %s, NOW(), %s)
            """
            cursor.execute(query_action, (admin_info['id'], 'del', formateur_id))
            conn.commit()

        return '', 204  
    else:
        return '', 500  

def get_admins():
    try:
        conn = x.connect()
        cursor = conn.cursor()

        query = """
        SELECT a.id, a.email, a.password, a.firstName, a.lastName, ap.privilege_name, aa.action_name, aa.date, aa.id_formateur
        FROM admin a
        LEFT JOIN action_admin aa ON a.id = aa.id_admin
        LEFT JOIN privileges ap ON a.id = ap.id_admin
        """

        cursor.execute(query)
        results = cursor.fetchall()

        admins_dict = {}
        for row in results:
            admin_id = row[0]
            if admin_id not in admins_dict:
                admins_dict[admin_id] = Admin(row[0], row[1], row[2], row[3], row[4])

            if row[5] is not None:
                privilege_name = row[5]
                if privilege_name not in admins_dict[admin_id].privileges:
                    admins_dict[admin_id].privileges.append(privilege_name)

            if row[6] is not None:
                date_dt = row[7]
                yy = date_dt.year
                month = date_dt.month
                day = date_dt.day
                date_tuple = (yy, month, day)
                admins_dict[admin_id].add_action(row[6], date_tuple, row[8])

        admins = list(admins_dict.values())

        cursor.close()
        for admin in admins:
            print(f"Admin ID: {admin.id}, Email: {admin.email}, Name: {admin.firstName} {admin.lastName}")
            print("Privileges:", admin.privileges)
            print("Actions:")
            for action in admin.actions:
                print(f"  Action: {action[0]}, Date: {action[1]}, Formateur ID: {action[2]}")
        activity_counts = calculate_activities_per_month(admins)
        print(calculate_privilege_percentages(admins))
        print("Activities per Month:", activity_counts)

        return admins
    
    except Exception as e:
        print("Error while fetching admins:", e)
        return None


def get_imageadmin_data_from_database(admin_id):
    try:
        conn = x.connect()
        cursor = conn.cursor()

        query = "SELECT image FROM admin WHERE id = %s"
        cursor.execute(query, (admin_id,))

        image_data = cursor.fetchone()[0]

        return image_data

    except Exception as e:
        print("Error fetching image data:", e)
        return None

@views.route('/get_imageadmin/<int:admin_id>')
def get_imageadmin(admin_id):
    image_data = get_imageadmin_data_from_database(admin_id)
    if image_data:
        return send_file(BytesIO(image_data), mimetype='image/png')
    return "Image not found", 404
def calculate_activities_per_month(admins):
   
    activities_per_month = defaultdict(int)
    
    for admin in admins:
        print(f"Admin ID: {admin.id}")  # Debug print
        for action in admin.actions:
            print(f"Action: {action}") 
            
            try:
                yy, month, day = action[1]
                activities_per_month[month] += 1
            except ValueError as e:
                print(f"Error parsing date {action[1]}: {e}")  # Debug print
                continue
    
    # Prepare the data in the format expected by Chart.js
    # Assuming months are from January (1) to December (12)
    activity_counts = []
    for month in range(1, 13):  # 12 months
        activity_counts.append(activities_per_month[month])
    print (activity_counts)
    
    return activity_counts
def get_top_active_admins(admins, n=3):
   
    for admin in admins:
        admin.activity_level = len(admin.actions)  

    sorted_admins = sorted(admins, key=lambda admin: admin.activity_level, reverse=True)

    return sorted_admins[:n]
def count_formateurs_added_by_me(formateurs):
    try:
        count = 0
        for formateur in formateurs:
            if formateur.dateajout and formateur.dateajout.month == datetime.now().month :
                count += 1
        return count
    except Exception as e:
        print(f"Error counting formateurs added : {e}")
        return 0
from collections import defaultdict
from datetime import datetime

def count_formateurs_by_month(formateurs):
    current_year= datetime.now().year

    formateurs_by_month = defaultdict(int)

    for formateur in formateurs:
        if formateur.dateajout:
            if formateur.dateajout.year==current_year:
                month = formateur.dateajout.month
                formateurs_by_month[month] += 1

    # Create a list for the count of formateurs by month
    formateurs_counts = [0] * 12  # Initialize for all months
    for month in range(1, 13):
        formateurs_counts[month - 1] = formateurs_by_month[month]

    return formateurs_counts
@views.route('/ajouterAdmin')
def ajouterAdmin():
    return render_template('ajouterAdmin.html')
@views.route('/ajouterFormateur')
def ajouterFormateur():
    return render_template('ajouterFormateur.html')
@views.route('/add_formateur', methods=['POST'])
def add_formateur():
    try:
        conn = x.connect()
        cursor = conn.cursor()

        # Extract form data
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        email = request.form['email']
        phone = request.form['phone']
        birthday = request.form['birthday']
        country = request.form['country']
        state = request.form['state']
        address = request.form['address']
        linkedin = request.form['linkedIn']
        domains = request.form.get('domains', '').split(',')

        # Handle file uploads
        image = request.files['image'].read() if 'image' in request.files and request.files['image'].filename != '' else None
        cv = request.files['cv'].read() if 'cv' in request.files and request.files['cv'].filename != '' else None

        # Insert into formateur table
        query = """
        INSERT INTO formateur (firstname, lastname, email, number, birthday, country, state, address, linkedin, image, cv, dateAjout)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        dateAjout = datetime.now()
        cursor.execute(query, (firstname, lastname, email, phone, birthday, country, state, address, linkedin, image, cv, dateAjout))
        formateur_id = cursor.lastrowid

        # Insert into domain table
        for domain in domains:
            domain = domain.strip()
            if domain:
                query = "INSERT INTO domain (formateur_id, domain_name) VALUES (%s, %s)"
                cursor.execute(query, (formateur_id, domain))

        conn.commit()
        cursor.close()

        return redirect(url_for('views.formateurs'))
    except Exception as e:
        print(e)  # Consider logging the error in production
        return redirect(url_for('views.ajouterFormateur'))
@views.route('/add_admin', methods=['POST'])
def add_admin():
        conn = x.connect()
        cursor = conn.cursor()

        # Extract form data
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if role == 'admin':
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            address = request.form.get('address', '')
            image = request.files['image'].read() if 'image' in request.files and request.files['image'].filename != '' else None
            date_added = datetime.now()

            # Insert into admin table
            query = """
            INSERT INTO admin (email, password, firstName, lastName, address, date, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (email, password, first_name, last_name, address, date_added, image))
            admin_id = cursor.lastrowid

            # Add privilege for the new admin
            privilege_query = "INSERT INTO privileges (id_admin, privilege_name) VALUES (%s, %s)"
            cursor.execute(privilege_query, (admin_id, 'aj'))

            # Log action in action_admin table
            current_admin_id = session.get('admin_id')  # Get the current admin's ID from the session
            action_query = """
            INSERT INTO action_admin (id_admin, action_name, date, id_formateur)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(action_query, (current_admin_id, 'aj', datetime.now(), None))

        elif role == 'superadmin':
            # Insert into super_admin table
            query = """
            INSERT INTO super_admin (email, password)
            VALUES (%s, %s)
            """
            cursor.execute(query, (email, password))

        conn.commit()
        cursor.close()

        return redirect(url_for('views.dashboard'))  # Adjust the redirect as needed


@views.route('/grant_modifier/<int:admin_id>', methods=['POST'])
def grant_modifier(admin_id):
    conn = x.connect()
    cursor = conn.cursor()
    
    # Check if the privilege already exists
    cursor.execute("SELECT * FROM privileges WHERE id_admin = %s AND privilege_name = %s", (admin_id, 'mod'))
    existing_privilege = cursor.fetchone()
    
    if not existing_privilege:
        privilege_query = "INSERT INTO privileges (id_admin, privilege_name) VALUES (%s, %s)"
        cursor.execute(privilege_query, (admin_id, 'mod'))
        conn.commit()
        flash('Privilege "Modifier" granted successfully!', 'success')
    else:
        flash('Privilege "Modifier" already granted.', 'info')
    
    cursor.close()
    conn.close()
    return redirect(url_for('views.dashboard'))

# Grant 'supprimer' privilege
@views.route('/grant_supprimer/<int:admin_id>', methods=['POST'])
def grant_supprimer(admin_id):
    conn = x.connect()
    cursor = conn.cursor()
    
    # Check if the privilege already exists
    cursor.execute("SELECT * FROM privileges WHERE id_admin = %s AND privilege_name = %s", (admin_id, 'del'))
    existing_privilege = cursor.fetchone()
    
    if not existing_privilege:
        privilege_query = "INSERT INTO privileges (id_admin, privilege_name) VALUES (%s, %s)"
        cursor.execute(privilege_query, (admin_id, 'del'))
        conn.commit()
        flash('Privilege "Supprimer" granted successfully!', 'success')
    else:
        flash('Privilege "Supprimer" already granted.', 'info')
    
    cursor.close()
    conn.close()
    return redirect(url_for('views.dashboard'))

def get_admin_notifications():
    query = """
        SELECT aa.id_action_admin, aa.action_name, aa.date, a.firstName, a.lastName, f.id, a.id
        FROM action_admin aa
        JOIN admin a ON aa.id_admin = a.id
        JOIN formateur f ON aa.id_formateur = f.id
        ORDER BY aa.date DESC
    """
    conn = x.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    notifications = cursor.fetchall()
    return [
        {
            "id_action_admin": notification[0],
            "action_name": notification[1],
            "date": notification[2],
            "admin_name": notification[3],
            "admin_last_name": notification[4],
            "formateur_id": notification[5],
            "admin_id":notification[6]
        }
        for notification in notifications
    ]
@views.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    is_super_admin = request.form.get('is_super_admin') == 'true'
    user = validate_login(email, password, is_super_admin)

    if user:
        flash('Connexion réussie', 'success')
        if is_super_admin:
            return redirect(url_for('views.dashboard'))
        else:
            admin = get_admin_by_email(email)
            session['admin'] = admin  
            print("Admin session data:", session.get('admin'))
            return redirect(url_for('views.formateurs'))
    else:
        flash('Email ou mot de passe incorrect', 'error')
        return redirect(url_for('views.form'))
@views.route('/login_superadmin', methods=['POST'])
def login_superadmin():
    email = request.form.get('email')
    password = request.form.get('password')

    user = validate_login(email, password, is_super_admin=True)

    if user:
        session['admin']= {
            'email':email,
        }
        return redirect(url_for('views.dashboard'))
    else:
        flash('Email ou mot de passe incorrect', 'error')
        return redirect(url_for('views.form'))


@views.route('/login_admin', methods=['POST'])
def login_admin():
    email = request.form.get('email')
    password = request.form.get('password')

    user = validate_login(email, password, is_super_admin=False)

    if user:
        admin = get_admin_by_email(email)
        session['admin'] = admin
        print(session['admin'])
        return redirect(url_for('views.formateurs'))
    else:
        flash('Email ou mot de passe incorrect', 'error')
        return redirect(url_for('views.form'))


def validate_login(email, password, is_super_admin):
    conn = x.connect()
    cursor = conn.cursor()
    print(email)
    if is_super_admin:
            query = "SELECT id, email, password FROM super_admin WHERE email = %s"
            print("1")
    else:
            query = "SELECT id, email, password FROM admin WHERE email = %s"
            print("0")
        
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    print(f"Result from database: {result}")
    if result and result[2] == password: 
            return result
    else:
            return None

    
    cursor.close()
    conn.close()

def get_admin_by_email(email):
    conn = x.connect()
    cursor = conn.cursor()
        
    query = """
        SELECT a.id, a.email, a.password, a.firstName, a.lastName, ap.privilege_name, aa.action_name, aa.date, aa.id_formateur
        FROM admin a
        LEFT JOIN action_admin aa ON a.id = aa.id_admin
        LEFT JOIN privileges ap ON a.id = ap.id_admin
        WHERE a.email = %s
        """
        
    cursor.execute(query, (email,))
    results = cursor.fetchall()

    if not results:
            return None
        
    admin_id = None
    admin_details = None
    privileges = set()
    actions = []

    for row in results:
            if admin_id is None:
                admin_id = row[0]
                admin_details = {
                    'id': row[0],
                    'email': row[1],
                    'password': row[2],
                    'firstName': row[3],
                    'lastName': row[4],
                    'privileges': set()
                }

            if row[5]:
                privileges.add(row[5])


    if admin_details:
            admin_details['privileges'] = list(privileges)

    return admin_details

   
    cursor.close()
    conn.close()
@views.route('/logout')
def logout():
    # Clear the session
    session.pop('admin', None)
    # Redirect to the index page
    return redirect(url_for('views.home'))