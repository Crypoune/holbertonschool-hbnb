from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text':     fields.String(required=True),
    'rating':   fields.Integer(required=True),
    'place_id': fields.String(required=True),
    'user_id':  fields.String(required=True),
})


@api.route('/')
class ReviewList(Resource):

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review created')
    @api.response(400, 'Validation error')
    def post(self):
        """Create a review"""
        data = api.payload
        if not facade.get_place(data['place_id']):
            return {'error': 'Place not found'}, 404
        if not facade.get_user(data['user_id']):
            return {'error': 'User not found'}, 404
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews')
    def get(self):
        """Get all reviews"""
        return [r.to_dict() for r in facade.get_all_reviews()], 200


@api.route('/<string:review_id>')
class ReviewDetail(Resource):

    @api.response(200, 'Review details')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        if not facade.get_review(review_id):
            return {'error': 'Review not found'}, 404
        try:
            updated = facade.update_review(review_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if not facade.get_review(review_id):
            return {'error': 'Review not found'}, 404
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
