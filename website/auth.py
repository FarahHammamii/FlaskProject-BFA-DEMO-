from flask import Blueprint, flash, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from .models import Admin, SuperAdmin
from .__init__ import x

auth = Blueprint('auth', __name__)

def load_admin(admin_id):
    try:
        conn = x.connect()
        cursor = conn.cursor()

        query_admin = """
        SELECT email, password, firstName, lastName
        FROM admin
        WHERE id = %s
        """

        cursor.execute(query_admin, (admin_id,))
        result_admin = cursor.fetchone()

        if result_admin:
            email, password, firstName, lastName = result_admin
            admin = Admin(admin_id, email, password, firstName, lastName)

            query_actions = """
            SELECT id_action_admin, action_name, date
            FROM action_admin
            WHERE id_admin = %s
            """
            cursor.execute(query_actions, (admin_id,))
            admin.actions = cursor.fetchall()

            query_requests = """
            SELECT id, request_name, date
            FROM requests
            WHERE id_admin = %s
            """
            cursor.execute(query_requests, (admin_id,))
            admin.requests = cursor.fetchall()

            cursor.close()
            Admin.admin = admin
    except Exception as e:
        print("Error while retrieving admin by ID:", e)
    return None

def load_super_admin(super_admin_id):
    try:
        conn = x.connect()
        cursor = conn.cursor()

        query_super_admin = """
        SELECT email, password
        FROM super_admin
        WHERE id = %s
        """

        cursor.execute(query_super_admin, (super_admin_id,))
        result_super_admin = cursor.fetchone()

        if result_super_admin:
            email, password = result_super_admin
            super_admin = SuperAdmin(super_admin_id, email, password)

            query_actions = """
            SELECT id_action_superadmin, action_name, date
            FROM action_superadmin
            WHERE id_superadmin = %s
            """
            cursor.execute(query_actions, (super_admin_id,))
            super_admin.actions = cursor.fetchall()

            query_accept = """
            SELECT id, id_request
            FROM accept_requests
            WHERE id_superadmin = %s
            """
            cursor.execute(query_accept, (super_admin_id,))
            super_admin.accept = cursor.fetchall()

            query_attribute = """
            SELECT id, privilege_name, id_superadmin, id_admin, id_formateur
            FROM attribute
            WHERE id_superadmin = %s
            """
            cursor.execute(query_attribute, (super_admin_id,))
            super_admin.attribute = cursor.fetchall()

            SuperAdmin.super_admin = super_admin
    except Exception as e:
        print("Error while retrieving super admin by ID:", e)
    return None

@auth.route('/login/superadmin', methods=['GET', 'POST'])
def login_superadmin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        con = x.connect()
        cur = con.cursor()
        
        cur.execute("SELECT * FROM super_admin WHERE email=%s", (email,))
        user = cur.fetchone()

        if user:
            if user[2] == password: 
                flash('Bienvenue', category="success")
                load_super_admin(user[0])
                return redirect(url_for('views.dashboard'))
            else:
                flash('Mot de passe incorrect', category="error")
                return redirect(url_for('views.form'))
        else:
            flash('Utilisateur non trouvé', category="error")
            return redirect(url_for('views.form'))

    return render_template('form.html', user=current_user)
@auth.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        con = x.connect()
        cur = con.cursor()
        
        cur.execute("SELECT * FROM admin WHERE email=%s", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user[2], password): 
            flash('Welcome', category="success")
            load_admin(user[0])
            return redirect(url_for('views.formateurs'))
        else:
            flash('Incorrect password or user not found', category="error")
            return redirect(url_for('views.form'))

    return render_template('login_admin.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_superadmin')) 
