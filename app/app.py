from flask import Flask, render_template, redirect, url_for #importar flask y render templates
import os
import psycopg2


app = Flask(__name__)

def get_db_conection(): #llamar base de datos
    try:
        conn = psycopg2.connect(host='localhost',  #Nombre del host
                               dbname='biblioteca', #Nombre de la Base de datos
                               user =os.environ['username2'], #Variable de entorno del nombre de usuario
                               password=os.environ['password2']) #Variable de entorno de la contraseña
        return conn #execption si la base de dato no es econtrada
    except psycopg2.Error as error:
        print(f"Error al conectar la base de datos: {error}")
        return None

@app.route("/")
def index():#para enlazar htmls tenemos que poner en el href de HTM: {{url_for('nombre_de_la_variable')}}
    conn = get_db_conection()#se llama la variable de la coneccion de base de datos.
    cur = conn.cursor()  #Cursor para llamar a la base de datos
    cur.execute('SELECT * FROM libros;') #Ejecutar comando para consulta de base de datos en SQL
    libros = cur.fetchall() #Nombre de la variable, en esta se guardan los arreglos de los arrgelos
    cur.close() #Cerramos el cursor
    conn.close() #Cerramos el conn
    return render_template('index.html', libros = libros)

@app.route("/acerca-de-nosotros")
def about_us():
    return render_template('sobre_nosotros.html')
    
@app.route("/mas")
def mas():
    return render_template('mas.html')

@app.route('/layout-admin')
def layout_admin():
    return render_template('layout_admin.html')

@app.route("/dasboard")
def dashboard():
    return render_template('dasboard.html')

@app.route("/acutalizacion")
def acutalizacion():
    return render_template('actualizacion.html')


def pagina_no_encontrada(error):
    return render_template('error404.html')

if __name__ == '__main__':
        app.register_error_handler(404, pagina_no_encontrada)
        app.run(debug=True, port=8080)