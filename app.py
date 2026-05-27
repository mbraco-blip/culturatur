from flask import Flask, jsonify, request
from dotenv import load_dotenv
import pymysql
import os

load_dotenv()
app = Flask(__name__)

def get_db():
    @app.route('/')
def index():
    return jsonify({'status': 'ok', 'msg': 'API CulturaTur no ar!'})
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/servicos', methods=['GET'])
def listar():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM servicos ORDER BY criado_em DESC")
    rows = cur.fetchall()
    db.close()
    return jsonify(rows)

@app.route('/api/servicos/categoria/<cat>', methods=['GET'])
def por_categoria(cat):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM servicos WHERE categoria=%s", (cat,))
    rows = cur.fetchall()
    db.close()
    return jsonify(rows)

@app.route('/api/servicos', methods=['POST'])
def cadastrar():
    d = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute("""INSERT INTO servicos
        (nome,categoria,cidade,descricao,preco,horario,contato,avaliacao)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (d['nome'],d['categoria'],d.get('cidade',''),
         d.get('descricao',''),d.get('preco',''),
         d.get('horario',''),d.get('contato',''),
         d.get('avaliacao',4.0)))
    db.commit()
    db.close()
    return jsonify({'id': cur.lastrowid, 'msg': 'Cadastrado!'}), 201

@app.route('/api/servicos/<int:id>', methods=['DELETE'])
def excluir(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM servicos WHERE id=%s", (id,))
    db.commit()
    db.close()
    return jsonify({'msg': 'Excluído!'})

@app.route('/')
def index():
    return jsonify({'status': 'ok', 'msg': 'API CulturaTur funcionando!'})
if __name__ == '__main__':
    app.run(debug=True)