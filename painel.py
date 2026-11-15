import streamlit as st
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime
from html import escape

st.set_page_config(page_title='NETUNO VISION | Ecobarreira Inteligente', page_icon='🔱', layout='wide', initial_sidebar_state='collapsed')
LOGO = Path(__file__).parent / 'logo_netuno.png'
# URL pública temporária do Flask. Atualize quando reiniciar o Cloudflare.
CAMERA_URL = 'https://tenant-instructors-suse-cake.trycloudflare.com'
# A IA ainda não foi treinada. Quando houver API, configure o endpoint abaixo.
IA_API_URL = ''

st.markdown('''<style>
.stApp{background:#07182d;color:#e2e8f0}.block-container{max-width:1450px;padding:1.6rem 2rem 3rem}
h1,h2,h3{color:#38bdf8!important}[data-testid="stMetric"]{background:#102b48;border:1px solid #285782;border-radius:14px;padding:18px}
[data-testid="stMetricLabel"] p{color:#cbd5e1!important}[data-testid="stMetricValue"]{color:white!important}
.hero{background:linear-gradient(115deg,#0d355a,#07182d);border:1px solid #285782;border-radius:18px;padding:22px;margin-bottom:15px}
.hero h1{margin:0;font-size:2.4rem!important}.subtitle{font-size:1.1rem;color:#e2e8f0;margin:4px 0}.small{color:#94a3b8;font-size:.9rem}
.panel{background:#102b48;border:1px solid #285782;border-radius:14px;padding:18px;color:#e2e8f0}
.lights{display:flex;gap:20px;justify-content:center;padding:12px}.light{width:43px;height:43px;border-radius:50%;border:2px solid #64748b}
</style>''',unsafe_allow_html=True)

c_logo,c_title=st.columns([1,7],vertical_alignment='center')
with c_logo:
    if LOGO.exists(): st.image(str(LOGO),width=110)
    else: st.markdown('## 🔱')
with c_title:
    st.markdown('''<div class="hero"><h1>NETUNO VISION</h1><div class="subtitle">Inteligência Artificial a Serviço dos Manguezais</div><div class="small">Ecobarreira Inteligente • Equipe Netuno • SESI Santos • FLL BIOGLOW</div></div>''',unsafe_allow_html=True)

modo=st.selectbox('Modo de operação',['Demonstração','Monitoramento Real'])
st.caption('A IA ainda está em desenvolvimento. Os dados de demonstração são fictícios; nenhuma classificação real foi validada.')

if modo=='Demonstração':
    st.info('🧪 MODO DEMONSTRAÇÃO — valores simulados, não representam análise da câmera.')
    with st.expander('Ajustar simulação',expanded=False):
        plastico=st.slider('Plástico (objetos)',0,50,18)
        madeira=st.slider('Madeira (objetos)',0,50,11)
        metal=st.slider('Metal (objetos)',0,50,4)
        outros=st.slider('Outros (objetos)',0,50,7)
        ocupacao=st.slider('Ocupação visual simulada (%)',0,100,42)
    contagens={'Plástico':plastico,'Madeira':madeira,'Metal':metal,'Outros':outros}
    fonte='Simulação'
else:
    st.warning('📡 MONITORAMENTO REAL — câmera disponível quando o servidor estiver ligado. A classificação por IA ficará indisponível até treinarmos e conectarmos um modelo validado.')
    contagens=None
    ocupacao=None
    fonte='IA ainda não integrada'
    if IA_API_URL:
        try:
            r=requests.get(IA_API_URL,timeout=5)
            r.raise_for_status()
            dados=r.json()
            # Contrato esperado da API de IA: contagens por categoria e ocupacao_visual_pct.
            categorias=dados.get('contagens',{})
            valor=dados.get('ocupacao_visual_pct')
            if all(isinstance(categorias.get(k),int) and categorias[k]>=0 for k in ('Plástico','Madeira','Metal','Outros')) and isinstance(valor,(int,float)) and 0<=valor<=100:
                contagens={k:categorias[k] for k in ('Plástico','Madeira','Metal','Outros')}
                ocupacao=float(valor)
                fonte='Análise automática (ainda requer validação)'
        except (requests.RequestException,ValueError,TypeError):
            st.warning('Não foi possível receber dados da IA.')

if ocupacao is None:
    situacao='SEM ANÁLISE'
    cor='#64748b'
else:
    situacao='NORMAL' if ocupacao<40 else 'ATENÇÃO' if ocupacao<75 else 'CRÍTICO'
    cor={'NORMAL':'#22c55e','ATENÇÃO':'#facc15','CRÍTICO':'#ef4444'}[situacao]

st.subheader('📊 Indicadores ambientais')
a,b,c,d=st.columns(4)
a.metric('Ocupação visual estimada',f'{ocupacao:.0f}%' if ocupacao is not None else '—')
b.metric('Resíduos identificados',sum(contagens.values()) if contagens is not None else '—')
c.metric('Situação',situacao)
d.metric('Origem dos dados',fonte)
st.caption('Ocupação visual = proporção da região observada coberta por resíduos visíveis; não equivale à capacidade total da ecobarreira.')

cam,alerta=st.columns([3,2],gap='large')
with cam:
    st.subheader('📷 Câmera da ecobarreira')
    @st.fragment(run_every='5s')
    def foto_ao_vivo():
        try:
            resposta=requests.get(CAMERA_URL.rstrip('/')+'/foto',timeout=5)
            resposta.raise_for_status()
            if not resposta.headers.get('Content-Type','').lower().startswith('image/'):
                raise ValueError('O servidor não retornou imagem')
            st.image(resposta.content,use_container_width=True)
            st.caption('Fotografia atualizada aproximadamente a cada 5 segundos. Não é vídeo contínuo.')
        except (requests.RequestException,ValueError):
            st.info('Câmera indisponível. Verifique o Flask, o Cloudflare e o endereço CAMERA_URL.')
    foto_ao_vivo()
with alerta:
    st.subheader('🚦 Central de alertas')
    verde='#22c55e' if situacao=='NORMAL' else '#334155'
    amarelo='#facc15' if situacao=='ATENÇÃO' else '#334155'
    vermelho='#ef4444' if situacao=='CRÍTICO' else '#334155'
    st.markdown(f'''<div class="panel"><div style="text-align:center">NÍVEL DE ALERTA</div><div class="lights"><div class="light" style="background:{verde}"></div><div class="light" style="background:{amarelo}"></div><div class="light" style="background:{vermelho}"></div></div><h2 style="text-align:center;color:{cor}!important">{escape(situacao)}</h2><p style="text-align:center">{'Exemplo demonstrativo. Limites de alerta provisórios.' if modo=='Demonstração' else 'Aguardando resultados da IA para gerar alertas.' if ocupacao is None else 'Estimativa automática; exige validação antes de uso operacional.'}</p></div>''',unsafe_allow_html=True)

st.divider()
st.subheader('🧠 Análise inteligente de resíduos')
if contagens is None:
    st.info('Ainda não existem contagens reais. Vamos treinar a IA para reconhecer plástico, madeira, metal e outros materiais.')
else:
    df=pd.DataFrame({'Material':list(contagens),'Objetos identificados':list(contagens.values())})
    st.bar_chart(df.set_index('Material'),y='Objetos identificados')
    st.caption('Contagem de objetos visíveis, não massa ou volume. Dados simulados.' if modo=='Demonstração' else 'Resultados automáticos sujeitos a validação.')

st.subheader('📈 Histórico de ocupação visual')
if modo=='Demonstração':
    df_hist=pd.DataFrame({'Horário':['08h','09h','10h','11h','12h'],'Ocupação visual (%)':[12,18,25,32,ocupacao]})
    st.line_chart(df_hist.set_index('Horário'))
    st.caption('Histórico fictício para demonstração.')
else:
    st.info('O histórico real será habilitado quando o processamento de IA estiver integrado e armazenando medições.')

st.divider()
st.markdown('<div style="text-align:center;color:#94a3b8">🔱 NETUNO VISION • Equipe Netuno • SESI Santos • Projeto de Inovação FLL BIOGLOW</div>',unsafe_allow_html=True)
