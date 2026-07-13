import csv
from pathlib import Path
from datetime import datetime

REPORT_FOLDER = Path("reports")
REPORT_FOLDER.mkdir(exist_ok=True)

def generate_report(statistics: dict) -> Path:

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_file = REPORT_FOLDER / f"report_{timestamp}.csv"

    with open(report_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["Smart File Organizer Report"])
        writer.writerow([])

        writer.writerow([
            "Generated On",
            datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        ])

        writer.writerow([])

        writer.writerow(["Category", "Count"])

        writer.writerow(["----------------", "-----"])

        for category, count in statistics.items():
            writer.writerow([category, count])

        writer.writerow([])

        writer.writerow([
            "Total Files",
            statistics.get("Total", 0)
        ])

    return report_file