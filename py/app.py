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
    def __init__(self, dni, nombre, apellido, contrasenia, edad, natalicio, telefono, email):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.contrasenia = contrasenia
        self.edad = edad
        self.natalicio = natalicio
        self.telefono = telefono
        self.email = email

    def modificar(self, n_nombre, n_apellido, n_contrasenia, n_edad, n_natalicio, n_telefono, n_email):
        self.nombre = n_nombre
        self.apellido = n_apellido
        self.contrasenia = n_contrasenia
        self.edad = n_edad
        self.natalicio = n_natalicio
        self.telefono = n_telefono
        self.email = n_email


# -------------------------------------------------------------------
# Definimos la clase "Administracion"
# -------------------------------------------------------------------
class Administracion:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def dar_alta_socio(self, dni, nombre, apellido, contrasenia, edad, natalicio, telefono, email):
        producto_existente = self.consultar_producto(dni)
        if producto_existente:
            return jsonify({'message': 'Ya existe un socio con ese DNI.'}), 400

        # nuevo_socio = Socio(dni, nombre, apellido, contrasenia, edad, natalicio, telefono, email)
        self.cursor.execute("INSERT INTO socios VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (dni, nombre, apellido, contrasenia, edad, natalicio, telefono, email))
        self.conexion.commit()
        return jsonify({'message': 'Socio dado de alta correctamente.'}), 200

    def consultar_socio(self, dni):
        self.cursor.execute("SELECT * FROM productos WHERE dni = ?", (dni,))
        row = self.cursor.fetchone()
        if row:
            dni, nombre, apellido, contrasenia, edad, natalicio, telefono, email = row
            return Socio(dni, nombre, apellido, contrasenia, edad, natalicio, telefono, email)
        return None

    def actualizar_socio(self, dni, nombre, apellido, contrasenia, edad, natalicio, telefono, email):
        socio = self.consultar_socio(dni)
        if socio:
            socio.modificar(nombre, apellido, contrasenia, edad, natalicio, telefono, email)
            self.cursor.execute("UPDATE socios SET nombre = ?, apellido = ?, contrasenia = ?, edad = ?, natalicio = ?, telefono = ?, email = ? WHERE dni = ?",
                                (nombre, apellido, contrasenia, edad, natalicio, telefono, email, dni))
            self.conexion.commit()
            return jsonify({'message': 'Socio modificado correctamente.'}), 200
        return jsonify({'message': 'Socio no encontrado.'}), 404

    def dar_baja_socio(self, dni):
        self.cursor.execute("DELETE FROM socios WHERE dni = ?", (dni,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Socio dado de baja correctamente.'}), 200
        return jsonify({'message': 'Socio no encontrado.'}), 404



