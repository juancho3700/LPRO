from collections import defaultdict
import json
from flask import Flask, Response, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from flask_socketio import SocketIO, emit



app = Flask(__name__)
socketio = SocketIO(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['LPRO']
collection = db['LPRO']

#def detectar_cambios_en_db():
 #   while True:
    #    cambios = True  
     #   if cambios:
     #       socketio.emit('actualizar_tablas', namespace='/')    

@app.route('/')
def index():
    usuarios_todos = list(collection.find())
    #usuarios_con_ubicacion = list(collection.find({'Ubicacion': {'$ne': ''}}))
    usuarios_con_ubicacion = defaultdict(list)
    
    for usuario in usuarios_todos:
        ubicacion = usuario.get('Ubicacion', '')
        if ubicacion:
            usuarios_con_ubicacion[ubicacion].append(usuario)
    
    # Convertir defaultdict a dict para evitar problemas con Jinja2
    usuarios_con_ubicacion = dict(usuarios_con_ubicacion)
    return render_template('index.html', usuarios_todos=usuarios_todos, usuarios_con_ubicacion=usuarios_con_ubicacion)


@app.route('/agregar', methods=['POST'])
def agregar_objeto():
    mac = request.form['mac']
    nombre = request.form['nombre']
    collection.insert_one({
        'MAC': mac,
        'Nombre': nombre,
        'Ubicacion': "",
        'ultima_actualizacion_rssi': 0,
        'RSSI': ""
    })
    #emit('actualizar_tablas', namespace='/')
    #return 
    socketio.emit('actualizar_tablas', namespace='/')
    return redirect(url_for('index'))



# Función para generar eventos SSE con los datos de usuarios conectados
def generar_evento_usuarios_conectados():
    # Filtrar usuarios conectados excluyendo aquellos con valores vacíos para los campos de Ubicacion y RSSI
    usuarios = list(collection.find({"$and": [{"Ubicacion": {"$ne": ""}}, {"RSSI": {"$ne": ""}}]}))
    # Convertir ObjectId a cadena en cada documento
    for usuario in usuarios:
        usuario['_id'] = str(usuario['_id'])
    return json.dumps(usuarios)

# Ruta para recibir eventos SSE de usuarios conectados
@app.route('/actualizar_usuarios_conectados')
def actualizar_usuarios_conectados():
    def eventos():
        while True:
            # Generar evento SSE con los datos de usuarios conectados
            yield f"data: {generar_evento_usuarios_conectados()}\n\n"
    return Response(eventos(), content_type='text/event-stream')

# Función para detectar cambios en la base de datos y emitir un evento a través de SocketIO
def detectar_cambios_en_db():
    with app.app_context():
        cambios = True  
        if cambios:
            socketio.emit('actualizar_tablas', namespace='/')    

if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)
