import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Comparador de Celulares", layout="wide")

@st.cache_data(ttl=300)
def cargar_datos():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1krkdGqGxRrmvROsGqkkG1l8EbrewYcEpodldvRwoF8k").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df = cargar_datos()

columnas_requeridas = ['País', 'Cliente', 'Marca', 'Modelo', 'Pantalla', 'Procesador', 'RAM',
                       'Almacenamiento', 'Cámara', 'Batería', 'Certificación', 'Sistema Operativo',
                       'Precio', 'Precio promoción']
if not all(col in df.columns for col in columnas_requeridas):
    st.error("⚠️ La hoja no contiene todas las columnas necesarias.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    pais = st.selectbox("Selecciona el país", ["Todos"] + sorted(df["País"].unique()))
with col2:
    cliente = st.selectbox("Selecciona el cliente", ["Todos"] + sorted(df["Cliente"].unique()))

if pais != "Todos":
    df = df[df["País"] == pais]
if cliente != "Todos":
    df = df[df["Cliente"] == cliente]

marcas = st.multiselect("Marca (máx. 5)", sorted(df["Marca"].unique()), max_selections=5)
if marcas:
    df = df[df["Marca"].isin(marcas)]

modelos = st.multiselect("Modelo (máx. 10)", sorted(df["Modelo"].unique()), max_selections=10)
if modelos:
    df = df[df["Modelo"].isin(modelos)]

st.markdown("### 📊 Comparativo de Celulares")
st.dataframe(df[columnas_requeridas], use_container_width=True)