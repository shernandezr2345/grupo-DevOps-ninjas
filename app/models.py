from datetime import datetime
from .extensions import db

class BlacklistModel(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    source_ip = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Blacklist {self.email}>'
