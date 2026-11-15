import os
from html import escape
from pathlib import Path

import requests
import streamlit as st

st.set_page_config(page_title='NETUNO VISION | Ecobarreira Inteligente', page_icon='🔱', layout='wide', initial_sidebar_state='collapsed')

PASTA = Path(__file__).resolve().parent
LOGO = PASTA / 'logo_netuno.png'

# URL pública do Flask/Cloudflare, sem /foto. Pode ser definida em
# Streamlit Cloud > App settings > Secrets: CAMERA_URL = "https://..."
try:
    CAMERA_URL_CONFIG = str(st.secrets.get('CAMERA_URL', os.getenv('CAMERA_URL', ''))).strip()
except Exception:
    CAMERA_URL_CONFIG = os.getenv('CAMERA_URL', '').strip()

st.markdown('''
<style>
:root {color-scheme: dark;}
.stApp {background: radial-gradient(circle at 50% -15%, #153b65 0%, #081a31 42%, #061326 100%);color:#f8fafc;}
.block-container {max-width:1320px;padding:2.0rem 2.2rem 4rem;}
header[data-testid="stHeader"] {background:transparent;}
#MainMenu,footer {visibility:hidden;}
h1,h2,h3,p {color:#f8fafc;}
h2,h3 {color:#e0f2fe!important;}
[data-testid="stWidgetLabel"] p, label p, [data-testid="stCaptionContainer"] p {color:#cbd5e1!important;}
[data-testid="stMetric"] {background:linear-gradient(150deg,#153656,#0c2744);border:1px solid #315676;border-radius:17px;padding:20px;min-height:132px;box-shadow:0 8px 22px #0002;}
[data-testid="stMetricLabel"] p {color:#cbd5e1!important;font-size:0.9rem!important;}
[data-testid="stMetricValue"] {color:#ffffff!important;}
[data-testid="stMetricValue"] div {color:#ffffff!important;}
[data-testid="stSelectbox"] > div > div, [data-testid="stTextInput"] input {background:#eaf3ff!important;color:#07182d!important;}
[data-testid="stAlert"] {background:#102b48!important;color:#f8fafc!important;border:1px solid #315676;border-radius:12px;}
[data-testid="stAlert"] p {color:#f8fafc!important;}
[data-testid="stExpander"] {background:#0b253f;border:1px solid #315676;border-radius:14px;}
[data-testid="stExpander"] summary p {color:#f8fafc!important;}
hr {border-color:#315676!important;}
.hero {border:1px solid #28577d;border-radius:24px;background:linear-gradient(140deg,#102e4e,#071b31);padding:24px 18px;text-align:center;box-shadow:0 18px 40px #0003;margin-bottom:14px;}
.hero-title {font-size:clamp(2.4rem,6vw,4.4rem);font-weight:900;letter-spacing:0.09em;color:#f8fafc;line-height:1.08;margin:8px 0;}
.hero-subtitle {color:#38bdf8;font-size:clamp(1rem,2vw,1.25rem);font-weight:650;margin:8px 0;}
.hero-meta {color:#cbd5e1;font-size:0.85rem;letter-spacing:0.09em;margin-top:12px;}
.section-kicker {color:#38bdf8;letter-spacing:0.14em;text-transform:uppercase;font-weight:750;font-size:0.8rem;margin:12px 0;}
.panel {border:1px solid #315676;background:linear-gradient(150deg,#102d4c,#091f38);border-radius:18px;padding:20px;}
.status-dot {display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:8px;vertical-align:middle;}
.small-muted {color:#cbd5e1;font-size:0.88rem;}
.light-row {display:flex;justify-content:center;gap:22px;margin:20px 0;}
.light {width:42px;height:42px;border-radius:50%;border:2px solid #64748b;}
.footer {text-align:center;color:#94a3b8;font-size:0.85rem;padding:16px;}
@media(max-width:768px){.block-container{padding:1rem .7rem 2rem}.hero{padding:20px 10px}.hero-title{letter-spacing:.03em}[data-testid="stMetric"]{padding:13px;min-height:110px}}
</style>
''', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    if LOGO.exists():
        _, centro, _ = st.columns([4, 1, 4])
        with centro:
            st.image(str(LOGO), use_container_width=True)
    else:
        st.markdown('<div style="font-size:2.8rem;text-align:center">🔱</div>', unsafe_allow_html=True)
    st.markdown('''<div class="hero-title">NETUNO VISION</div>
    <div class="hero-subtitle">Inteligência Artificial a Serviço dos Manguezais</div>
    <div class="hero-meta">ECOBARREIRA INTELIGENTE · EQUIPE NETUNO · SESI SANTOS · FLL BIOGLOW</div>''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.caption('Central de monitoramento ambiental · Mangue São Manoel · Protótipo em desenvolvimento')
st.info('📡 MONITORAMENTO REAL — A câmera pode mostrar imagens reais. A IA para identificar e contar resíduos ainda será implementada e validada.')


def classificar(ocupacao):
    if ocupacao is None:
        return 'AGUARDANDO IA', '#94a3b8', 'A identificação automática ainda não está conectada.'
    if ocupacao < 40:
        return 'NORMAL', '#22c55e', 'Ocupação visual abaixo do limiar de atenção.'
    if ocupacao < 75:
        return 'ATENÇÃO', '#facc15', 'A ocupação visual merece acompanhamento.'
    return 'CRÍTICO', '#ef4444', 'Ocupação visual elevada. Recomenda-se inspeção.'


def foto_da_camera(url):
    if not url:
        st.info('Câmera ainda não configurada. Informe o endereço do servidor Flask/Cloudflare abaixo.')
        return
    try:
        resposta = requests.get(url.rstrip('/') + '/foto', timeout=7)
        resposta.raise_for_status()
        if not resposta.headers.get('content-type', '').lower().startswith('image/'):
            raise ValueError('A resposta não contém uma imagem.')
        st.image(resposta.content, use_container_width=True)
        st.caption('Fotografia da ESP32-CAM · Atualização automática aproximada a cada 5 segundos')
    except (requests.RequestException, ValueError):
        st.warning('Não foi possível acessar a câmera. Verifique o notebook, o Flask e o endereço do Cloudflare.')


ocupacao, quantidades, total = None, None, None
situacao, cor, mensagem = classificar(None)
origem = 'IA PENDENTE'

st.markdown('<div class="section-kicker">Visão geral do sistema</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric('Ocupação visual', f'{ocupacao}%' if ocupacao is not None else '—')
with c2:
    st.metric('Resíduos identificados', str(total) if total is not None else '—')
with c3:
    st.metric('Situação', situacao)
with c4:
    st.metric('Origem dos dados', origem)
st.caption('Ocupação visual será a fração da região observada coberta por resíduos visíveis, após implementação e validação da IA.')

st.divider()
st.markdown('<div class="section-kicker">Monitoramento e alertas</div>', unsafe_allow_html=True)
col_camera, col_alerta = st.columns([3, 2], gap='large')
with col_camera:
    st.subheader('📷 Câmera da ecobarreira')
    with st.expander('Configurar endereço da câmera', expanded=False):
        st.caption('Use o endereço HTTPS temporário criado pelo Cloudflare, sem acrescentar /foto. Não compartilhe a câmera publicamente sem autorização.')
        url_digitada = st.text_input('Endereço HTTPS da câmera', value=CAMERA_URL_CONFIG, placeholder='https://seu-tunel.trycloudflare.com')
    # Evita consultas a URLs arbitrárias: restringe a HTTPS no domínio temporário Cloudflare.
    from urllib.parse import urlparse
    url = url_digitada.strip().rstrip('/')
    parsed = urlparse(url)
    if url and not (parsed.scheme == 'https' and parsed.hostname and parsed.hostname.endswith('.trycloudflare.com') and parsed.path in ('', '/')):
        st.error('Informe apenas um endereço HTTPS válido terminado em .trycloudflare.com, sem caminho adicional.')
    else:
        @st.fragment(run_every='5s')
        def atualizar_camera():
            foto_da_camera(url)
        atualizar_camera()
with col_alerta:
    st.subheader('🚦 Central de alertas')
    cores = ['#22c55e' if situacao == 'NORMAL' else '#334155', '#facc15' if situacao == 'ATENÇÃO' else '#334155', '#ef4444' if situacao == 'CRÍTICO' else '#334155']
    luzes = ''.join(f'<div class="light" style="background:{c};box-shadow:0 0 12px {c}55"></div>' for c in cores)
    st.markdown(f'''<div class="panel" style="text-align:center;min-height:270px">
        <div class="small-muted">NÍVEL DE ALERTA</div><div class="light-row">{luzes}</div>
        <div style="font-size:1.7rem;font-weight:850;color:{cor}">{escape(situacao)}</div>
        <p style="color:#e2e8f0;margin-top:12px">{escape(mensagem)}</p>
        </div>''', unsafe_allow_html=True)
    st.caption('Os alertas serão ativados somente após a implementação e validação da estimativa de ocupação visual.')

st.divider()
st.markdown('<div class="section-kicker">Inteligência artificial e classificação</div>', unsafe_allow_html=True)
st.subheader('🧠 Análise inteligente de resíduos')
st.info('Aguardando desenvolvimento e validação da IA para classificar plástico, madeira, metal e outros. Nenhuma contagem real está disponível ainda.')

st.divider()
st.subheader('📈 Histórico de ocupação visual')
st.info('O histórico real aparecerá quando o servidor de IA começar a registrar análises com data e horário.')

with st.expander('🔬 Como funcionará a IA no NETUNO VISION'):
    st.markdown('''**1. Captura:** a ESP32-CAM fotografa a ecobarreira.  
**2. Processamento:** o notebook recebe as imagens e executa o modelo de visão computacional.  
**3. Classificação:** o modelo identifica possíveis resíduos das categorias plástico, madeira, metal e outros.  
**4. Ocupação visual:** uma etapa de segmentação estima a área visível ocupada por resíduos na região monitorada.  
**5. Validação:** os alunos comparam resultados automáticos com imagens anotadas manualmente.  
**6. Alertas:** o painel apresenta resultados e tendências depois de validar os limites adotados.

*O modelo de IA ainda não está implementado neste arquivo. A câmera, isoladamente, não identifica materiais.*''')

st.markdown('<div class="footer">🔱 NETUNO VISION · Inteligência Artificial a Serviço dos Manguezais<br>Equipe Netuno · SESI Santos · FLL BIOGLOW · Projeto de inovação</div>', unsafe_allow_html=True)
