
from flask import Blueprint, request

from utils import ai_funcs
from utils import db_funcs
from models import db, CompanyEmissions

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/get_suggestion/<int:result_id>')
def get_suggestion(result_id=None):
    if result_id is None:
        return {
            'status_code': 1,
            'response': 'No result_id was found!'
        }

    data = db_funcs.get_results(result_id)
    if data.suggestion is not None:
        return {
            'status_code': 0,
            'response': data.suggestion.suggestion
        }

    response = ai_funcs.get_suggestion(data)
    if response['status_code'] != 0:
        return {
            'status_code': 2,
            'response': response['suggestion']
        }

    db_funcs.save_suggestion(result_id, response['suggestion'])

    return {
        'status_code': 0,
        'response': response['suggestion']
    }


@api_bp.route('/data/')
def data():
    query = CompanyEmissions.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            CompanyEmissions.id.like(f'%{search}%'),
            CompanyEmissions.name.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': CompanyEmissions.query.count(),
        'draw': request.args.get('draw', type=int),
    }
