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

PORTAL = """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cultura e Turismo — Portal Municipal</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Rawline',Calibri,sans-serif;background:#f4f4f4;color:#333}
a{color:inherit;text-decoration:none}

/* BARRA GOVBR */
.govbr-bar{background:#1351b4;height:40px;display:flex;align-items:center;padding:0 1.5rem}
.govbr-bar-inner{max-width:1100px;margin:0 auto;width:100%;display:flex;align-items:center;justify-content:space-between}
.govbr-logo{display:flex;align-items:center;gap:8px;color:#fff;font-size:0.85rem;font-weight:600}
.govbr-logo-mark{background:#fff;color:#1351b4;font-weight:900;font-size:13px;padding:2px 7px;border-radius:3px;letter-spacing:0.5px}
.govbr-links{display:flex;gap:1.2rem}
.govbr-links a{color:#fff;font-size:0.75rem;opacity:0.9}
.govbr-links a:hover{opacity:1;text-decoration:underline}

/* HEADER MINISTERIO */
.mtur-header{background:#fff;border-bottom:4px solid #00a300;padding:0}
.mtur-header-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:0.8rem 1.5rem;gap:1rem}
.mtur-brand{display:flex;align-items:center;gap:12px}
.mtur-escudo{width:44px;height:44px;background:#00a300;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:22px;color:#fff}
.mtur-title{line-height:1.2}
.mtur-title strong{display:block;font-size:1rem;color:#1351b4;font-weight:700}
.mtur-title span{font-size:0.75rem;color:#555}
.mtur-search{display:flex;border:1.5px solid #ccc;border-radius:4px;overflow:hidden;max-width:320px;flex:1}
.mtur-search input{flex:1;padding:8px 12px;border:none;font-size:0.9rem;outline:none}
.mtur-search button{background:#1351b4;color:#fff;border:none;padding:8px 14px;cursor:pointer;font-size:13px}

/* NAV */
.mtur-nav{background:#1351b4}
.mtur-nav-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;gap:0;padding:0 1.5rem}
.mtur-nav a{color:#fff;font-size:0.82rem;padding:12px 16px;display:block;border-bottom:3px solid transparent;transition:background 0.2s}
.mtur-nav a:hover,.mtur-nav a.active{background:rgba(255,255,255,0.1);border-bottom-color:#fff}
.mtur-nav .btn-cadastrar{margin-left:auto;background:#00a300;color:#fff;padding:8px 16px;border-radius:4px;font-size:0.82rem;font-weight:700;border:none;cursor:pointer;display:flex;align-items:center;gap:6px}
.mtur-nav .btn-cadastrar:hover{background:#007a00}

/* HERO BANNER */
.hero{background:linear-gradient(135deg,#003366 0%,#1351b4 50%,#00a300 100%);color:#fff;padding:3rem 1.5rem;position:relative;overflow:hidden}
.hero::after{content:'';position:absolute;right:-100px;top:-100px;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,0.05)}
.hero-inner{max-width:1100px;margin:0 auto;position:relative}
.hero-label{font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;background:rgba(255,255,255,0.15);display:inline-block;padding:4px 12px;border-radius:2px;margin-bottom:1rem}
.hero h1{font-size:2rem;font-weight:700;margin-bottom:0.5rem;line-height:1.2}
.hero p{font-size:1rem;opacity:0.85;max-width:540px;line-height:1.6;margin-bottom:1.5rem}
.hero-search{display:flex;max-width:500px;border-radius:4px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.2)}
.hero-search input{flex:1;padding:14px 16px;border:none;font-size:1rem;outline:none}
.hero-search button{background:#00a300;color:#fff;border:none;padding:14px 20px;cursor:pointer;font-weight:700;font-size:0.9rem}

/* BREADCRUMB */
.breadcrumb{background:#fff;border-bottom:1px solid #e0e0e0;padding:8px 1.5rem;font-size:0.78rem;color:#555}
.breadcrumb-inner{max-width:1100px;margin:0 auto}
.breadcrumb span{color:#1351b4}

/* FILTROS */
.filtros-bar{background:#fff;border-bottom:1px solid #e0e0e0;padding:12px 1.5rem}
.filtros-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.filtros-label{font-size:0.78rem;color:#555;margin-right:4px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px}
.chip{background:none;border:1.5px solid #ccc;padding:5px 14px;border-radius:20px;cursor:pointer;font-size:0.8rem;color:#555;transition:all 0.2s}
.chip:hover{border-color:#1351b4;color:#1351b4}
.chip.active{background:#1351b4;border-color:#1351b4;color:#fff}
.chip.active.verde{background:#00a300;border-color:#00a300}

/* STATS */
.stats{background:#f0f4ff;border-bottom:1px solid #d0d8f0;padding:12px 1.5rem}
.stats-inner{max-width:1100px;margin:0 auto;display:flex;gap:2rem;flex-wrap:wrap}
.stat{font-size:0.82rem;color:#444}
.stat strong{color:#1351b4;font-size:1.1rem;margin-right:4px}

/* MAIN */
.main-layout{max-width:1100px;margin:1.5rem auto;padding:0 1.5rem;display:grid;grid-template-columns:220px 1fr;gap:1.5rem}

/* SIDEBAR */
.sidebar{display:flex;flex-direction:column;gap:1rem}
.sidebar-box{background:#fff;border:1px solid #ddd;border-radius:4px;overflow:hidden}
.sidebar-box-title{background:#1351b4;color:#fff;padding:10px 14px;font-size:0.82rem;font-weight:700;text-transform:uppercase;letter-spacing:0.5px}
.sidebar-list{list-style:none}
.sidebar-list li a{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;font-size:0.83rem;color:#333;border-bottom:1px solid #eee;transition:background 0.2s;cursor:pointer}
.sidebar-list li a:hover{background:#f0f4ff;color:#1351b4}
.sidebar-list li a .badge{background:#e8f0fe;color:#1351b4;font-size:0.7rem;padding:2px 8px;border-radius:10px;font-weight:600}

/* CARDS */
.cards-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem}
.cards-header h2{font-size:1rem;font-weight:700;color:#333}
.cards-header span{font-size:0.8rem;color:#666}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem}
.card{background:#fff;border:1px solid #ddd;border-radius:4px;overflow:hidden;transition:box-shadow 0.2s,transform 0.2s;cursor:pointer}
.card:hover{box-shadow:0 4px 16px rgba(0,0,0,0.12);transform:translateY(-2px)}
.card-img{height:130px;display:flex;align-items:center;justify-content:center;font-size:2.8rem;position:relative}
.bg-cultura{background:linear-gradient(135deg,#e8eaf6,#9fa8da)}
.bg-turismo{background:linear-gradient(135deg,#e8f5e9,#66bb6a)}
.bg-gastronomia{background:linear-gradient(135deg,#fff3e0,#ffa726)}
.bg-entretenimento{background:linear-gradient(135deg,#fce4ec,#f48fb1)}
.card-cat-bar{height:4px}
.cat-bar-cultura{background:#1351b4}
.cat-bar-turismo{background:#00a300}
.cat-bar-gastronomia{background:#e65100}
.cat-bar-entretenimento{background:#880e4f}
.card-body{padding:12px 14px}
.card-cat{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;margin-bottom:4px}
.cat-cultura{color:#1351b4}.cat-turismo{color:#00a300}.cat-gastronomia{color:#e65100}.cat-entretenimento{color:#880e4f}
.card-title{font-size:0.95rem;font-weight:700;margin-bottom:5px;color:#1a1a1a;line-height:1.3}
.card-desc{font-size:0.8rem;color:#555;line-height:1.6;margin-bottom:8px}
.card-footer{display:flex;justify-content:space-between;align-items:center;padding-top:8px;border-top:1px solid #eee;font-size:0.75rem;color:#666}
.card-rating{color:#00a300;font-weight:700}
.tag-gratuito{background:#e8f5e9;color:#1b5e20;font-size:0.68rem;padding:2px 8px;border-radius:2px;font-weight:600}
.tag-pago{background:#fff3e0;color:#e65100;font-size:0.68rem;padding:2px 8px;border-radius:2px;font-weight:600}
.empty{text-align:center;padding:3rem;color:#888;grid-column:1/-1;background:#fff;border:1px solid #ddd;border-radius:4px}
.loading{text-align:center;padding:3rem;color:#888;grid-column:1/-1}

/* MODAL */
.modal-bg{position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:200;display:none;align-items:flex-start;justify-content:center;padding:2rem 1rem;overflow-y:auto}
.modal-bg.open{display:flex}
.modal{background:#fff;border-radius:4px;width:100%;max-width:560px;overflow:hidden;margin:auto}
.modal-header{background:#1351b4;color:#fff;padding:1rem 1.5rem;display:flex;align-items:center;justify-content:space-between}
.modal-header h2{font-size:1rem;font-weight:700}
.modal-close{background:none;border:none;color:#fff;font-size:20px;cursor:pointer;line-height:1}
.modal-body{padding:1.5rem}
.form-group{margin-bottom:1rem}
.form-group label{display:block;font-size:0.8rem;font-weight:700;color:#333;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.3px}
.form-group input,.form-group select,.form-group textarea{width:100%;padding:9px 12px;border:1.5px solid #ccc;border-radius:4px;font-size:0.9rem;color:#333;outline:none;transition:border-color 0.2s}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{border-color:#1351b4}
.form-group textarea{min-height:80px;resize:vertical}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.modal-footer{padding:1rem 1.5rem;background:#f4f4f4;border-top:1px solid #ddd;display:flex;gap:8px;justify-content:flex-end}
.btn-primary{background:#1351b4;color:#fff;border:none;padding:10px 20px;border-radius:4px;cursor:pointer;font-size:0.88rem;font-weight:700}
.btn-primary:hover{background:#0c3d8a}
.btn-secondary{background:#fff;color:#333;border:1.5px solid #ccc;padding:10px 16px;border-radius:4px;cursor:pointer;font-size:0.88rem}

/* FOOTER */
.footer{background:#1351b4;color:#fff;padding:2rem 1.5rem;margin-top:2rem}
.footer-inner{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.5rem}
.footer h4{font-size:0.85rem;font-weight:700;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid rgba(255,255,255,0.2);padding-bottom:6px}
.footer ul{list-style:none}
.footer ul li{margin-bottom:5px}
.footer ul li a{color:rgba(255,255,255,0.8);font-size:0.8rem}
.footer ul li a:hover{color:#fff}
.footer-bottom{background:#003d99;padding:10px 1.5rem;text-align:center;font-size:0.75rem;color:rgba(255,255,255,0.7)}

/* TOAST */
.toast{position:fixed;bottom:2rem;right:2rem;background:#00a300;color:#fff;padding:12px 20px;border-radius:4px;opacity:0;transition:opacity 0.3s;pointer-events:none;z-index:300;font-size:0.9rem;box-shadow:0 4px 12px rgba(0,0,0,0.2)}
.toast.show{opacity:1}

@media(max-width:768px){
  .main-layout{grid-template-columns:1fr}
  .sidebar{display:none}
  .form-row{grid-template-columns:1fr}
  .govbr-links{display:none}
}
</style>
</head>
<body>

<!-- BARRA GOV.BR -->
<div class="govbr-bar">
  <div class="govbr-bar-inner">
    <div class="govbr-logo">
      <span class="govbr-logo-mark">GOV.BR</span>
      <span>Portal do Governo</span>
    </div>
    <div class="govbr-links">
      <a href="#">Acesso à Informação</a>
      <a href="#">Participe</a>
      <a href="#">Legislação</a>
      <a href="#">Órgãos do Governo</a>
    </div>
  </div>
</div>

<!-- HEADER -->
<div class="mtur-header">
  <div class="mtur-header-inner">
    <div class="mtur-brand">
      <div class="mtur-escudo">🏛️</div>
      <div class="mtur-title">
        <strong>Secretaria de Cultura e Turismo</strong>
        <span>Prefeitura Municipal de Bauru</span>
      </div>
    </div>
    <div class="mtur-search">
      <input type="text" id="busca-header" placeholder="Buscar serviços..." oninput="renderCards()">
      <button onclick="renderCards()">🔍</button>
    </div>
  </div>
</div>

<!-- NAV -->
<nav class="mtur-nav">
  <div class="mtur-nav-inner">
    <a href="#" class="active">Página Inicial</a>
    <a href="#">Serviços</a>
    <a href="#">Agenda de Eventos</a>
    <a href="#">Acesso à Informação</a>
    <a href="#">Contato</a>
    <button class="btn-cadastrar" onclick="abrirModal()">+ Cadastrar Serviço</button>
  </div>
</nav>

<!-- HERO -->
<div class="hero">
  <div class="hero-inner">
    <div class="hero-label">Portal Oficial</div>
    <h1>Cultura e Turismo em Bauru</h1>
    <p>Encontre os melhores serviços culturais, pontos turísticos, gastronomia e entretenimento da cidade.</p>
    <div class="hero-search">
      <input type="text" id="busca-hero" placeholder="Buscar por nome, local ou categoria..." oninput="syncBusca(this)">
      <button onclick="renderCards()">Buscar</button>
    </div>
  </div>
</div>

<!-- BREADCRUMB -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <span>Página Inicial</span> &rsaquo; <span>Catálogo de Serviços</span>
  </div>
</div>

<!-- STATS -->
<div class="stats">
  <div class="stats-inner" id="stats"></div>
</div>

<!-- FILTROS -->
<div class="filtros-bar">
  <div class="filtros-inner">
    <span class="filtros-label">Filtrar por:</span>
    <button class="chip active" onclick="setFiltro('todos',this)">Todos</button>
    <button class="chip" onclick="setFiltro('cultura',this)">🎭 Cultura</button>
    <button class="chip verde" onclick="setFiltro('turismo',this)">🏛️ Turismo</button>
    <button class="chip" onclick="setFiltro('gastronomia',this)">🍽️ Gastronomia</button>
    <button class="chip" onclick="setFiltro('entretenimento',this)">🎵 Entretenimento</button>
  </div>
</div>

<!-- LAYOUT PRINCIPAL -->
<div class="main-layout">

  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="sidebar-box">
      <div class="sidebar-box-title">Categorias</div>
      <ul class="sidebar-list" id="sidebar-cats"></ul>
    </div>
    <div class="sidebar-box">
      <div class="sidebar-box-title">Informações</div>
      <ul class="sidebar-list">
        <li><a href="#">📋 Como se cadastrar</a></li>
        <li><a href="#">📞 Fale Conosco</a></li>
        <li><a href="#">📍 Mapa da cidade</a></li>
        <li><a href="#">📅 Agenda cultural</a></li>
      </ul>
    </div>
  </aside>

  <!-- CONTEUDO -->
  <main>
    <div class="cards-header">
      <h2 id="section-title">Todos os Serviços</h2>
      <span id="count-label"></span>
    </div>
    <div class="grid" id="grid">
      <div class="loading">Carregando serviços...</div>
    </div>
  </main>

</div>

<!-- FOOTER -->
<footer class="footer">
  <div class="footer-inner">
    <div>
      <h4>Secretaria de Cultura e Turismo</h4>
      <ul>
        <li><a href="#">Sobre a Secretaria</a></li>
        <li><a href="#">Agenda de Eventos</a></li>
        <li><a href="#">Notícias</a></li>
        <li><a href="#">Legislação</a></li>
      </ul>
    </div>
    <div>
      <h4>Serviços</h4>
      <ul>
        <li><a href="#">Cadastro de Prestadores</a></li>
        <li><a href="#">Certidões</a></li>
        <li><a href="#">Habilitações</a></li>
        <li><a href="#">Incentivo Fiscal</a></li>
      </ul>
    </div>
    <div>
      <h4>Acesso à Informação</h4>
      <ul>
        <li><a href="#">Transparência</a></li>
        <li><a href="#">Ouvidoria</a></li>
        <li><a href="#">e-SIC</a></li>
        <li><a href="#">LGPD</a></li>
      </ul>
    </div>
    <div>
      <h4>Contato</h4>
      <ul>
        <li><a href="#">📧 cultura@bauru.sp.gov.br</a></li>
        <li><a href="#">📞 (14) 3104-1234</a></li>
        <li><a href="#">📍 Praça das Cerejeiras, 1-59</a></li>
        <li><a href="#">Bauru - SP, CEP 17040-070</a></li>
      </ul>
    </div>
  </div>
</footer>
<div class="footer-bottom">
  © 2026 Prefeitura Municipal de Bauru — Todos os direitos reservados
</div>

<!-- MODAL CADASTRO -->
<div class="modal-bg" id="modal">
  <div class="modal">
    <div class="modal-header">
      <h2>Cadastrar Novo Serviço</h2>
      <button class="modal-close" onclick="fecharModal()">✕</button>
    </div>
    <div class="modal-body">
      <div class="form-group">
        <label>Nome do Serviço *</label>
        <input id="f-nome" placeholder="Ex: Museu Histórico Municipal">
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Categoria *</label>
          <select id="f-cat">
            <option value="cultura">🎭 Cultura</option>
            <option value="turismo">🏛️ Turismo</option>
            <option value="gastronomia">🍽️ Gastronomia</option>
            <option value="entretenimento">🎵 Entretenimento</option>
          </select>
        </div>
        <div class="form-group">
          <label>Cidade *</label>
          <input id="f-cidade" placeholder="Ex: Bauru, SP">
        </div>
      </div>
      <div class="form-group">
        <label>Descrição *</label>
        <textarea id="f-desc" placeholder="Descreva o serviço oferecido..."></textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Preço</label>
          <input id="f-preco" placeholder="Ex: Gratuito ou R$ 20,00">
        </div>
        <div class="form-group">
          <label>Avaliação (1–5)</label>
          <input id="f-nota" type="number" min="1" max="5" step="0.1" placeholder="4.5">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Horário</label>
          <input id="f-horario" placeholder="Ex: Ter-Dom 9h–17h">
        </div>
        <div class="form-group">
          <label>Contato</label>
          <input id="f-contato" placeholder="Ex: (14) 99999-0000">
        </div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn-secondary" onclick="fecharModal()">Cancelar</button>
      <button class="btn-primary" onclick="salvar()">💾 Salvar Serviço</button>
    </div>
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
    renderStats();
    renderSidebar();
    renderCards();
  }catch(e){
    document.getElementById('grid').innerHTML='<div class="empty">Erro ao carregar. Tente novamente.</div>';
  }
}

function renderStats(){
  const tots={todos:db.length,cultura:0,turismo:0,gastronomia:0,entretenimento:0};
  db.forEach(s=>tots[s.categoria]=(tots[s.categoria]||0)+1);
  document.getElementById('stats').innerHTML=`
    <div class="stat"><strong>${tots.todos}</strong> serviços cadastrados</div>
    <div class="stat"><strong>${tots.cultura||0}</strong> Cultura</div>
    <div class="stat"><strong>${tots.turismo||0}</strong> Turismo</div>
    <div class="stat"><strong>${tots.gastronomia||0}</strong> Gastronomia</div>
    <div class="stat"><strong>${tots.entretenimento||0}</strong> Entretenimento</div>
  `;
}

function renderSidebar(){
  const tots={cultura:0,turismo:0,gastronomia:0,entretenimento:0};
  db.forEach(s=>tots[s.categoria]=(tots[s.categoria]||0)+1);
  document.getElementById('sidebar-cats').innerHTML=Object.entries(CATS).map(([k,v])=>`
    <li><a onclick="setFiltroSidebar('${k}')" style="cursor:pointer">
      ${EMOJIS[k]} ${v} <span class="badge">${tots[k]||0}</span>
    </a></li>
  `).join('');
}

function renderCards(){
  const q=(document.getElementById('busca-hero').value||document.getElementById('busca-header').value||'').toLowerCase();
  const data=db.filter(s=>{
    const mc=filtro==='todos'||s.categoria===filtro;
    const mq=!q||s.nome.toLowerCase().includes(q)||s.cidade.toLowerCase().includes(q)||s.descricao.toLowerCase().includes(q);
    return mc&&mq;
  });
  const titles={todos:'Todos os Serviços',cultura:'Cultura',turismo:'Turismo',gastronomia:'Gastronomia',entretenimento:'Entretenimento'};
  document.getElementById('section-title').textContent=titles[filtro];
  document.getElementById('count-label').textContent=data.length+' resultado'+(data.length!==1?'s':'')+' encontrado'+(data.length!==1?'s':'');
  const grid=document.getElementById('grid');
  if(!data.length){grid.innerHTML='<div class="empty">Nenhum serviço encontrado para este filtro.</div>';return;}
  const gratis=p=>(p||'').toLowerCase().includes('gratu')||p==='0';
  grid.innerHTML=data.map(s=>`
    <div class="card">
      <div class="card-img bg-${s.categoria}">${EMOJIS[s.categoria]||'📍'}</div>
      <div class="card-cat-bar cat-bar-${s.categoria}"></div>
      <div class="card-body">
        <div class="card-cat cat-${s.categoria}">${CATS[s.categoria]||s.categoria}</div>
        <div class="card-title">${s.nome}</div>
        <div class="card-desc">${(s.descricao||'').slice(0,95)}${(s.descricao||'').length>95?'…':''}</div>
        <div class="card-footer">
          <span>📍 ${s.cidade}</span>
          <span class="${gratis(s.preco)?'tag-gratuito':'tag-pago'}">${gratis(s.preco)?'Gratuito':s.preco}</span>
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

function setFiltroSidebar(f){
  filtro=f;
  document.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
  renderCards();
}

function syncBusca(el){
  document.getElementById('busca-header').value=el.value;
  renderCards();
}

function abrirModal(){document.getElementById('modal').classList.add('open')}
function fecharModal(){document.getElementById('modal').classList.remove('open')}

async function salvar(){
  const nome=document.getElementById('f-nome').value.trim();
  const cidade=document.getElementById('f-cidade').value.trim();
  const desc=document.getElementById('f-desc').value.trim();
  if(!nome||!cidade||!desc){toast('Preencha os campos obrigatórios (*)');return;}
  const body={
    nome,cidade,descricao:desc,
    categoria:document.getElementById('f-cat').value,
    preco:document.getElementById('f-preco').value||'Consulte',
    horario:document.getElementById('f-horario').value||'A confirmar',
    contato:document.getElementById('f-contato').value||'—',
    avaliacao:parseFloat(document.getElementById('f-nota').value)||4.0
  };
  await fetch('/api/servicos',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  fecharModal();
  toast('Serviço cadastrado com sucesso!');
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
</html>"""

if __name__ == '__main__':
    app.run(debug=True)