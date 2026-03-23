from flask_restx import Namespace, Resource, fields, abort
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name':  fields.String(required=True),
    'email':      fields.String(required=True),
})


@api.route('/')
class UserList(Resource):

    @api.expect(user_model, validate=True)
    @api.response(201, 'User created')
    @api.response(400, 'Validation error')
    def post(self):
        """Create a new user"""
        if facade.get_user_by_email(api.payload['email']):
            return {'error': 'Email already registered'}, 400
        try:
            user = facade.create_user(api.payload)
            return user.to_dict(), 201
        except ValueError as e:
            abort(400, message=str(e))

    @api.response(200, 'List of users')
    def get(self):
        """Get all users"""
        return [u.to_dict() for u in facade.get_all_users()], 200


@api.route('/<string:user_id>')
class UserDetail(Resource):

    @api.response(200, 'User details')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            abort(404, message='User not found')
        return user.to_dict(), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated')
    @api.response(400, 'Validation error')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update a user"""
        user = facade.get_user(user_id)
        if not user:
            abort(404, message='User not found')
        try:
            return facade.update_user(user_id, api.payload).to_dict(), 200
        except ValueError as e:
            abort(400, message=str(e))
