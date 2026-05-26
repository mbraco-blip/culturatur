from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

app.config['MYSQL_HOST']     = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER']     = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB']       = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/api/servicos', methods=['GET'])
def listar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM servicos ORDER BY criado_em DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    return jsonify([dict(zip(cols, r)) for r in rows])

@app.route('/api/servicos/categoria/<cat>', methods=['GET'])
def por_categoria(cat):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM servicos WHERE categoria=%s", (cat,))
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    return jsonify([dict(zip(cols, r)) for r in rows])

@app.route('/api/servicos', methods=['POST'])
def cadastrar():
    d = request.json
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO servicos
        (nome,categoria,cidade,descricao,preco,horario,contato,avaliacao)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (d['nome'],d['categoria'],d.get('cidade',''),
         d.get('descricao',''),d.get('preco',''),
         d.get('horario',''),d.get('contato',''),
         d.get('avaliacao',4.0)))
    mysql.connection.commit()
    return jsonify({'id': cur.lastrowid, 'msg': 'Cadastrado!'}), 201

@app.route('/api/servicos/<int:id>', methods=['DELETE'])
def excluir(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM servicos WHERE id=%s", (id,))
    mysql.connection.commit()
    return jsonify({'msg': 'Excluído!'})

if __name__ == '__main__':
    app.run(debug=True)