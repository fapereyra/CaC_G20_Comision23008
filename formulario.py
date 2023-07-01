from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, PasswordField
from wtforms.validators import InputRequired, Length, Email, NumberRange

class ContactForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired(), Length(min=2, max=20)])
    apellido = StringField('Apellido', validators=[InputRequired(), Length(min=2, max=20)])
    edad = IntegerField('Edad', validators=[InputRequired(),NumberRange(min=1, max=110, message='Introdice una edad valida') ])
    nacimiento = DateField('Fecha de Nacimiento', validators =[InputRequired()])
    contrasena = PasswordField('Contrasena', validators=[InputRequired(), Length(min=4, max=32)])
    email = StringField('Email', validators=[InputRequired(), Length(min=6, max=50), Email()])
    telefono = IntegerField('Telefono', validators=[InputRequired(),NumberRange(min=1, max=110, message='Introduce correctamente, Ej: 1138383833') ])
    submit = SubmitField('Enviar')