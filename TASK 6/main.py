from pathlib import Path
from festdesk import process_department_files

def main():
    root = Path(__file__).parent
    input_dir = root / "data"
    output_dir = root / "output"
    try:
        master, errors, event_rows = process_department_files(input_dir, output_dir)
        print(f"Valid unique registrations: {len(master)}")
        print(f"Event lists created: {len(event_rows)}")
        print(f"Rejected/duplicate lines: {len(errors)}")
        print(f"Output directory: {output_dir}")
    except FileNotFoundError:
        print(f"Input directory not found: {input_dir}")

if __name__ == "__main__":
    main()
