from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from .models import BlacklistModel
from .schemas import BlacklistSchema
from .extensions import db

blacklist_schema = BlacklistSchema()

class BlacklistResource(Resource):
    
    @jwt_required()
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        try:
            data = blacklist_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        if BlacklistModel.query.filter_by(email=data.email).first():
            return {"message": "Email already exists in the blacklist"}, 409

        source_ip = request.remote_addr

        new_entry = BlacklistModel(
            email=data.email,
            app_uuid=data.app_uuid,
            blocked_reason=data.blocked_reason,
            source_ip=source_ip
        )
        
        db.session.add(new_entry)
        db.session.commit()

        return {"message": "Email added to blacklist successfully"}, 201

class BlacklistCheckResource(Resource):

    @jwt_required()
    def get(self, email):
        entry = BlacklistModel.query.filter_by(email=email).first()
        
        if entry:
            return {
                "is_blacklisted": True,
                "reason": entry.blocked_reason,
                "timestamp": entry.created_at.isoformat()
            }, 200
        else:
            return {"is_blacklisted": False}, 200
