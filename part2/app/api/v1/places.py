from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title':       fields.String(required=True),
    'description': fields.String(default=''),
    'price':       fields.Float(required=True),
    'latitude':    fields.Float(required=True),
    'longitude':   fields.Float(required=True),
    'owner_id':    fields.String(required=True),
})


@api.route('/')
class PlaceList(Resource):

    @api.response(200, 'List of places')
    def get(self):
        """Get all places"""
        return [{'id': p.id, 'title': p.title, 'latitude': p.latitude, 'longitude': p.longitude}
                for p in facade.get_all_places()], 200

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created')
    @api.response(400, 'Validation error')
    def post(self):
        """Create a place"""
        try:
            place = facade.create_place(api.payload)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<string:place_id>')
class PlaceDetail(Resource):

    @api.response(200, 'Place details')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get a place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        owner = facade.get_user(place.owner_id)
        result = place.to_dict()
        result['owner'] = {
            'id':         owner.id,
            'first_name': owner.first_name,
            'last_name':  owner.last_name,
            'email':      owner.email,
        } if owner else None
        return result, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place"""
        if not facade.get_place(place_id):
            return {'error': 'Place not found'}, 404
        try:
            updated = facade.update_place(place_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<string:place_id>/reviews')
class PlaceReviews(Resource):

    @api.response(200, 'Reviews for place')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a place"""
        if not facade.get_place(place_id):
            return {'error': 'Place not found'}, 404
        return [r.to_dict() for r in facade.get_reviews_by_place(place_id)], 200
