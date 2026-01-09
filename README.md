# ⚽ SoccerPredict - Previsão de Resultados do Brasileirão

Projeto de Machine Learning para prever resultados de partidas do Campeonato Brasileiro.

## 📁 Estrutura do Projeto

```
SoccerPredict/
│
├── dados/                              # Dados processados
│   └── brasileirao_dados_processados.csv
│
├── src/                                # Scripts Python
│   ├── 01_coleta_dados.py             # Coleta e processamento de dados
│   └── 02_treinar_ia.py               # Treinamento do modelo de IA
│
├── venv/                               # Ambiente virtual Python
├── requirements.txt                    # Dependências do projeto
└── README.md                           # Este arquivo
```

## 🚀 Como Começar

### 1. Criar e Ativar o Ambiente Virtual

**No macOS/Linux:**
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate
```

**No Windows:**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate
```

### 2. Instalar Dependências

Com o ambiente virtual ativado:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Executar os Scripts

**Passo 1: Coletar e processar dados**
```bash
python src/01_coleta_dados.py
```

**Passo 2: Treinar a IA** (em desenvolvimento)
```bash
python src/02_treinar_ia.py
```

## 📦 Dependências Principais

- **pandas**: Manipulação de dados
- **numpy**: Computação numérica
- **scikit-learn**: Machine Learning
- **matplotlib/seaborn**: Visualização de dados

## 🎯 Próximos Passos

- [x] Coleta e processamento de dados
- [ ] Treinamento do modelo de IA
- [ ] Avaliação de performance
- [ ] Interface para fazer previsões
- [ ] Deploy do modelo

## 👤 Autor

Victor Hugo Prada Teixeira
Janeiro 2026

---
**Status**: 🚧 Em desenvolvimento

