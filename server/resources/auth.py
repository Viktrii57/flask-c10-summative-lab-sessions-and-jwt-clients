from flask import request, session
from flask_restful import Resource
from models import db, User
from schemas import user_schema
from marshmallow import ValidationError

class SignupResource(Resource):
    """Registers a new user and sets initial session."""
    def post(self):
        json_data = request.get_json() or {}
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
            return {'message': 'Username or email already exists'}, 409

        user = User(username=data['username'], email=data['email'])
        user.password = data['password']

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return user_schema.dump(user), 201


class LoginResource(Resource):
    """Authenticates credentials and establishes session."""
    def post(self):
        json_data = request.get_json() or {}
        email = json_data.get('email')
        password = json_data.get('password')

        if not email or not password:
            return {'message': 'Email and password required'}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {'message': 'Invalid credentials'}, 401

        session['user_id'] = user.id
        return user_schema.dump(user), 200


class LogoutResource(Resource):
    """Clears user session."""
    def delete(self):
        if 'user_id' not in session:
            return {'message': 'Unauthorized'}, 401
        
        session.pop('user_id', None)
        return {}, 204


class CheckSessionResource(Resource):
    """Checks active session state on application refresh."""
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'message': 'Unauthorized'}, 401

        user = User.query.get(user_id)
        if not user:
            session.pop('user_id', None)
            return {'message': 'User not found'}, 401

        return user_schema.dump(user), 200