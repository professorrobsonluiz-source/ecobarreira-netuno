import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title='NETUNO VISION | Ecobarreira Inteligente', page_icon='🔱', layout='wide', initial_sidebar_state='collapsed')

FOTO_URL = 'https://netuno-camera.professorrobsonluiz.workers.dev/foto'
AO_VIVO_URL = 'https://camera.netunovision.com.br/ao-vivo'

st.markdown('''<style>
.stApp {background:linear-gradient(145deg,#071a31,#0b2746);color:#f5fbff}
.block-container {padding-top:1.5rem;max-width:1800px}
h1,h2,h3,p,span,label {color:inherit}
h1 {font-size:2.6rem!important;letter-spacing:.05em}
h3 {font-size:1.25rem!important}
[data-testid="stMetric"] {background:#123251;border:1px solid #28557a;padding:1rem;border-radius:12px}
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {color:white}
[data-baseweb="tab-list"] {gap:12px}
button[data-baseweb="tab"] {color:#c7e8ff!important;font-weight:700}
button[aria-selected="true"][data-baseweb="tab"] {color:#ffffff!important;border-bottom:3px solid #40c9ff!important}
.info-panel {background:#123251;border:1px solid #28557a;border-radius:12px;padding:18px 20px;margin:8px 0 16px}
.info-row {padding:12px 0;border-bottom:1px solid #2a4b68}
.info-row:last-child {border-bottom:none}
.info-label {font-size:11px;color:#73cfff;letter-spacing:.09em;text-transform:uppercase}
.info-value {font-size:14px;color:white;font-weight:600;margin-top:4px}
.smallnote {color:#9ab8d0;font-size:12px}
[data-testid="stMainBlockContainer"],.block-container{max-width:100%!important;padding-left:2rem!important;padding-right:2rem!important}
.section-kicker{font-size:12px;font-weight:800;letter-spacing:.15em;color:#52c8ff;text-transform:uppercase;margin:28px 0 8px}
.dash-card{background:linear-gradient(140deg,#153858,#0b2541);border:1px solid #315979;border-radius:16px;padding:22px;box-shadow:0 6px 20px #0002}
.compact{min-height:215px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.card-eyebrow{font-size:12px;letter-spacing:.12em;color:#9ddcff;font-weight:750}
.card-big{font-size:36px;font-weight:850;color:#fff;margin:12px 0}
.card-help{color:#b4cee3;font-size:13px;line-height:1.6}
.signal{display:flex;gap:15px;margin:20px 0}
.signal span{display:block;width:42px;height:42px;border-radius:50%;background:#33465c;border:1px solid #6a879e}
.progress-track{width:100%;height:12px;border-radius:12px;background:#294a68;margin:8px 0 16px}
.material-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:18px 0}
.material-card{background:#081c34;border:1px solid #315979;border-radius:14px;text-align:center;padding:22px 10px}
.material-symbol{font-size:27px;margin-bottom:7px}
.material-label{font-size:16px;color:#fff;font-weight:750}
.material-value{font-size:30px;color:#fff;font-weight:850;margin-top:8px}
.overview-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:12px 0 26px}
.overview-card{background:linear-gradient(145deg,#163a59,#102d4b);border:1px solid #315979;border-radius:14px;padding:20px 18px;min-height:158px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 6px 20px #00000016}
.overview-top{display:flex;align-items:center;gap:9px;color:#c4e0f2;font-size:13px;font-weight:700;line-height:1.35}
.overview-icon{font-size:21px;flex-shrink:0}
.overview-value{font-size:25px;line-height:1.2;font-weight:750;color:#fff;margin-top:13px;overflow-wrap:anywhere}
.overview-help{font-size:12px;color:#a6c5da;line-height:1.4;margin-top:8px}
@media(max-width:1050px){.overview-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.overview-grid{grid-template-columns:1fr}}
@media(max-width:850px){.material-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.block-container{padding-left:.8rem!important;padding-right:.8rem!important}}
</style>''', unsafe_allow_html=True)

header_a, header_b = st.columns([1, 6], vertical_alignment='center')
with header_a:
    try:
        st.image('logo_netuno.png', width=115)
    except Exception:
        st.markdown('## 🔱')
with header_b:
    st.title('NETUNO VISION')
    st.markdown('**Inteligência Artificial a Serviço dos Manguezais**')
    st.caption('ECOBARREIRA INTELIGENTE · EQUIPE NETUNO · SESI SANTOS · FLL BIOGLOW')
st.divider()
st.caption('CENTRAL DE MONITORAMENTO AMBIENTAL · MANGUE SÃO MANOEL')
st.markdown('### Visão geral do sistema')
st.markdown('''<div class="overview-grid">
  <div class="overview-card">
    <div class="overview-top"><span class="overview-icon">🌊</span><span>Ocupação da ecobarreira</span></div>
    <div class="overview-value">— %</div>
    <div class="overview-help">Aguardando análise visual</div>
  </div>
  <div class="overview-card">
    <div class="overview-top"><span class="overview-icon">♻️</span><span>Resíduos identificados</span></div>
    <div class="overview-value">—</div>
    <div class="overview-help">Classificação em desenvolvimento</div>
  </div>
  <div class="overview-card">
    <div class="overview-top"><span class="overview-icon">📡</span><span>Situação ambiental</span></div>
    <div class="overview-value">Em análise</div>
    <div class="overview-help">Monitoramento em implantação</div>
  </div>
  <div class="overview-card">
    <div class="overview-top"><span class="overview-icon">🧠</span><span>Inteligência artificial</span></div>
    <div class="overview-value">Em preparação</div>
    <div class="overview-help">Reconhecimento de materiais</div>
  </div>
</div>''', unsafe_allow_html=True)

st.markdown('### 📡 Monitoramento e alertas')
left,right=st.columns([3.2,1],gap='large')
with left:
    tab_live,tab_photo=st.tabs(['🎥 Câmera ao vivo','📷 Fotografias automáticas'])
    with tab_live:
        st.markdown('#### Transmissão ao vivo da ecobarreira')
        # Exibe apenas as imagens, sem o cabecalho da pagina remota.
        components.html("""
        <!doctype html><html><head><meta charset="utf-8">
        <style>
        *{box-sizing:border-box}html,body{margin:0;overflow:hidden;background:#071a31}
        .camera{width:100%;height:650px;display:flex;align-items:center;justify-content:center;overflow:hidden}
        img{display:block;width:100%;height:100%;object-fit:contain;border-radius:10px}
        </style></head><body>
        <div class="camera"><img id="live" alt="Camera da ecobarreira"></div>
        <script>
        const el=document.getElementById('live');
        const endpoint='https://camera.netunovision.com.br/foto';
        let pending=false;
        function refresh(){
          if(pending)return;
          pending=true;
          const pic=new Image();
          pic.onload=()=>{el.src=pic.src;pending=false};
          pic.onerror=()=>{pending=false};
          pic.src=endpoint+'?t='+Date.now();
        }
        refresh();setInterval(refresh,1200);
        </script></body></html>
        """,height=655,scrolling=False)
    with tab_photo:
        st.markdown('#### Última fotografia da ecobarreira')
        # Cache busting is driven by a Streamlit fragment, not a manual refresh.
        @st.fragment(run_every='15s')
        def foto_atualizada():
            timestamp = int(datetime.now().timestamp())
            st.markdown(f'<img src="{FOTO_URL}?t={timestamp}" style="display:block;width:100%;max-height:720px;object-fit:contain;border-radius:10px;background:#050e19" alt="Última fotografia da ecobarreira">', unsafe_allow_html=True)
            st.caption('Consulta de nova fotografia a cada 15 segundos; a ESP32-CAM envia imagens aproximadamente a cada 60 segundos.')
        foto_atualizada()
with right:
    st.markdown('### 🌿 Monitoramento ambiental')
    st.markdown('''<div class="info-panel">
      <div class="info-row"><div class="info-label">Monitoramento por câmera</div><div class="info-value">Transmissão remota e registros fotográficos</div></div>
      <div class="info-row"><div class="info-label">Acompanhamento remoto</div><div class="info-value">Fotografias disponíveis pela internet</div></div>
      <div class="info-row"><div class="info-label">Inteligência artificial</div><div class="info-value">Identificação de resíduos em desenvolvimento</div></div>
      <div class="info-row"><div class="info-label">Área de monitoramento</div><div class="info-value">Mangue São Manoel · Baixada Santista</div></div>
      <div class="info-row"><div class="info-label">Objetivo ambiental</div><div class="info-value">Acompanhar o acúmulo de resíduos e apoiar ações de limpeza</div></div>
    </div>''',unsafe_allow_html=True)

st.markdown('<div class="section-kicker">Monitoramento e indicadores</div>', unsafe_allow_html=True)
col_alert,col_occup=st.columns(2,gap='large')
with col_alert:
    st.markdown('### 🚦 Central de alertas')
    st.markdown('''<div class="dash-card compact">
      <div class="card-eyebrow">NÍVEL DE ALERTA</div>
      <div class="signal"><span></span><span></span><span></span></div>
      <div style="font-size:20px;font-weight:800;color:#fff">AGUARDANDO IA</div>
      <div class="card-help" style="margin-top:12px">Os alertas serão ativados após a validação dos critérios ambientais.</div>
    </div>''',unsafe_allow_html=True)
with col_occup:
    st.markdown('### 📊 Ocupação visual')
    st.markdown('''<div class="dash-card compact">
      <div class="card-eyebrow">SUPERFÍCIE VISÍVEL OCUPADA</div>
      <div class="card-big">—%</div>
      <div class="progress-track"></div>
      <div class="card-help">Aguardando a primeira medição da inteligência artificial.</div>
    </div>''',unsafe_allow_html=True)

st.markdown('<div class="section-kicker">Inteligência artificial e classificação</div>',unsafe_allow_html=True)
st.markdown('### 🧠 Resíduos por material')
st.markdown('''<div class="dash-card">
  <div class="card-help">Categorias previstas para identificação automática de resíduos</div>
  <div class="material-grid">
    <div class="material-card"><div class="material-symbol">♻️</div><div class="material-label">Plástico</div><div class="material-value">—</div></div>
    <div class="material-card"><div class="material-symbol">🪵</div><div class="material-label">Madeira</div><div class="material-value">—</div></div>
    <div class="material-card"><div class="material-symbol">🔩</div><div class="material-label">Metal</div><div class="material-value">—</div></div>
    <div class="material-card"><div class="material-symbol">📦</div><div class="material-label">Outros</div><div class="material-value">—</div></div>
  </div>
  <div class="card-help">A classificação automática está em desenvolvimento. Os indicadores serão preenchidos com dados reais após a integração da IA.</div>
</div>''',unsafe_allow_html=True)
