"""Task 3: Custom exceptions and explicit attendance-file error handling."""
from pathlib import Path
import os
import tempfile

class InvalidRecord(Exception):
    """Raised when an attendance row is not in register,date,status format."""

def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    register, date_text, status = (part.strip() for part in parts)
    if not register or not date_text or status not in ("P", "A"):
        raise InvalidRecord(f"invalid status or empty field ({status!r})")
    return register, date_text, status

def summarise(path):
    present = absent = 0
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    _, _, status = parse_line(line)
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
                except InvalidRecord as error:
                    errors.append((line_number, str(error)))
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except UnicodeDecodeError:
        raise
    return present, absent, errors

if __name__ == "__main__":
    sample = (
        "192311001,2026-10-08,P\n"
        "192311003,2026-10-08\n"
        "192311004,2026-10-08,X\n"
    )
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".csv",
                                     delete=False) as temp:
        temp.write(sample)
        sample_path = temp.name
    try:
        print(summarise(sample_path))
    finally:
        os.remove(sample_path)
