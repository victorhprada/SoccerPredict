"""
Script de Coleta e Processamento de Dados do Brasileirão
========================================================

Este script baixa dados históricos de partidas do Campeonato Brasileiro
e cria features (características) úteis para treinar uma IA de previsão.

Autor: Victor
Data: Janeiro 2026
"""

import pandas as pd
import os


def carregar_dados_brasileirao():
    """
    Baixa dados do Campeonato Brasileiro diretamente da internet.
    
    Returns:
        pandas.DataFrame: DataFrame com os dados das partidas
    """
    print("Iniciando download dos dados...")
    
    # Lista de URLs com dados do campeonato brasileiro (Série A) de 2020 a 2023
    # Estes são links diretos para arquivos CSV mantidos pela comunidade (football-data.co.uk ou similares)
    urls = [
        "https://www.football-data.co.uk/new/BRA.csv" 
    ]
    
    lista_dfs = []
    
    for url in urls:
        try:
            # O pandas lê o CSV direto da internet
            df = pd.read_csv(url)
            lista_dfs.append(df)
            print(f"✓ Sucesso ao baixar: {url}")
        except Exception as e:
            print(f"✗ Erro ao baixar {url}: {e}")
            
    if lista_dfs:
        # Junta tudo numa tabela só
        df_final = pd.concat(lista_dfs, ignore_index=True)
        return df_final
    else:
        return None


def limpar_e_traduzir_dados(dados):
    """
    Seleciona colunas essenciais e traduz para português.
    
    Args:
        dados (pandas.DataFrame): DataFrame bruto
        
    Returns:
        pandas.DataFrame: DataFrame limpo e traduzido
    """
    # 1. Selecionar apenas colunas essenciais
    colunas_desejadas = ['Date', 'Home', 'Away', 'HG', 'AG', 'Res']
    df_limpo = dados[colunas_desejadas].copy()
    
    # 2. Renomear para português
    df_limpo.columns = ['Data', 'Mandante', 'Visitante', 'Gols_Mandante', 'Gols_Visitante', 'Resultado']
    
    # 3. Converter a coluna 'Data' para formato de data real
    df_limpo['Data'] = pd.to_datetime(df_limpo['Data'], dayfirst=True)
    
    # 4. Ordenar por data (do jogo mais antigo para o mais novo)
    df_limpo = df_limpo.sort_values('Data')
    
    return df_limpo


def criar_variavel_alvo(df):
    """
    Cria a variável alvo (target) que queremos prever.
    H (Home) = 1, D (Draw) = 0, A (Away) = 2
    
    Args:
        df (pandas.DataFrame): DataFrame com coluna 'Resultado'
        
    Returns:
        pandas.DataFrame: DataFrame com coluna 'Alvo' adicionada
    """
    # Mapeamento: Dicionário que diz "Troque H por 1, D por 0, A por 2"
    mapa_resultado = {'H': 1, 'D': 0, 'A': 2}
    
    # Aplica o mapeamento numa nova coluna chamada 'Alvo'
    df['Alvo'] = df['Resultado'].map(mapa_resultado)
    
    # Criar coluna de "Total de Gols" (útil para Over/Under)
    df['Total_Gols'] = df['Gols_Mandante'] + df['Gols_Visitante']
    
    return df


def calcular_media_gols(df):
    """
    Calcula a média acumulada de gols de cada time até aquele momento.
    Isso evita "Data Leakage" (não usamos dados futuros para prever o passado).
    
    Args:
        df (pandas.DataFrame): DataFrame com os dados das partidas
        
    Returns:
        pandas.DataFrame: DataFrame com colunas de média de gols adicionadas
    """
    # Dicionário para guardar o total de gols e jogos de cada time
    stats_times = {}
    
    medias_mandante = []
    medias_visitante = []
    
    for indice, linha in df.iterrows():
        mandante = linha['Mandante']
        visitante = linha['Visitante']
        
        # Pega a média histórica do mandante até agora (se não tiver, assume 1.0)
        m_gols = stats_times.get(mandante, {'gols': 0, 'jogos': 0})
        media_m = m_gols['gols'] / m_gols['jogos'] if m_gols['jogos'] > 0 else 1.0
        medias_mandante.append(media_m)
        
        # Pega a média histórica do visitante até agora
        v_gols = stats_times.get(visitante, {'gols': 0, 'jogos': 0})
        media_v = v_gols['gols'] / v_gols['jogos'] if v_gols['jogos'] > 0 else 1.0
        medias_visitante.append(media_v)
        
        # ATUALIZA os dados DEPOIS de salvar a média
        # Isso evita o "Data Leakage" (vazamento de dados)
        stats_times[mandante] = {
            'gols': m_gols['gols'] + linha['Gols_Mandante'], 
            'jogos': m_gols['jogos'] + 1
        }
        stats_times[visitante] = {
            'gols': v_gols['gols'] + linha['Gols_Visitante'], 
            'jogos': v_gols['jogos'] + 1
        }
        
    df['Media_Gols_Mandante'] = medias_mandante
    df['Media_Gols_Visitante'] = medias_visitante
    
    return df


def salvar_dados(df, nome_arquivo='brasileirao_dados_processados.csv'):
    """
    Salva o DataFrame processado em um arquivo CSV.
    
    Args:
        df (pandas.DataFrame): DataFrame para salvar
        nome_arquivo (str): Nome do arquivo de saída
    """
    # Garante que a pasta 'dados' existe
    os.makedirs('../dados', exist_ok=True)
    
    # Caminho completo do arquivo
    caminho_arquivo = os.path.join('../dados', nome_arquivo)
    
    # Salva o arquivo
    df.to_csv(caminho_arquivo, index=False)
    
    print(f"\n{'='*60}")
    print(f"✓ Sucesso! O arquivo '{nome_arquivo}' foi salvo.")
    print(f"📁 Local: {os.path.abspath(caminho_arquivo)}")
    print(f"📊 Total de partidas: {len(df)}")
    print(f"{'='*60}")


def main():
    """
    Função principal que executa todo o pipeline de coleta e processamento.
    """
    print("\n" + "="*60)
    print("   COLETA E PROCESSAMENTO DE DADOS DO BRASILEIRÃO")
    print("="*60 + "\n")
    
    # Passo 1: Baixar dados
    dados = carregar_dados_brasileirao()
    
    if dados is None:
        print("❌ Não foi possível carregar os dados.")
        return
    
    print(f"✓ Dados carregados! Total de partidas: {dados.shape[0]}")
    
    # Passo 2: Limpar e traduzir
    print("\n📝 Limpando e traduzindo dados...")
    df_limpo = limpar_e_traduzir_dados(dados)
    print("✓ Dados limpos!")
    
    # Passo 3: Criar variável alvo
    print("\n🎯 Criando variável alvo (resultado para prever)...")
    df_com_alvo = criar_variavel_alvo(df_limpo)
    print("✓ Variável alvo criada!")
    
    # Passo 4: Calcular features (características)
    print("\n🧮 Calculando features (média de gols histórica)...")
    df_final = calcular_media_gols(df_com_alvo)
    print("✓ Features calculadas!")
    
    # Passo 5: Mostrar amostra dos dados
    print("\n📊 Amostra dos dados processados:")
    print(df_final[['Data', 'Mandante', 'Visitante', 'Media_Gols_Mandante', 
                    'Media_Gols_Visitante', 'Resultado', 'Alvo']].tail(10))
    
    # Passo 6: Salvar arquivo
    print("\n💾 Salvando arquivo...")
    salvar_dados(df_final)
    
    print("\n✅ Pipeline de coleta de dados concluído com sucesso!")
    print("🚀 Próximo passo: Treinar a IA (rode o arquivo 02_treinar_ia.py)\n")


if __name__ == "__main__":
    main()

