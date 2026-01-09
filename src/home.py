import streamlit as st

st.set_page_config(
    page_title="Sports Analytics Hub",
    page_icon="📈",
    layout="wide"
)

st.title("🏆 Sports Analytics Hub")

st.markdown("""
Bem-vindo ao seu centro de inteligência esportiva. 
Este projeto utiliza **Ciência de Dados** e **Machine Learning** para analisar padrões em diferentes esportes.

### 👈 Selecione um Módulo no menu lateral

---

### 📊 Módulos Disponíveis

#### ⚽ Futebol (Brasileirão)
* **Previsão de Resultados:** IA treinada com histórico de 2020-2024.
* **Análise de Forma:** Compare o momento atual dos times.
* **Calculadora de Odds:** Probabilidade estatística de vitória.

#### 🏀 Basquete (NBA)
* **Dados em Tempo Real:** Conexão direta com a API da NBA.
* **Classificação:** Tabela Leste/Oeste atualizada.
* **Stats:** (Em breve) Mapa de arremessos e performance de jogadores.

---
*Desenvolvido com Python, Streamlit e Scikit-Learn.*
""")