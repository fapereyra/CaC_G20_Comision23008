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
            deporte TEXT NOT NULL,
            categoria INTEGER NOT NULL,
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
            edad INTEGER NOT NULL,
            natalacio INTEGER NOT NULL,
            telefono INTEGER NOT NULL,
            deporte TEXT NOT NULL
            )""")
conn.commit()
cursor.close()
conn.close()
#--------------------------------------------------------------#
conn = conectar()
cursor = conn.cursor()
cursor.excute("""CREATE TABLE IF NOT EXISTS actividades (
            id_a INTEGER PRIMARY KEY,
            deporte TEXT NOT NULL,
            categoria TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            natalicio INTEGER NOT NULL,
            )""")
conn.commit()
cursor.close()
conn.close()

#-----------------AGREGAR CONTENIDO CRUZANDO DATOS-------------#
conn = conectar()
cursor = conn.cursor()
cursor.excute("""INSERT INTO actividades
            (deporte, categoria, nombre, apellido, natalicio,)
            SELECT actividades(deportes, categoria,)
            FROM deportes,
            SELECT actividades(nombre, apellido, natalicio,)
            FROM socios,""")
conn.commit()
cursor.close()
conn.close()