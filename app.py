# Importar librerias necesarias
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/reservas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

CORS(app)  # Habilitar CORS en toda la aplicación
db = SQLAlchemy(app)
ma = Marshmallow(app)


#Estructura de tablas
class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(10), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    lugar_alojamiento = db.Column(db.String(100), nullable=False)
    foto_lugar = db.Column(db.String(100), nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    fecha_salida = db.Column(db.Date, nullable=False)

    def __init__(self, nombre, apellido, dni, telefono, email, lugar_alojamiento,
                 foto_lugar, fecha_ingreso, fecha_salida):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.email = email
        self.lugar_alojamiento = lugar_alojamiento
        self.foto_lugar = foto_lugar
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida

# Creacion de tablas
with app.app_context():
    db.create_all()

# Creo el esquema para Marshmallow
class ReservaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'apellido', 'dni', 'telefono', 'email',
                  'lugar_alojamiento', 'foto_lugar', 'fecha_ingreso', 'fecha_salida')

reserva_schema = ReservaSchema()
reservas_schema = ReservaSchema(many=True)

# Consulta toda la informacion de la tabla reservas
@app.route('/reservas', methods=['GET'])
def get_reservas():
    reservas = Reserva.query.all()
    resultado = []
    for reserva in reservas:
        resultado.append({
            'id': reserva.id,
            'nombre': reserva.nombre,
            'apellido': reserva.apellido,
            'dni': reserva.dni,
            'telefono': reserva.telefono,
            'email': reserva.email,
            'lugar_alojamiento': reserva.lugar_alojamiento,
            'foto_lugar': reserva.foto_lugar,
            'fecha_ingreso': reserva.fecha_ingreso.isoformat(),
            'fecha_salida': reserva.fecha_salida.isoformat()
        })
    return jsonify(resultado)

# Crea una reserva nueva
@app.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.json
    reserva = Reserva(
        nombre=data['nombre'],
        apellido=data['apellido'],
        dni=data['dni'],
        telefono=data['telefono'],
        email=data['email'],
        lugar_alojamiento=data['lugar_alojamiento'],
        foto_lugar=data['foto_lugar'],
        fecha_ingreso=datetime.fromisoformat(data['fecha_ingreso']),
        fecha_salida=datetime.fromisoformat(data['fecha_salida'])
    )
    db.session.add(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva creada exitosamente'})

# Actualiza una reserva existente
@app.route('/reservas/<int:id>', methods=['PUT'])
def update_reserva(id):
    reserva = Reserva.query.get(id)
    if reserva is None:
        return jsonify({'message': 'Reserva no encontrada'}), 404

    data = request.json
    reserva.nombre = data['nombre']
    reserva.apellido = data['apellido']
    reserva.dni = data['dni']
    reserva.telefono = data['telefono']
    reserva.email = data['email']
    reserva.lugar_alojamiento = data['lugar_alojamiento']
    reserva.foto_lugar = data['foto_lugar']
    reserva.fecha_ingreso = datetime.fromisoformat(data['fecha_ingreso'])
    reserva.fecha_salida = datetime.fromisoformat(data['fecha_salida'])

    db.session.commit()
    return jsonify({'message': 'Reserva actualizada exitosamente'})

# Borra una reserva existente
@app.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    reserva = Reserva.query.get(id)
    if reserva is None:
        return jsonify({'message': 'Reserva no encontrada'}), 404

    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva eliminada exitosamente'})

if __name__ == '__main__':
    app.run(debug=True)