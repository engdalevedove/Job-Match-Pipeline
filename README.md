# 🎯 Job-Match-Pipeline

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-SHA--256%20Deduplication-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Serverless%20CI%2FCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Telegram Bot](https://img.shields.io/badge/Telegram-Real--Time%20Alerts-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)

> **Pipeline ETL automatizado em Python para coleta, ranqueamento por aderência técnica (*weighted scoring*), deduplicação idempotente e entrega de alertas de vagas em tempo real via Telegram.**

---

## 💡 O Problema & A Solução

Acompanhar diariamente centenas de vagas no LinkedIn e no Indeed exige triagem manual repetitiva, gera fadiga de busca e faz com que boas oportunidades passem despercebidas nas primeiras horas de publicação.

O **Job-Match-Pipeline** transforma essa busca em um fluxo de dados autônomo:
1. **Coleta Multi-Perfil:** Extrai oportunidades de múltiplas frentes (Remoto Brasil, Presencial/Híbrido Regional e Remoto Global) sem depender de login na conta pessoal.
2. **Motor de Scoring Ponderado:** Avalia título e descrição da vaga via expressões regulares (*word boundaries*), atribuindo pesos específicos às *hard skills* e descartando senioridades ou escopos fora do alvo.
3. **Garantia de Idempotência:** Gera um hash criptográfico (`SHA-256`) por vaga e persiste o histórico em banco **SQLite** versionado via CI/CD, garantindo **zero notificações duplicadas**.
4. **Execução 100% Serverless:** Roda automaticamente todos os dias às **08:00 (BRT)** via **GitHub Actions** e envia apenas as vagas de alta aderência direto no celular pelo **Telegram Bot API**.

---

## 🏗 Arquitetura do Pipeline

```mermaid
flowchart LR
    A[GitHub Actions Cron] --> B[Scraper Resiliente\nLinkedIn & Indeed]
    B --> C[Scoring Ponderado &\nFiltros Negativos]
    C --> D[(SQLite State DB\nSHA-256 Deduplication)]
    D -->|Apenas Vagas Inéditas| E[Telegram Bot API\nAlertas em Tempo Real]