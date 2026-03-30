from flask import Flask
from flask_restx import Api


def create_app(config_name='default'):
    app = Flask(__name__)

    # ── Charger la configuration ──
    from config import config
    app.config.from_object(config.get(config_name, config['default']))

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns, path='/api/v1/users')

    from app.api.v1.amenities import api as amenities_ns
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    from app.api.v1.places import api as places_ns
    api.add_namespace(places_ns, path='/api/v1/places')

    from app.api.v1.reviews import api as reviews_ns
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app