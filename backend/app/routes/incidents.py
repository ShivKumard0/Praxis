from flask import Blueprint, jsonify, request
from ..utils.db import query_db, get_db
import datetime

incidents_bp = Blueprint('incidents', __name__)

# Mock data for incidents since we don't have a table for it yet
# In a real app, this would be in the DB
MOCK_INCIDENTS = [
    {'id': 1, 'type': 'Stockout', 'severity': 'High', 'description': 'Furniture stock critical in North Region', 'date': '2025-10-15', 'status': 'Open'},
    {'id': 2, 'type': 'Delay', 'severity': 'Medium', 'description': 'Supplier A delivery delayed by 3 days', 'date': '2025-10-14', 'status': 'Investigating'},
    {'id': 3, 'type': 'Price', 'severity': 'Low', 'description': 'Competitor price drop detected for Tables', 'date': '2025-10-12', 'status': 'Resolved'}
]

MOCK_COMMENTS = []

@incidents_bp.route('/incidents-log', methods=['GET'])
def get_incidents():
    return jsonify(MOCK_INCIDENTS)

@incidents_bp.route('/comments', methods=['GET', 'POST'])
def handle_comments():
    if request.method == 'POST':
        data = request.get_json()
        comment = {
            'id': len(MOCK_COMMENTS) + 1,
            'user': 'Supply Chain Mgr', # Mock user
            'text': data.get('text'),
            'chart_id': data.get('chart_id'),
            'timestamp': datetime.datetime.now().isoformat()
        }
        MOCK_COMMENTS.append(comment)
        return jsonify(comment), 201
        
    return jsonify(MOCK_COMMENTS)
