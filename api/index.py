from flask import Flask, jsonify, request, render_template_string
from dotenv import load_dotenv
import pymysql
import os

load_dotenv()
app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template_string(PORTAL)

@app.route('/api/servicos', methods=['GET'])
def listar():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM servicos ORDER BY criado_em DESC")
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

PORTAL = '''<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CulturaTur — Cultura e Turismo</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Georgia,serif;background:#F5F0E8;color:#2C2C2A}
.header{background:#1A1A2E;color:#fff;padding:0}
.header-inner{display:flex;align-items:center;justify-content:space-between;padding:0 2rem;height:64px;max-width:1100px;margin:0 auto}
.logo{font-size:1.2rem;font-weight:700;color:#fff}
.logo span{color:#C8922A}
.btn-add{background:#C8922A;color:#1A1A2E;border:none;padding:8px 18px;border-radius:6px;cursor:pointer;font-size:0.85rem;font-weight:700}
.hero{background:linear-gradient(135deg,#1A1A2E,#16213E);color:#fff;padding:3rem 2rem;text-align:center}
.hero h1{font-size:2rem;margin-bottom:0.5rem}
.hero h1 span{color:#C8922A}
.hero p{color:#B0B0C0;margin-bottom:1.5rem}
.search-bar{display:flex;max-width:500px;margin:0 auto;border-radius:8px;overflow:hidden}
.search-bar input{flex:1;padding:12px 16px;border:none;font-size:1rem;font-family:Georgia,serif}
.search-bar button{background:#C8922A;color:#1A1A2E;border:none;padding:12px 20px;cursor:pointer;font-weight:700}
.filters{background:#fff;border-bottom:1px solid #ddd;padding:1rem 2rem;display:flex;gap:8px;flex-wrap:wrap;max-width:1100px;margin:0 auto}
.chip{background:none;border:1.5px solid #ccc;padding:6px 16px;border-radius:20px;cursor:pointer;font-size:0.82rem;font-family:Georgia,serif}
.chip.active{background:#1A1A2E;border-color:#1A1A2E;color:#fff}
.main{max-width:1100px;margin:2rem auto;padding:0 2rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.2rem}
.card{background:#fff;border-radius:12px;border:0.5px solid #ddd;overflow:hidden;cursor:pointer;transition:transform 0.2s,box-shadow 0.2s}
.card:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,0.1)}
.card-img{height:140px;display:flex;align-items:center;justify-content:center;font-size:3rem}
.bg-cultura{background:linear-gradient(135deg,#EEEDFE,#AFA9EC)}
.bg-turismo{background:linear-gradient(135deg,#E1F5EE,#5DCAA5)}
.bg-gastronomia{background:linear-gradient(135deg,#FAECE7,#F0997B)}
.bg-entretenimento{background:linear-gradient(135deg,#FBEAF0,#ED93B1)}
.card-body{padding:1rem}
.card-cat{font-size:0.72rem;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;margin-bottom:4px}
.cat-cultura{color:#533AB7}.cat-turismo{color:#0F8B8D}.cat-gastronomia{color:#993C1D}.cat-entretenimento{color:#993556}
.card-title{font-size:1rem;font-weight:700;margin-bottom:6px;color:#1A1A2E}
.card-desc{font-size:0.83rem;color:#5F5E5A;line-height:1.6;margin-bottom:8px}
.card-meta{display:flex;justify-content:space-between;font-size:0.78rem;color:#5F5E5A;padding-top:8px;border-top:0.5px solid #eee}
.card-rating{color:#C8922A;font-weight:700}
.empty{text-align:center;padding:3rem;color:#5F5E5A;grid-column:1/-1}
.modal-bg{position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:100;display:none;align-items:center;justify-content:center;padding:1rem}
.modal-bg.open{display:flex}
.modal{background:#fff;border-radius:16px;padding:2rem;width:100%;max-width:500px;max-height:90vh;overflow-y:auto;position:relative}
.modal h2{font-size:1.2rem;margin-bottom:1rem}
.close{position:absolute;top:1rem;right:1rem;background:none;border:none;font-size:20px;cursor:pointer}
label{display:block;font-size:0.8rem;font-weight:700;text-transform:uppercase;margin:12px 0 4px}
input,select,textarea{width:100%;padding:10px;border:1.5px solid #ddd;border-radius:8px;font-size:0.95rem;font-family:Georgia,serif}
textarea{min-height:70px;resize:vertical}
.btn-salvar{width:100%;background:#1A1A2E;color:#fff;border:none;padding:12px;border-radius:8px;cursor:pointer;font-size:1rem;font-family:Georgia,serif;margin-top:1rem}
.toast{position:fixed;bottom:2rem;right:2rem;background:#1A1A2E;color:#fff;padding:12px 20px;border-radius:8px;opacity:0;transition:opacity 0.3s;pointer-events:none;z-index:200}
.toast.show{opacity:1}
.loading{text-align:center;padding:3rem;color:#5F5E5A;grid-column:1/-1}
</style>
</head>
<body>
<header class="header">
  <div class="header-inner">
    <div class="logo">🌿 Cultura<span>Tur</span></div>
    <button class="btn-add" onclick="abrirModal()">+ Cadastrar</button>
  </div>
</header>

<div class="hero">
  <h1>Descubra <span>Cultura & Turismo</span></h1>
  <p>Os melhores serviços culturais e turísticos da sua região</p>
  <div class="search-bar">
    <input id="busca" type="text" placeholder="Buscar serviços..." oninput="renderCards()">
    <button onclick="renderCards()">Buscar</button>
  </div>
</div>

<div class="filters" style="justify-content:center">
  <button class="chip active" onclick="setFiltro('todos',this)">Todos</button>
  <button class="chip" onclick="setFiltro('cultura',this)">🎭 Cultura</button>
  <button class="chip" onclick="setFiltro('turismo',this)">🏛️ Turismo</button>
  <button class="chip" onclick="setFiltro('gastronomia',this)">🍽️ Gastronomia</button>
  <button class="chip" onclick="setFiltro('entretenimento',this)">🎵 Entretenimento</button>
</div>

<main class="main">
  <div class="grid" id="grid"><div class="loading">Carregando serviços...</div></div>
</main>

<div class="modal-bg" id="modal">
  <div class="modal">
    <button class="close" onclick="fecharModal()">✕</button>
    <h2>Cadastrar Serviço</h2>
    <label>Nome</label><input id="f-nome" placeholder="Ex: Museu Histórico">
    <label>Categoria</label>
    <select id="f-cat">
      <option value="cultura">🎭 Cultura</option>
      <option value="turismo">🏛️ Turismo</option>
      <option value="gastronomia">🍽️ Gastronomia</option>
      <option value="entretenimento">🎵 Entretenimento</option>
    </select>
    <label>Cidade</label><input id="f-cidade" placeholder="Ex: Bauru, SP">
    <label>Descrição</label><textarea id="f-desc"></textarea>
    <label>Preço</label><input id="f-preco" placeholder="Ex: Gratuito ou R$ 20,00">
    <label>Horário</label><input id="f-horario" placeholder="Ex: Ter-Dom 9h-17h">
    <label>Contato</label><input id="f-contato" placeholder="Ex: (14) 99999-0000">
    <label>Avaliação (1-5)</label><input id="f-nota" type="number" min="1" max="5" step="0.1" placeholder="4.5">
    <button class="btn-salvar" onclick="salvar()">💾 Salvar</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const EMOJIS={cultura:'🎭',turismo:'🏛️',gastronomia:'🍽️',entretenimento:'🎵'};
const CATS={cultura:'Cultura',turismo:'Turismo',gastronomia:'Gastronomia',entretenimento:'Entretenimento'};
let db=[], filtro='todos';

async function carregar(){
  try{
    const r=await fetch('/api/servicos');
    db=await r.json();
    renderCards();
  }catch(e){
    document.getElementById('grid').innerHTML='<div class="empty">Erro ao carregar. Tente novamente.</div>';
  }
}

function renderCards(){
  const q=(document.getElementById('busca').value||'').toLowerCase();
  const data=db.filter(s=>{
    const mc=filtro==='todos'||s.categoria===filtro;
    const mq=!q||s.nome.toLowerCase().includes(q)||s.cidade.toLowerCase().includes(q)||s.descricao.toLowerCase().includes(q);
    return mc&&mq;
  });
  const grid=document.getElementById('grid');
  if(!data.length){grid.innerHTML='<div class="empty">Nenhum serviço encontrado.</div>';return;}
  grid.innerHTML=data.map(s=>`
    <div class="card" onclick="">
      <div class="card-img bg-${s.categoria}">${EMOJIS[s.categoria]||'📍'}</div>
      <div class="card-body">
        <div class="card-cat cat-${s.categoria}">${CATS[s.categoria]||s.categoria}</div>
        <div class="card-title">${s.nome}</div>
        <div class="card-desc">${s.descricao.slice(0,90)}${s.descricao.length>90?'…':''}</div>
        <div class="card-meta">
          <span>📍 ${s.cidade}</span>
          <span class="card-rating">${parseFloat(s.avaliacao).toFixed(1)} ★</span>
        </div>
      </div>
    </div>`).join('');
}

function setFiltro(f,el){
  filtro=f;
  document.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
  renderCards();
}

function abrirModal(){document.getElementById('modal').classList.add('open')}
function fecharModal(){document.getElementById('modal').classList.remove('open')}

async function salvar(){
  const nome=document.getElementById('f-nome').value.trim();
  const cidade=document.getElementById('f-cidade').value.trim();
  const desc=document.getElementById('f-desc').value.trim();
  if(!nome||!cidade||!desc){toast('Preencha nome, cidade e descrição.');return;}
  const body={
    nome, cidade, descricao:desc,
    categoria:document.getElementById('f-cat').value,
    preco:document.getElementById('f-preco').value||'Consulte',
    horario:document.getElementById('f-horario').value||'A confirmar',
    contato:document.getElementById('f-contato').value||'—',
    avaliacao:parseFloat(document.getElementById('f-nota').value)||4.0
  };
  await fetch('/api/servicos',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  fecharModal();
  toast('Serviço cadastrado!');
  carregar();
}

function toast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg;t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),3000);
}

document.getElementById('modal').addEventListener('click',e=>{if(e.target===document.getElementById('modal'))fecharModal()});
carregar();
</script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(debug=True)