"""Task 2: Process all daily biometric attendance files in a folder."""
from pathlib import Path
import sys

def process_month(folder, output_folder):
    folder = Path(folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    counts = {}  # register -> [present days, absent days]
    damaged = []
    daily_files = sorted(folder.glob("*.txt"))

    for file_path in daily_files:
        try:
            with file_path.open("r", encoding="utf-8") as file:
                for line_number, raw in enumerate(file, start=1):
                    if not raw.strip():
                        continue
                    fields = [part.strip() for part in raw.strip().split(",")]
                    if len(fields) != 3:
                        damaged.append((file_path.name, line_number, "expected 3 fields"))
                        continue
                    register, date_text, status = fields
                    if not register or not date_text or status not in {"P", "A"}:
                        damaged.append((file_path.name, line_number, "missing field or invalid status"))
                        continue
                    counts.setdefault(register, [0, 0])
                    counts[register][0 if status == "P" else 1] += 1
        except (OSError, UnicodeDecodeError) as error:
            damaged.append((file_path.name, 0, str(error)))

    total_days = len(daily_files)
    percentage_lines = ["Register Number,Present,Absent,Attendance Percentage"]
    below_lines = ["Register Number,Attendance Percentage"]
    for register in sorted(counts):
        present, absent = counts[register]
        recorded = present + absent
        percentage = (present / recorded * 100) if recorded else 0.0
        percentage_lines.append(f"{register},{present},{absent},{percentage:.2f}")
        if percentage < 75:
            below_lines.append(f"{register},{percentage:.2f}")

    (output_folder / "attendance_percentage.csv").write_text(
        "\n".join(percentage_lines) + "\n", encoding="utf-8")
    (output_folder / "below_75_percent.csv").write_text(
        "\n".join(below_lines) + "\n", encoding="utf-8")
    with (output_folder / "damaged_lines.log").open("w", encoding="utf-8") as log:
        for filename, line_number, reason in damaged:
            log.write(f"{filename}: line {line_number}: {reason}\n")

    return counts, damaged, total_days

if __name__ == "__main__":
    root = Path(__file__).parent
    input_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "daily_files"
    output_dir = root / "output"
    try:
        counts, damaged, days = process_month(input_dir, output_dir)
        print(f"Daily files processed: {days}")
        print(f"Students found: {len(counts)}")
        print(f"Damaged lines/files: {len(damaged)}")
        print(f"Reports written to: {output_dir}")
    except FileNotFoundError:
        print(f"Input folder does not exist: {input_dir}")
