#-- INSTALAR COMPLEMENTO SQL PARA PYTHON --#
import sqlite3

DATABASE = "datos.db"

#-- CREAR BASE DE DATOS --#
def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

conn = conectar()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS deportes (
            id_d INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria INTEGER NOT NULL,
            arancel INTEGER NOT NULL
            )""")
conn.commit()
cursor.close()
conn.close()
#--------------------------------------------------------#
conn = conectar()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS socios (
            id_s INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            contrasenia TEXT NOT NULL,
            edad INTEGER NOT NULL,
            natalacio INTEGER NOT NULL,
            telefono INTEGER NOT NULL,
            email TEXT NOT NULL
            )""")
conn.commit()
cursor.close()
conn.close()
#--------------------------------------------------------------#
conn = conectar()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS actividades (
            id_a INTEGER PRIMARY KEY,
            inscriptos INTEGER FOREGIN KEY,
            deporte INTEGER FOREGIN KEY
            )""")
conn.commit()
cursor.close()
conn.close()

#-----------------AGREGAR CONTENIDO CRUZANDO DATOS-------------#
conn = conectar()
cursor = conn.cursor()
cursor.execute("""INSERT INTO actividades
               (inscriptos, deporte)
               VALUES( (SELECT id_s FROM socios), (SELECT id_d FROM deportes))""")
conn.commit()
cursor.close()
conn.close()

conn = conectar()
cursor = conn.cursor()
i = 1
n = "Fabricio"
a = "Denuncio"
c = "constrasenia"
e = 35
na = 1988
t = 12345678
em = "denunciofabricio@gmail.com"
d = 1
no = "futbol"
ca = 1988
ar = 1000

cursor.execute("""INSERT INTO socios
            (id_s, nombre, apellido, contraseña, edad, natalacio, telefono, email),
            INSERT INTO deportes
            VALUES(?,?,?,?,?,?,?,?)""", (i, n, a, c, e, na, t, em))
            
cursor.execute("""INSERT INTO deportes
           (id_d, nombre, categoria, arancel)
            VALUES(?,?,?,?)""", (d, no, ca, ar))
conn.commit()
cursor.close()
conn.close()