from pathlib import Path
from datetime import datetime
import hashlib
from zoneinfo import ZoneInfo

import requests
import streamlit as st
import altair as alt

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
.compact-card {min-height:220px;display:flex;flex-direction:column;justify-content:center;}
.status-subtitle {font-size:.78rem;letter-spacing:.12em;color:#dbeafe;text-align:center;}
.occupancy-number {font-size:2.6rem;font-weight:850;color:#fff;text-align:center;margin:12px 0;}
.occupancy-track {height:12px;background:#294863;border-radius:99px;margin:6px 0 14px;overflow:hidden;}
.occupancy-fill {width:0%;height:100%;background:#38bdf8;border-radius:99px;}
.live-pill {display:inline-flex;align-items:center;gap:7px;background:#103c34;border:1px solid #287b61;border-radius:30px;color:#85f3bd;font-size:.76rem;font-weight:800;letter-spacing:.08em;padding:5px 11px;}
.live-dot {width:8px;height:8px;background:#5ee9a4;border-radius:50%;box-shadow:0 0 10px #5ee9a4;}
.camera-caption {color:#bdd3e5;font-size:.8rem;margin:7px 0 0;}
.system-card {background:linear-gradient(140deg,#102e4d,#0b233e);border:1px solid #285578;border-radius:17px;padding:20px 22px;}
.system-row {padding:13px 0;border-bottom:1px solid #294b68;}
.system-row:last-child {border-bottom:0;}
.system-label {font-size:.77rem;color:#a9c7dc;letter-spacing:.04em;margin-bottom:5px;}
.system-value {color:#f4faff;font-weight:650;font-size:.97rem;overflow-wrap:anywhere;}
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

st.markdown('<div class="section-title">Monitoramento e alertas</div>', unsafe_allow_html=True)
# Câmera à esquerda e informações do sistema à direita.
# A imagem mais recente é obtida diretamente do Cloudflare Worker/R2.
# O ESP32-CAM envia uma nova imagem aproximadamente a cada 60 segundos.
CAMERA_URL = "https://netuno-camera.professorrobsonluiz.workers.dev/foto"
cam_col, info_col = st.columns([3, 2], gap="large")

with cam_col:
    tab_fotos, tab_ao_vivo = st.tabs(["📷 Fotografias automáticas", "🎥 Câmera ao vivo"])

    with tab_fotos:
        @st.fragment(run_every="15s")
        def show_camera():
            st.markdown("### Última fotografia da ecobarreira")
            try:
                response = requests.get(
                    CAMERA_URL,
                    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
                    params={"t": int(datetime.now().timestamp())},
                    timeout=12,
                )
                response.raise_for_status()
                if not response.headers.get("content-type", "").lower().startswith("image/"):
                    raise ValueError("O servidor não retornou uma imagem")
                if not response.content or len(response.content) > 3_000_000:
                    raise ValueError("Imagem vazia ou acima do limite de 3 MB")

                assinatura = hashlib.sha256(response.content).hexdigest()
                agora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%H:%M:%S")
                if st.session_state.get("ultima_assinatura_camera") != assinatura:
                    st.session_state["ultima_assinatura_camera"] = assinatura
                    st.session_state["ultima_mudanca_camera"] = agora
                    st.session_state["mudanca_observada_camera"] = (
                        st.session_state.get("camera_ja_consultada", False)
                    )
                st.session_state["camera_ja_consultada"] = True

                st.image(response.content, use_container_width=True)
                if st.session_state.get("mudanca_observada_camera", False):
                    st.caption(
                        "Nova imagem detectada neste painel às "
                        f"{st.session_state['ultima_mudanca_camera']} (horário de Brasília). "
                        "Verificação a cada 15 segundos."
                    )
                else:
                    st.caption(
                        "Última fotografia armazenada. O horário da captura não está disponível. "
                        "Verificação a cada 15 segundos."
                    )
                st.caption("Uma fotografia armazenada pode continuar visível mesmo com a câmera desligada.")
            except (requests.RequestException, ValueError):
                st.warning("Não foi possível carregar a fotografia. Verifique a conexão da câmera.")

        show_camera()

    with tab_ao_vivo:
        st.markdown("### Transmissão ao vivo")
        st.info(
            "A câmera transmite vídeo na rede Wi-Fi local. Para assistir pela internet "
            "de qualquer lugar, ainda será necessário configurar um serviço de transmissão. "
            "As fotografias automáticas já funcionam remotamente."
        )
        # O endereço é da ESP32-CAM na rede do hotspot e pode mudar.
        # Um link HTTP aberto em outra aba evita tentar embutir conteúdo inseguro
        # (HTTP) dentro da página pública HTTPS do Streamlit.
        endereco_local = st.text_input(
            "Endereço IP local da ESP32-CAM",
            value="10.202.149.175",
            help="Confira o IP no Monitor Serial quando conectar a câmera ao hotspot.",
        ).strip()
        import ipaddress
        try:
            ipaddress.IPv4Address(endereco_local)
            url_camera_local = f"http://{endereco_local}/"
            st.link_button("🎥 Abrir câmera ao vivo (mesma rede Wi-Fi)", url_camera_local)
            st.caption(
                "Abra pelo dispositivo conectado à mesma rede da ESP32-CAM. "
                "Na página da câmera, clique em Start Stream. "
                "O endereço pode mudar após reiniciar o hotspot."
            )
        except ipaddress.AddressValueError:
            st.warning("Informe um endereço IPv4 válido da ESP32-CAM.")

with info_col:
    st.markdown("### 🌿 Monitoramento ambiental")
    st.markdown('''<div class="system-card">
      <div class="system-row"><div class="system-label">MONITORAMENTO POR CÂMERA</div><div class="system-value">Captura automática de imagens a cada 60 segundos</div></div>
      <div class="system-row"><div class="system-label">ACOMPANHAMENTO REMOTO</div><div class="system-value">Fotografias disponíveis pela internet</div></div>
      <div class="system-row"><div class="system-label">INTELIGÊNCIA ARTIFICIAL</div><div class="system-value">Identificação de resíduos em desenvolvimento</div></div>
      <div class="system-row"><div class="system-label">ÁREA DE MONITORAMENTO</div><div class="system-value">Mangue São Manoel · Baixada Santista</div></div>
      <div class="system-row"><div class="system-label">OBJETIVO AMBIENTAL</div><div class="system-value">Acompanhar o acúmulo de resíduos e apoiar ações de limpeza</div></div>
    </div>''', unsafe_allow_html=True)
    st.caption("As fotografias não comprovam que a câmera esteja conectada neste instante.")

alert_column, occupancy_column = st.columns(2, gap="medium")
with alert_column:
    st.markdown('### 🚦 Central de alertas')
    st.markdown('''<div class="card compact-card" style="text-align:center">
      <div class="status-subtitle">NÍVEL DE ALERTA</div>
      <div class="lights"><span class="light" style="background:#334155"></span><span class="light" style="background:#334155"></span><span class="light" style="background:#334155"></span></div>
      <div style="font-size:1.35rem;font-weight:850;color:#fff">AGUARDANDO IA</div>
      <p class="note">Alertas disponíveis após implementação da IA e validação dos limites.</p>
    </div>''', unsafe_allow_html=True)
with occupancy_column:
    st.markdown('### 📊 Ocupação visual')
    st.markdown('''<div class="card compact-card">
      <div class="status-subtitle">SUPERFÍCIE VISÍVEL OCUPADA</div>
      <div class="occupancy-number">—%</div>
      <div class="occupancy-track"><div class="occupancy-fill"></div></div>
      <div class="note" style="text-align:center">Aguardando medições reais da inteligência artificial.</div>
    </div>''', unsafe_allow_html=True)

st.markdown('<div class="section-title">Inteligência artificial e classificação</div>', unsafe_allow_html=True)
st.markdown('### 🧠 Resíduos por material')
st.markdown('''<div class="card"><div class="note">Categorias que o modelo deverá reconhecer:</div><div class="materials"><div class="material"><div class="material-name">Plástico</div><div class="material-value">—</div></div><div class="material"><div class="material-name">Madeira</div><div class="material-value">—</div></div><div class="material"><div class="material-name">Metal</div><div class="material-value">—</div></div><div class="material"><div class="material-name">Outros</div><div class="material-value">—</div></div></div><div class="note">Aguardando treinamento e validação do modelo. Nenhum objeto foi contabilizado automaticamente.</div></div>''', unsafe_allow_html=True)

st.markdown('<div class="section-title">Evolução do monitoramento</div>', unsafe_allow_html=True)
st.markdown('### 📈 Histórico de ocupação visual')

# Não há resultados da IA ainda: o gráfico fica vazio, sem valores inventados.
# No futuro, as medições reais poderão ser fornecidas no formato:
# {"minuto": 15, "ocupacao": 37.5}
medicoes_ocupacao = []

grafico_ocupacao = (
    alt.Chart(alt.Data(values=medicoes_ocupacao))
    .mark_line(color="#38bdf8", strokeWidth=3, point=True)
    .encode(
        x=alt.X(
            "minuto:Q",
            title="Tempo de monitoramento (min)",
            scale=alt.Scale(domain=[0, 60]),
            axis=alt.Axis(values=[0, 15, 30, 45, 60], grid=False, labelAngle=0),
        ),
        y=alt.Y(
            "ocupacao:Q",
            title="Ocupação visual (%)",
            scale=alt.Scale(domain=[0, 100]),
            axis=alt.Axis(values=[0, 25, 50, 75, 100], grid=True, format=".0f"),
        ),
        tooltip=[
            alt.Tooltip("minuto:Q", title="Minuto"),
            alt.Tooltip("ocupacao:Q", title="Ocupação (%)", format=".1f"),
        ],
    )
    .properties(height=230, background="#0b233e")
    .configure_view(strokeOpacity=0)
    .configure_axis(
        labelColor="#ffffff",
        titleColor="#ffffff",
        gridColor="#ffffff",
        gridOpacity=0.20,
        domainColor="#ffffff",
        domainOpacity=0.55,
        tickColor="#ffffff",
        labelFontSize=12,
        titleFontSize=12,
        labelPadding=9,
    )
)
st.altair_chart(grafico_ocupacao, use_container_width=True, theme=None)

st.markdown('<div class="footer-note">🔱 NETUNO VISION · Inteligência Artificial a Serviço dos Manguezais<br>Equipe Netuno · SESI Santos · FLL BIOGLOW</div>', unsafe_allow_html=True)
