from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Email

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=35), Email(message='Invalid email format')])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=120)])
    bio = StringField('Bio', validators=[Length(max=150)])
    submit = SubmitField('Update Profile')