from flask import Flask,render_template,request,redirect,url_for,session
from datetime import datetime
import config
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config["MYSQL_USER"]= config.MYSQL_USER
app.config["MYSQL_DB"]= config.MYSQL_DB
app.config["MYSQL_PASSWORD"]= config.MYSQL_PASSWORD
app.config['SECRET_KEY'] = config.HEX_SEC_KEY

mysql= MySQL(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/armas')
def armas():
    return render_template('tasks.html')

@app.route('/login',methods= ["POST"])
def login():
    email= request.form["email"]
    password= request.form["password"]
    cur=mysql.connection.cursor()
    cur.execute("select * from users where email= %s and password=%s", (email,password))
    user=cur.fetchone()
    cur.close()
    if user is not None:
        session['email'] = email
        session['name'] = user[1]

        return redirect(url_for('tasks'))
    else:
        return render_template('login.html', message="Email o contraseña incorrectos")

@app.route("/tasks",methods=['GET'])
def tasks ():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('tasks.html', tasks = tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
       
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        link=request.form['link']
        # Obtener la fecha y hora actual
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO tasks (nombre, descripcion,link,fecha) VALUES (%s, %s, %s, %s)", (nombre, descripcion, link,fecha_actual))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('tasks'))
    
@app.route('/edit_task/<int:id>', methods=['POST'])
def edit_task(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        link=request.form['link']
        cur.execute("UPDATE tasks SET nombre = %s, descripcion = %s WHERE id = %s", (nombre, descripcion, id, link))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('tasks'))

@app.route('/delete_task', methods=['POST'])
def delete_task():
    cur = mysql.connection.cursor()
    id = request.form['task_id']
    print("Valor de id:", id)
    cur.execute("DELETE FROM tasks WHERE id = %s", (id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('tasks'))

nombre = "Cristian Jesús Balam Ciime"
edad = "19 Años"
email = "cristian.balam.cime@gmail.com"
ubi = "Progreso, Yucatán, México"


@app.route("/personal")
def personal():
  return render_template("personal.html", nombre=nombre, edad=edad, email=email, ubi=ubi)

@app.route("/habilidades")
def habilidades():
  return render_template("habilidades.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
  if request.method == "GET":
    return render_template("contacto.html")
  else:
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]
    # Procesar la información del formulario
    return render_template("contacto.html", success=True, name=name, email=email, message=message)
  



if __name__ =='__main__':
    app.run(debug=True)