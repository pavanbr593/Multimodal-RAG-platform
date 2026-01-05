def compute_confidence(num_sources: int) -> float:
    if num_sources >= 5:
        return 0.95
    if num_sources >= 3:
        return 0.85
    if num_sources >= 1:
        return 0.70
    return 0.40
