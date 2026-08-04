from flask import request, session
from flask_restful import Resource
from models import db, JournalEntry
from schemas import entry_schema, entries_schema
from marshmallow import ValidationError

def get_authenticated_user_id():
    """Helper method to enforce session authorization."""
    return session.get('user_id')

class EntryListResource(Resource):
    """Handles user-scoped resource listing (paginated) and creation."""
    def get(self):
        user_id = get_authenticated_user_id()
        if not user_id:
            return {'message': 'Unauthorized access'}, 401

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        pagination = JournalEntry.query.filter_by(user_id=user_id)\
            .order_by(JournalEntry.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return {
            'entries': entries_schema.dump(pagination.items),
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }, 200

    def post(self):
        user_id = get_authenticated_user_id()
        if not user_id:
            return {'message': 'Unauthorized access'}, 401

        json_data = request.get_json() or {}
        try:
            data = entry_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        entry = JournalEntry(
            title=data['title'],
            content=data['content'],
            category=data.get('category', 'General'),
            mood_score=data.get('mood_score', 5),
            user_id=user_id
        )
        db.session.add(entry)
        db.session.commit()

        return entry_schema.dump(entry), 201


class EntryResource(Resource):
    """Handles GET, PUT, and DELETE operations for a specific entry owned by the user."""
    def get(self, entry_id):
        user_id = get_authenticated_user_id()
        if not user_id:
            return {'message': 'Unauthorized access'}, 401

        entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            return {'message': 'Resource not found or unauthorized'}, 404

        return entry_schema.dump(entry), 200

    def put(self, entry_id):
        user_id = get_authenticated_user_id()
        if not user_id:
            return {'message': 'Unauthorized access'}, 401

        entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            return {'message': 'Resource not found or unauthorized'}, 404

        json_data = request.get_json() or {}
        try:
            data = entry_schema.load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 400

        entry.title = data.get('title', entry.title)
        entry.content = data.get('content', entry.content)
        entry.category = data.get('category', entry.category)
        entry.mood_score = data.get('mood_score', entry.mood_score)

        db.session.commit()
        return entry_schema.dump(entry), 200

    def delete(self, entry_id):
        user_id = get_authenticated_user_id()
        if not user_id:
            return {'message': 'Unauthorized access'}, 401

        entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if not entry:
            return {'message': 'Resource not found or unauthorized'}, 404

        db.session.delete(entry)
        db.session.commit()
        return {'message': 'Entry deleted successfully'}, 200