from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True),
})


@api.route('/')
class AmenityList(Resource):

    @api.response(200, 'List of amenities')
    def get(self):
        """Get all amenities"""
        return [a.to_dict() for a in facade.get_all_amenities()], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created')
    @api.response(400, 'Validation error')
    def post(self):
        """Create an amenity"""
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<string:amenity_id>')
class AmenityDetail(Resource):

    @api.response(200, 'Amenity details')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity"""
        if not facade.get_amenity(amenity_id):
            return {'error': 'Amenity not found'}, 404
        try:
            updated = facade.update_amenity(amenity_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
