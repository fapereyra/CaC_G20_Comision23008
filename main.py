import os
from flask import Flask, jsonify, request, render_template, url_for
from flask_cors import CORS
from formulario import FormularioInscripcion
from flask_bootstrap import Bootstrap



app = Flask(__name__)
CORS(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

Bootstrap(app)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/socios', methods=["GET", "POST"])
def formulario_socio():
    form = FormularioInscripcion()
    if form.validate_on_submit():
        form_data = request.form
        # send_email(form_data['name'], form_data['email'], form_data['message'], type='contact')
        # return render_template('contact.html', title='Gracias por ponerte en contacto!',
        #                        subtitle='Tendras tu respuesta muy rapido', form=form)
    return render_template("formulario.html", title=False, form=form)

if __name__ == '__main__':
    app.run(debug=True)