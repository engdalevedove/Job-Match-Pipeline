import logging
import pandas as pd
from jobspy import scrape_jobs

logger = logging.getLogger(__name__)


def fetch_jobs_from_profiles(profiles: list[dict]) -> pd.DataFrame:
    all_frames = []

    for profile in profiles:
        profile_name = profile["name"]
        for term in profile["terms"]:
            logger.info(f"[{profile_name}] Buscando termo: '{term}'")
            try:
                df = scrape_jobs(
                    site_name=profile["sites"],
                    search_term=term,
                    location=profile["location"],
                    results_wanted=profile["results_wanted"],
                    hours_old=profile["hours_old"],
                    country_indeed=profile["country_indeed"],
                    is_remote=profile["is_remote"],
                )
                if df is not None and not df.empty:
                    df["search_profile"] = profile_name
                    all_frames.append(df)
            except Exception as exc:
                logger.warning(f"Falha ao extrair '{term}' em [{profile_name}]: {exc}")

    if not all_frames:
        return pd.DataFrame()

    combined = pd.concat(all_frames, ignore_index=True)
    combined = combined.drop_duplicates(subset=["job_url"]).reset_index(drop=True)
    return combined