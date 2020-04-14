from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, FileField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional
from wtforms.fields.html5 import DateTimeLocalField
from flask_uploads import UploadSet, IMAGES #AS added
from flask_wtf.file import FileField, FileAllowed, FileRequired #AS added

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


class UploadForm(FlaskForm): #AS added
    file = FileField()
    #images = UploadSet('images', IMAGES)
    #upload = FileField('file', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
