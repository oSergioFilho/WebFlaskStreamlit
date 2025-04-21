from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)
DB_PATH = os.path.join(os.getcwd(), 'devices.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            nome TEXT NOT NULL,
            trafego REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/devices', methods=['POST'])
def add_device():
    data = request.get_json() or {}
    for key in ('ip','nome','trafego'):
        if key not in data:
            return jsonify({'error': f'Missing field {key}'}), 400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO devices (ip,nome,trafego) VALUES (?,?,?)',
              (data['ip'], data['nome'], data['trafego']))
    conn.commit()
    conn.close()
    return jsonify({'message':'Dispositivo adicionado'}), 201

@app.route('/devices', methods=['GET'])
def list_devices():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id,ip,nome,trafego FROM devices')
    rows = c.fetchall()
    conn.close()
    devices = [dict(id=r[0], ip=r[1], nome=r[2], trafego=r[3]) for r in rows]
    return jsonify(devices)

@app.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM devices WHERE id=?', (device_id,))
    conn.commit()
    conn.close()
    return jsonify({'message':'Dispositivo removido'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)