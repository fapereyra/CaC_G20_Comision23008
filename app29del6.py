import sqlite3
from flask import Flask,  jsonify, request
from flask_cors import CORS


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
            nombre varchar (30) NOT NULL,
            apellido varchar (30) NOT NULL,
            deporte varchar (30)
            PRIMARY KEY (dni)
        )
    ''')
    # natalacio date NOT NULL,
    # edad int(3) NOT NULL,
    # telefono int(12) NOT NULL,
    # email varchar (30) NOT NULL,
    # contrasenia varchar (30) NOT NULL,
    # 
    # 
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS actividades (
    #         id_a int (4) NOT NULL,
    #         inscriptos int (4) NOT NULL,
    #         deporte int (4) NOT NULL,
    #         PRIMARY KEY (id_a),
    #         FOREIGN KEY (inscriptos) REFERENCES socios (id_s),
    #         FOREIGN KEY (deporte) REFERENCES deportes (id_d)
    #     )
    # ''')
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS deportes (
    #         id_d int (4) NOT NULL,
    #         nombre varchar (30) NOT NULL,
    #         categoria int (4) NOT NULL,
    #         arancel int (5) NOT NULL,
    #         PRIMARY KEY (`id_d`)
    #     )
    # ''')
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
    def __init__(self, dni, nombre, apellido, deporte):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.deporte = deporte
#        self.contrasenia = contrasenia
#        self.edad = edad
#        self.natalicio = natalicio
#        self.telefono = telefono
#        self.email = email

    def modificar(self, n_nombre, n_apellido, n_deporte):
        self.nombre = n_nombre
        self.apellido = n_apellido
        self.deporte = n_deporte
#        self.contrasenia = n_contrasenia
#        self.edad = n_edad
#        self.natalicio = n_natalicio
#        self.telefono = n_telefono
#        self.email = n_email


# -------------------------------------------------------------------
# Definimos la clase "Administracion"
# -------------------------------------------------------------------
class Administracion:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def dar_alta_socio(self, dni, nombre, apellido, deporte):
        socio_existente = self.consultar_socio(dni)
        if socio_existente:
            return jsonify({'message': 'Ya existe un socio con ese DNI.'}), 400

        # nuevo_socio = Socio(dni, nombre, apellido, deporte)
        self.cursor.execute("INSERT INTO socios VALUES (?, ?, ?, ?)", (dni, nombre, apellido, deporte))
        self.conexion.commit()
        return jsonify({'message': 'Socio dado de alta correctamente.'}), 200

    def consultar_socio(self, dni):
        self.cursor.execute("SELECT * FROM productos WHERE dni = ?", (dni,))
        row = self.cursor.fetchone()
        if row:
            dni, nombre, apellido, deporte = row
            return Socio(dni, nombre, apellido, deporte)
        return None

    def actualizar_socio(self, dni, nombre, apellido, deporte):
        socio = self.consultar_socio(dni)
        if socio:
            socio.modificar(nombre, apellido, deporte)
            self.cursor.execute("UPDATE socios SET nombre = ?, apellido = ?, deporte = ? WHERE dni = ?",
                                (nombre, apellido, deporte, dni))
            self.conexion.commit()
            return jsonify({'message': 'Socio modificado correctamente.'}), 200
        return jsonify({'message': 'Socio no encontrado.'}), 404

    def dar_baja_socio(self, dni):
        self.cursor.execute("DELETE FROM socios WHERE dni = ?", (dni,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Socio dado de baja correctamente.'}), 200
        return jsonify({'message': 'Socio no encontrado.'}), 404
# -------------------------------------------------------------------
# Definimos la clase "Inscripcion"
# -------------------------------------------------------------------
class Inscripcion:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()
        self.inscripto = []

    def agregar(self, dni, deporte, inscripto):
        socio = Administracion.consultar_socio(dni)
        if dni is None:
            return jsonify({'message': 'El socio no existe.'}), 404
        if socio.deporte >= 3: #ESTO HAY QUE IMPLEMENTARLO MEJOR PARA QUE PUEDE TENER ALGUNOS DEPORTES DIFERENTES
            return jsonify({'message': 'Solo se puede agregar 3.'}), 400

        for inscripto in self.inscripto:
            if inscripto.dni == dni:
                inscripto.deporte += deporte
                self.cursor.execute("UPDATE socios SET deporte = deporte - ? WHERE dni = ?",
                                    (deporte, dni))
                self.conexion.commit()
                return jsonify({'message': 'Socio inscripto correctamente.'}), 200

        #CODIGO PARA AGREGAR UN NUEVO DEPORTE (SI QUISIERAMOS) 
        #nuevo_item = Producto(codigo, producto.descripcion, cantidad, producto.precio)
        #self.items.append(nuevo_item)
        #self.cursor.execute("UPDATE productos SET cantidad = cantidad - ? WHERE codigo = ?",
        #                    (cantidad, codigo))
        #self.conexion.commit()
        #return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200

    def quitar(self, dni, deporte, inscripto):
        for inscripto in self.inscripto:
            if inscripto.dni == dni:
                if deporte > inscripto.deporte:
                    return jsonify({'message': 'Tiene que tener al menos una inscripción a un deporte, no puede no tener ninguna.'}), 400
                inscripto.deporte -= deporte
                if inscripto.deporte == 0:
                    self.inscripto.remove(inscripto)
                self.cursor.execute("UPDATE socio SET deporte = deporte + ? WHERE dni = ?",
                                    (deporte, dni))
                self.conexion.commit()
                return jsonify({'message': 'Socio sin inscripciones.'}), 200

        return jsonify({'message': 'El Socio no se ha inscripto a ningun deporte.'}), 404

    def mostrar(self):
        socio_inscripto = []
        for inscripto in self.inscripto:
            socio = {'dni': inscripto.dni, 'nombre': inscripto.nombre, 'deporte': inscripto.deporte,}
                        #'arancel': inscripto.arancel} #COMPLETAR LUEGO CON ESE CAMPO
            socio_inscripto.append(socio)
        return jsonify(socio_inscripto), 200


# -------------------------------------------------------------------
# Configuración y rutas de la API Flask
# -------------------------------------------------------------------

app = Flask(__name__)
CORS(app)

inscripcion = Inscripcion()         # Instanciamos una inscripcion
inscripto = Administracion()        # Instanciamos un inscripto

# Ruta para obtener los datos de un producto según su código
@app.route('/socios/<int:dni>', methods=['GET'])
def obtener_socio(dni):
    socio = inscripto.consultar_producto(dni)
    if socio:
        return jsonify({
            'dni': socio.dni,
            'nombre': socio.nombre,
            'apellido': socio.apellido,
            'deporte': socio.deporte
        }), 200
    return jsonify({'message': 'Socio no encontrado.'}), 404

# Ruta para obtener la lista de productos del inventario
@app.route('/socios', methods=['GET'])
def obtener_socio():
    return inscripto.consultar_socio() #-- NO ESTA IGUAL AL EJEMPLO ETAPA 4 --#
#-- EN EL EJEMPLO HAY UNA FUNCION: listar_productos QUE NOSOTROS NO TENEMOS.
#   ASI QUE LLAME A LA FUNCION MÁS PARECIDA A ESA --#

# Ruta para agregar un producto al inventario
@app.route('/socios', methods=['POST'])
def dar_alta_socio():
    dni = request.json.get('dni')
    nombre = request.json.get('nombre')
    apellido = request.json.get('apellido')
    deporte = request.json.get('deporte')
    return inscripto.dar_alta_socio(dni, nombre, apellido, deporte)

# Ruta para modificar un producto del inventario
@app.route('/socios/<int:dni>', methods=['PUT'])
def actualizar_socio(dni):
    nuevo_deporte = request.json.get('deporte')
    return inscripto.actualizar_socio(dni, nuevo_deporte)

# Ruta para eliminar un producto del inventario
@app.route('/socios/<int:dni>', methods=['DELETE'])
def dar_baja_socio(dni):
    return inscripto.dar_baja_socio(dni)

# Ruta para agregar un producto al carrito
@app.route('/inscripcion', methods=['POST'])
def agregar_inscripcion():
    dni = request.json.get('dni')
    deporte = request.json.get('deporte')
    inscripto = Administracion()
    return inscripcion.agregar(dni, deporte, inscripto)

# Ruta para quitar un producto del carrito
@app.route('/inscripcion', methods=['DELETE'])
def quitar_inscripcion():
    dni = request.json.get('dni')
    deporte = request.json.get('deporte')
    inscripto = Administracion()
    return inscripcion.quitar(dni, deporte, inscripto)

# Ruta para obtener el contenido del carrito
@app.route('/inscripcion', methods=['GET'])
def obtener_inscripcion():
    return inscripcion.mostrar()

# Ruta para obtener la lista de productos del inventario
@app.route('/')
def index():
    return 'API de Inventario'

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run()


