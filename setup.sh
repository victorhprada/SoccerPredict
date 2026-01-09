#!/bin/bash
# Script de Configuração do Ambiente SoccerPredict
# ================================================

echo "⚽ Configurando ambiente SoccerPredict..."
echo ""

# Ativar ambiente virtual
echo "📦 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip --quiet

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt --quiet

echo ""
echo "✅ Ambiente configurado com sucesso!"
echo ""
echo "🚀 Para começar:"
echo "   1. Execute: source venv/bin/activate"
echo "   2. Execute: python src/01_coleta_dados.py"
echo ""

