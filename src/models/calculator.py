from src.models.user import db
from datetime import datetime

class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(255), nullable=False)
    result = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'expression': self.expression,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
