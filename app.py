import sqlite3
import os
from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_cors import CORS
from formulario import FormularioInscripcion
from flask_bootstrap import Bootstrap4

# Configurar la conexión a la base de datos SQLite
DATABASE = 'administracion.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Crear la/s tabla/s si no existe/n
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS socios (
            dni int (8) NOT NULL,
            nombreyapellido varchar (45) NOT NULL,
            sexo varchar (10) NOT NULL,
            categoria varchar (10) NOT NULL,
            PRIMARY KEY (dni)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deportes (
            id_d int (4) NOT NULL,
            nombre varchar (30) NOT NULL,
            arancel int (5) NOT NULL,
            PRIMARY KEY (`id_d`)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscripciones (
            id int (4) NOT NULL,
            dni_socio int (4) NOT NULL,
            id_deporte int (4) NOT NULL,
            PRIMARY KEY (`id`),
            FOREIGN KEY (`dni_socio`) REFERENCES socios (`dni`),
            FOREIGN KEY (`id_deporte`) REFERENCES deportes (`id_d`)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Verificar si la base de datos existe, si no, crearla y crear la/s tabla/s
def create_database():
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

# Crear la base de datos y la/s tabla/s si no existen
create_database()


# -------------------------------------------------------------------
# Definimos la clase "Socio"
# -------------------------------------------------------------------
class Socio:
    def __init__(self, dni, nombreyapellido, sexo, fechanacimiento):
        self.dni = dni
        self.nombreyapellido = nombreyapellido
        self.sexo = sexo
        self.fechanacimiento = fechanacimiento

    def modificar(self, n_nombreyapellido, n_sexo, n_fechanacimiento):
        self.nombreyapellido = n_nombreyapellido
        self.sexo = n_sexo
        self.fechanacimiento = n_fechanacimiento

# -------------------------------------------------------------------
# Definimos la clase "Deportes"
# -------------------------------------------------------------------
class Deportes: #-- CREO QUE FALTA CONECTAR CON BASE DE DATOS --#
    def __init__(self, id_d, nombre, categoria, arancel):
        self.id_d = id_d
        self.nombre = nombre
        self.categoria = categoria
        self.arancel = arancel

    def consultar_deporte(self, id_d):
        self.cursor.execute("SELECT * FROM deportes WHERE id_d = ?", (id_d,))
        row = self.cursor.fetchone()
        if row:
            id_d, nombre, categoria, arancel = row
            return Deportes(id_d, nombre, categoria, arancel)
        return None

# -------------------------------------------------------------------
# Definimos la clase "Inscripciones"
# -------------------------------------------------------------------
class Inscripcion:
    def __init__(self, dni_socio, id_d):
        self.dni_socio = dni_socio
        self.id_d = id_d


# -------------------------------------------------------------------
# Definimos la clase "Administracion"
# -------------------------------------------------------------------
class AdministracionDeSocios:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def dar_alta_socio(self, dni, nombreyapellido, sexo, fechanacimiento):
        socio_existente = self.consultar_socio(dni)
        if socio_existente:
            return jsonify({'message': 'Ya existe un socio con ese DNI.'}), 400

        self.cursor.execute("INSERT INTO socios VALUES (?, ?, ?, ?)", (dni, nombreyapellido, sexo, fechanacimiento))
        self.conexion.commit()
        return jsonify({'message': 'Socio dado de alta correctamente.'}), 200

    def consultar_socio(self, dni):
        self.cursor.execute("SELECT * FROM socios WHERE dni = ?", (dni,))
        row = self.cursor.fetchone()
        if row:
            dni, nombreyapellido, sexo, fechanacimiento = row
            return Socio(dni, nombreyapellido, sexo, fechanacimiento)
        return None

    def actualizar_socio(self, dni, nombreyapellido, sexo, fechanacimiento):
        socio = self.consultar_socio(dni)
        if socio:
            socio.modificar(nombreyapellido, sexo, fechanacimiento)
            self.cursor.execute("UPDATE socios SET nombreyapellido = ?, sexo = ?, fechanacimiento = ? WHERE dni = ?",
                                (nombreyapellido, sexo, fechanacimiento, dni))
            self.conexion.commit()
            return jsonify({'message': 'Socio modificado correctamente.'}), 200
        return jsonify({'message': 'Socio no encontrado.'}), 404

    def listar_socios(self):
        self.cursor.execute("SELECT * FROM socios")
        rows = self.cursor.fetchall()
        socios = []
        for row in rows:
            dni, nombreyapellido, sexo, fechanacimiento = row
            producto = {'dni': dni, 'nombreyapellido': nombreyapellido, 'sexo': sexo, 'fechanacimiento': fechanacimiento}
            socios.append(producto)
        return jsonify(socios), 200

    def dar_baja_socio(self, dni):
        InscripcionADeporte.desincribir_todos_los_deportes(dni)

        self.cursor.execute("DELETE FROM socios WHERE dni = ?", (dni,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Socio dado de baja correctamente.'}), 200
        return jsonify({'message': 'Socio no encontrado.'}), 404


# -------------------------------------------------------------------
# Definimos la clase "Inscripcion"
# -------------------------------------------------------------------
class InscripcionADeporte:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def consultar_inscripcion(self, dni, id_d):
        self.cursor.execute("SELECT * FROM inscripciones WHERE dni_socio = ? AND id_deporte = ?", (dni, id_d))
        row = self.cursor.fetchone()
        if row:
            dni_socio, id_d = row
            return Inscripcion(dni_socio, id_d)
        return None

    def inscribir(self, dni, id_d, id):
        socio = AdministracionDeSocios.consultar_socio(dni)
        if socio is None:
            return jsonify({'message': 'El socio no existe.'}), 404

        inscripcion = InscripcionADeporte.consultar_inscripcion(id, dni, id_d)
        if inscripcion is None:
            self.cursor.execute("INSERT INTO inscripciones VALUES (?, ?, ?)", (id, dni, id_d))
            self.conexion.commit()
            return jsonify({'message': 'Socio inscripto correctamente.'}), 200
        return jsonify({'message': 'El socio ya se encuentra inscripto en este deporte'}), 404

    def desinscribir(self, dni, id_d):
        self.cursor.execute("DELETE FROM inscripciones WHERE dni = ? AND id_deporte = ?", (dni, id_d))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Socio desinscripto correctamente.'}), 200
        return jsonify({'message': 'Inscripcion no encontrada.'}), 404

    def desincribir_todos_los_deportes(self, dni):
        self.cursor.execute("DELETE FROM inscripciones WHERE dni = ?", (dni,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Socio desinscripto correctamente.'}), 200
        return jsonify({'message': 'Inscripcion no encontrada.'}), 404

    def mostrar(self):
        self.cursor.execute("SELECT * FROM inscripciones")
        inscripciones_procesadas = {}
        inscripciones = self.cursor.fetchall()
        for inscripcion in inscripciones:
            id, dni_socio, id_deporte = inscripcion

            self.cursor.execute("SELECT * FROM socios WHERE dni = ?", (dni_socio,))
            dni, nombreyapellido, sexo, categoria = self.cursor.fetchone()

            self.cursor.execute("SELECT * FROM deportes WHERE id_d = ?", (id_deporte,))
            id_d, nombre, arancel = self.cursor.fetchone()

            # INCOMPLETO

            # socio = {'dni': inscripto.dni, 'nombre': inscripto.nombre, 'deporte': inscripto.deporte,}
            #             #'arancel': inscripto.arancel} #COMPLETAR LUEGO CON ESE CAMPO
            # socio_inscripto.append(socio)
        return jsonify(inscripciones_procesadas), 200


# -------------------------------------------------------------------
# Configuración y rutas de la API Flask
# -------------------------------------------------------------------

app = Flask(__name__)
CORS(app)
Bootstrap4(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

inscripcion = InscripcionADeporte()         # Instanciamos una inscripcion
administracion = AdministracionDeSocios()   # Instanciamos una administracion

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/deportes', methods=["GET"])
def deportes():
    return render_template("deportes.html")

@app.route('/institucional', methods=["GET"])
def institucional():
    return render_template("institucional.html")

@app.route('/consultas', methods=["GET"])
def consultas():
    return render_template("consultas.html")

# Ruta para obtener los datos de un socio según su DNI
@app.route('/socios/<int:dni>', methods=['GET'])
def obtener_socio(dni):
    socio = administracion.consultar_socio(dni)
    if socio:
        return jsonify({
            'dni': socio.dni,
            'nombreyapellido': socio.nombreyapellido,
            'sexo': socio.sexo,
            'fechanacimiento': socio.fechanacimiento
        }), 200
    return jsonify({'message': 'Socio no encontrado.'}), 404

# Ruta para obtener la lista de socios dados de alta
@app.route('/socios', methods=['GET'])
def obtener_socios():
    return administracion.listar_socios()

# Ruta para dar de alta un socio
@app.route('/socios', methods=['POST'])
def dar_alta_socio():
    dni = request.json.get('dni')
    nombreyapellido = request.json.get('nombreyapellido')
    sexo = request.json.get('sexo')
    fechanacimiento = request.json.get('fechanacimieno')
    return administracion.dar_alta_socio(dni, nombreyapellido, sexo, fechanacimiento)

# Ruta para modificar la informacion de un socio -- CREO QUE ESTO QUEDARÍA SIN EFECTO --
@app.route('/socios/<int:codigo>', methods=['PUT'])
def modificar_socio(dni):
    nuevo_nombreyapellido = request.json.get('nombreyapellido')
    nuevo_sexo = request.json.get('sexo')
    nuevo_fechanacimiento = request.json.get('fechanacimiento')
    return administracion.actualizar_socio(dni, nuevo_nombreyapellido, nuevo_sexo, nuevo_fechanacimiento)

# Ruta para dar de baja un socio
@app.route('/socios/<int:dni>', methods=['DELETE'])
def dar_baja_socio(dni):
    return administracion.dar_baja_socio(dni)

# Ruta para agregar inscribir un socio a un deporte
@app.route('/inscripciones', methods=['POST'])
def agregar_inscripcion():
    id = request.json.get('id')
    dni_socio = request.json.get('dni_socio')
    id_d = request.json.get('id_d')
    return inscripcion.inscribir(dni_socio, id_d, id)

# Ruta para dar de baja un socio de un deporte
@app.route('/inscripciones', methods=['DELETE'])
def quitar_inscripcion():
    dni_socio = request.json.get('dni_socio')
    id_d = request.json.get('id_d')
    return inscripcion.desinscribir(dni_socio, id_d)

# Ruta para obtener el contenido de las incripciones
@app.route('/inscripciones', methods=['GET'])
def obtener_inscripciones():
    return inscripcion.mostrar()

# Ruta para obtener la lista de socios de la administracion
# @app.route('/socios')
# def obtener_socios():
#     return administracion.listar_socios()

@app.route('/formulario', methods=["GET", "POST"])
def formulario_socio():
    form = FormularioInscripcion()
    if request.method == 'POST':
        if form.validate_on_submit():
            form_data = request.form
            return redirect(url_for("formulario_exitoso"))
    return render_template("formulario.html", form=form)

@app.route('/formulario_exitoso', methods=["GET", "POST"])
def formulario_exitoso():
    return render_template("formulario_exitoso.html")

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run(debug=True)


# INSERT INTO tabla_destino (columna1, columna2, columna3, ...)
#-- ESTO DEBERÍA IR EN ALGUNA PARTE ESPECIFICA DEL CODIGO PARA QUE CUANDO VAYA A BUSCAR LOS DATOS EN LAS TABLAS
#   PARA PEGARLOS EN inscripciones, EFECTIVAMENTE HAYA DATOS PARA RECUPERAR.  --#

# conn = conectar()
# cursor = conn.cursor()
# cursor.execute("""INSERT INTO inscripciones
#                (dni_socio, id_d)
#                VALUES((?), (SELECT dni_socio FROM socios), (SELECT id_d FROM deportes))""")
# conn.commit()
# cursor.close()
# conn.close()

# SELECT columna1, columna2, columna3, ...
# FROM tabla_origen
# WHERE condicion;
