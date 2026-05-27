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

@app.route('/api/servicos/<int:id>', methods=['PUT'])
def editar(id):
    d = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute("""UPDATE servicos SET nome=%s,categoria=%s,cidade=%s,
        descricao=%s,preco=%s,horario=%s,contato=%s,avaliacao=%s WHERE id=%s""",
        (d['nome'],d['categoria'],d.get('cidade',''),d.get('descricao',''),
         d.get('preco',''),d.get('horario',''),d.get('contato',''),
         d.get('avaliacao',4.0),id))
    db.commit()
    db.close()
    return jsonify({'msg': 'Atualizado!'})

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
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Secretaria de Cultura e Turismo — Prefeitura de Bauru</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Raleway',sans-serif;background:#f4f4f4;color:#1b1b1b;font-size:16px}
a{text-decoration:none;color:inherit}
img{max-width:100%}
ul{list-style:none}
button{cursor:pointer;font-family:'Raleway',sans-serif}

/* ── ACESSIBILIDADE ── */
.skip-links{position:absolute;top:-999px;left:0;z-index:9999}
.skip-links a{background:#1351b4;color:#fff;padding:8px 16px;font-size:14px;font-weight:600}
.skip-links a:focus{top:0;position:relative}

/* ── BARRA GOVBR ── */
.govbr-bar{background:#071d41;height:40px;display:flex;align-items:center}
.govbr-bar-inner{max-width:1200px;margin:0 auto;width:100%;padding:0 1rem;display:flex;align-items:center;justify-content:space-between}
.govbr-logo{display:flex;align-items:center;gap:10px}
.govbr-badge{background:#fff;color:#071d41;font-weight:700;font-size:12px;padding:3px 8px;border-radius:2px;letter-spacing:.5px}
.govbr-bar-links{display:flex;gap:1.5rem}
.govbr-bar-links a{color:rgba(255,255,255,.85);font-size:12px;font-weight:500}
.govbr-bar-links a:hover{color:#fff;text-decoration:underline}

/* ── HEADER ── */
.site-header{background:#fff;border-bottom:3px solid #1351b4}
.site-header-inner{max-width:1200px;margin:0 auto;padding:.8rem 1rem;display:flex;align-items:center;justify-content:space-between;gap:1rem}
.brand{display:flex;align-items:center;gap:14px}
.brand-icon{width:52px;height:52px;background:#1351b4;border-radius:4px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:26px;flex-shrink:0}
.brand-text strong{display:block;font-size:1.1rem;color:#1351b4;font-weight:700;line-height:1.2}
.brand-text span{font-size:.8rem;color:#555;font-weight:500}
.header-right{display:flex;align-items:center;gap:12px}
.header-search{display:flex;border:1.5px solid #888;border-radius:100px;overflow:hidden;height:38px}
.header-search input{padding:0 14px;border:none;font-size:.9rem;width:240px;outline:none;font-family:'Raleway',sans-serif;background:transparent}
.header-search button{background:#1351b4;color:#fff;border:none;padding:0 14px;font-size:14px}
.header-search button:hover{background:#0c3d8a}
.btn-acessar{background:#1351b4;color:#fff;border:none;padding:8px 16px;border-radius:100px;font-size:.82rem;font-weight:600;display:flex;align-items:center;gap:6px}
.btn-acessar:hover{background:#0c3d8a}

/* ── NAVBAR ── */
.navbar{background:#1351b4;position:relative}
.navbar-inner{max-width:1200px;margin:0 auto;padding:0 1rem;display:flex;align-items:stretch}
.nav-item{position:relative}
.nav-item>a,.nav-item>button{color:#fff;font-size:.85rem;font-weight:600;padding:14px 16px;display:flex;align-items:center;gap:5px;background:none;border:none;border-bottom:3px solid transparent;transition:background .2s,border-color .2s;white-space:nowrap}
.nav-item>a:hover,.nav-item>button:hover,.nav-item.open>a,.nav-item.open>button{background:rgba(255,255,255,.12);border-bottom-color:#fff}
.nav-item>a.active{border-bottom-color:#00a300}
.nav-arrow{font-size:10px;transition:transform .2s}
.nav-item.open .nav-arrow{transform:rotate(180deg)}
.dropdown{display:none;position:absolute;top:100%;left:0;background:#fff;border-top:3px solid #00a300;border:1px solid #ddd;border-top:3px solid #00a300;min-width:220px;z-index:500;box-shadow:0 4px 16px rgba(0,0,0,.15)}
.nav-item.open .dropdown{display:block}
.dropdown li a{display:block;padding:10px 16px;font-size:.83rem;color:#1b1b1b;border-bottom:1px solid #f0f0f0;transition:background .15s}
.dropdown li a:hover{background:#f0f4ff;color:#1351b4}
.dropdown-group{padding:8px 0 4px;border-top:1px solid #eee}
.dropdown-group-title{font-size:.72rem;font-weight:700;color:#888;text-transform:uppercase;letter-spacing:.7px;padding:4px 16px 2px}
.nav-mobile-btn{display:none;background:none;border:none;color:#fff;font-size:24px;padding:10px}

/* ── BREADCRUMB ── */
.breadcrumb{background:#f8f8f8;border-bottom:1px solid #e0e0e0;padding:8px 1rem;font-size:.78rem}
.breadcrumb-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:6px;color:#555}
.breadcrumb a{color:#1351b4}
.breadcrumb a:hover{text-decoration:underline}
.breadcrumb .sep{color:#999}

/* ── HERO / BANNER ── */
.hero{background:linear-gradient(135deg,#071d41 0%,#1351b4 60%,#00a300 100%);padding:3rem 1rem;color:#fff;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;right:-120px;top:-120px;width:480px;height:480px;border-radius:50%;background:rgba(255,255,255,.04)}
.hero-inner{max-width:1200px;margin:0 auto;position:relative}
.hero-tag{display:inline-block;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);color:#fff;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;padding:4px 12px;border-radius:2px;margin-bottom:1rem}
.hero h1{font-size:2rem;font-weight:700;margin-bottom:.6rem;line-height:1.2}
.hero p{font-size:1rem;opacity:.85;max-width:560px;line-height:1.7;margin-bottom:1.5rem}
.hero-busca{display:flex;max-width:520px;border-radius:4px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.25)}
.hero-busca input{flex:1;padding:14px 18px;border:none;font-size:1rem;font-family:'Raleway',sans-serif;outline:none}
.hero-busca button{background:#00a300;color:#fff;border:none;padding:14px 22px;font-size:.9rem;font-weight:700;transition:background .2s}
.hero-busca button:hover{background:#007a00}
.hero-tags{margin-top:1rem;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.hero-tags span{font-size:.75rem;opacity:.7}
.hero-tags a{font-size:.75rem;background:rgba(255,255,255,.15);color:#fff;padding:3px 10px;border-radius:100px;border:1px solid rgba(255,255,255,.25)}
.hero-tags a:hover{background:rgba(255,255,255,.25)}

/* ── DESTAQUES RÁPIDOS ── */
.destaques{background:#fff;border-bottom:1px solid #e0e0e0}
.destaques-inner{max-width:1200px;margin:0 auto;padding:0 1rem;display:flex}
.destaque-item{flex:1;display:flex;align-items:center;gap:10px;padding:14px 16px;border-right:1px solid #eee;color:#1b1b1b;font-size:.83rem;font-weight:600;transition:background .2s}
.destaque-item:last-child{border-right:none}
.destaque-item:hover{background:#f0f4ff;color:#1351b4}
.destaque-item .icon{font-size:20px;flex-shrink:0}

/* ── LAYOUT PRINCIPAL ── */
.main-wrap{max-width:1200px;margin:1.5rem auto;padding:0 1rem;display:grid;grid-template-columns:260px 1fr;gap:1.5rem}

/* ── SIDEBAR ── */
.sidebar{display:flex;flex-direction:column;gap:1rem}
.sidebar-box{background:#fff;border:1px solid #ddd;border-radius:2px;overflow:hidden}
.sidebar-box-hd{background:#1351b4;color:#fff;padding:10px 14px;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.sidebar-box-hd.verde{background:#00a300}
.sidebar-nav li a,.sidebar-nav li button{display:flex;align-items:center;justify-content:space-between;width:100%;padding:10px 14px;font-size:.83rem;color:#1b1b1b;border-bottom:1px solid #f0f0f0;background:none;border-left:none;border-right:none;border-top:none;text-align:left;transition:background .15s,color .15s}
.sidebar-nav li a:hover,.sidebar-nav li button:hover{background:#f0f4ff;color:#1351b4}
.sidebar-nav li a.active{background:#e8f0fe;color:#1351b4;font-weight:600;border-left:3px solid #1351b4}
.sidebar-badge{background:#e8f0fe;color:#1351b4;font-size:.7rem;padding:2px 8px;border-radius:100px;font-weight:700}
.sidebar-badge.verde{background:#e8f5e9;color:#1b5e20}
.sidebar-filter label{display:flex;align-items:center;gap:8px;padding:8px 14px;font-size:.82rem;color:#333;cursor:pointer;border-bottom:1px solid #f5f5f5}
.sidebar-filter label:hover{background:#f9f9f9}
.sidebar-filter input[type=checkbox]{accent-color:#1351b4;width:15px;height:15px}
.sidebar-filter input[type=range]{width:100%;accent-color:#1351b4;margin:4px 0}
.sidebar-filter .range-row{padding:8px 14px;font-size:.8rem;color:#555}
.sidebar-filter .range-row span{color:#1351b4;font-weight:700}

/* ── AREA CONTEUDO ── */
.content-area{}
.content-toolbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;flex-wrap:wrap;gap:8px}
.content-title{font-size:1.1rem;font-weight:700;color:#1b1b1b}
.content-subtitle{font-size:.8rem;color:#666;margin-top:2px}
.toolbar-right{display:flex;align-items:center;gap:8px}
.btn-view{background:#fff;border:1px solid #ccc;padding:6px 10px;border-radius:2px;font-size:13px;color:#555;display:flex;align-items:center;gap:4px}
.btn-view.active{background:#1351b4;border-color:#1351b4;color:#fff}
.btn-ordenar{background:#fff;border:1px solid #ccc;padding:6px 12px;border-radius:2px;font-size:.8rem;color:#333}
.btn-cadastrar{background:#00a300;color:#fff;border:none;padding:8px 16px;border-radius:2px;font-size:.82rem;font-weight:700;display:flex;align-items:center;gap:6px}
.btn-cadastrar:hover{background:#007a00}

/* ── FILTROS CHIPS ── */
.chips-bar{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:1rem}
.chip{background:#fff;border:1.5px solid #ccc;padding:5px 14px;border-radius:100px;font-size:.78rem;color:#555;font-family:'Raleway',sans-serif;transition:all .2s}
.chip:hover{border-color:#1351b4;color:#1351b4}
.chip.active{background:#1351b4;border-color:#1351b4;color:#fff;font-weight:600}

/* ── CARDS GRADE ── */
.cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1rem}
.card{background:#fff;border:1px solid #ddd;border-radius:2px;overflow:hidden;transition:box-shadow .2s,transform .2s;display:flex;flex-direction:column}
.card:hover{box-shadow:0 4px 18px rgba(0,0,0,.12);transform:translateY(-2px)}
.card-thumb{height:130px;display:flex;align-items:center;justify-content:center;font-size:2.8rem;position:relative;flex-shrink:0}
.bg-cultura{background:linear-gradient(135deg,#e8eaf6,#9fa8da)}
.bg-turismo{background:linear-gradient(135deg,#e8f5e9,#66bb6a)}
.bg-gastronomia{background:linear-gradient(135deg,#fff3e0,#ffb74d)}
.bg-entretenimento{background:linear-gradient(135deg,#fce4ec,#f48fb1)}
.card-stripe{height:4px}
.stripe-cultura{background:#1351b4}.stripe-turismo{background:#00a300}.stripe-gastronomia{background:#e65100}.stripe-entretenimento{background:#880e4f}
.card-body{padding:12px 14px;flex:1;display:flex;flex-direction:column}
.card-cat{font-size:.68rem;text-transform:uppercase;letter-spacing:.8px;font-weight:700;margin-bottom:4px}
.cat-cultura{color:#1351b4}.cat-turismo{color:#00a300}.cat-gastronomia{color:#e65100}.cat-entretenimento{color:#880e4f}
.card-title{font-size:.92rem;font-weight:700;margin-bottom:6px;color:#1b1b1b;line-height:1.3}
.card-desc{font-size:.78rem;color:#555;line-height:1.6;margin-bottom:auto}
.card-meta{margin-top:10px;padding-top:8px;border-top:1px solid #eee;display:flex;justify-content:space-between;align-items:center;font-size:.75rem;color:#666;flex-wrap:wrap;gap:4px}
.card-local{display:flex;align-items:center;gap:3px}
.card-rating{color:#00a300;font-weight:700}
.tag{font-size:.68rem;padding:2px 8px;border-radius:2px;font-weight:600}
.tag-gratis{background:#e8f5e9;color:#1b5e20}
.tag-pago{background:#fff3e0;color:#e65100}
.card-actions{padding:8px 14px;border-top:1px solid #eee;display:flex;gap:6px}
.btn-sm{font-size:.75rem;padding:5px 10px;border-radius:2px;border:1px solid #ccc;background:#fff;color:#333;display:flex;align-items:center;gap:4px}
.btn-sm:hover{background:#f0f0f0}
.btn-sm.azul{background:#1351b4;color:#fff;border-color:#1351b4}
.btn-sm.azul:hover{background:#0c3d8a}
.btn-sm.vermelho{background:#fff;color:#c0392b;border-color:#e0a0a0}
.btn-sm.vermelho:hover{background:#fdf0f0}

/* ── LISTA VIEW ── */
.cards-list{display:flex;flex-direction:column;gap:.8rem}
.card-list-item{background:#fff;border:1px solid #ddd;border-radius:2px;display:flex;overflow:hidden;transition:box-shadow .2s}
.card-list-item:hover{box-shadow:0 2px 12px rgba(0,0,0,.1)}
.card-list-thumb{width:100px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:2.2rem}
.card-list-stripe{width:4px;flex-shrink:0}
.card-list-body{flex:1;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;gap:1rem}
.card-list-info{flex:1}
.card-list-actions{display:flex;gap:6px;flex-shrink:0}

/* ── PAGINACAO ── */
.paginacao{display:flex;align-items:center;justify-content:center;gap:4px;margin-top:1.5rem}
.pag-btn{background:#fff;border:1px solid #ddd;width:36px;height:36px;display:flex;align-items:center;justify-content:center;font-size:.83rem;color:#1351b4;border-radius:2px;transition:background .2s}
.pag-btn:hover{background:#f0f4ff}
.pag-btn.active{background:#1351b4;color:#fff;border-color:#1351b4}
.pag-btn.disabled{color:#ccc;pointer-events:none}

/* ── SECOES EXTRAS ── */
.section-extra{background:#fff;border:1px solid #ddd;border-radius:2px;padding:1.2rem;margin-top:1rem}
.section-extra h3{font-size:.9rem;font-weight:700;color:#1351b4;margin-bottom:1rem;padding-bottom:6px;border-bottom:2px solid #e8f0fe}
.noticias-list li{padding:8px 0;border-bottom:1px solid #f0f0f0;font-size:.83rem}
.noticias-list li:last-child{border-bottom:none}
.noticias-list a{color:#1351b4;font-weight:600;display:block;margin-bottom:2px}
.noticias-list a:hover{text-decoration:underline}
.noticias-list .data{font-size:.72rem;color:#888}
.agenda-list li{padding:8px 0;border-bottom:1px solid #f0f0f0;font-size:.83rem;display:flex;gap:10px;align-items:flex-start}
.agenda-list li:last-child{border-bottom:none}
.agenda-data{background:#1351b4;color:#fff;padding:4px 8px;border-radius:2px;text-align:center;min-width:44px;font-size:.72rem;font-weight:700;flex-shrink:0}
.agenda-data .dia{font-size:1.1rem;display:block;line-height:1}

/* ── MODAL ── */
.modal-bg{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:900;display:none;align-items:flex-start;justify-content:center;padding:2rem 1rem;overflow-y:auto}
.modal-bg.open{display:flex}
.modal{background:#fff;border-radius:2px;width:100%;max-width:600px;margin:auto;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.25)}
.modal-hd{background:#1351b4;color:#fff;padding:1rem 1.5rem;display:flex;align-items:center;justify-content:space-between}
.modal-hd h2{font-size:1rem;font-weight:700}
.modal-close{background:none;border:none;color:#fff;font-size:22px;line-height:1;padding:0 4px}
.modal-body{padding:1.5rem}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.form-group{margin-bottom:1rem}
.form-group label{display:block;font-size:.78rem;font-weight:700;color:#333;text-transform:uppercase;letter-spacing:.3px;margin-bottom:5px}
.form-group input,.form-group select,.form-group textarea{width:100%;padding:9px 12px;border:1.5px solid #ccc;border-radius:2px;font-size:.9rem;font-family:'Raleway',sans-serif;color:#1b1b1b;outline:none;transition:border-color .2s}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{border-color:#1351b4}
.form-group textarea{min-height:80px;resize:vertical}
.form-group .hint{font-size:.72rem;color:#888;margin-top:3px}
.modal-ft{padding:1rem 1.5rem;background:#f8f8f8;border-top:1px solid #ddd;display:flex;gap:8px;justify-content:flex-end}
.btn-primary{background:#1351b4;color:#fff;border:none;padding:10px 22px;border-radius:2px;font-size:.88rem;font-weight:700;font-family:'Raleway',sans-serif}
.btn-primary:hover{background:#0c3d8a}
.btn-secondary{background:#fff;color:#333;border:1.5px solid #ccc;padding:10px 16px;border-radius:2px;font-size:.88rem;font-family:'Raleway',sans-serif}
.btn-secondary:hover{background:#f0f0f0}
.btn-danger{background:#c0392b;color:#fff;border:none;padding:10px 16px;border-radius:2px;font-size:.88rem;font-family:'Raleway',sans-serif}

/* ── MODAL DETALHE ── */
.detalhe-hero{height:180px;display:flex;align-items:center;justify-content:center;font-size:4rem}
.detalhe-info{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin:1rem 0}
.detalhe-row{font-size:.85rem;padding:6px 0;border-bottom:1px solid #f0f0f0}
.detalhe-row strong{color:#555;font-size:.72rem;text-transform:uppercase;display:block;margin-bottom:2px}

/* ── FOOTER ── */
.site-footer{background:#071d41;color:#fff;margin-top:2rem}
.footer-top{max-width:1200px;margin:0 auto;padding:2rem 1rem;display:grid;grid-template-columns:repeat(4,1fr);gap:2rem}
.footer-col h4{font-size:.82rem;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:.8rem;padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,.15)}
.footer-col ul li{margin-bottom:5px}
.footer-col ul li a{color:rgba(255,255,255,.75);font-size:.78rem;transition:color .2s}
.footer-col ul li a:hover{color:#fff;text-decoration:underline}
.footer-mid{background:#1351b4;padding:.8rem 1rem}
.footer-mid-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.5rem}
.footer-mid-inner a{color:rgba(255,255,255,.85);font-size:.78rem}
.footer-mid-inner a:hover{color:#fff;text-decoration:underline}
.footer-bottom{background:#040f21;padding:.8rem 1rem;text-align:center;font-size:.75rem;color:rgba(255,255,255,.5)}

/* ── TOAST ── */
.toast{position:fixed;bottom:1.5rem;right:1.5rem;padding:12px 20px;border-radius:2px;color:#fff;font-size:.88rem;font-weight:600;opacity:0;transition:opacity .3s;pointer-events:none;z-index:999;box-shadow:0 4px 16px rgba(0,0,0,.25)}
.toast.ok{background:#00a300}
.toast.erro{background:#c0392b}
.toast.show{opacity:1}

/* ── STATS BAR ── */
.stats-bar{background:#e8f0fe;border-bottom:1px solid #c5d5f5;padding:.6rem 1rem}
.stats-bar-inner{max-width:1200px;margin:0 auto;display:flex;gap:2rem;flex-wrap:wrap;font-size:.8rem;color:#1351b4}
.stats-bar strong{font-weight:700;font-size:.95rem}

/* ── CONFIRMACAO ── */
.confirm-box{background:#fff3cd;border:1px solid #ffc107;border-radius:2px;padding:1rem 1.5rem;margin-bottom:1rem;font-size:.88rem}

/* ── EMPTY ── */
.empty-state{background:#fff;border:1px solid #ddd;padding:3rem;text-align:center;color:#888;grid-column:1/-1}
.empty-state .big{font-size:3rem;margin-bottom:.5rem}

/* ── RESPONSIVO ── */
@media(max-width:900px){
  .main-wrap{grid-template-columns:1fr}
  .sidebar{display:none}
  .footer-top{grid-template-columns:1fr 1fr}
  .detalhe-info{grid-template-columns:1fr}
}
@media(max-width:600px){
  .hero h1{font-size:1.5rem}
  .destaques{display:none}
  .govbr-bar-links{display:none}
  .form-row{grid-template-columns:1fr}
  .footer-top{grid-template-columns:1fr}
  .header-search{display:none}
}
</style>
</head>
<body>

<div class="skip-links">
  <a href="#conteudo">Ir para o conteúdo</a>
  <a href="#nav-principal">Ir para o menu</a>
  <a href="#rodape">Ir para o rodapé</a>
</div>

<!-- BARRA GOV -->
<div class="govbr-bar" role="banner">
  <div class="govbr-bar-inner">
    <div class="govbr-logo">
      <span class="govbr-badge">GOV.BR</span>
      <span style="color:rgba(255,255,255,.7);font-size:12px;margin-left:4px">Prefeitura Municipal de Bauru</span>
    </div>
    <div class="govbr-bar-links">
      <a href="#">Acesso à Informação</a>
      <a href="#">Participe</a>
      <a href="#">Legislação</a>
      <a href="#">Canais</a>
    </div>
  </div>
</div>

<!-- HEADER -->
<header class="site-header">
  <div class="site-header-inner">
    <div class="brand">
      <div class="brand-icon">🏛️</div>
      <div class="brand-text">
        <strong>Secretaria de Cultura e Turismo</strong>
        <span>Prefeitura Municipal de Bauru — SP</span>
      </div>
    </div>
    <div class="header-right">
      <div class="header-search">
        <input type="text" id="hbusca" placeholder="O que você procura?" oninput="syncBusca(this.value)">
        <button onclick="renderCards()" title="Buscar">🔍</button>
      </div>
      <button class="btn-acessar" onclick="abrirModal()">+ Cadastrar Serviço</button>
    </div>
  </div>
</header>

<!-- NAVBAR -->
<nav class="navbar" id="nav-principal" role="navigation" aria-label="Menu principal">
  <div class="navbar-inner">
    <div class="nav-item">
      <a href="#" class="active">Página Inicial</a>
    </div>
    <div class="nav-item" id="nav-servicos">
      <button onclick="toggleNav('nav-servicos')">Serviços <span class="nav-arrow">▾</span></button>
      <ul class="dropdown">
        <li><a href="#" onclick="setFiltro('todos');return false">Todos os Serviços</a></li>
        <li><a href="#" onclick="setFiltro('cultura');return false">🎭 Cultura</a></li>
        <li><a href="#" onclick="setFiltro('turismo');return false">🏛️ Turismo</a></li>
        <li><a href="#" onclick="setFiltro('gastronomia');return false">🍽️ Gastronomia</a></li>
        <li><a href="#" onclick="setFiltro('entretenimento');return false">🎵 Entretenimento</a></li>
        <div class="dropdown-group"><div class="dropdown-group-title">Ações</div></div>
        <li><a href="#" onclick="abrirModal();return false">+ Cadastrar Serviço</a></li>
      </ul>
    </div>
    <div class="nav-item" id="nav-assuntos">
      <button onclick="toggleNav('nav-assuntos')">Assuntos <span class="nav-arrow">▾</span></button>
      <ul class="dropdown">
        <li><a href="#">Notícias</a></li>
        <li><a href="#">Campanhas</a></li>
        <li><a href="#">Agenda de Eventos</a></li>
        <li><a href="#">Dados e Estatísticas</a></li>
        <li><a href="#">Calendário Cultural</a></li>
      </ul>
    </div>
    <div class="nav-item" id="nav-info">
      <button onclick="toggleNav('nav-info')">Acesso à Informação <span class="nav-arrow">▾</span></button>
      <ul class="dropdown">
        <div class="dropdown-group"><div class="dropdown-group-title">Institucional</div></div>
        <li><a href="#">Sobre a Secretaria</a></li>
        <li><a href="#">Organograma</a></li>
        <li><a href="#">Competências</a></li>
        <div class="dropdown-group"><div class="dropdown-group-title">Transparência</div></div>
        <li><a href="#">Receitas e Despesas</a></li>
        <li><a href="#">Licitações e Contratos</a></li>
        <li><a href="#">Convênios</a></li>
        <div class="dropdown-group"><div class="dropdown-group-title">Cidadão</div></div>
        <li><a href="#">Ouvidoria</a></li>
        <li><a href="#">e-SIC</a></li>
        <li><a href="#">LGPD</a></li>
      </ul>
    </div>
    <div class="nav-item" id="nav-comp">
      <button onclick="toggleNav('nav-comp')">Composição <span class="nav-arrow">▾</span></button>
      <ul class="dropdown">
        <li><a href="#">Gabinete do Secretário</a></li>
        <li><a href="#">Departamento de Cultura</a></li>
        <li><a href="#">Departamento de Turismo</a></li>
        <li><a href="#">Conselho Municipal de Turismo</a></li>
        <li><a href="#">Conselho Municipal de Cultura</a></li>
      </ul>
    </div>
    <div class="nav-item">
      <a href="#">Contato</a>
    </div>
  </div>
</nav>

<!-- BREADCRUMB -->
<div class="breadcrumb">
  <div class="breadcrumb-inner">
    <a href="#">Início</a><span class="sep">›</span>
    <span id="bc-current">Catálogo de Serviços</span>
  </div>
</div>

<!-- HERO -->
<section class="hero">
  <div class="hero-inner">
    <div class="hero-tag">Portal Oficial</div>
    <h1>Cultura e Turismo em Bauru</h1>
    <p>Encontre serviços culturais, pontos turísticos, gastronomia e entretenimento. Cadastre e divulgue seu espaço.</p>
    <div class="hero-busca">
      <input type="text" id="hero-busca" placeholder="Buscar serviços, locais, categorias..." oninput="syncBusca(this.value)">
      <button onclick="renderCards()">Buscar</button>
    </div>
    <div class="hero-tags">
      <span>Mais buscados:</span>
      <a href="#" onclick="setTermoBusca('museu');return false">Museu</a>
      <a href="#" onclick="setTermoBusca('parque');return false">Parque</a>
      <a href="#" onclick="setTermoBusca('gastronomia');return false">Gastronomia</a>
      <a href="#" onclick="setTermoBusca('teatro');return false">Teatro</a>
      <a href="#" onclick="setTermoBusca('gratuito');return false">Gratuito</a>
    </div>
  </div>
</section>

<!-- DESTAQUES -->
<div class="destaques">
  <div class="destaques-inner">
    <a href="#" class="destaque-item" onclick="setFiltro('cultura');return false"><span class="icon">🎭</span> Cultura</a>
    <a href="#" class="destaque-item" onclick="setFiltro('turismo');return false"><span class="icon">🏛️</span> Turismo</a>
    <a href="#" class="destaque-item" onclick="setFiltro('gastronomia');return false"><span class="icon">🍽️</span> Gastronomia</a>
    <a href="#" class="destaque-item" onclick="setFiltro('entretenimento');return false"><span class="icon">🎵</span> Entretenimento</a>
    <a href="#" class="destaque-item" onclick="abrirModal();return false"><span class="icon">➕</span> Cadastrar</a>
  </div>
</div>

<!-- STATS BAR -->
<div class="stats-bar">
  <div class="stats-bar-inner" id="stats-bar"></div>
</div>

<!-- MAIN -->
<div class="main-wrap" id="conteudo">

  <!-- SIDEBAR -->
  <aside class="sidebar">

    <div class="sidebar-box">
      <div class="sidebar-box-hd">Categorias</div>
      <ul class="sidebar-nav" id="sidebar-cats"></ul>
    </div>

    <div class="sidebar-box">
      <div class="sidebar-box-hd verde">Filtros</div>
      <div class="sidebar-filter" id="sidebar-filtros">
        <div style="padding:8px 14px;font-size:.75rem;font-weight:700;color:#555;text-transform:uppercase;border-bottom:1px solid #f0f0f0">Gratuidade</div>
        <label><input type="checkbox" id="f-gratis" onchange="renderCards()"> Somente gratuitos</label>
        <div style="padding:8px 14px;font-size:.75rem;font-weight:700;color:#555;text-transform:uppercase;border-bottom:1px solid #f0f0f0;border-top:1px solid #f0f0f0">Avaliação mínima</div>
        <div class="range-row">
          <input type="range" id="f-nota" min="1" max="5" step="0.5" value="1" oninput="document.getElementById('nota-val').textContent=this.value+' ★';renderCards()">
          <div>Mínimo: <span id="nota-val">1 ★</span></div>
        </div>
      </div>
    </div>

    <div class="sidebar-box">
      <div class="sidebar-box-hd">Informações Úteis</div>
      <ul class="sidebar-nav">
        <li><a href="#">📋 Como se cadastrar</a></li>
        <li><a href="#">📞 Fale Conosco</a></li>
        <li><a href="#">📍 Mapa de Bauru</a></li>
        <li><a href="#">📅 Agenda Cultural</a></li>
        <li><a href="#">🏆 Prêmios e Selos</a></li>
        <li><a href="#">📰 Legislação</a></li>
      </ul>
    </div>

    <div class="sidebar-box">
      <div class="sidebar-box-hd verde">Últimas Notícias</div>
      <ul class="noticias-list" style="padding:0 0 4px">
        <li style="padding:10px 14px">
          <a href="#">Festival de Inverno 2026 abre inscrições</a>
          <span class="data">27/05/2026</span>
        </li>
        <li style="padding:10px 14px;border-top:1px solid #f0f0f0">
          <a href="#">Museu recebe exposição nacional em junho</a>
          <span class="data">25/05/2026</span>
        </li>
        <li style="padding:10px 14px;border-top:1px solid #f0f0f0">
          <a href="#">Bauru entre os 10 destinos mais visitados do interior</a>
          <span class="data">20/05/2026</span>
        </li>
      </ul>
    </div>

    <div class="sidebar-box">
      <div class="sidebar-box-hd">Agenda de Eventos</div>
      <ul class="agenda-list" style="padding:4px 0">
        <li style="padding:8px 14px">
          <div class="agenda-data"><span class="dia">15</span>JUN</div>
          <div><div style="font-size:.82rem;font-weight:600">Feira de Artesanato</div><div style="font-size:.72rem;color:#888">Praça das Cerejeiras</div></div>
        </li>
        <li style="padding:8px 14px;border-top:1px solid #f0f0f0">
          <div class="agenda-data"><span class="dia">22</span>JUN</div>
          <div><div style="font-size:.82rem;font-weight:600">Festival de Música</div><div style="font-size:.72rem;color:#888">Parque Vitória Régia</div></div>
        </li>
        <li style="padding:8px 14px;border-top:1px solid #f0f0f0">
          <div class="agenda-data"><span class="dia">05</span>JUL</div>
          <div><div style="font-size:.82rem;font-weight:600">Semana do Turismo</div><div style="font-size:.72rem;color:#888">Centro de Convenções</div></div>
        </li>
      </ul>
    </div>

  </aside>

  <!-- CONTEUDO PRINCIPAL -->
  <main>

    <div class="content-toolbar">
      <div>
        <div class="content-title" id="content-title">Catálogo de Serviços</div>
        <div class="content-subtitle" id="content-subtitle"></div>
      </div>
      <div class="toolbar-right">
        <button class="btn-view active" id="btn-grade" onclick="setView('grade')" title="Grade">⊞ Grade</button>
        <button class="btn-view" id="btn-lista" onclick="setView('lista')" title="Lista">☰ Lista</button>
        <select class="btn-ordenar" onchange="setOrdem(this.value)">
          <option value="recente">Mais recentes</option>
          <option value="az">A → Z</option>
          <option value="nota">Melhor avaliação</option>
        </select>
        <button class="btn-cadastrar" onclick="abrirModal()">+ Cadastrar</button>
      </div>
    </div>

    <div class="chips-bar">
      <button class="chip active" onclick="setFiltro('todos',this)">Todos</button>
      <button class="chip" onclick="setFiltro('cultura',this)">🎭 Cultura</button>
      <button class="chip" onclick="setFiltro('turismo',this)">🏛️ Turismo</button>
      <button class="chip" onclick="setFiltro('gastronomia',this)">🍽️ Gastronomia</button>
      <button class="chip" onclick="setFiltro('entretenimento',this)">🎵 Entretenimento</button>
    </div>

    <div id="cards-container">
      <div class="cards-grid"><div class="empty-state"><div class="big">⏳</div>Carregando serviços...</div></div>
    </div>

    <div class="paginacao" id="paginacao"></div>

  </main>
</div>

<!-- FOOTER -->
<footer class="site-footer" id="rodape">
  <div class="footer-top">
    <div class="footer-col">
      <h4>Secretaria de Cultura e Turismo</h4>
      <ul>
        <li><a href="#">Sobre a Secretaria</a></li>
        <li><a href="#">Missão e Visão</a></li>
        <li><a href="#">Organograma</a></li>
        <li><a href="#">Secretário(a)</a></li>
        <li><a href="#">Legislação</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Serviços</h4>
      <ul>
        <li><a href="#">Catálogo de Serviços</a></li>
        <li><a href="#">Cadastro de Prestadores</a></li>
        <li><a href="#">Incentivo Fiscal</a></li>
        <li><a href="#">Certificações</a></li>
        <li><a href="#">Agenda de Eventos</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Acesso à Informação</h4>
      <ul>
        <li><a href="#">Transparência</a></li>
        <li><a href="#">Ouvidoria</a></li>
        <li><a href="#">e-SIC</a></li>
        <li><a href="#">LGPD</a></li>
        <li><a href="#">Licitações</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contato</h4>
      <ul>
        <li><a href="#">📧 cultura@bauru.sp.gov.br</a></li>
        <li><a href="#">📞 (14) 3104-1234</a></li>
        <li><a href="#">📍 Praça das Cerejeiras, 1-59</a></li>
        <li><a href="#">Bauru — SP, CEP 17040-070</a></li>
        <li><a href="#">Seg–Sex: 8h–17h</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-mid">
    <div class="footer-mid-inner">
      <div style="display:flex;gap:1.5rem;flex-wrap:wrap">
        <a href="#">Mapa do Site</a>
        <a href="#">Acessibilidade</a>
        <a href="#">Política de Privacidade</a>
        <a href="#">Termos de Uso</a>
      </div>
      <div style="font-size:.75rem;color:rgba(255,255,255,.7)">Versão 2.0 — 2026</div>
    </div>
  </div>
  <div class="footer-bottom">
    © 2026 Prefeitura Municipal de Bauru — Secretaria de Cultura e Turismo — Todos os direitos reservados
  </div>
</footer>

<!-- MODAL CADASTRO/EDITAR -->
<div class="modal-bg" id="modal-form">
  <div class="modal">
    <div class="modal-hd">
      <h2 id="modal-form-title">Cadastrar Novo Serviço</h2>
      <button class="modal-close" onclick="fecharModal('modal-form')">✕</button>
    </div>
    <div class="modal-body">
      <input type="hidden" id="f-id">
      <div class="form-group">
        <label>Nome do Serviço *</label>
        <input id="f-nome" placeholder="Ex: Museu Histórico Municipal de Bauru">
        <div class="hint">Nome completo do estabelecimento ou serviço</div>
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
          <label>Cidade / Estado *</label>
          <input id="f-cidade" placeholder="Ex: Bauru, SP">
        </div>
      </div>
      <div class="form-group">
        <label>Descrição *</label>
        <textarea id="f-desc" placeholder="Descreva o serviço, o que o visitante encontrará, diferenciais..."></textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Preço / Ingresso</label>
          <input id="f-preco" placeholder="Ex: Gratuito ou R$ 25,00">
        </div>
        <div class="form-group">
          <label>Avaliação (1 a 5)</label>
          <input id="f-nota" type="number" min="1" max="5" step="0.1" placeholder="Ex: 4.5">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Horário de Funcionamento</label>
          <input id="f-horario" placeholder="Ex: Ter–Dom 9h–17h">
        </div>
        <div class="form-group">
          <label>Telefone / Site</label>
          <input id="f-contato" placeholder="Ex: (14) 3104-1234">
        </div>
      </div>
    </div>
    <div class="modal-ft">
      <button class="btn-secondary" onclick="fecharModal('modal-form')">Cancelar</button>
      <button class="btn-primary" onclick="salvar()">💾 Salvar Serviço</button>
    </div>
  </div>
</div>

<!-- MODAL DETALHE -->
<div class="modal-bg" id="modal-detalhe">
  <div class="modal">
    <div class="modal-hd" id="detalhe-hd">
      <h2 id="detalhe-titulo">Detalhes do Serviço</h2>
      <button class="modal-close" onclick="fecharModal('modal-detalhe')">✕</button>
    </div>
    <div id="detalhe-body"></div>
  </div>
</div>

<!-- MODAL CONFIRMAR EXCLUSÃO -->
<div class="modal-bg" id="modal-confirm">
  <div class="modal" style="max-width:440px">
    <div class="modal-hd" style="background:#c0392b">
      <h2>Confirmar Exclusão</h2>
      <button class="modal-close" onclick="fecharModal('modal-confirm')">✕</button>
    </div>
    <div class="modal-body">
      <div class="confirm-box">⚠️ Tem certeza que deseja excluir este serviço? Esta ação não pode ser desfeita.</div>
      <p id="confirm-nome" style="font-weight:700;font-size:.95rem"></p>
    </div>
    <div class="modal-ft">
      <button class="btn-secondary" onclick="fecharModal('modal-confirm')">Cancelar</button>
      <button class="btn-danger" onclick="confirmarExcluir()">🗑️ Sim, excluir</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const EMOJIS={cultura:'🎭',turismo:'🏛️',gastronomia:'🍽️',entretenimento:'🎵'};
const CATS={cultura:'Cultura',turismo:'Turismo',gastronomia:'Gastronomia',entretenimento:'Entretenimento'};
const CORES={cultura:'#1351b4',turismo:'#00a300',gastronomia:'#e65100',entretenimento:'#880e4f'};
let db=[],filtroAtivo='todos',viewMode='grade',ordemAtiva='recente',pagAtual=1,perPage=9,excluirId=null;

async function carregar(){
  try{
    const r=await fetch('/api/servicos');
    db=await r.json();
    renderStats();renderSidebar();renderCards();
  }catch(e){toast('Erro ao carregar dados.','erro')}
}

function renderStats(){
  const t={todos:db.length,cultura:0,turismo:0,gastronomia:0,entretenimento:0};
  db.forEach(s=>t[s.categoria]=(t[s.categoria]||0)+1);
  document.getElementById('stats-bar').innerHTML=
    `<span><strong>${t.todos}</strong> serviços</span>`+
    Object.entries(CATS).map(([k,v])=>`<span>${EMOJIS[k]} <strong>${t[k]||0}</strong> ${v}</span>`).join('');
}

function renderSidebar(){
  const t={cultura:0,turismo:0,gastronomia:0,entretenimento:0};
  db.forEach(s=>t[s.categoria]=(t[s.categoria]||0)+1);
  document.getElementById('sidebar-cats').innerHTML=
    `<li><a href="#" onclick="setFiltro('todos');return false" class="${filtroAtivo==='todos'?'active':''}">📋 Todos os serviços <span class="sidebar-badge">${db.length}</span></a></li>`+
    Object.entries(CATS).map(([k,v])=>
      `<li><a href="#" onclick="setFiltro('${k}');return false" class="${filtroAtivo===k?'active':''}">
        ${EMOJIS[k]} ${v} <span class="sidebar-badge ${k==='turismo'?'verde':''}">${t[k]||0}</span>
      </a></li>`).join('');
}

function filtrarDados(){
  const q=(document.getElementById('hero-busca').value||'').toLowerCase();
  const soGratis=document.getElementById('f-gratis').checked;
  const minNota=parseFloat(document.getElementById('f-nota').value)||1;
  let data=db.filter(s=>{
    const mc=filtroAtivo==='todos'||s.categoria===filtroAtivo;
    const mq=!q||s.nome.toLowerCase().includes(q)||s.cidade.toLowerCase().includes(q)||s.descricao.toLowerCase().includes(q)||s.categoria.includes(q)||(s.preco||'').toLowerCase().includes(q);
    const mg=!soGratis||(s.preco||'').toLowerCase().includes('gratu');
    const mn=parseFloat(s.avaliacao)>=minNota;
    return mc&&mq&&mg&&mn;
  });
  if(ordemAtiva==='az') data.sort((a,b)=>a.nome.localeCompare(b.nome));
  else if(ordemAtiva==='nota') data.sort((a,b)=>parseFloat(b.avaliacao)-parseFloat(a.avaliacao));
  return data;
}

function renderCards(){
  const data=filtrarDados();
  const titles={todos:'Todos os Serviços',cultura:'Cultura',turismo:'Turismo',gastronomia:'Gastronomia',entretenimento:'Entretenimento'};
  document.getElementById('content-title').textContent=titles[filtroAtivo];
  document.getElementById('content-subtitle').textContent=data.length+' resultado'+(data.length!==1?'s':'')+' encontrado'+(data.length!==1?'s':'');
  document.getElementById('bc-current').textContent=titles[filtroAtivo];
  const totalPag=Math.ceil(data.length/perPage)||1;
  if(pagAtual>totalPag)pagAtual=1;
  const slice=data.slice((pagAtual-1)*perPage,pagAtual*perPage);
  const cont=document.getElementById('cards-container');
  if(!data.length){
    cont.innerHTML='<div class="cards-grid"><div class="empty-state"><div class="big">🔍</div>Nenhum serviço encontrado com os filtros selecionados.</div></div>';
    document.getElementById('paginacao').innerHTML='';return;
  }
  const gratis=p=>(p||'').toLowerCase().includes('gratu')||p==='0'||p==='R$ 0,00';
  if(viewMode==='grade'){
    cont.innerHTML=`<div class="cards-grid">${slice.map(s=>cardGrade(s,gratis)).join('')}</div>`;
  } else {
    cont.innerHTML=`<div class="cards-list">${slice.map(s=>cardLista(s,gratis)).join('')}</div>`;
  }
  renderPaginacao(totalPag,data.length);
}

function cardGrade(s,gratis){
  return`<div class="card">
    <div class="card-thumb bg-${s.categoria}">${EMOJIS[s.categoria]||'📍'}</div>
    <div class="card-stripe stripe-${s.categoria}"></div>
    <div class="card-body">
      <div class="card-cat cat-${s.categoria}">${CATS[s.categoria]||s.categoria}</div>
      <div class="card-title">${s.nome}</div>
      <div class="card-desc">${(s.descricao||'').slice(0,100)}${(s.descricao||'').length>100?'…':''}</div>
      <div class="card-meta">
        <span class="card-local">📍 ${s.cidade}</span>
        <span class="${gratis(s.preco)?'tag tag-gratis':'tag tag-pago'}">${gratis(s.preco)?'Gratuito':s.preco}</span>
        <span class="card-rating">${parseFloat(s.avaliacao).toFixed(1)} ★</span>
      </div>
    </div>
    <div class="card-actions">
      <button class="btn-sm azul" onclick="verDetalhe(${s.id})">Ver mais</button>
      <button class="btn-sm" onclick="editarServico(${s.id})">✏️ Editar</button>
      <button class="btn-sm vermelho" onclick="pedirExcluir(${s.id},'${s.nome.replace(/'/g,"\\'")}')">🗑️</button>
    </div>
  </div>`;
}

function cardLista(s,gratis){
  return`<div class="card-list-item">
    <div class="card-list-thumb bg-${s.categoria}">${EMOJIS[s.categoria]||'📍'}</div>
    <div class="card-list-stripe stripe-${s.categoria}"></div>
    <div class="card-list-body">
      <div class="card-list-info">
        <div class="card-cat cat-${s.categoria}" style="margin-bottom:2px">${CATS[s.categoria]}</div>
        <div class="card-title" style="margin-bottom:4px">${s.nome}</div>
        <div style="font-size:.78rem;color:#555">${(s.descricao||'').slice(0,80)}…</div>
        <div class="card-meta" style="margin-top:6px;padding-top:0;border-top:none">
          <span class="card-local">📍 ${s.cidade}</span>
          <span class="${gratis(s.preco)?'tag tag-gratis':'tag tag-pago'}">${gratis(s.preco)?'Gratuito':s.preco}</span>
          <span class="card-rating">${parseFloat(s.avaliacao).toFixed(1)} ★</span>
        </div>
      </div>
      <div class="card-list-actions">
        <button class="btn-sm azul" onclick="verDetalhe(${s.id})">Ver mais</button>
        <button class="btn-sm" onclick="editarServico(${s.id})">✏️</button>
        <button class="btn-sm vermelho" onclick="pedirExcluir(${s.id},'${s.nome.replace(/'/g,"\\'")}')">🗑️</button>
      </div>
    </div>
  </div>`;
}

function renderPaginacao(total,count){
  if(total<=1){document.getElementById('paginacao').innerHTML='';return;}
  let html='';
  html+=`<button class="pag-btn ${pagAtual===1?'disabled':''}" onclick="irPag(${pagAtual-1})">‹</button>`;
  for(let i=1;i<=total;i++){
    html+=`<button class="pag-btn ${i===pagAtual?'active':''}" onclick="irPag(${i})">${i}</button>`;
  }
  html+=`<button class="pag-btn ${pagAtual===total?'disabled':''}" onclick="irPag(${pagAtual+1})">›</button>`;
  document.getElementById('paginacao').innerHTML=html;
}

function irPag(p){pagAtual=p;renderCards();window.scrollTo(0,400)}

function setFiltro(f,el){
  filtroAtivo=f;pagAtual=1;
  document.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
  if(el)el.classList.add('active');
  else{
    document.querySelectorAll('.chip').forEach(c=>{
      if((f==='todos'&&c.textContent.trim()==='Todos')||c.textContent.toLowerCase().includes(CATS[f]||''))c.classList.add('active');
    });
  }
  renderSidebar();renderCards();
  window.scrollTo(0,400);
}

function setView(v){
  viewMode=v;
  document.getElementById('btn-grade').classList.toggle('active',v==='grade');
  document.getElementById('btn-lista').classList.toggle('active',v==='lista');
  renderCards();
}

function setOrdem(o){ordemAtiva=o;pagAtual=1;renderCards()}

function syncBusca(v){
  document.getElementById('hero-busca').value=v;
  document.getElementById('hbusca').value=v;
  pagAtual=1;renderCards();
}

function setTermoBusca(t){syncBusca(t)}

function verDetalhe(id){
  const s=db.find(x=>x.id===id);if(!s)return;
  const gratis=(s.preco||'').toLowerCase().includes('gratu');
  document.getElementById('detalhe-hd').style.background=CORES[s.categoria]||'#1351b4';
  document.getElementById('detalhe-titulo').textContent=s.nome;
  document.getElementById('detalhe-body').innerHTML=`
    <div class="detalhe-hero bg-${s.categoria}">${EMOJIS[s.categoria]}</div>
    <div class="modal-body">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
        <span class="cat-${s.categoria}" style="font-size:.72rem;font-weight:700;text-transform:uppercase">${CATS[s.categoria]}</span>
        <span class="${gratis?'tag tag-gratis':'tag tag-pago'}">${gratis?'Gratuito':s.preco}</span>
        <span style="color:#00a300;font-weight:700;margin-left:auto">${parseFloat(s.avaliacao).toFixed(1)} ★</span>
      </div>
      <p style="font-size:.88rem;line-height:1.7;color:#444;background:#f8f8f8;padding:12px;border-left:3px solid ${CORES[s.categoria]};margin-bottom:1rem">${s.descricao}</p>
      <div class="detalhe-info">
        <div class="detalhe-row"><strong>📍 Localização</strong>${s.cidade}</div>
        <div class="detalhe-row"><strong>💰 Preço</strong>${s.preco||'Consulte'}</div>
        <div class="detalhe-row"><strong>🕐 Horário</strong>${s.horario||'A confirmar'}</div>
        <div class="detalhe-row"><strong>📞 Contato</strong>${s.contato||'—'}</div>
      </div>
    </div>
    <div class="modal-ft">
      <button class="btn-secondary" onclick="fecharModal('modal-detalhe')">Fechar</button>
      <button class="btn-sm" style="padding:8px 14px" onclick="editarServico(${s.id});fecharModal('modal-detalhe')">✏️ Editar</button>
      <button class="btn-danger" onclick="pedirExcluir(${s.id},'${s.nome.replace(/'/g,"\\'")}');fecharModal('modal-detalhe')">🗑️ Excluir</button>
    </div>`;
  document.getElementById('modal-detalhe').classList.add('open');
}

function abrirModal(s){
  document.getElementById('modal-form-title').textContent=s?'Editar Serviço':'Cadastrar Novo Serviço';
  document.getElementById('f-id').value=s?s.id:'';
  document.getElementById('f-nome').value=s?s.nome:'';
  document.getElementById('f-cat').value=s?s.categoria:'cultura';
  document.getElementById('f-cidade').value=s?s.cidade:'';
  document.getElementById('f-desc').value=s?s.descricao:'';
  document.getElementById('f-preco').value=s?s.preco:'';
  document.getElementById('f-horario').value=s?s.horario:'';
  document.getElementById('f-contato').value=s?s.contato:'';
  document.getElementById('f-nota').value=s?s.avaliacao:'';
  document.getElementById('modal-form').classList.add('open');
}

function editarServico(id){
  const s=db.find(x=>x.id===id);if(s)abrirModal(s);
}

function pedirExcluir(id,nome){
  excluirId=id;
  document.getElementById('confirm-nome').textContent=nome;
  document.getElementById('modal-confirm').classList.add('open');
}

async function confirmarExcluir(){
  if(!excluirId)return;
  await fetch('/api/servicos/'+excluirId,{method:'DELETE'});
  fecharModal('modal-confirm');
  toast('Serviço excluído com sucesso.','ok');
  excluirId=null;
  await carregar();
}

function fecharModal(id){document.getElementById(id).classList.remove('open')}

async function salvar(){
  const nome=document.getElementById('f-nome').value.trim();
  const cidade=document.getElementById('f-cidade').value.trim();
  const desc=document.getElementById('f-desc').value.trim();
  if(!nome||!cidade||!desc){toast('Preencha os campos obrigatórios (*)','erro');return;}
  const body={
    nome,cidade,descricao:desc,
    categoria:document.getElementById('f-cat').value,
    preco:document.getElementById('f-preco').value||'Consulte',
    horario:document.getElementById('f-horario').value||'A confirmar',
    contato:document.getElementById('f-contato').value||'—',
    avaliacao:parseFloat(document.getElementById('f-nota').value)||4.0
  };
  const id=document.getElementById('f-id').value;
  if(id){
    await fetch('/api/servicos/'+id,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    toast('Serviço atualizado!','ok');
  } else {
    await fetch('/api/servicos',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    toast('Serviço cadastrado!','ok');
  }
  fecharModal('modal-form');
  await carregar();
}

function toast(msg,tipo='ok'){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast '+tipo+' show';
  setTimeout(()=>t.classList.remove('show'),3500);
}

function toggleNav(id){
  const el=document.getElementById(id);
  document.querySelectorAll('.nav-item').forEach(n=>{if(n.id!==id)n.classList.remove('open')});
  el.classList.toggle('open');
}

document.addEventListener('click',e=>{
  if(!e.target.closest('.nav-item'))document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('open'));
  if(e.target.classList.contains('modal-bg'))e.target.classList.remove('open');
});

carregar();
</script>
</body>
</html>"""

if __name__ == '__main__':
    app.run(debug=True)
