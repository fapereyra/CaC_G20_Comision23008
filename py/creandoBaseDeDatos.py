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
            id_d int (4) NOT NULL,
            nombre varchar (30) NOT NULL,
            categoria int (4) NOT NULL,
            arancel int (5) NOT NULL,
            PRIMARY KEY (`id_d`)
            )""")

conn.commit()
cursor.close()
conn.close()
#--------------------------------------------------------#
conn = conectar()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS socios (
            id_s int (4) NOT NULL,
            nombre varchar (30) NOT NULL,
            apellido varchar (30) NOT NULL,
            contrasenia varchar (30) NOT NULL,
            edad int(3) NOT NULL,
            natalacio date NOT NULL,
            telefono int(12) NOT NULL,
            email varchar (30) NOT NULL,
            PRIMARY KEY (id_s)
            )""")
conn.commit()
cursor.close()
conn.close()
#--------------------------------------------------------------#
conn = conectar()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS actividades (
            id_a int (4) NOT NULL,
            inscriptos int (4) NOT NULL,
            deporte int (4) NOT NULL,
            PRIMARY KEY (id_a),
            FOREIGN KEY (inscriptos) REFERENCES socios (id_s),
            FOREIGN KEY (deporte) REFERENCES deportes (id_d)
            )""")
conn.commit()
cursor.close()
conn.close()

#-----------------AGREGAR CONTENIDO CRUZANDO DATOS-------------#

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

cursor.execute("""INSERT OR REPLACE INTO socios
            (id_s, nombre, apellido, contrasenia, edad, natalacio, telefono, email)
            VALUES(?,?,?,?,?,?,?,?)""", (i, n, a, c, e, na, t, em))
            
cursor.execute("""INSERT OR REPLACE INTO deportes
           (id_d, nombre, categoria, arancel)
            VALUES(?,?,?,?)""", (d, no, ca, ar))
conn.commit()
cursor.close()
conn.close()


conn = conectar()
cursor = conn.cursor()
cursor.execute("""INSERT OR REPLACE INTO actividades
               (inscriptos, deporte)
               VALUES((SELECT id_s FROM socios), (SELECT id_d FROM deportes))""")
conn.commit()
cursor.close()
conn.close()
