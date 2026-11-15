import logging
import yaml
from pathlib import Path
from dotenv import load_dotenv

from src.database import init_db, generate_job_hash, is_job_seen, save_job
from src.scraper import fetch_jobs_from_profiles
from src.matcher import filter_and_rank_jobs
from src.notifier import send_telegram_alerts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_config(path: str = "config/profile_config.yaml") -> dict:
    with open(Path(path), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_pipeline() -> None:
    load_dotenv()
    init_db()
    config = load_config()

    logger.info("Iniciando extração de vagas...")
    raw_jobs = fetch_jobs_from_profiles(config["search_profiles"])
    logger.info(f"Total de vagas brutas únicas coletadas: {len(raw_jobs)}")

    if raw_jobs.empty:
        logger.info("Nenhuma vaga retornada nesta execução.")
        return

    ranked_jobs = filter_and_rank_jobs(raw_jobs, config["scoring"])
    logger.info(f"Vagas acima do score mínimo ({config['scoring']['min_score']}%): {len(ranked_jobs)}")

    new_jobs = []
    for _, row in ranked_jobs.iterrows():
        job_hash = generate_job_hash(row.get("title", ""), row.get("company", ""), row.get("job_url", ""))
        if not is_job_seen(job_hash):
            save_job(
                job_hash=job_hash,
                title=str(row.get("title", "")),
                company=str(row.get("company", "")),
                site=str(row.get("site", "")),
                job_url=str(row.get("job_url", "")),
                score=int(row["match_score"]),
            )
            new_jobs.append(row)

    logger.info(f"Vagas inéditas para notificação: {len(new_jobs)}")

    if new_jobs:
        import pandas as pd
        send_telegram_alerts(pd.DataFrame(new_jobs))


if __name__ == "__main__":
    run_pipeline()