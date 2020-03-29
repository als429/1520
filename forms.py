from flask_wtf import FlaskForm
log('flask_wtf imported')
from wtforms import StringField, FloatField, FileField, SubmitField, DateTimeField, IntegerField
log('wtforms imported')
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional
log('wtforms.validators imported')
from wtforms.fields.html5 import DateTimeLocalField
log('wtforms.fields.html5 imported')

def log(msg):
    """Log a simple message."""
    # Look at: https://console.cloud.google.com/logs to see your logs.
    # Make sure you have "stdout" selected.
    print('main: %s' % msg)

class MyFloatField(FloatField):
    def __init__(self, *args, **kwargs):
        super(MyFloatField, self).__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0])
            except ValueError:
                self.data = None
                raise ValueError(self.gettext(''))


class MyIntegerField(IntegerField):
    def __init__(self, *args, **kwargs):
        super(MyIntegerField, self).__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                self.data = None
                raise ValueError(self.gettext(''))


class FoodRegistrationForm(FlaskForm):
    fname = StringField("Meal title", validators=[InputRequired()], render_kw={"placeholder": "Meal title"})
    fcost = MyFloatField("Cost", validators=[InputRequired(), NumberRange(min=0, max=1000, message="Cost must be between $0 and $1000.")], render_kw={"placeholder": "Cost"})
    location = StringField("autocomplete", validators=[InputRequired()], render_kw={"placeholder": "Address", "class": "location", "id": "autocomplete", "onFocus": "geolocate()"})
    file = FileField("input file", validators=[Optional()], render_kw={"class": "inputfile", "type": "file"})
    fcategory = StringField("Type categories", validators=[InputRequired()], render_kw={"placeholder": "Categories"})
    fingredients = StringField("Type ingredients", validators=[InputRequired()], render_kw={"placeholder": "Ingredients"})
    fphone_number = StringField("Phone number", validators=[InputRequired()], render_kw={"placeholder": "Phone number"})
    submit = SubmitField('Sell Leftovers')


class DinnerRegistrationForm(FoodRegistrationForm):
    ftime = DateTimeLocalField("Host date", validators=[InputRequired()], render_kw={"placeholder": "Time"}, format="%Y-%m-%dT%H:%M")
    favailable_seats = MyIntegerField("Available seats", validators=[InputRequired(), NumberRange(min=1, message="Available seats should be a number greater than 0.")], render_kw={"placeholder": "Available seats"})
