import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import leaguestandings

st.set_page_config(page_title="NBA Analytics", page_icon="🏀", layout="wide")

st.title("🏀 NBA - Analytics Center")
st.write("Dados oficiais extraídos diretamente da API da NBA.")

# Função para buscar dados da NBA (Com Cache para não ser bloqueado pela API)
@st.cache_data(ttl=3600) # Atualiza a cada 1 hora
def buscar_classificacao():
    try:
        # Puxa a classificação da temporada atual (2024-25 ou atual)
        standings = leaguestandings.LeagueStandings(season='2024-25')
        df = standings.get_data_frames()[0]
        return df
    except Exception as e:
        st.error(f"Erro ao conectar na NBA API: {e}")
        return None

with st.spinner('Conectando aos servidores da NBA...'):
    df_nba = buscar_classificacao()

if df_nba is not None:
    # Selecionar colunas interessantes
    # TeamCity, TeamName, Conference, W (Vitórias), L (Derrotas), WinPCT (Aproveitamento)
    cols = ['Conference', 'TeamCity', 'TeamName', 'WINS', 'LOSSES', 'WinPCT', 'L10']
    df_clean = df_nba[cols].copy()
    
    # Traduzindo colunas
    df_clean.columns = ['Conferência', 'Cidade', 'Time', 'Vitórias', 'Derrotas', '% Vitória', 'Últimos 10']
    
    # Separando Leste e Oeste
    oeste = df_clean[df_clean['Conferência'] == 'West'].sort_values('% Vitória', ascending=False)
    leste = df_clean[df_clean['Conferência'] == 'East'].sort_values('% Vitória', ascending=False)

    # Exibindo lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌲 Conferência Oeste")
        st.dataframe(oeste.style.highlight_max(axis=0, color='lightgreen', subset=['Vitórias']), hide_index=True)
        
    with col2:
        st.subheader("🏙️ Conferência Leste")
        st.dataframe(leste.style.highlight_max(axis=0, color='lightgreen', subset=['Vitórias']), hide_index=True)