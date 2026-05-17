import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import plotly.express as px
import warnings

# Ignorar UserWarning do pandas read_sql com conexão psycopg2 direta
warnings.filterwarnings("ignore", "pandas only supports SQLAlchemy connectable")

# ==========================================
# 1. Page Configuration & Custom CSS (UI Premium)
# ==========================================
st.set_page_config(
    page_title="E-commerce Analytics", layout="wide", initial_sidebar_state="expanded"
)


def apply_custom_css():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');

    /* Fundo da página com EFEITO CINEMÁTICO e VIGNETTE sobre o seu GIF */
    .stApp {
        background-image: radial-gradient(circle at center, rgba(10, 15, 30, 0.65) 0%, rgba(5, 7, 15, 0.95) 100%), url("https://raw.githubusercontent.com/WellingtonMartinsSantos/WellingtonMartinsSantos/refs/heads/main/LogoGit.gif");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    .stApp > header {
        background-color: transparent !important;
    }
    
    /* Efeito Glassmorphism "Evolve" para os Cards de Métricas */
    [data-testid="stMetric"], div[data-testid="metric-container"] {
        background: rgba(20, 25, 40, 0.4) !important; /* Fundo transparente */
        backdrop-filter: blur(12px); /* Efeito de vidro borrado */
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #00F0FF; /* Detalhe Cyber/Moderno na lateral */
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover, div[data-testid="metric-container"]:hover {
        transform: translateY(-5px) scale(1.02);
        background: rgba(30, 35, 55, 0.6) !important;
        border-left: 4px solid #FF0055; /* Muda de cor no hover */
        box-shadow: 0 8px 32px 0 rgba(255, 0, 85, 0.2);
    }
    
    /* Textos dos KPIs com pegada de Design System */
    div[data-testid="stMetricLabel"] > label > div {
        color: #8B9BB4 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.85rem;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 1.8rem !important; 
        white-space: pre-wrap !important;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
    }
    
    /* Títulos Gerais (Estilo Evolve com Glow em vez de clip de texto para não quebrar emojis) */
    h1 {
        color: #F8FAFC !important;
        font-family: 'Inter', sans-serif;
        font-weight: 900 !important;
        letter-spacing: -1.5px;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.6); /* Glow Cyan */
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #F8FAFC !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
    }
    
    p, span {
        font-family: 'Inter', sans-serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }
    
    /* Sidebar com estilo Glass (translúcido) */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 30, 0.7) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Espaçamento extra do topo */
    .block-container {
        padding-top: 3rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


apply_custom_css()

# ==========================================
# 2. Database Connection & Utils
# ==========================================
load_dotenv()


@st.cache_resource
def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("SUPABASE_HOST"),
            port=os.getenv("SUPABASE_PORT", "5432"),
            dbname=os.getenv("SUPABASE_DB", "postgres"),
            user=os.getenv("SUPABASE_USER"),
            password=os.getenv("SUPABASE_PASSWORD"),
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar no banco de dados: {e}")
        return None


def load_data(query):
    conn = get_connection()
    if conn:
        try:
            return pd.read_sql_query(query, conn)
        except Exception as e:
            st.error(f"Erro ao executar query: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


def format_brl(value):
    if pd.isna(value):
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number(value):
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}".replace(",", ".")


# Estilo global dos gráficos
PLOTLY_THEME = "plotly_dark"
COLOR_PALETTE = px.colors.qualitative.Pastel

# ==========================================
# 3. Pages Implementation
# ==========================================


def page_vendas():
    st.title("📊 Vendas e Receita")
    st.markdown("Visão executiva do faturamento e tendências comerciais.")
    st.markdown("<br>", unsafe_allow_html=True)

    df = load_data("SELECT * FROM public_gold_sales.vendas_temporais")
    if df.empty:
        st.warning(
            "Nenhum dado encontrado na tabela public_gold_sales.vendas_temporais."
        )
        return

    # Optional Filter
    if "mes_venda" in df.columns:
        meses = df["mes_venda"].dropna().unique().tolist()
        mes_selecionado = st.selectbox(
            "📅 Selecione o Mês para Filtrar", ["Todos"] + sorted(meses)
        )
        if mes_selecionado != "Todos":
            df = df[df["mes_venda"] == mes_selecionado]

    # KPIs
    receita_total = df["receita_total"].sum() if "receita_total" in df.columns else 0
    total_vendas = df["total_vendas"].sum() if "total_vendas" in df.columns else 0
    ticket_medio = receita_total / total_vendas if total_vendas > 0 else 0
    clientes_unicos = (
        df["total_clientes_unicos"].max()
        if "total_clientes_unicos" in df.columns
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Receita Total", format_brl(receita_total))
    with col2:
        st.metric("📦 Volume de Vendas", format_number(total_vendas))
    with col3:
        st.metric("🛒 Ticket Médio", format_brl(ticket_medio))
    with col4:
        st.metric("👥 Clientes (Pico)", format_number(clientes_unicos))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Gráficos
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if "data_venda" in df.columns and "receita_total" in df.columns:
            df_dia = (
                df.groupby("data_venda", as_index=False)["receita_total"]
                .sum()
                .sort_values("data_venda")
            )
            fig1 = px.area(
                df_dia,
                x="data_venda",
                y="receita_total",
                title="📈 Receita Diária",
                template=PLOTLY_THEME,
                color_discrete_sequence=["#4CAF50"],
            )
            fig1.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig1, use_container_width=True)

    with col_g2:
        if "dia_semana_nome" in df.columns and "receita_total" in df.columns:
            ordem_dias = [
                "Segunda",
                "Terca",
                "Quarta",
                "Quinta",
                "Sexta",
                "Sabado",
                "Domingo",
            ]
            df_semana = df.groupby("dia_semana_nome", as_index=False)[
                "receita_total"
            ].sum()
            df_semana["ordem"] = pd.Categorical(
                df_semana["dia_semana_nome"], categories=ordem_dias, ordered=True
            )
            df_semana = df_semana.sort_values("ordem")
            fig2 = px.bar(
                df_semana,
                x="dia_semana_nome",
                y="receita_total",
                title="📅 Receita por Dia da Semana",
                template=PLOTLY_THEME,
                color_discrete_sequence=["#3182ce"],
            )
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig2, use_container_width=True)

    if "hora_venda" in df.columns and "total_vendas" in df.columns:
        df_hora = (
            df.groupby("hora_venda", as_index=False)["total_vendas"]
            .sum()
            .sort_values("hora_venda")
        )
        fig3 = px.bar(
            df_hora,
            x="hora_venda",
            y="total_vendas",
            title="⏱️ Volume de Vendas por Hora",
            template=PLOTLY_THEME,
            color_discrete_sequence=["#805ad5"],
        )
        fig3.update_xaxes(type="category")
        fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3, use_container_width=True)


def page_clientes():
    st.title("👥 Análise de Clientes")
    st.markdown("Métricas de fidelização, segmentação e perfil da base de clientes.")
    st.markdown("<br>", unsafe_allow_html=True)

    df = load_data("SELECT * FROM public_gold_cs.clientes_segmentacao")
    if df.empty:
        st.warning(
            "Nenhum dado encontrado na tabela public_gold_cs.clientes_segmentacao."
        )
        return

    # KPIs
    total_clientes = len(df)
    if "segmento_cliente" in df.columns:
        df_vip = df[df["segmento_cliente"] == "VIP"]
        clientes_vip = len(df_vip)
        receita_vip = (
            df_vip["receita_total"].sum() if "receita_total" in df_vip.columns else 0
        )
    else:
        clientes_vip, receita_vip = 0, 0
    ticket_medio_geral = (
        df["ticket_medio"].mean() if "ticket_medio" in df.columns else 0
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Clientes", format_number(total_clientes))
    with col2:
        st.metric("⭐ Clientes VIP", format_number(clientes_vip))
    with col3:
        st.metric("💎 Receita VIP", format_brl(receita_vip))
    with col4:
        st.metric("🛒 Tkt Médio Geral", format_brl(ticket_medio_geral))

    st.markdown("<br>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if "segmento_cliente" in df.columns:
            df_seg = df.groupby("segmento_cliente", as_index=False).size()
            fig1 = px.pie(
                df_seg,
                values="size",
                names="segmento_cliente",
                title="📊 Distribuição por Segmento",
                hole=0.5,
                template=PLOTLY_THEME,
                color_discrete_sequence=COLOR_PALETTE,
            )
            fig1.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig1, use_container_width=True)

    with col_g2:
        if "segmento_cliente" in df.columns and "receita_total" in df.columns:
            df_seg_rec = df.groupby("segmento_cliente", as_index=False)[
                "receita_total"
            ].sum()
            fig2 = px.bar(
                df_seg_rec,
                x="segmento_cliente",
                y="receita_total",
                title="💰 Receita por Segmento",
                template=PLOTLY_THEME,
                color_discrete_sequence=["#ecc94b"],
            )
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig2, use_container_width=True)

    col_g3, col_g4 = st.columns(2)

    with col_g3:
        if (
            "ranking_receita" in df.columns
            and "nome_cliente" in df.columns
            and "receita_total" in df.columns
        ):
            # Gráfico 3 - Top 10 Clientes por Receita (barras horizontais)
            df_top10 = df.nsmallest(10, "ranking_receita").sort_values(
                "receita_total", ascending=True
            )
            fig3 = px.bar(
                df_top10,
                x="receita_total",
                y="nome_cliente",
                orientation="h",
                title="🏆 Top 10 Clientes por Receita",
                template=PLOTLY_THEME,
                color_discrete_sequence=["#4299E1"],
            )
            fig3.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig3, use_container_width=True)

    with col_g4:
        if "estado" in df.columns:
            # Gráfico 4 - Clientes por Estado (barras)
            df_estado = (
                df.groupby("estado", as_index=False)
                .size()
                .sort_values("size", ascending=False)
            )
            fig4 = px.bar(
                df_estado,
                x="estado",
                y="size",
                title="🗺️ Clientes por Estado",
                template=PLOTLY_THEME,
                color_discrete_sequence=["#ED8936"],
            )
            fig4.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### 📋 Tabela Detalhada")
    if "segmento_cliente" in df.columns:
        segmentos = df["segmento_cliente"].unique().tolist()
        filtro_seg = st.selectbox("Filtrar por Segmento", ["Todos"] + segmentos)

        if filtro_seg != "Todos":
            st.dataframe(
                df[df["segmento_cliente"] == filtro_seg], use_container_width=True
            )
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)


def page_pricing():
    st.title("💲 Inteligência de Preços")
    st.markdown("Comparativo de preços x concorrência e impacto nas vendas.")
    st.markdown("<br>", unsafe_allow_html=True)

    df = load_data("SELECT * FROM public_gold_pricing.precos_competitividade")
    if df.empty:
        st.warning(
            "Nenhum dado encontrado na tabela public_gold_pricing.precos_competitividade."
        )
        return

    # Filter
    if "categoria" in df.columns:
        categorias = df["categoria"].unique().tolist()
        filtro_cat = st.multiselect("Filtrar por Categoria", options=categorias)

        if filtro_cat:
            df = df[df["categoria"].isin(filtro_cat)]

    # KPIs
    total_produtos = len(df)
    mais_caros = (
        len(df[df["classificacao_preco"] == "MAIS_CARO_QUE_TODOS"])
        if "classificacao_preco" in df.columns
        else 0
    )
    mais_baratos = (
        len(df[df["classificacao_preco"] == "MAIS_BARATO_QUE_TODOS"])
        if "classificacao_preco" in df.columns
        else 0
    )
    dif_media = (
        df["diferenca_percentual_vs_media"].mean()
        if "diferenca_percentual_vs_media" in df.columns
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Produtos Analisados", format_number(total_produtos))
    with col2:
        st.metric("🚨 Mais Caros (Risco)", format_number(mais_caros))
    with col3:
        st.metric("🟢 Mais Baratos", format_number(mais_baratos))
    with col4:
        st.metric(
            "⚖️ Dif. vs Mercado",
            f"{dif_media:+.1f}%" if pd.notnull(dif_media) else "N/A",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        if "classificacao_preco" in df.columns:
            # Gráfico 1 - Distribuicao por Classificacao (pizza)
            df_class = df.groupby("classificacao_preco", as_index=False).size()
            fig1 = px.pie(
                df_class,
                values="size",
                names="classificacao_preco",
                title="Posicionamento de Preço vs Concorrência",
                template=PLOTLY_THEME,
                color_discrete_sequence=COLOR_PALETTE,
                hole=0.4,
            )
            fig1.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig1, use_container_width=True)

    with col_g2:
        if "categoria" in df.columns and "diferenca_percentual_vs_media" in df.columns:
            # Gráfico 2 - Diferenca % Media por Categoria (barras)
            df_cat_dif = df.groupby("categoria", as_index=False)[
                "diferenca_percentual_vs_media"
            ].mean()
            # Verde para mais barato (negativo), vermelho para mais caro (positivo)
            df_cat_dif["color"] = df_cat_dif["diferenca_percentual_vs_media"].apply(
                lambda x: "red" if x > 0 else "green"
            )
            fig2 = px.bar(
                df_cat_dif,
                x="categoria",
                y="diferenca_percentual_vs_media",
                title="Competitividade por Categoria",
                color="color",
                color_discrete_map="identity",
            )
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Scatter interativo
    if (
        "diferenca_percentual_vs_media" in df.columns
        and "quantidade_total" in df.columns
    ):
        fig3 = px.scatter(
            df,
            x="diferenca_percentual_vs_media",
            y="quantidade_total",
            color=(
                "classificacao_preco" if "classificacao_preco" in df.columns else None
            ),
            size="receita_total" if "receita_total" in df.columns else None,
            hover_name="nome_produto" if "nome_produto" in df.columns else None,
            title="🎯 Elasticidade: Competitividade x Volume de Vendas",
            template=PLOTLY_THEME,
            color_discrete_sequence=COLOR_PALETTE,
        )
        fig3.add_vline(x=0, line_width=2, line_dash="dash", line_color="#E2E8F0")
        fig3.update_xaxes(range=[-10, 10], title="Diferença % vs Média")
        fig3.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", title_x=0.5
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 🚨 Produtos em Alerta (Mais caros que todos os concorrentes)")
    if "classificacao_preco" in df.columns:
        df_alertas = df[df["classificacao_preco"] == "MAIS_CARO_QUE_TODOS"]
        colunas_mostrar = [
            "produto_id",
            "nome_produto",
            "categoria",
            "nosso_preco",
            "preco_maximo_concorrentes",
            "diferenca_percentual_vs_media",
        ]
        # Filtra apenas colunas que existem no dataframe
        colunas_existentes = [
            col for col in colunas_mostrar if col in df_alertas.columns
        ]

        if not df_alertas.empty:
            st.dataframe(df_alertas[colunas_existentes], use_container_width=True)
        else:
            st.success(
                "Não há produtos mais caros que todos os concorrentes no momento!"
            )


# ==========================================
# 4. App Layout and Navigation
# ==========================================
st.sidebar.markdown(
    """
<div style="text-align: center; margin-bottom: 30px;">
    <h2 style="color: #F8FAFC; text-shadow: 0 0 15px rgba(255, 0, 85, 0.6); font-weight: 900; letter-spacing: -1px; margin-bottom: 0;">⚡ E-Commerce </h2>
    <p style="color: #8B9BB4; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 500; margin-top: 5px;">Executive Dashboard</p>
</div>
""",
    unsafe_allow_html=True,
)

page = st.sidebar.radio("", ["📊 Vendas", "👥 Clientes", "💲 Preços"])

st.sidebar.markdown("---")
st.sidebar.info(
    "Dashboard consumindo dados em real-time do Data Warehouse (Supabase/dbt)."
)

st.sidebar.markdown(
    """
    <div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
        <a href="https://github.com/WellingtonMartinsSantos" target="_blank" style="transition: transform 0.2s;">
            <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" style="border-radius: 6px; width: 100%; max-width: 110px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);"/>
        </a>
        <a href="https://www.linkedin.com/in/wellingtonmartinsdata/" target="_blank" style="transition: transform 0.2s;">
            <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" style="border-radius: 6px; width: 100%; max-width: 110px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);"/>
        </a>
    </div>
    <div style="text-align: center; margin-top: 15px; font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #8B9BB4; font-weight: 500; letter-spacing: 0.5px;">
        Data Warehouse & Analytics<br>by Wellington Martins Santos
    </div>
    """,
    unsafe_allow_html=True,
)

if page == "📊 Vendas":
    page_vendas()
elif page == "👥 Clientes":
    page_clientes()
elif page == "💲 Preços":
    page_pricing()
