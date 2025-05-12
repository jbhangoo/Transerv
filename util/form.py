# form.py
# Form helpers
from flask import flash, render_template

def form_submit_error_response(form, template:str, **template_args):
    """
    If form was submitted and has errors then render template with errors reported
    'form' will be passed to template. Other kwargs can optionally be passed to template too
    :param form:        The form to validate
    :param template:    The template to render to user
    :param template_args:      Additional files to pass to template
    :return: If errors, return error template otherwise None
    """
    if form.validate_on_submit():
        return None

    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {field}: {error}", "danger")
    template_args["form"] = form
    return render_template(template, **template_args)
