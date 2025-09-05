from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from forms.query_form import QueryForm

query_bp = Blueprint('query', __name__, url_prefix='/query')
@query_bp.route('/', methods=['GET'])
@login_required
def querier():
    """ Query tool page """
    return render_template('querier.html', form=QueryForm())
