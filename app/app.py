from flask import Flask, render_template, redirect, url_for #importar flask y render templates

app = Flask(__name__)

@app.route("/")
def index():#para enlazar htmls tenemos que poner en el href de HTM: {{url_for('nombre_de_la_variable')}}
    return render_template('index.html')

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

def pagina_no_encontrada(error):
    return render_template('error404.html')

if __name__ == '__main__':
        app.register_error_handler(404, pagina_no_encontrada)
        app.run(debug=True, port=8080)