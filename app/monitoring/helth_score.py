def calculate_health_score(cpu: float, mem: float, disk: float) -> float:
    """0-100 score, lower is worse"""
    return max(0, 100 - (cpu * 0.4 + mem * 0.4 + disk * 0.2))
