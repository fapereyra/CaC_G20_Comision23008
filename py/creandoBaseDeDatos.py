#-- INSTALAR COMPLEMENTO SQL PARA PYTHON --#
import sqlite3

DATABASE = "datos.db"

#-- CREAR BASE DE DATOS --#
def conectar():
    conn = sqlite3.conect(DATABASE)
    conn.row_factory = sqlite3.row  
    return conn

conn = conectar()
cursor = conn.cursor()
cursor.excute("""CREATE TABLE IF NOT EXISTS deportes (
            id_d INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria INTEGER NOT NULL,
            arancel INTEGER NOT NULL,
            )""")
conn.commit()
cursor.close()
conn.close()
#--------------------------------------------------------#
conn = conectar()
cursor = conn.cursor()
cursor.excute("""CREATE TABLE IF NOT EXISTS socios (
            id_s INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            contrasenia TEXT NOT NULL,
            edad INTEGER NOT NULL,
            natalacio INTEGER NOT NULL,
            telefono INTEGER NOT NULL,
            email TEXT NOT NULL,
            )""")
conn.commit()
cursor.close()
conn.close()
#--------------------------------------------------------------#
conn = conectar()
cursor = conn.cursor()
cursor.excute("""CREATE TABLE IF NOT EXISTS actividades (
            id_a INTEGER PRIMARY KEY,
            inscriptos INTEGER FOREIGN KEY,
            deporte INTEGER FOREIGN KEY,
            )""")
conn.commit()
cursor.close()
conn.close()

#-----------------AGREGAR CONTENIDO CRUZANDO DATOS-------------#
conn = conectar()
cursor = conn.cursor()

conn = conectar()
cursor = conn.cursor()
c = 1
d = "Tecladito numerico"
s = 1200
p = 890

cursor.excute("""INSERT INTO productos
            (codigo, descripcion, cantidad, precio)
            VALUES(?,?,?,?)""", (c,d,s,p))

conn.commit()
cursor.close()
conn.close()


cursor.excute("""INSERT INTO actividades
            (deporte, categoria, nombre, apellido, natalicio,)
            SELECT actividades(deportes, categoria,)
            FROM deportes,
            SELECT actividades(nombre, apellido, natalicio,)
            FROM socios,""")
conn.commit()
cursor.close()
conn.close()
