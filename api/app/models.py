from app import db
from flask import current_app
from datetime import datetime, timedelta


class FeatureRequest(db.Model):
    """This class defines the feature request table."""

    __tablename__ = 'feature_requests'

    # define the columns of the table, starting with its primary key
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String())
    client_id = db.Column(db.Integer)
    client_priority = db.Column(db.Integer, default=1)
    product_area = db.Column(db.String(34))
    date_target = db.Column(db.DateTime)


    def __init__(self, title):
        """Initialize the feature request with a name and its creator."""
        self.title = title

    def save(self):
        """Save a feature request.
        This applies for both creating a new feature request
        and updating an existing onupdate
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a given feature request."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return a representation of a feature request instance."""
        return "<FeatureRequest: {}>".format(self.title)
