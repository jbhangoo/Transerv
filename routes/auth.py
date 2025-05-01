from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from decorators import role_required
from models.data import User, Role, db, UserRole
from forms.user import LoginForm, RegistrationForm
from util.form import form_submit_error_response
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
    form = LoginForm()
    error_response = form_submit_error_response(form, 'auth/login.html')
    if error_response:
        return error_response

    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if current_user:
            print(f"{current_user}\n Name={current_user.get_id()} auth?{current_user.is_authenticated}, active?{current_user.is_active}, Anon?{current_user.is_anonymous}, ")
        else:
            print("No current user")
        return redirect(next_page or url_for('index'))
    flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN)
def register():
    form = RegistrationForm()
    form.role_id.choices = [(r.id, r.name) for r in Role.query.all()]

    error_response = form_submit_error_response(form, 'auth/register.html')
    if error_response:
        return error_response

    user = User(
        username=form.username.data,
        password=form.password.data,
        role_id=form.role_id.data,
        email=form.email.data,
    )
    db.session.add(user)
    db.session.commit()
    flash('User created successfully', 'success')
    return redirect(url_for('user.user_list'))
