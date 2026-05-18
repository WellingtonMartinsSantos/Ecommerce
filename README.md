---

# 🛒 E-Commerce Data Warehouse & Executive Analytics

## 📋 Overview

This project implements an end-to-end **Data Platform** that simulates the data ecosystem of a large e-commerce operation. It uses the modern **Medallion Architecture (Bronze, Silver, Gold)** modeled with `dbt` and persisted in a cloud PostgreSQL database.

The data workflow culminates in an interactive, premium-designed **Executive Dashboard** built with Streamlit, enabling data-driven decisions for C-level management.

This project demonstrates real-world data modeling, analytics engineering, and business intelligence practices.

---

## 🎯 Project Objective

The main goal of this project is to showcase:

- Implementation of Medallion Architecture
- Analytics Engineering with dbt (Data Build Tool)
- Modern cloud database integration (Supabase)
- Complex business rules (Customer Segmentation, Pricing Elasticity)
- Advanced UI/UX dashboard design (Glassmorphism & Neon themes)
- Production-oriented configuration management

---

## 🏗️ Architecture

<img src="Picture Architecture/Picture Architecture.png" alt="E-Commerce Architecture" width="100%">

---
- **Bronze (Raw):** Direct 1:1 replication of the operational e-commerce tables (`vendas`, `clientes`, `produtos`, `preco_competidores`).
- **Silver (Cleansed):** Data sanitization, type casting, and standardizations (e.g., date formatting) without heavy filtering or joins.
- **Gold (Business/Data Marts):** Complex aggregations, ranking logic, and business rules designed for direct consumption (Sales, Customer Success, and Pricing).
- **Presentation (Dashboard):** Streamlit application reading directly from the Gold layer to serve real-time analytics.


## 🧠 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python |
| Data Modeling | dbt (Data Build Tool) |
| Database | PostgreSQL (Supabase) |
| Data Processing | Pandas |
| Dashboard UI | Streamlit |
| Data Visualization | Plotly Express |

---

## 📁 Project Structure
```bash
.
├── Ecommerce/                  # dbt project directory
│   ├── models/
│   │   ├── bronze/             # Raw ingestion models
│   │   ├── silver/             # Cleansed and standardized models
│   │   └── gold/               # Business-ready Data Marts
│   └── dbt_project.yml         # dbt configuration file
├── case-01-dashboard/          # Streamlit App directory
│   ├── app.py                  # Main dashboard script
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment variables template
└── README.md                   # Project documentation
```
---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone git@github.com:WellingtonMartinsSantos/ProjetoEcommerce.git
cd ProjetoEcommerce/case-01-dashboard
```

### 2️⃣ Configure Environment Variables

Create a `.env` file inside the `case-01-dashboard` directory:
```bash
SUPABASE_HOST=your_supabase_host
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=your_user
SUPABASE_PASSWORD=your_password
```

### 3️⃣ Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4️⃣ Start the Dashboard

Run the Streamlit application:
```bash
streamlit run app.py
```
Open your browser and go to [E-commerce](https://welldadose-commerce.streamlit.app/).

---

## 📊 Dashboard Features

The Streamlit dashboard is split into three main analytical pillars:

- **Sales Panel:** Tracks total revenue, sales volume, and average ticket size over time.
- **Customer Success:** Highlights VIP customer segmentation, retention, and the top 10 highest-value clients.
- **Pricing Intelligence:** Features an elasticity scatter plot comparing internal prices against market competitors, alerting for over-priced products.

This dashboard is designed with a **Premium Glassmorphism** aesthetic to serve executive-level users.

---

## 💡 Key Data Engineering Concepts Demonstrated

- Medallion Architecture implementation
- Modular SQL data modeling with dbt
- Separation of concerns (Raw vs Business logic)
- Environment-based configuration & Secrets management
- Cloud database connectivity
- Advanced data visualization and UI/UX design

---

## 🚀 Potential Improvements

- Implement CI/CD pipelines with GitHub Actions for dbt models
- Add unit testing and data quality tests in dbt
- Create a real-time data ingestion pipeline (Streaming)
- Add containerization (Docker) for the Streamlit dashboard

---

## 📌 Final Notes

This project reflects real-world Analytics Engineering workflows and demonstrates practical experience with:

- dbt Data Modeling
- PostgreSQL integration
- Business Intelligence and Dashboards
- Production-ready project structure

Designed to simulate industry-standard analytics engineering practices.

---

## 📞 Contact

#### 👨‍💻 Author : Wellington Martins Santos
#### Linkedin: [wellingtonmartinsdata](https://www.linkedin.com/in/wellingtonmartinsdata/)
#### GitHub: [WellingtonMartinsSantos](https://github.com/WellingtonMartinsSantos)
