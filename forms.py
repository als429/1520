from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, FileField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional
from wtforms.fields.html5 import DateTimeLocalField


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


class FoodRegistrationForm(FlaskForm):
    fname = StringField("Meal title", validators=[InputRequired()], render_kw={"placeholder": "Meal title"})
    fcost = MyFloatField("Cost", validators=[InputRequired(), NumberRange(min=0, max=1000, message="Cost must be between $0 and $1000.")], render_kw={"placeholder": "Cost"})
    location = StringField("autocomplete", validators=[InputRequired()], render_kw={"placeholder": "Address", "class": "location", "id": "autocomplete", "onFocus": "geolocate()"})
    file = FileField("input file", validators=[Optional()], render_kw={"class": "inputfile", "type": "file"})
    fcategory = StringField("Type categories", validators=[InputRequired()], render_kw={"placeholder": "Categories"})
    fingredients = StringField("Type ingredients", validators=[InputRequired()], render_kw={"placeholder": "Ingredients"})
    submit = SubmitField('Sell Leftovers')


class DinnerRegistrationForm(FoodRegistrationForm):
    ftime = DateTimeLocalField("Host date", validators=[InputRequired()], render_kw={"placeholder": "Time"}, format="%Y-%m-%dT%H:%M")
