"""Task 4: Append daily book returns safely to one log."""
from pathlib import Path

def save_returns(books, log_path):
    log_path = Path(log_path)
    with log_path.open("a", encoding="utf-8", newline="\n") as log:
        for book in books:
            log.write(book.rstrip("\r\n") + "\n")

def process(day_file, log_path):
    day_file = Path(day_file)
    with day_file.open("r", encoding="utf-8") as source:
        books = [line.strip() for line in source if line.strip()]
    save_returns(books, log_path)

def main():
    folder = Path(__file__).parent
    log_path = folder / "returns.log"
    log_path.write_text("", encoding="utf-8")  # clean run for demonstration
    for day in ("day1.txt", "day2.txt", "day3.txt"):
        try:
            process(folder / day, log_path)
        except FileNotFoundError:
            print(f"Missing daily file: {day}")
        except PermissionError:
            print(f"Permission denied: {day}")
        except UnicodeDecodeError:
            print(f"Encoding problem: {day}")
    print("Final log:")
    print(log_path.read_text(encoding="utf-8"), end="")

if __name__ == "__main__":
    main()
