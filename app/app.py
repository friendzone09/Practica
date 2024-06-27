from flask import Flask, render_template, redirect, url_for, request,  flash #importar flask y render templates
import os
import psycopg2
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf=CSRFProtect() #libreria flask_wtf

#-------------------------------------LLAMADA A LA BASE DE DATOS-----------------------------------------------------

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
    
#----------------------------------FIN DE LA LLAMADA A LA  BASE DE DATOS----------------------------------------------
    
app.secret_key='mysecretkey'

#----------------------------------------INICIO READ---------------------------------------------------------------

@app.route("/")
def index():#para enlazar htmls tenemos que poner en el href de HTM: {{url_for('nombre_de_la_variable')}}
    conn = get_db_conection()#se llama la variable de la conexion de base de datos.
    cur = conn.cursor()  #Cursor para llamar a la base de datos
    cur.execute('SELECT * FROM pais WHERE estado IS true ORDER BY nombre') #Ejecutar comando para consulta de base de datos en SQL
    pais = cur.fetchall() #Nombre de la variable, en esta se guardan los arreglos de los arrgelos
    cur.close() #Cerramos el cursor
    conn.close() #Cerramos el conn
    return render_template('index.html', pais = pais)

#---------------------------------------- FIN READ-------------------------------------------------------------------

#================================================INICIO LISTAR PAISES===========================================

def listar_paises():
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pais WHERE estado IS true ORDER BY nombre ASC')
    pais= cur.fetchall()
    cur.close()
    conn.close()
    return pais

#===================================================FIN LISTAR PAISES===========================================

@app.route("/administrar")
def administrar():
    return render_template('administrar.html')

#------------------------------------INICIO CREATE------------------------------------------------------------------

@app.route("/dasboard/pais/nuevo", methods= ('GET', 'POST'))#Para crear un registro se crea una nueva ruta, esta no la vera el usuario final
def pais_nuevo(): #los metodos "GET" y "POST" sirven para indicar que en esta ruta se ejecutaran estos comando
    if request.method == 'POST': #Si el "reques.method" recibe el metodo POST se ejecuta el IF
        nombre = request.form['nombre'] #Indica una variable, seguido de un request.form y entre corchetes[] poner el nombre del input declarado en el HTML
        
        conn = get_db_conection() #se llama la variable de la conexion de base de datos.
        cur = conn.cursor() #Cursor para llamar la base de datos.
        cur.execute('INSERT INTO pais(nombre)' #el cur ejecuta la consulta SQL [En este caso un INSERT para un registro]
                    'VALUES (%s)', 
                    (nombre,))
        conn.commit()
        cur.close() #se cierra el cursor
        conn.close() #Se cirra la base de datos.
    
        flash('Libro registrado') #Al registrar el dato correctamente se lanza este flash con el mensaje deseado.
        return redirect(url_for('index')) #Al terminar el registro se redirige a la direccion de "index"
    return redirect(url_for('administrar')) #En el caso que un usuario ponga la ruta para el registro de un algo se pone este return para regresarlo a un sitio que si sea accesible para este.
    #Eso es todo para el registro de un algo en python UwU
    #------------------------------FIN CREATE----------------------------------------------------------------------
   
   
#--------------------------------------INICIO UPDATE---------------------------------------------------------------

#Al momento de hacer el editar basicamente se hace lo mismo que con el "Read" podemos copiar y pegar los codigos
#de el read y cambiar unas cosas, como esto:

@app.route("/pais/editar/<string:id_pais>")#Obviamente primero la ruta
def pais_editar(id_pais): #Tambien se edita el "def"
    conn=get_db_conection()
    cur =  conn.cursor() 
    cur.execute('SELECT * FROM pais WHERE id_pais={0}'.format(id_pais))
    pais=cur.fetchall() 
    conn.commit()
    cur.close()#cerrar crusor
    conn.close()#Cerrar conn
    return render_template('pais_editar.html', pais=pais[0])# Y por ultimo, al render template que se dirijirar 
    
@app.route("/dasboard/pais/editar/<string:id>", methods= ['POST'])#Esto es como el de regitrar, se cambia primero la ruta y ahora se agrega la id
def pais_editar_proceso(id): #Aqui igual se pone la id
    if request.method == 'POST': 
        nombre = request.form['nombre'] 
        estado = request.form['estado']
        
        
        conn = get_db_conection()
        cur = conn.cursor() 
        sql ="UPDATE pais SET nombre=%s, estado=%s WHERE id_pais=%s;"#Aqui cambia, ya que se le asigna la consulta SQL
        #a una variable. NOTA: no olvides poner el WHERE porque si no editara TODA la base de datos
        valores =(nombre, estado, id) #Igual aqui, se ejecuta en que valores ira cada modificacion atraves de una variable
        cur.execute(sql,valores) #Se ejecutan las bariables
        conn.commit()
        cur.close() #se cierra el cursor
        conn.close() #Se cirra la base de datos.
    
        flash('Libro editado') #Al editar el dato correctamente se lanza este flash con el mensaje deseado.
        return redirect(url_for('index')) #Al terminar la edicion se redirige a la direccion de "index"
    return redirect(url_for('administrar')) #En el caso que un usuario ponga la ruta para la edicion de un algo se pone este return para regresarlo a un sitio que si sea accesible para este.
    #Eso es todo para la edicion de un algo en python UwU    
    
    #--------------------------------------FIN UPDATE---------------------------------------------------------------

#=======================================INICIO READ EDITORIAL====================================================
@app.route("/editoriales")
def editorial():
    conn = get_db_conection()
    cur = conn.cursor()  
    cur.execute('SELECT editorial.nombre_editorial, pais.nombre ' 
                'FROM public.editorial INNER JOIN public.pais' 
                ' ON editorial.fk_pais = pais.id_pais ORDER BY editorial.nombre_editorial ASC') 
    editorial = cur.fetchall() 
    cur.close() 
    conn.close() 
    return render_template('editorial.html', editorial = editorial)

#============================================FIN READ EDITORIAL====================================================


#=========================================INICIO REGISTRAR EDITORIAL==========================================
@app.route('/editoriales/registrar')
def editorial_registrar():
    return render_template('editorial_registrar.html', paises=listar_paises())

@app.route("/editoriales/registrar/proceso", methods= ('GET', 'POST'))
def editorial_registrar_proceso():
    if request.method == 'POST': 
        nombre_editorial = request.form['nombre_editorial']
        fk_pais = request.form['fk_pais'] 
        
        conn = get_db_conection() 
        cur = conn.cursor() 
        cur.execute('INSERT INTO editorial(nombre_editorial, fk_pais)' 
                    'VALUES (%s, %s)', 
                    (nombre_editorial, fk_pais))
        conn.commit()
        cur.close() 
        conn.close()
    
        flash('Editorial registrada') 
        return redirect(url_for('editorial')) 
    return redirect(url_for('editorial')) 




    
#=========================================FIN REGISTRAR EDITORIAL==========================================



#================================INICIO READ AUTOR============================================================

@app.route('/autor')
def autor():
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT autor.nombre_autor, autor.apellido_autor, pais.nombre'
                ' FROM autor INNER JOIN pais ON autor.fk_pais = pais.id_pais '
                'WHERE visualizacion_autor IS true')
    autores=cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('autores.html', autores=autores)

#=========================================FIN READ AUTOR======================================================

#========================================INICIO REGISTRAR AUTOR===============================================

@app.route('/autor/registrar')
def autor_registrar():
    return render_template('autor_registrar.html', paises=listar_paises())

@app.route("/autor/registrar/proceso", methods= ('GET', 'POST'))
def autor_registrar_proceso():
    if request.method == 'POST': 
        nombre_autor = request.form['nombre_autor']
        apellido_autor = request.form['apellido_autor']
        fk_pais = request.form['fk_pais'] 
        
        conn = get_db_conection() 
        cur = conn.cursor() 
        cur.execute('INSERT INTO autor(nombre_autor, apellido_autor, fk_pais)' 
                    'VALUES (%s, %s, %s)', 
                    (nombre_autor, apellido_autor, fk_pais,))
        conn.commit()
        cur.close() 
        conn.close()
    
        flash('Autor registrada') 
        return redirect(url_for('autor')) 
    return redirect(url_for('autor')) 



#===============================================FIN REGISTRAR AUTOR ==========================================
    

@app.route('/layout-admin')
def layout_admin():
    return render_template('layout_admin.html')

@app.route("/dasboard")
def dashboard():
    return render_template('dasboard.html')

@app.route("/acutalizacion")
def acutalizacion():
    return render_template('actualizacion.html')

#----------------------------------------VISION DE DATOS PAIS---------------------------------------------------------

@app.route("/pais/<string:id_pais>")#Al utilizar estas llaves de abrir y cerrar "<>" declaras una variable
def pais_ver(id_pais):
    conn=get_db_conection()#Conectar a base de datos
    cur =  conn.cursor() #Abrir cursos
    cur.execute('SELECT * FROM pais WHERE id_pais={0}'.format(id_pais))#Consulta SQL
    pais=cur.fetchall() #"pais" es el nombre de el arreglo o lista, en esta se guarda los datos de la consulta SQL
    conn.commit()
    cur.close()#cerrar crusor
    conn.close()#Cerrar conn
    return render_template('pais_ver.html', pais=pais[0])#REGRESA EL TEMPLATE Y SE AGREGA "pais = pais" para la vista en el template

#----------------------------------------FIN VISION DE DATOS PAIS---------------------------------------------------------

#------------------------------------------INICIO ELIMINAR DATOS---------------------------------------------------


@app.route('/eliminar/pais/<string:id_pais>')
def eliminar_pais(id_pais):
    activo=False
    conn = get_db_conection()
    cur = conn.cursor()
    sql = "UPDATE pais SET estado=%s WHERE id_pais=%s"
    valores= (activo,id_pais)
    cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    flash('Se elimino el pais')
    return redirect(url_for('index'))
    
    

#------------------------------------------FIN ELIMINAR DATOS---------------------------------------------------


def pagina_no_encontrada(error):
    return render_template('error404.html')

if __name__ == '__main__':
        csrf.init_app(app)
        app.register_error_handler(404, pagina_no_encontrada)
        app.run(debug=True, port=8080)