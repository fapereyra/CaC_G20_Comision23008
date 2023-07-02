from flask import Flask, jsonify, request
from flask_cors import CORS
from tablas import create_database
from objetos import InscripcionADeporte, AdministracionDeSocios

# Crear la base de datos y la/s tabla/s si no existen
create_database()

# -------------------------------------------------------------------
# Configuración y rutas de la API Flask
# -------------------------------------------------------------------

app = Flask(__name__)
CORS(app)

inscripcion = InscripcionADeporte()         # Instanciamos una inscripcion
administracion = AdministracionDeSocios()   # Instanciamos una administracion

# Ruta para obtener los datos de un socio según su DNI
@app.route('/socios/<int:dni>', methods=['GET'])
def obtener_socio(dni):
    socio = administracion.consultar_socio(dni)
    if socio:
        return jsonify({
            'dni': socio.dni,
            'nombreyapellido': socio.nombreyapellido,
            'sexo': socio.sexo,
            'categoria': socio.categoria
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
    categoria = request.json.get('categoria')
    return administracion.dar_alta_socio(dni, nombreyapellido, sexo, categoria)

# Ruta para modificar la informacion de un socio -- CREO QUE ESTO QUEDARÍA SIN EFECTO --
@app.route('/socios/<int:codigo>', methods=['PUT'])
def modificar_socio(dni):
    nuevo_nombreyapellido = request.json.get('nombreyapellido')
    nuevo_sexo = request.json.get('sexo')
    nueva_categoria = request.json.get('categoria')
    return administracion.actualizar_socio(dni, nuevo_nombreyapellido, nuevo_sexo, nueva_categoria)

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

# Ruta para obtener las inscripciones de un socio
@app.route('/inscripciones/<int:dni>', methods=['GET'])
def obtener_inscripciones_socio():
    dni_socio = request.json.get('dni_socio')
    return inscripcion.mostrar_inscripciones_socio(dni_socio)

# Ruta para obtener todas las incripciones
@app.route('/inscripciones', methods=['GET'])
def obtener_inscripciones():
    return inscripcion.mostrar_todas_inscripciones()

# Ruta para obtener la lista de socios de la administracion
@app.route('/socios')
def obtener_socios():
    return administracion.listar_socios()

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run()
