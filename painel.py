
import streamlit as st
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime
from html import escape

# ============================================================
# ECOBARREIRA INTELIGENTE - EQUIPE NETUNO
# SESI SANTOS | FLL BIOGLOW
# ============================================================

st.set_page_config(
    page_title="Ecobarreira Inteligente | Netuno",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PASTA = Path(__file__).parent
LOGO = PASTA / "logo_netuno.png"

# Endereço LOCAL do sensor.
# Para o monitoramento pela internet, será necessária
# uma integração com um serviço acessível na nuvem.
IP_ESP32 = "http://10.225.196.237"

if "historico_real" not in st.session_state:
    st.session_state.historico_real = []


# ============================================================
# IDENTIDADE VISUAL
# ============================================================

st.markdown("""
<style>
    :root {
        --fundo: #07182d;
        --cartao: #102b48;
        --cartao-claro: #143655;
        --borda: #285782;
        --azul: #38bdf8;
        --texto: #f1f5f9;
        --secundario: #cbd5e1;
    }

    header[data-testid="stHeader"],
    [data-testid="stToolbar"] {
        display: none !important;
    }

    #MainMenu, footer {
        visibility: hidden !important;
    }

    .stApp {
        background: var(--fundo);
        color: var(--texto);
    }

    .block-container {
        max-width: 1500px;
        padding: 1.5rem 2rem 3rem;
    }

    h1, h2, h3 {
        color: var(--azul) !important;
    }

    h1 {
        font-size: clamp(1.8rem, 3vw, 2.7rem) !important;
        letter-spacing: 0.02em;
    }

    h3 {
        font-size: 1.4rem !important;
    }

    .stApp p,
    .stApp label,
    .stApp label p,
    .stApp [data-testid="stWidgetLabel"] p,
    .stApp [data-testid="stCaptionContainer"] p {
        color: var(--secundario);
    }

    .stApp [data-testid="stAlert"] {
        background: var(--cartao) !important;
        border: 1px solid var(--borda) !important;
        border-radius: 12px !important;
    }

    .stApp [data-testid="stAlert"] p,
    .stApp [data-testid="stAlert"] div {
        color: #ffffff !important;
    }

    .stApp [data-testid="stAlert"] svg {
        color: var(--azul) !important;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg, #163c60 0%, #102b48 100%
        );
        padding: 22px;
        border: 1px solid var(--borda);
        border-radius: 16px;
        min-height: 130px;
    }

    [data-testid="stMetricLabel"] p {
        color: #cbd5e1 !important;
        font-weight: 500;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: #ffffff !important;
        font-size: clamp(1.2rem, 2vw, 2rem) !important;
        overflow-wrap: anywhere;
    }

    .stApp [data-testid="stExpander"] {
        background: #0d253f;
        border: 1px solid var(--borda);
        border-radius: 12px;
    }

    .stApp [data-testid="stExpander"] summary,
    .stApp [data-testid="stExpander"] summary p {
        color: #f1f5f9 !important;
    }

    .stApp .stButton button {
        background: #0284c7 !important;
        color: white !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 10px !important;
    }

    .stApp .stButton button p {
        color: white !important;
    }

    .stApp [data-testid="stSelectbox"] > div > div,
    .stApp [data-testid="stNumberInput"] input {
        background: #f1f5f9 !important;
        color: #0f172a !important;
        border-radius: 8px;
    }

    .stApp hr {
        border-color: #284766;
        opacity: 0.65;
    }

    .netuno-subtitulo {
        font-size: 1rem;
        color: #f1f5f9;
        font-weight: 600;
        margin: 0.2rem 0 0.4rem;
    }

    .netuno-local {
        font-size: 0.88rem;
        color: #94a3b8;
    }

    .netuno-faixa {
        background: linear-gradient(
            90deg, #10365a, #0c2945
        );
        border: 1px solid #285782;
        border-left: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 14px 18px;
        color: #f1f5f9;
        margin: 8px 0 16px;
    }

    .netuno-status {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #102b48;
        border: 1px solid #285782;
        border-radius: 12px;
        padding: 16px 18px;
        color: #f1f5f9;
        min-height: 72px;
        margin-bottom: 8px;
    }

    .netuno-status strong {
        color: #ffffff;
        font-size: 0.98rem;
    }

    .netuno-status small {
        color: #cbd5e1;
        display: block;
        margin-top: 3px;
    }

    .netuno-indicador {
        width: 12px;
        height: 12px;
        min-width: 12px;
        border-radius: 50%;
        box-shadow: 0 0 12px currentColor;
    }

    .netuno-video {
        background: linear-gradient(
            145deg, #06101f, #0c2540
        );
        border: 1px solid #285782;
        border-radius: 16px;
        min-height: 320px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 25px;
        text-align: center;
        color: #e2e8f0;
    }

    .netuno-alerta {
        background: linear-gradient(
            145deg, #143655, #102b48
        );
        border: 1px solid #285782;
        border-radius: 16px;
        min-height: 320px;
        padding: 26px 18px;
        text-align: center;
        color: #e2e8f0;
    }

    .netuno-semaforo {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 28px 0 24px;
    }

    .netuno-luz {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: 2px solid #64748b;
    }

    .netuno-rodape {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        padding: 12px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.8rem 2rem;
        }

        h1 {
            font-size: 1.7rem !important;
        }

        [data-testid="stMetric"] {
            min-height: 110px;
            padding: 14px;
        }

        .netuno-video,
        .netuno-alerta {
            min-height: 260px;
        }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# CABEÇALHO
# ============================================================

col_logo, col_titulo, col_modo = st.columns(
    [1, 5, 2],
    vertical_alignment="center"
)

with col_logo:
    if LOGO.exists():
        st.image(str(LOGO), width=120)
    else:
        st.markdown("## 🔱")

with col_titulo:
    st.title("ECOBARREIRA INTELIGENTE")
    st.markdown(
        '<div class="netuno-subtitulo">'
        'Equipe Netuno | SESI Santos | FLL BIOGLOW'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="netuno-local">'
        'Central de Monitoramento Ambiental • Mangue São Manoel'
        '</div>',
        unsafe_allow_html=True
    )

with col_modo:
    modo = st.selectbox(
        "Modo de operação",
        ["Demonstração", "Monitoramento Real"]
    )

st.divider()


# ============================================================
# CLASSIFICAÇÃO DO NÍVEL DE RESÍDUOS
# ============================================================

def classificar(nivel, conectado):
    if not conectado:
        return (
            "SEM LEITURA",
            "#94a3b8",
            "Sensor sem comunicação. Verifique a conexão."
        )

    if nivel is None:
        return (
            "AGUARDANDO CALIBRAÇÃO",
            "#38bdf8",
            "Sensor conectado. O nível de acúmulo "
            "ainda precisa ser calibrado."
        )

    if nivel < 40:
        return (
            "NORMAL",
            "#22c55e",
            "Acúmulo de resíduos dentro do esperado."
        )

    if nivel < 75:
        return (
            "ATENÇÃO",
            "#facc15",
            "O acúmulo de resíduos está aumentando. "
            "Recomenda-se acompanhamento."
        )

    return (
        "CRÍTICO",
        "#ef4444",
        "Acúmulo elevado. Recomenda-se avaliar "
        "a necessidade de retirada dos resíduos."
    )


# ============================================================
# CARTÃO DE STATUS
# ============================================================

def mostrar_status(titulo, detalhe, cor):
    titulo = escape(titulo)
    detalhe = escape(detalhe)

    st.markdown(
        f"""
        <div class="netuno-status">
            <span class="netuno-indicador"
                  style="background:{cor};color:{cor};">
            </span>
            <div>
                <strong>{titulo}</strong>
                <small>{detalhe}</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAINEL PRINCIPAL
# ============================================================

def mostrar_painel(
    distancia,
    nivel,
    conectado,
    horario,
    modo_atual
):
    situacao, cor, mensagem = classificar(
        nivel, conectado
    )

    # STATUS DO SISTEMA
    st.subheader("📡 Status do sistema")

    col_sensor, col_camera_status = st.columns(
        2, gap="medium"
    )

    with col_sensor:
        if modo_atual == "Demonstração":
            mostrar_status(
                "Sensor de resíduos",
                "Modo demonstração • Dados simulados",
                "#38bdf8"
            )
        elif conectado:
            mostrar_status(
                "Sensor de resíduos",
                "Online • Recebendo medições",
                "#22c55e"
            )
        else:
            mostrar_status(
                "Sensor de resíduos",
                "Offline • Sem comunicação",
                "#ef4444"
            )

    with col_camera_status:
        mostrar_status(
            "Câmera de monitoramento",
            "Aguardando integração do vídeo",
            "#94a3b8"
        )

    st.divider()

    # INDICADORES
    st.subheader("📊 Indicadores ambientais")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Distância medida",
            f"{distancia:.1f} cm"
            if distancia is not None else "—"
        )

    with c2:
        st.metric(
            "Acúmulo estimado",
            f"{nivel}%"
            if nivel is not None else "Não calibrado"
        )

    with c3:
        st.metric("Situação", situacao)

    with c4:
        st.metric("Última leitura", horario)

    st.divider()

    # CÂMERA E CENTRAL DE ALERTAS
    col_camera, col_alerta = st.columns(
        [3, 2],
        gap="large"
    )

    with col_camera:
        st.subheader("📷 Câmera de monitoramento")

        st.markdown(
            """
            <div class="netuno-video">
                <div style="font-size:52px;">📷</div>
                <div style="
                    font-size:20px;
                    font-weight:700;
                    margin-top:10px;
                    color:#ffffff;
                ">
                    Monitoramento por imagem
                </div>
                <div style="
                    font-size:14px;
                    margin-top:10px;
                    color:#cbd5e1;
                ">
                    Transmissão em tempo real
                    ainda não disponível.
                </div>
                <div style="
                    margin-top:20px;
                    padding:8px 15px;
                    background:#173654;
                    border:1px solid #285782;
                    border-radius:20px;
                    font-size:12px;
                    color:#cbd5e1;
                ">
                    Aguardando conexão da câmera
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_alerta:
        st.subheader("🚦 Central de alertas")

        verde = (
            "#22c55e"
            if situacao == "NORMAL" else "#334155"
        )

        amarelo = (
            "#facc15"
            if situacao == "ATENÇÃO" else "#334155"
        )

        vermelho = (
            "#ef4444"
            if situacao == "CRÍTICO" else "#334155"
        )

        st.markdown(
            f"""
            <div class="netuno-alerta">
                <div style="
                    color:#cbd5e1;
                    font-size:13px;
                    letter-spacing:1px;
                ">
                    NÍVEL DE ALERTA
                </div>

                <div class="netuno-semaforo">
                    <div class="netuno-luz"
                         style="background:{verde};"></div>
                    <div class="netuno-luz"
                         style="background:{amarelo};"></div>
                    <div class="netuno-luz"
                         style="background:{vermelho};"></div>
                </div>

                <div style="
                    color:{cor};
                    font-size:clamp(19px,2vw,29px);
                    font-weight:800;
                    overflow-wrap:anywhere;
                    margin-bottom:15px;
                ">
                    {escape(situacao)}
                </div>

                <div style="
                    color:#e2e8f0;
                    font-size:15px;
                    line-height:1.6;
                ">
                    {escape(mensagem)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # HISTÓRICO
    st.subheader("📈 Histórico de monitoramento")

    if modo_atual == "Demonstração":
        historico = pd.DataFrame({
            "Horário": [
                "08h", "09h", "10h", "11h", "12h"
            ],
            "Acúmulo (%)": [
                12, 18, 25, 32, nivel
            ]
        })

        st.line_chart(
            historico.set_index("Horário"),
            y="Acúmulo (%)"
        )

        st.caption(
            "Gráfico demonstrativo com dados simulados. "
            "Não representa medições reais do mangue."
        )

    else:
        registros = st.session_state.historico_real

        if registros:
            tabela = pd.DataFrame(registros)
            tabela["Horário"] = pd.to_datetime(
                tabela["Horário"]
            )
            tabela = tabela.set_index("Horário")

            st.line_chart(
                tabela,
                y="Distância (cm)"
            )

            st.caption(
                "Histórico das medições recebidas "
                "nesta sessão. Os dados ainda não "
                "são salvos permanentemente."
            )
        else:
            st.info(
                "Aguardando medições reais para "
                "formar o histórico."
            )

    st.divider()

    st.markdown(
        """
        <div class="netuno-rodape">
            🔱 Equipe Netuno • SESI Santos<br>
            Projeto de Inovação • FLL BIOGLOW<br>
            Ecobarreira Inteligente — Monitoramento Ambiental
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MODO DEMONSTRAÇÃO
# ============================================================

if modo == "Demonstração":

    st.markdown(
        """
        <div class="netuno-faixa">
            <strong>🧪 MODO DEMONSTRAÇÃO</strong><br>
            Os valores apresentados são simulados
            para demonstrar o funcionamento do sistema.
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander(
        "⚙️ Configurações de demonstração",
        expanded=False
    ):
        nivel_demo = st.slider(
            "Simular acúmulo de resíduos (%)",
            min_value=0,
            max_value=100,
            value=42
        )

        distancia_demo = st.number_input(
            "Distância simulada (cm)",
            min_value=0.0,
            max_value=400.0,
            value=15.0
        )

    mostrar_painel(
        distancia=distancia_demo,
        nivel=nivel_demo,
        conectado=True,
        horario=datetime.now().strftime("%H:%M:%S"),
        modo_atual="Demonstração"
    )


# ============================================================
# MONITORAMENTO REAL
# ============================================================

else:

    st.markdown(
        """
        <div class="netuno-faixa">
            <strong>📡 MONITORAMENTO REAL</strong><br>
            Tentativa de atualização a cada 5 segundos.
            A conexão com o sensor ainda depende de
            integração com a internet.
        </div>
        """,
        unsafe_allow_html=True
    )

    @st.fragment(run_every="5s")
    def atualizar_monitoramento():

        distancia = None
        conectado = False
        horario = "—"

        try:
            resposta = requests.get(
                IP_ESP32,
                timeout=2
            )

            resposta.raise_for_status()
            dados = resposta.json()

            if (
                dados.get("sensor") == "ok"
                and dados.get("distancia_cm") is not None
            ):
                distancia = float(
                    dados["distancia_cm"]
                )

                conectado = True
                horario = datetime.now().strftime(
                    "%H:%M:%S"
                )

                st.session_state.historico_real.append({
                    "Horário": datetime.now(),
                    "Distância (cm)": distancia
                })

                st.session_state.historico_real = (
                    st.session_state.historico_real[-300:]
                )

        except (
            requests.RequestException,
            ValueError,
            TypeError
        ):
            conectado = False

        # Sem calibração, não calculamos
        # um percentual de acúmulo real.
        mostrar_painel(
            distancia=distancia,
            nivel=None,
            conectado=conectado,
            horario=horario,
            modo_atual="Monitoramento Real"
        )

    atualizar_monitoramento()
