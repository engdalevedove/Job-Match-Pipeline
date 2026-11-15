import os
import logging
import requests
import pandas as pd

logger = logging.getLogger(__name__)


def send_telegram_alerts(jobs_df: pd.DataFrame) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.warning("Credenciais do Telegram ausentes. Exibindo vagas apenas no console.")
        for _, job in jobs_df.iterrows():
            print(f"[{job['match_score']}%] {job['title']} @ {job['company']} -> {job['job_url']}")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for _, job in jobs_df.iterrows():
        msg = (
            f"🎯 *Match: {job['match_score']}%* | _{job['search_profile']}_\n"
            f"💼 *{job['title']}*\n"
            f"🏢 {job.get('company', 'Empresa não informada')} ({job.get('location', 'N/A')})\n"
            f"🛠 Skills: `{job['matched_skills']}`\n"
            f"🔗 [Aplicar na vaga ({job['site']})]({job['job_url']})"
        )
        try:
            resp = requests.post(
                url,
                json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True},
                timeout=15,
            )
            resp.raise_for_status()
        except Exception as exc:
            logger.error(f"Erro ao enviar mensagem ao Telegram: {exc}")