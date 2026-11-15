# 🎯 Job-Match-Pipeline

Pipeline automatizado de Engenharia de Dados e *NLP Scoring* para extração, filtragem inteligente, deduplicação e notificação em tempo real de vagas de emprego (LinkedIn e Indeed) via Telegram Bot API.

## 🏗 Arquitetura do Pipeline

```mermaid
flowchart LR
    A[GitHub Actions Cron] --> B[Scraper Resiliente\nLinkedIn & Indeed]
    B --> C[Scoring Ponderado &\nFiltros Negativos]
    C --> D[(SQLite State DB\nSHA-256 Deduplication)]
    D -->|Apenas Vagas Inéditas| E[Telegram Bot API\nAlertas em Tempo Real]