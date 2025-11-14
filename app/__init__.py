from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import create_access_token
from .extensions import db, ma, jwt
from .resources import BlacklistResource, BlacklistCheckResource

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Use provided config or default to Config
    if config_name:
        app.config.from_object(config_name)
    else:
        app.config.from_object('app.config.Config')

    api = Api(app) 

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from . import models

    # Only create tables automatically if not in testing mode
    if not app.config.get('TESTING', False):
        with app.app_context():
            db.create_all()

    api.add_resource(BlacklistResource, '/blacklists')
    api.add_resource(BlacklistCheckResource, '/blacklists/<string:email>')

    @app.route('/get-token')
    def get_token():
        access_token = create_access_token(identity="static_user")
        return jsonify(access_token=access_token)

    @app.route('/health')
    def health_check():
        try:
            db.session.execute('SELECT 1')
            db_status = "ok"
        except Exception as e:
            db_status = "error"
            print(str(e))

        return jsonify({
            "status": "ok", 
            "message": "API is running - Test for blue/green deployment!",
            "database_status": db_status
        }), 200

    return app
