
import streamlit as st
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Ecobarreira Inteligente | Netuno",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PASTA = Path(__file__).parent
LOGO = PASTA / "logo_netuno.png"

# IP local do ESP32 no Wi-Fi do Cubot.
# Atualize caso o endereço mude.
IP_ESP32 = "http://10.225.196.237"

# HISTÓRICO DESTA SESSÃO
if "historico_real" not in st.session_state:
    st.session_state.historico_real = []

# ESTILO
st.markdown("""
<style>
.stApp {
    background: #07182d;
    color: #e2e8f0;
}
.block-container {
    max-width: 95%;
    padding: 1.4rem 2rem 3rem;
}
h1, h2, h3 {
    color: #38bdf8 !important;
}
.stApp label,
.stApp label p,
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stCaptionContainer"] p {
    color: #cbd5e1 !important;
}
.stApp [data-testid="stAlert"] p {
    color: #e2e8f0 !important;
}
[data-testid="stMetric"] {
    background: #123456;
    padding: 18px;
    border: 1px solid #2563eb;
    border-radius: 14px;
}
[data-testid="stMetricLabel"] p {
    color: #e2e8f0 !important;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #ffffff !important;
}
.stApp .stButton button {
    background: #0284c7 !important;
    color: #ffffff !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
}
.stApp .stButton button p {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# CABEÇALHO
col_logo, col_titulo, col_modo = st.columns([1, 5, 2])

with col_logo:
    if LOGO.exists():
        st.image(str(LOGO), width=125)
    else:
        st.write("🔱")

with col_titulo:
    st.title("ECOBARREIRA INTELIGENTE")
    st.markdown("**Equipe Netuno | SESI Santos | FLL BIOGLOW**")
    st.caption(
        "Central de Monitoramento Ambiental • Mangue São Manoel"
    )

with col_modo:
    modo = st.selectbox(
        "Modo de operação",
        ["Demonstração", "Monitoramento Real"]
    )

st.divider()


def classificar(nivel, conectado):
    if not conectado:
        return (
            "SEM LEITURA",
            "#64748b",
            "Verificar sensor ou comunicação com o ESP32."
        )

    if nivel is None:
        return (
            "AGUARDANDO CALIBRAÇÃO",
            "#38bdf8",
            "Distância recebida. Acúmulo ainda não calibrado."
        )

    if nivel < 40:
        return (
            "NORMAL",
            "#22c55e",
            "Nível de resíduos dentro do esperado."
        )

    if nivel < 75:
        return (
            "ATENÇÃO",
            "#facc15",
            "Acompanhar o acúmulo de resíduos."
        )

    return (
        "CRÍTICO",
        "#ef4444",
        "Solicitar avaliação para retirada dos resíduos."
    )


def mostrar_painel(distancia, nivel, conectado, horario, modo_atual):
    situacao, cor, mensagem = classificar(nivel, conectado)

    # STATUS DOS EQUIPAMENTOS
    st.subheader("📡 Status dos equipamentos")

    col_sensor, col_camera_status = st.columns(2)

    with col_sensor:
        if modo_atual == "Demonstração":
            st.info("ESP32 | Dados simulados")
        elif conectado:
            st.success("🟢 ESP32 | Comunicação ativa")
        else:
            st.error("🔴 ESP32 | Sem comunicação")

    with col_camera_status:
        st.info("📷 ESP32-CAM | Aguardando integração")

    st.divider()

    # MÉTRICAS
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

    # CÂMERA E ALERTA
    col_camera, col_alerta = st.columns([3, 2], gap="large")

    with col_camera:
        st.subheader("📷 Câmera de monitoramento")
        st.markdown("""
        <div style="
            background:#06101f;
            border:1px solid #2563eb;
            border-radius:14px;
            height:300px;
            display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:column;
            color:#94a3b8;
        ">
            <div style="font-size:45px;">📷</div>
            <div>ESP32-CAM</div>
            <div style="font-size:13px;">
                Aguardando integração do vídeo
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_alerta:
        st.subheader("🚦 Central de alertas")

        verde = "#22c55e" if situacao == "NORMAL" else "#334155"
        amarelo = "#facc15" if situacao == "ATENÇÃO" else "#334155"
        vermelho = "#ef4444" if situacao == "CRÍTICO" else "#334155"

        st.markdown(f"""
        <div style="
            background:#123456;
            border:1px solid #2563eb;
            border-radius:14px;
            min-height:300px;
            padding:25px;
            text-align:center;
        ">
            <div style="
                display:flex;
                justify-content:center;
                gap:18px;
                margin:25px 0;
            ">
                <div style="
                    width:43px;height:43px;border-radius:50%;
                    background:{verde};
                "></div>
                <div style="
                    width:43px;height:43px;border-radius:50%;
                    background:{amarelo};
                "></div>
                <div style="
                    width:43px;height:43px;border-radius:50%;
                    background:{vermelho};
                "></div>
            </div>
            <h2 style="color:{cor} !important;">{situacao}</h2>
            <p style="color:#e2e8f0;">{mensagem}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # HISTÓRICO
    st.subheader("📊 Histórico de monitoramento")

    if modo_atual == "Demonstração":
        historico = pd.DataFrame({
            "Horário": ["08h", "09h", "10h", "11h", "12h"],
            "Acúmulo (%)": [12, 18, 25, 32, nivel]
        })

        st.line_chart(
            historico.set_index("Horário"),
            y="Acúmulo (%)"
        )

        st.caption("Gráfico demonstrativo com dados simulados.")

    else:
        registros = st.session_state.historico_real

        if registros:
            tabela = pd.DataFrame(registros)
            tabela["Horário"] = pd.to_datetime(tabela["Horário"])
            tabela = tabela.set_index("Horário")

            st.line_chart(
                tabela,
                y="Distância (cm)"
            )

            st.caption(
                "Histórico de distâncias reais desta sessão. "
                "Os dados ainda não são salvos em arquivo."
            )
        else:
            st.info("Aguardando medições reais para formar o gráfico.")

    st.divider()
    st.caption(
        "Equipe Netuno • SESI Santos • "
        "Projeto de Inovação FLL BIOGLOW"
    )


# MODO DEMONSTRAÇÃO
if modo == "Demonstração":
    st.info("MODO DEMONSTRAÇÃO — os valores são simulados.")

    with st.expander(
        "⚙️ Configurações de demonstração",
        expanded=False
    ):
        nivel_demo = st.slider(
            "Simular acúmulo de resíduos (%)",
            0, 100, 42
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


# MONITORAMENTO REAL
else:
    st.caption("MONITORAMENTO REAL — atualização a cada 5 segundos")

    @st.fragment(run_every="5s")
    def atualizar_monitoramento():
        distancia = None
        conectado = False
        horario = "—"

        try:
            resposta = requests.get(IP_ESP32, timeout=2)
            resposta.raise_for_status()
            dados = resposta.json()

            if (
                dados.get("sensor") == "ok"
                and dados.get("distancia_cm") is not None
            ):
                distancia = float(dados["distancia_cm"])
                conectado = True
                horario = datetime.now().strftime("%H:%M:%S")

                st.session_state.historico_real.append({
                    "Horário": datetime.now(),
                    "Distância (cm)": distancia
                })

                # Mantém as últimas 300 leituras na memória.
                st.session_state.historico_real = (
                    st.session_state.historico_real[-300:]
                )

        except (requests.RequestException, ValueError, TypeError):
            conectado = False

        # Sem calibração, não estimamos percentual.
        mostrar_painel(
            distancia=distancia,
            nivel=None,
            conectado=conectado,
            horario=horario,
            modo_atual="Monitoramento Real"
        )

    atualizar_monitoramento()
