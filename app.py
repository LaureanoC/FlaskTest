from flask import Flask, flash, redirect 
from flask import render_template 
from flaskext.mysql import MySQL
from flask import render_template,request
from datetime import datetime # Para agregar dos fotos por si tienen el mismo nombre


app = Flask(__name__) 
mysql = MySQL() 
app.config['MYSQL_DATABASE_HOST'] ='sql10.freesqldatabase.com' 
app.config['MYSQL_DATABASE_USER']='sql10586711' 
app.config['MYSQL_DATABASE_PASSWORD']='47rsACL2TF' 
app.config['MYSQL_DATABASE_BD']='sql10586711' 
mysql.init_app(app)



@app.route('/')
def index():
    sql = "SELECT * FROM `sql10586711`.empleados;"
    conn = mysql.connect() 
    cursor = conn.cursor() 
    cursor.execute(sql)
    empleados = cursor.fetchall() 
    print (empleados)  
    return render_template('empleados/index.html', empleados  = empleados) #Le enviamos información al template es decir a la UI

@app.route('/create') 
def create(): 
    return render_template('empleados/create.html')


@app.route('/store', methods=['POST']) 
def storage():
  _nombre = request.form['txtNombre'] 
  _correo = request.form['txtCorreo'] 
  _foto = request.files['txtFoto'] 
  sql = "INSERT INTO `sql10586711`.`empleados` (`nombre`, `correo`,`foto`) VALUES (%s, %s, %s);" #Pongo las %s porque son strings, aun no se ejecuta es una variable

  now = datetime.now() 
  tiempo = now.strftime("%Y%H%M%S")
  nuevoNombreFoto = None
  if _foto.filename != '':
    nuevoNombreFoto = tiempo + _foto.filename 
    _foto.save("uploads/" + nuevoNombreFoto)
  datos = (_nombre,_correo,nuevoNombreFoto)

 
  conn = mysql.connect() 
  cursor = conn.cursor() 
  cursor.execute(sql,datos) #Por aca le paso los parametros
  conn.commit()         #Ya funciona!
  return render_template('empleados/index.html')

@app.route('/destroy/<int:id>')
def destroy(id):
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute("DELETE FROM `sql10586711`.`empleados` WHERE id_empleado = %s", (id))
  conn.commit() 
  return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
  conn = mysql.connect() 
  cursor = conn.cursor() 
  cursor.execute("SELECT * FROM `sql10586711`.`empleados` WHERE id_empleado = %s", (id)) 
  empleados = cursor.fetchall() 
  conn.commit() 
  return render_template('empleados/edit.html', empleados = empleados)
  
@app.route('/update', methods = ['POST'])
def update(): 
  _nombre = request.form['txtNombre'] 
  _correo = request.form['txtCorreo'] 
  _foto = request.files['txtFoto'] 
  _apellido = request.form['txtApellido']
  id = request.form['txtID'] 
  sql = "UPDATE `sql10586711`.`empleados` SET `nombre`= %s, apellido = %s, `correo`= %s WHERE id_empleado = %s;" 
  datos = (_nombre,_apellido,_correo,id)

  conn = mysql.connect() 
  cursor = conn.cursor() 

  cursor.execute(sql,datos) 
  conn.commit() 
  return redirect('/')
  

@app.route('/actividades')
def actividades():
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('SELECT e.nombre, e.apellido, e.correo, a.desc_actividad, ea.fecha_hora FROM `sql10586711`.`empleados_actividad` ea RIGHT JOIN sql10586711.actividades a on a.id_actividad = ea.id_actividad RIGHT JOIN sql10586711.empleados e on e.id_empleado = ea.id_empleado')
  actividades = cursor.fetchall()
  conn.commit()
  return render_template('/actividades/actividades.html', actividades=actividades)

if __name__=='__main__':
    app.run(debug=True)


