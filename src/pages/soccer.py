import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Preditor Brasileirão MVP",
    page_icon="⚽",
)

# --- TÍTULO E CABEÇALHO ---
st.title("⚽ Inteligência Artificial do Brasileirão")
st.write("Este projeto usa Machine Learning para prever resultados com base em médias de gols históricas.")

# --- 1. CARREGAMENTO DOS DADOS (COM CACHE PARA FICAR RÁPIDO) ---
@st.cache_data
def carregar_dados():
    # Pega o diretório onde o arquivo app.py está
    diretorio_atual = os.path.dirname(__file__)
    
    # Sobe um nível (..) para sair de 'src' e entra em 'dados'
    caminho_arquivo = os.path.join(diretorio_atual, '..', '..', 'dados', 'brasileirao_dados_processados.csv')

    # Debug: Se der erro, o site vai mostrar onde está tentando procurar
    if not os.path.exists(caminho_arquivo):
        st.error(f"Arquivo não encontrado em: {caminho_arquivo}")
        return pd.DataFrame()
    
    df = pd.read_csv(caminho_arquivo)
    
    # --- NOVA LÓGICA: CALCULAR FORMA RECENTE (PONTOS NOS ÚLTIMOS 5 JOGOS) ---
    def calcular_forma(df, window=5):
        # Cria um dicionário para guardar os pontos de cada time jogo a jogo
        pontos_map = {} # Ex: {'Flamengo': [3, 1, 0, 3, 3...]}
        
        forma_mandante = []
        forma_visitante = []
        
        for i, row in df.iterrows():
            m, v = row['Mandante'], row['Visitante']
            res = row['Resultado'] # H=Mandante, A=Visitante, D=Empate
            
            # Recupera histórico recente (ou 0 se não tiver)
            hist_m = pontos_map.get(m, [])
            hist_v = pontos_map.get(v, [])
            
            # Calcula a média dos últimos 5 jogos ANTES dessa partida
            # Se tiver menos de 5 jogos, pega a média do que tem
            fm = sum(hist_m[-window:]) / window if len(hist_m) >= window else sum(hist_m) / len(hist_m) if len(hist_m) > 0 else 0
            fv = sum(hist_v[-window:]) / window if len(hist_v) >= window else sum(hist_v) / len(hist_v) if len(hist_v) > 0 else 0
            
            forma_mandante.append(fm)
            forma_visitante.append(fv)
            
            # Atualiza os pontos DEPOIS do jogo para o futuro
            pts_m = 3 if res == 'H' else 1 if res == 'D' else 0
            pts_v = 3 if res == 'A' else 1 if res == 'D' else 0
            
            if m not in pontos_map: pontos_map[m] = []
            if v not in pontos_map: pontos_map[v] = []
            
            pontos_map[m].append(pts_m)
            pontos_map[v].append(pts_v)
            
        df['Forma_Mandante'] = forma_mandante
        df['Forma_Visitante'] = forma_visitante
        return df

    df = calcular_forma(df)
    return df

df = carregar_dados()
df.fillna(0, inplace=True)

# --- 2. TREINAMENTO DO MODELO (NO BACKEND) ---
def treinar_modelo(df):
    # Prepara os dados igual fizemos no script anterior
    features = ['Media_Gols_Mandante', 'Media_Gols_Visitante', 'Forma_Mandante', 'Forma_Visitante']
    # Remove linhas vazias
    df_treino = df.dropna(subset=features + ['Alvo'])
    
    X = df_treino[features]
    y = df_treino['Alvo']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

modelo = treinar_modelo(df)


# --- 3. INTERFACE DO USUÁRIO (SIDEBAR) ---
st.sidebar.header("Defina o Jogo")

# Lista única de todos os times que aparecem na coluna Mandante
lista_times = sorted(df['Mandante'].unique())

time_mandante = st.sidebar.selectbox("Time da Casa (Mandante)", lista_times, index=0)
time_visitante = st.sidebar.selectbox("Time de Fora (Visitante)", lista_times, index=1)

# --- 4. RECUPERANDO ESTATÍSTICAS DOS TIMES SELECIONADOS ---
# Precisamos pegar a ÚLTIMA média de gols registrada para esses times
def pegar_stats_recentes(time, df, eh_mandante=True):
    coluna_filtro = 'Mandante' if eh_mandante else 'Visitante'
    coluna_media = 'Media_Gols_Mandante' if eh_mandante else 'Media_Gols_Visitante'
    
    # Filtra jogos desse time e pega o último
    jogos_time = df[df[coluna_filtro] == time]
    
    if jogos_time.empty:
        return 1.0 # Valor padrão se não achar dados
    
    return jogos_time.iloc[-1][coluna_media]

media_mandante = pegar_stats_recentes(time_mandante, df, eh_mandante=True)
media_visitante = pegar_stats_recentes(time_visitante, df, eh_mandante=False)

# Captura a forma recente (último registro do time no dataframe)
forma_mandante = df[df['Mandante'] == time_mandante].iloc[-1]['Forma_Mandante']
forma_visitante = df[df['Visitante'] == time_visitante].iloc[-1]['Forma_Visitante']

# Exibe na tela para você ver
col1, col2 = st.columns(2)
with col1:
    st.metric("Ataque", f"{media_mandante:.2f}")
    st.metric("Momento (Forma)", f"{forma_mandante:.2f}") # Nova Métrica
with col2:
    st.metric("Ataque", f"{media_visitante:.2f}")
    st.metric("Momento (Forma)", f"{forma_visitante:.2f}") # Nova Métrica

if st.button("🔮 Prever Resultado"):
    # Atualiza o input com 4 colunas
    input_dados = pd.DataFrame({
        'Media_Gols_Mandante': [media_mandante],
        'Media_Gols_Visitante': [media_visitante],
        'Forma_Mandante': [forma_mandante],
        'Forma_Visitante': [forma_visitante]
    })
    
    # Previsão direta
    previsao = modelo.predict(input_dados)[0]
    # Probabilidades (Certeza do modelo)
    probs = modelo.predict_proba(input_dados)[0]
    
    # Mapeamento do resultado
    resultado_texto = {0: "Empate", 1: f"Vitória do {time_mandante}", 2: f"Vitória do {time_visitante}"}
    
    st.divider()
    st.subheader(f"Resultado Previsto: {resultado_texto[previsao]}")
    
    # Exibe as probabilidades em barras
    st.write("Probabilidades calculadas pelo modelo:")
    prob_df = pd.DataFrame({
        "Resultado": ["Empate", "Vitória Mandante", "Vitória Visitante"],
        "Probabilidade": probs
    })
    
    st.bar_chart(prob_df.set_index("Resultado"))

    # Dica de aposta simples
    maior_prob = max(probs)
    if maior_prob > 0.5:
        st.success(f"O modelo está confiante ({maior_prob:.0%}) neste resultado!")
    else:
        st.warning(f"Jogo difícil! O modelo não tem certeza absoluta (Maior chance: {maior_prob:.0%}).")