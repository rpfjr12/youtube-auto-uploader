from typing import Dict, List, Optional

CPM_RANKING = {
    "personal finance": 18.0,
    "business": 16.0,
    "technology": 14.5,
    "investing": 17.0,
    "marketing": 13.0,
    "productivity": 12.0,
    "motivation": 10.5,
    "psychology": 9.5,
    "health": 11.0,
    "lifestyle": 8.5,
    "education": 12.5,
    "general": 7.0,
}


def score_niche(niche: str, weight: float = 1.0) -> float:
    """Score a niche by its CPM ranking and an optional weight."""
    base = CPM_RANKING.get(niche.lower(), CPM_RANKING.get("general", 7.0))
    normalized = max(0.0, min(1.0, (base / 20.0)))
    return normalized * weight


def rank_niches(niches: Optional[List[str]] = None) -> List[Dict[str, float]]:
    """Return niches sorted by expected CPM score."""
    if niches is None:
        niches = list(CPM_RANKING.keys())
    ranked = []
    for niche in niches:
        ranked.append({"niche": niche, "score": score_niche(niche)})
    return sorted(ranked, key=lambda item: item["score"], reverse=True)


def best_niche(preferred_niches: Optional[List[str]] = None) -> str:
    """Select the best niche from a preferred list."""
    if not preferred_niches:
        return "general"
    scored = rank_niches(preferred_niches)
    return scored[0]["niche"] if scored else "general"
