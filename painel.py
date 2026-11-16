import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title='NETUNO VISION | Ecobarreira Inteligente', page_icon='🔱', layout='wide', initial_sidebar_state='collapsed')

FOTO_URL = 'https://netuno-camera.professorrobsonluiz.workers.dev/foto'
AO_VIVO_URL = 'https://camera.netunovision.com.br/ao-vivo'

st.markdown('''<style>
.stApp {background:linear-gradient(145deg,#071a31,#0b2746);color:#f5fbff}
.block-container {padding-top:1.5rem;max-width:1600px}
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
a,b,c,d=st.columns(4)
with a: st.metric('Ocupação visual', '—')
with b: st.metric('Resíduos identificados', '—')
with c: st.metric('Situação', 'AGUARDANDO IA')
with d: st.metric('Análise inteligente', 'PENDENTE')

st.markdown('### 📡 Monitoramento e alertas')
left,right=st.columns([1.6,1],gap='large')
with left:
    tab_live,tab_photo=st.tabs(['🎥 Câmera ao vivo','📷 Fotografias automáticas'])
    with tab_live:
        st.markdown('#### Transmissão ao vivo da ecobarreira')
        # Embed remote HTML page; its JavaScript refreshes the picture every second.
        components.iframe(AO_VIVO_URL, height=690, scrolling=True)
        st.caption('Atualização aproximada a cada segundo. Para funcionar, o notebook com Flask e Cloudflare Tunnel precisa estar ligado e conectado à câmera.')
        st.markdown(f'[Abrir transmissão em outra aba, se necessário]({AO_VIVO_URL})')
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
    st.caption('A disponibilidade da última fotografia não confirma que a câmera esteja conectada neste instante.')

col_alert,col_occup=st.columns(2,gap='large')
with col_alert:
    st.markdown('### 🚦 Central de alertas')
    st.markdown('<div class="info-panel" style="text-align:center"><div class="info-label">Nível de alerta</div><h3>⚪ ⚪ ⚪</h3><strong>AGUARDANDO IA</strong><p class="smallnote">Alertas disponíveis após implementação e validação dos limites.</p></div>',unsafe_allow_html=True)
with col_occup:
    st.markdown('### 📊 Ocupação visual')
    st.markdown('<div class="info-panel" style="text-align:center"><div class="info-label">Superfície visível ocupada</div><h2>—%</h2><p class="smallnote">Aguardando medições reais da inteligência artificial.</p></div>',unsafe_allow_html=True)
    st.progress(0)

st.caption('INTELIGÊNCIA ARTIFICIAL E CLASSIFICAÇÃO')
st.markdown('### 🧠 Resíduos por material')
st.info('Classificação de plástico, madeira, metal e outros materiais: em desenvolvimento. Nenhum resultado de IA é apresentado como medição real antes da integração.')
