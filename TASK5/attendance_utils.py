def attendance_percentage(present, total):
    """Return attendance percentage; zero when no sessions are recorded."""
    return (present / total * 100) if total else 0.0

def absent_for_three_days(day_statuses):
    """Return True when all three consecutive statuses are absent ('A')."""
    return len(day_statuses) >= 3 and all(x == "A" for x in day_statuses[-3:])
