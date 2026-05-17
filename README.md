<div align="center">
  <img src="https://raw.githubusercontent.com/WellingtonMartinsSantos/WellingtonMartinsSantos/refs/heads/main/LogoGit.gif" alt="E-Commerce Analytics Logo" width="100%">
</div>

<h1 align="center">🛒 E-Commerce Data Warehouse & Executive Dashboard</h1>

<p align="center">
  <em>Um projeto ponta a ponta de Engenharia de Dados e Analytics, utilizando a Arquitetura Medalhão (Bronze, Silver, Gold), dbt, PostgreSQL e Streamlit.</em>
</p>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
</div>

<br>

## 📖 Visão Geral

Este projeto simula o ecossistema de dados de um grande **E-commerce**, passando desde o armazenamento bruto até a visualização executiva para a tomada de decisões na diretoria.

O fluxo de dados foi desenhado utilizando boas práticas de modelagem de **Data Warehouse**, culminando num painel analítico interativo, responsivo e com design premium (*Glassmorphism & Dark Neon Theme*).

---

## 🏗️ Arquitetura de Dados (Medallion Architecture)

Toda a transformação de dados ocorre dentro do próprio banco de dados (PostgreSQL via Supabase) através do **dbt (Data Build Tool)**, respeitando as três camadas clássicas:

1. 🥉 **Camada Bronze (Raw):** Réplica 1:1 das tabelas operacionais do E-commerce (`vendas`, `clientes`, `produtos`, `preco_competidores`).
2. 🥈 **Camada Silver (Cleaned):** Tabelas higienizadas. Realizamos padronização de datas, tratamentos de nulos e criação de regras simples (`faixa_preco`). **Sem joins e sem filtros drásticos.**
3. 🥇 **Camada Gold (Data Marts):** Onde reside a inteligência de negócios. Cruzamentos pesados, lógicas de ranqueamento, classificações e agregações criadas especificamente para consumo do Dashboard.
   - `vendas_temporais`: Desempenho e faturamento.
   - `clientes_segmentacao`: Curva ABC, identificação de Clientes VIPs.
   - `precos_competitividade`: Lógica de *Pricing* e comparação contra concorrentes do mercado.

---

## 📊 Dashboard Executivo (Streamlit)

A aplicação foi construída visando uma navegação fluída, dividida em três pilares analíticos:

*   **📈 Painel de Vendas:** Faturamento, ticket médio diário, e horários de pico.
*   **👥 Customer Success:** Perfil da base de clientes, faturamento por região, top 10 maiores compradores e métricas de fidelização.
*   **💲 Pricing Intelligence:** Gráficos de elasticidade (Preço vs Volume) e uma tabela de alerta para produtos com preço acima da média do mercado.

### 🎨 Design System
A interface foi fortemente customizada usando CSS puro dentro do Streamlit para aplicar um visual inspirado em plataformas modernas de tecnologia:
*   Fundo animado sutil com escurecimento de *Vignette*.
*   Efeito *Glassmorphism* (fundo de vidro translúcido com *blur*).
*   Tipografia de alto contraste com "Neon Glow" nos títulos para garantir elegância e legibilidade.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.11+
* Git
* Uma conta no [Supabase](https://supabase.com/) (PostgreSQL)

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/WellingtonMartinsSantos/ProjetoEcommerce.git
   cd ProjetoEcommerce/case-01-dashboard
   ```

2. **Configure o Ambiente Virtual e Dependências:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configuração do Banco de Dados:**
   - Crie um arquivo `.env` na pasta `case-01-dashboard`.
   - Utilize o arquivo `.env.example` como base e adicione as suas credenciais do banco PostgreSQL/Supabase:
     ```env
     SUPABASE_HOST=your_supabase_host
     SUPABASE_PORT=5432
     SUPABASE_DB=postgres
     SUPABASE_USER=postgres
     SUPABASE_PASSWORD=your_password
     ```

4. **Inicie o Painel:**
   ```bash
   streamlit run app.py
   ```
   O dashboard estará disponível em `http://localhost:8501`.

*(Nota: Para rodar as transformações dbt do zero, acesse a pasta `Ecommerce` e execute `dbt run` configurando o arquivo profiles.yml).*

---

## 👨‍💻 Autor

Desenvolvido com ☕ e Dados por **Wellington Martins Santos**.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/wellingtonmartinsdata/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/WellingtonMartinsSantos)
