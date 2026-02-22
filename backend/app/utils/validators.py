def clamp_percent(x: float) -> float:
    if x < 0:
        return 0.0
    if x > 100:
        return 100.0
    return float(x)