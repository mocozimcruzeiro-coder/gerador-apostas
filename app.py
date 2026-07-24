import streamlit as st
import pandas as pd
import random

# Configuração da página
st.set_page_config(
    page_title="Gerador de Múltiplas de Alto Valor",
    page_icon="⚽",
    layout="wide"
)

# Estilização básica CSS
st.markdown("""
    <style>
    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    .main-title {
        color: #10b981;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Banco de dados simulado (Em um app real, aqui entraria a chamada de uma API de Futebol)
@st.cache_data
def carregar_jogos_do_dia():
    return [
        {"id": 1, "liga": "Premier League", "casa": "Arsenal", "fora": "Everton", "media_gols": 2.6, "odd_u55": 1.05, "odd_h3": 1.08},
        {"id": 2, "liga": "La Liga", "casa": "Real Madrid", "fora": "Getafe", "media_gols": 2.4, "odd_u55": 1.06, "odd_h3": 1.07},
        {"id": 3, "liga": "Serie A Italia", "casa": "Juventus", "fora": "Lazio", "media_gols": 2.1, "odd_u55": 1.04, "odd_h3": 1.09},
        {"id": 4, "liga": "Brasileirão", "casa": "Palmeiras", "fora": "Fortaleza", "media_gols": 2.3, "odd_u55": 1.05, "odd_h3": 1.06},
        {"id": 5, "liga": "Bundesliga", "casa": "Bayern de Munique", "fora": "Mainz", "media_gols": 3.4, "odd_u55": 1.11, "odd_h3": 1.12},
        {"id": 6, "liga": "Ligue 1", "casa": "PSG", "fora": "Rennes", "media_gols": 2.9, "odd_u55": 1.08, "odd_h3": 1.10},
        {"id": 7, "liga": "Primeira Liga", "casa": "Benfica", "fora": "Braga", "media_gols": 2.2, "odd_u55": 1.04, "odd_h3": 1.05},
        {"id": 8, "liga": "Brasileirão", "casa": "Flamengo", "fora": "Internacional", "media_gols": 2.5, "odd_u55": 1.06, "odd_h3": 1.07},
    ]

# Título da Aplicação
st.markdown("<h1 class='main-title'>⚽ Gerador Inteligente de Múltiplas</h1>", unsafe_allow_html=True)
st.write("Estratégia focada em alta taxa de acerto com Menos de 5.5 Gols e Handicap +3.0.")

st.divider()

# Sidebar: Filtros e Parâmetros
st.sidebar.header("⚙️ Configurações do Bilhete")

qtd_pernas = st.sidebar.slider("Número de jogos na múltipla", min_value=2, max_value=6, value=4)

foco_mercado = st.sidebar.radio(
    "Foco do Mercado",
    ["Misto (Recomendado)", "Apenas Menos de 5.5 Gols", "Apenas Handicap +3.0"]
)

valor_aposta = st.sidebar.number_input("Valor da Aposta (R$)", min_value=5.0, value=50.0, step=5.0)

botao_gerar = st.sidebar.button("🎲 Gerar Novo Bilhete", type="primary", use_container_width=True)

# Processamento e Geração dos Jogos
jogos = carregar_jogos_do_dia()

# Função para selecionar e montar a múltipla
def montar_multipla(lista_jogos, quantidade, tipo_mercado):
    selecionados = random.sample(lista_jogos, min(quantidade, len(lista_jogos)))
    bilhete = []
    
    for jogo in selecionados:
        # Lógica de seleção do mercado
        if tipo_mercado == "Apenas Menos de 5.5 Gols":
            escolha = "u55"
        elif tipo_mercado == "Apenas Handicap +3.0":
            escolha = "h3"
        else:
            escolha = random.choice(["u55", "h3"])
            
        if escolha == "u55":
            bilhete.append({
                "Partida": f"{jogo['casa']} vs {jogo['fora']}",
                "Liga": jogo['liga'],
                "Entrada": "Menos de 5.5 Gols",
                "Odd": jogo['odd_u55'],
                "Confiança": "96%"
            })
        else:
            bilhete.append({
                "Partida": f"{jogo['casa']} vs {jogo['fora']}",
                "Liga": jogo['liga'],
                "Entrada": f"Handicap +3.0 ({jogo['fora']})",
                "Odd": jogo['odd_h3'],
                "Confiança": "94%"
            })
            
    return bilhete

# Gerar bilhete
bilhete_atual = montar_multipla(jogos, qtd_pernas, foco_mercado)

# Cálculo de Odds Totais e Retorno
odd_total = 1.0
for item in bilhete_atual:
    odd_total *= item["Odd"]

retorno_potencial = valor_aposta * odd_total

# Painel Superior com Resultados
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Odd Total Combinada", value=f"{odd_total:.2f}")

with col2:
    st.metric(label="Aposta Inicial", value=f"R$ {valor_aposta:.2f}")

with col3:
    st.metric(label="Retorno Potencial", value=f"R$ {retorno_potencial:.2f}", delta=f"R$ {retorno_potencial - valor_aposta:.2f}")

with col4:
    # Estimativa de probabilidade combinada simples
    prob_estimada = (1 / odd_total) * 0.92 * 100
    st.metric(label="Probabilidade Estimada", value=f"{prob_estimada:.1f}%")

st.divider()

# Exibição do Bilhete
st.subheader("📋 Jogos Selecionados para o Bilhete")

df_bilhete = pd.DataFrame(bilhete_atual)
st.dataframe(
    df_bilhete,
    column_config={
        "Odd": st.column_config.NumberColumn("Odd", format="%.2f"),
    },
    use_container_width=True,
    hide_index=True
)

st.info("💡 Dica de Gestão: Múltiplas com 3 a 4 pernas nesses mercados mantêm uma taxa de acerto extremamente elevada ao longo de várias rodadas.")
