from . import db # db name from init py
from flask_login import UserMixin 
from sqlalchemy.sql import func # to get current date value
import pytz
# define our database fields for notes and user

# notes data
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # default will be current date value
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # refer the user who created the notes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def formatted_date(self, tz_name='US/Eastern'):
        """ Return formatted date in a specific timezone """
        if self.date:
            utc_date = self.date.replace(tzinfo=pytz.utc)  # Set timezone info to UTC
            tz = pytz.timezone(tz_name)
            local_date = utc_date.astimezone(tz)
            return local_date.strftime('%a, %b %d, %Y %I:%M %p')
        return ""
    

# user data
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    fname = db.Column(db.String(150))
    notes = db.relationship('Note')
    

