from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def Hola():
    return '<h1>Hola bienvenidos al sitio web de angel ricardo  </h1>'
@app.route('/plantilla')
def plantilla():
    data={
        'titulo':'Página tituloso',
        'mensaje':'Hola'
    }
    return render_template('pagina1.html',data)
app.run(debug=True)