import os
import requests
import pandas as pd
import altair as alt
import streamlit as st
import streamlit.components.v1 as components

# URL do backend (via docker-compose)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5000')

st.set_page_config(page_title='Monitoramento de Tráfego de Rede', layout='wide')
st.title('Monitoramento de Tráfego de Rede')

# 1) Registro de Dispositivo
st.markdown('---')
st.subheader('Registro de Dispositivo')
ip = st.text_input('Endereço IP')
nome = st.text_input('Nome do dispositivo')
trafego = st.number_input('Taxa de tráfego (Mbps)', min_value=0.0)
if st.button('Registrar'):
    resp = requests.post(f'{BACKEND_URL}/devices',
                         json={'ip': ip, 'nome': nome, 'trafego': trafego})
    if resp.status_code == 201:
        st.success('✅ Dispositivo registrado!')
        components.html("<script>window.top.location.reload();</script>", height=0)
    else:
        st.error(f'❌ Falha ao registrar: {resp.text}')

# 2) Carrega dispositivos
st.markdown('---')
resp = requests.get(f'{BACKEND_URL}/devices')
if resp.status_code != 200:
    st.error('Erro ao carregar dispositivos.')
    st.stop()

df = pd.DataFrame(resp.json())
if df.empty:
    st.info('Nenhum dispositivo cadastrado.')
    st.stop()

df['status'] = df['trafego'].apply(lambda x: 'Alto' if x > 50 else 'Normal')

# 3) Gráfico de Barras (labels na horizontal)
st.markdown('---')
st.subheader('Dispositivos Registrados')
chart = (
    alt.Chart(df)
       .mark_bar()
       .encode(
           x=alt.X('nome:N', title=None, axis=alt.Axis(labelAngle=0)),
           y=alt.Y('trafego:Q', title='Taxa de Tráfego (Mbps)'),
           color=alt.condition(alt.datum.trafego > 50,
                               alt.value('red'),
                               alt.value('green'))
       )
       .properties(height=250)
)
st.altair_chart(chart, use_container_width=True)

# 4) Tabela com Remoção
st.markdown('---')
cols = st.columns([2,3,2,2,1])
for col, h in zip(cols, ['Endereço IP','Nome','Taxa (Mbps)','Status','']):
    col.markdown(f'**{h}**')

for r in df.itertuples():
    c1,c2,c3,c4,c5 = st.columns([2,3,2,2,1])
    c1.write(r.ip)
    c2.write(r.nome)
    c3.write(f'{r.trafego:.1f}')
    badge = 'red' if r.status=='Alto' else 'green'
    c4.markdown(
    f"<span style='color:white; background:{badge}; padding:4px 6px; "
    f"border-radius:4px'>{r.status}</span>",
    unsafe_allow_html=True
)

    if c5.button('Remover', key=f'rm_{r.id}'):
        dr = requests.delete(f'{BACKEND_URL}/devices/{r.id}')
        if dr.status_code == 200:
            st.success('✅ Dispositivo removido!')
            components.html("<script>window.top.location.reload();</script>", height=0)
        else:
            st.error(f'❌ Falha ao remover: {dr.text}')