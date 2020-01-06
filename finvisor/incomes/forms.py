from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, SubmitField, StringField
from wtforms.validators import DataRequired, Optional


class IncomeForm(FlaskForm):
    date = DateField('Date (Optional)', validators=[Optional()], format=f'%Y-%m-%d')
    title = StringField('Title', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')

