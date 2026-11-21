# Organisation A: all functionality in one script.

def attendance_percentage(present, total):
    """Return attendance percentage; zero when no sessions are recorded."""
    return (present / total * 100) if total else 0.0

def absent_for_three_days(day_statuses):
    """Return True when all three consecutive statuses are absent ('A')."""
    return len(day_statuses) >= 3 and all(x == "A" for x in day_statuses[-3:])

def main():
    present, total = 18, 22
    print(f"Attendance: {attendance_percentage(present, total):.2f}%")
    print("Absent for three consecutive days:", absent_for_three_days(["P", "A", "A", "A"]))
if __name__ == "__main__":
    main()
