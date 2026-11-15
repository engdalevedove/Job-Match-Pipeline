import re
import pandas as pd


def calculate_match(row: pd.Series, scoring_cfg: dict) -> tuple[int, list[str]]:
    title = str(row.get("title", "") or "")
    description = str(row.get("description", "") or "")
    full_text = f"{title} {description}".lower()

    # Normaliza pontuação do título para pegar variações como "Sr." ou "(Sênior)"
    title_clean = re.sub(r"[^\w\s]", " ", title.lower())
    for neg in scoring_cfg.get("negative_keywords", []):
        if re.search(rf"\b{re.escape(neg.lower())}\b", title_clean):
            return 0, []

    skills_weights: dict = scoring_cfg.get("skills_weights", {})
    target_sum: int = scoring_cfg.get("target_weight_sum", 15)

    matched_skills = []
    earned_weight = 0

    for skill, weight in skills_weights.items():
        pattern = rf"\b{re.escape(skill.lower())}\b"
        if re.search(pattern, full_text):
            matched_skills.append(skill)
            earned_weight += weight

    # Bônus de aderência para vagas explicitamente Pleno / Mid-Level
    if re.search(r"\b(pleno|pl|mid|mid-level)\b", title_clean):
        earned_weight += 2

    score = min(100, int((earned_weight / target_sum) * 100))
    return score, matched_skills


def filter_and_rank_jobs(df: pd.DataFrame, scoring_cfg: dict) -> pd.DataFrame:
    if df.empty:
        return df

    min_score = scoring_cfg.get("min_score", 60)
    results = df.apply(lambda r: calculate_match(r, scoring_cfg), axis=1)

    df["match_score"] = [res[0] for res in results]
    df["matched_skills"] = [", ".join(res[1]) for res in results]

    filtered = df[df["match_score"] >= min_score].copy()
    filtered = filtered.sort_values(by="match_score", ascending=False).reset_index(drop=True)
    return filtered