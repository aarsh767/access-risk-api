"""Accessibility risk scoring: compares a traveler's needs against a destination's features.

Returns a 0-100 risk score (higher = riskier) plus the specific gaps that drove it,
so a traveler can see *why* a destination scored the way it did.
"""

# How much each unmet need contributes to risk, by severity the traveler reports (1-3).
WEIGHTS = {
    "wheelchair": ("step_free_access", 12),
    "low_vision": ("tactile_signage", 7),
    "hearing": ("visual_alerts", 6),
    "medical": ("hospital_within_10km", 10),
    "dietary": ("allergen_labeling", 4),
}


def score(needs: dict[str, int], features: dict[str, bool]) -> dict:
    total, gaps = 0, []
    for need, severity in needs.items():
        if need not in WEIGHTS:
            raise ValueError(f"unknown need: {need}")
        if not 1 <= severity <= 3:
            raise ValueError(f"severity for {need} must be 1-3")
        feature, weight = WEIGHTS[need]
        if not features.get(feature, False):
            total += weight * severity
            gaps.append(feature)
    risk = min(total, 100)
    level = "low" if risk < 25 else "moderate" if risk < 60 else "high"
    return {"risk": risk, "level": level, "gaps": gaps}
