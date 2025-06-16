"""
User Management routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from handlers.decorators import role_required
from models.data import db, UserRole, Role, User, Survey
from forms.user_form import EditUserForm
from util.form import form_submit_error_response

user_bp = Blueprint('user', __name__)


@user_bp.route('/users')
@login_required
@role_required(UserRole.ADMIN)
def user_list():
    """
    List all users
    :return:
    """
    results = db.session.query(User, Role).outerjoin(Role, User.role_id == Role.id).all()
    return render_template('user/user_list.html', current_user=current_user, users=results)


@user_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN)
def user_edit(user_id):
    """
    Edit a user entry
    :param user_id:
    :return:
    """
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    form.role_id.choices = [(r.id, r.name) for r in Role.query.all()]

    current_role = db.session.query(Role).filter(Role.id == current_user.role_id).first()
    current_user_role = {'id':current_user.id,
                         'level': current_role.level,
                         'name': current_role.name}

    recent_surveys = (Survey.query
                      .filter(Survey.user_id == user.id)
                      .order_by(Survey.created_at.desc())
                      .limit(5).all())

    error_response = form_submit_error_response(form, 'user/user_edit.html',
                                                current_user_role=current_user_role,
                                                user=user,
                                                recent_surveys=recent_surveys)
    if error_response:
        return error_response
    if form.password.data:
        user.set_password(form.password.data)
    form.populate_obj(user)
    if form.name.data != user.name:
        user.name = form.name.data
    if form.role_id.data != user.role_id:
        user.role_id = form.role_id.data
    if form.is_active.data != user.is_active:
        user.is_active = form.is_active.data
    db.session.commit()
    flash('User updated successfully', 'success')
    return redirect(url_for('user.list_users'))


@user_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@role_required(UserRole.SUPERUSER)
def user_delete(user_id):
    """
    Delete a user entry by marking as deleted
    :param user_id:
    :return:
    """
    user = User.query.get_or_404(user_id)
    if user.role.name == 'superuser' and current_user.id != user.id:
        flash('Cannot delete other superusers', 'danger')
        return redirect(url_for('user.list_users'))

    user.is_active = False
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('user.list_users'))
