import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from dotenv import load_dotenv

load_dotenv()

#crear instancia
app = Flask(__name__)
CORS(app)

#Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Lectura(db.Model):
    __tablename__ = 'lecturas'
    id_lectura = db.Column(db.String, primary_key = True)
    modulo = db.Column(db.String)
    hora = db.Column(db.Date)
    temperatura = db.Column(db.Float)
    humedad = db.Column(db.Float)
    co = db.Column(db.Float)
    co2 = db.Column(db.Float)
    amoniaco = db.Column(db.Float)

#Crear las tablas si no existen
with app.app_context():
    db.create_all()

#endpoint para obtener todos los alumnos
@app.route('/lecturas',methods=['GET'])
def get_lecturas():
    lectura = db.session.query(Lectura).where(Lectura.modulo == "M1").order_by(Lectura.hora.desc()).first()
    lista = []
    lista.append({
        'id_lectura': lectura.id_lectura,
        'modulo': lectura.modulo,
        'hora': lectura.hora,
        'temperatura': lectura.temperatura,
        'humedad': lectura.humedad,
        'co': lectura.co,
        'co2': lectura.co2,
        'amoniaco': lectura.amoniaco
    })
    return jsonify(lista)

#endpoint para agregar un nuevo alumno
@app.route('/lecturas', methods=['POST'])
def insert_lectura():
    data = request.get_json()
    nueva_lectura = Lectura(
        id_lectura = data['id_lectura'],
        modulo = data['modulo'],
        hora = data['hora'],
        temperatura = data['temperatura'],
        humedad = data['humedad'],
        co = data['co'],
        co2 = data['co2'],
        amoniaco = data['amoniaco']
    )
    db.session.add(nueva_lectura)
    db.session.commit()
    return jsonify({
        'msg':'Lectura agregado correctamente'
    })

if __name__ == '__main__':
    app.run(debug=True)

