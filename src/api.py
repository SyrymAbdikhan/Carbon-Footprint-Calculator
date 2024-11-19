
from utils import get_ai_suggestion

from flask import Blueprint, request
from models import db, CompanyEmissions, ReductionSuggestions

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/get_suggestion/')
def get_suggestion():
    result_id = request.args.get('result_id', None, type=int)
    if result_id is None:
        return {
            'status_code': 1,
            'response': ''
        }

    data = CompanyEmissions.query.filter_by(id=result_id).first()
    if data.suggestion is not None:
        return {
            'status_code': 0,
            'response': data.suggestion.suggestion
        }

    response = get_ai_suggestion(data)
    if response['status_code'] != 0:
        return {
            'status_code': 2,
            'response': response['suggestion']
        }

    suggestion = ReductionSuggestions(
        result_id=result_id,
        suggestion=response['suggestion']
    )
    db.session.add(suggestion)
    db.session.commit()

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
