from datetime import datetime
from html import escape
from pathlib import Path

import requests
import streamlit as st

st.set_page_config(page_title="NETUNO VISION | Ecobarreira Inteligente", page_icon="🔱", layout="wide", initial_sidebar_state="collapsed")
ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "logo_netuno.png"
st.markdown("""
<style>
:root {color-scheme: dark;}
.stApp {background:linear-gradient(155deg,#07162a 0%,#0a2340 60%,#071629 100%);color:#f8fafc;}
/* O Streamlit costuma limitar a largura; liberar praticamente toda a tela. */
[data-testid="stMainBlockContainer"], .block-container {max-width: 100% !important; width:100% !important; padding:1.1rem 2.0rem 3rem !important;}
[data-testid="stHeader"] {background:transparent;}
#MainMenu,footer {visibility:hidden;}
h1,h2,h3,p {color:#f8fafc;}
h2,h3 {color:#f1f5f9!important;}
[data-testid="stCaptionContainer"] p, [data-testid="stWidgetLabel"] p, label p {color:#cbd5e1!important;}
[data-testid="stMetric"] {background:linear-gradient(140deg,#153858,#0c2948);border:1px solid #285578;border-radius:16px;padding:19px 21px;min-height:118px;box-shadow:0 8px 20px #0002;}
[data-testid="stMetricLabel"] p {color:#b9d3e7!important;font-size:.95rem!important;}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] div {color:#fff!important;font-size:clamp(1.1rem,1.7vw,2rem)!important;overflow-wrap:anywhere;}
[data-testid="stAlert"] {background:#112d4a!important;border:1px solid #285578!important;border-radius:13px!important;}
[data-testid="stAlert"] p, [data-testid="stAlert"] div {color:#eaf5ff!important;}
[data-testid="stExpander"] {background:#102b47;border:1px solid #285578;border-radius:12px;}
[data-testid="stExpander"] summary p {color:#f8fafc!important;}
[data-testid="stTextInput"] input {background:#102b47!important;color:#fff!important;border:1px solid #3a6687!important;}
hr {border-color:#285578!important;opacity:.65;}
.brand {font-size:clamp(2.0rem,3.5vw,3.5rem);font-weight:900;letter-spacing:.055em;line-height:1.12;color:#fff;margin:0 0 5px;}
.tagline {font-size:clamp(.95rem,1.3vw,1.22rem);font-weight:650;color:#38bdf8;margin:0 0 8px;}
.brandmeta {font-size:.82rem;letter-spacing:.08em;color:#a7c7df;}
.section-title {font-size:.78rem;letter-spacing:.17em;text-transform:uppercase;color:#38bdf8;font-weight:800;margin:15px 0 12px;}
.card {background:linear-gradient(140deg,#102e4d,#0b233e);border:1px solid #285578;border-radius:17px;padding:20px;}
.card-title {font-size:1.2rem;font-weight:750;color:#fff;margin-bottom:12px;}
.camera-empty {min-height:280px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;background:#07182d;border:1px dashed #315e7e;border-radius:12px;color:#cbd5e1;text-align:center;padding:20px;}
.lights {display:flex;justify-content:center;gap:22px;margin:22px 0;}
.light {width:46px;height:46px;border-radius:50%;border:2px solid #6b849a;}
.materials {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:14px 0;}
.material {background:#071b32;border:1px solid #315676;border-radius:12px;padding:16px;text-align:center;color:#fff;}
.material-name {color:#fff;font-weight:700;font-size:1rem;}
.material-value {color:#fff;font-size:1.7rem;font-weight:800;margin:5px 0;}
.note {color:#b5cee2;font-size:.85rem;line-height:1.55;}
.footer-note {text-align:center;color:#9fbad0;font-size:.82rem;padding:20px 0;}
@media(max-width:850px){[data-testid="stMainBlockContainer"],.block-container{padding:1rem .8rem 2rem!important;}.materials{grid-template-columns:repeat(2,minmax(0,1fr));}.brand{font-size:2rem;}}
</style>
""", unsafe_allow_html=True)

# Cabeçalho construído com colunas reais do Streamlit, sem HTML envolvendo widgets.
logo_col, title_col = st.columns([1, 11], gap="medium", vertical_alignment="center")
with logo_col:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    else:
        st.markdown("## 🔱")
with title_col:
    st.markdown('''<div class="brand">NETUNO VISION</div><div class="tagline">Inteligência Artificial a Serviço dos Manguezais</div><div class="brandmeta">ECOBARREIRA INTELIGENTE · EQUIPE NETUNO · SESI SANTOS · FLL BIOGLOW</div>''', unsafe_allow_html=True)
st.divider()
st.markdown('<div class="section-title">Central de monitoramento ambiental · Mangue São Manoel</div>', unsafe_allow_html=True)

# A IA ainda não foi desenvolvida. Não fabricar resultados.
ocupacao = None
contagens = None
situacao = "AGUARDANDO IA"

st.markdown('<div class="section-title">Visão geral do sistema</div>', unsafe_allow_html=True)
a, b, c, d = st.columns(4, gap="medium")
with a:
    st.metric("Ocupação visual", "—")
with b:
    st.metric("Resíduos identificados", "—")
with c:
    st.metric("Situação", situacao)
with d:
    st.metric("Análise inteligente", "PENDENTE")
st.caption("Sem dados simulados: a ocupação e as contagens serão exibidas após a implementação e validação da IA.")

st.markdown('<div class="section-title">Monitoramento e alertas</div>', unsafe_allow_html=True)
cam_col, alert_col = st.columns([7, 3], gap="large")
with cam_col:
    st.markdown('### 📷 Câmera da ecobarreira')
    camera_url = "https://camera.netunovision.com.br"

    @st.fragment(run_every="5s")
    def show_camera():
        try:
            response = requests.get(camera_url + "/foto", timeout=6)
            response.raise_for_status()
            if not response.headers.get("content-type", "").lower().startswith("image/"):
                raise ValueError("O servidor não retornou uma imagem")
            if len(response.content) > 3_000_000:
                raise ValueError("Imagem acima do limite")
            st.image(response.content, use_container_width=True)
            st.caption("Imagem real da ESP32-CAM · Atualização aproximada a cada 5 segundos")
        except (requests.RequestException, ValueError):
            st.warning("Câmera indisponível. Verifique se a ESP32-CAM, o Flask e o Cloudflare Tunnel estão funcionando.")
    show_camera()
with alert_col:
    st.markdown('### 🚦 Central de alertas')
    st.markdown('''<div class="card" style="text-align:center;min-height:280px"><div class="note" style="letter-spacing:.13em">NÍVEL DE ALERTA</div><div class="lights"><span class="light" style="background:#334155"></span><span class="light" style="background:#334155"></span><span class="light" style="background:#334155"></span></div><div style="font-size:1.45rem;font-weight:850;color:#e2e8f0">AGUARDANDO IA</div><p class="note">Alertas serão ativados somente após o reconhecimento de resíduos e a validação dos limites.</p></div>''', unsafe_allow_html=True)

st.markdown('<div class="section-title">Inteligência artificial e classificação</div>', unsafe_allow_html=True)
st.markdown('### 🧠 Resíduos por material')
st.markdown('''<div class="card"><div class="note">Categorias que o modelo deverá reconhecer:</div><div class="materials"><div class="material"><div class="material-name">Plástico</div><div class="material-value">—</div></div><div class="material"><div class="material-name">Madeira</div><div class="material-value">—</div></div><div class="material"><div class="material-name">Metal</div><div class="material-value">—</div></div><div class="material"><div class="material-name">Outros</div><div class="material-value">—</div></div></div><div class="note">Aguardando treinamento e validação do modelo. Nenhum objeto foi contabilizado automaticamente.</div></div>''', unsafe_allow_html=True)

st.markdown('<div class="section-title">Evolução do monitoramento</div>', unsafe_allow_html=True)
st.markdown('### 📈 Histórico de ocupação visual')

# Estrutura do gráfico pronta, sem inventar dados de ocupação.
# Quando a IA estiver integrada, substituir a lista vazia por medições reais
# no formato {"minuto": 0, "ocupacao": 25.0}.
import altair as alt
medicoes_ocupacao = []
grafico_ocupacao = (
    alt.Chart(alt.Data(values=medicoes_ocupacao))
    .mark_line(color="#38bdf8", strokeWidth=3, point=True)
    .encode(
        x=alt.X("minuto:Q", title="Tempo de monitoramento (min)", scale=alt.Scale(domain=[0, 60])),
        y=alt.Y("ocupacao:Q", title="Ocupação visual (%)", scale=alt.Scale(domain=[0, 100])),
        tooltip=[alt.Tooltip("minuto:Q", title="Minuto"), alt.Tooltip("ocupacao:Q", title="Ocupação (%)")],
    )
    .properties(height=285)
    .configure_view(strokeOpacity=0)
    .configure_axis(labelColor="#cbd5e1", titleColor="#e2e8f0", gridColor="#254660", domainColor="#54718b", tickColor="#54718b")
)
st.altair_chart(grafico_ocupacao, use_container_width=True)

st.markdown('<div class="footer-note">🔱 NETUNO VISION · Inteligência Artificial a Serviço dos Manguezais<br>Equipe Netuno · SESI Santos · FLL BIOGLOW</div>', unsafe_allow_html=True)
