import shutil
from pathlib import Path
from typing import Callable

from modules.file_utils import scan_folder, get_category
from modules.duplicate_detector import move_duplicates
from modules.logger import logger


class FileOrganizer:

    def __init__(self, folder_path: str) -> None:

        self.folder = Path(folder_path)
        self.statistics = self.create_statistics()

    @staticmethod
    def create_statistics() -> dict:

        return {
            "Images": 0,
            "Documents": 0,
            "Videos": 0,
            "Audio": 0,
            "Archives": 0,
            "Code": 0,
            "Programs": 0,
            "Others": 0,
            "Duplicates": 0,
            "Total": 0
        }

    def create_folder(self, category: str) -> Path:

        destination_folder = self.folder / category
        destination_folder.mkdir(exist_ok=True)

        return destination_folder#

    def organize(
        self,
        progress_callback: Callable[[float], None] | None = None
    ) -> dict:

        logger.info(f"Selected Folder: {self.folder}")

        duplicate_count = move_duplicates(self.folder)
        self.statistics["Duplicates"] = duplicate_count

        file_list = scan_folder(self.folder)

        total_files = len(file_list)
        self.statistics["Total"] = total_files

        if total_files == 0:

            logger.info("No files found.")

            return self.statistics

        for index, file in enumerate(file_list, start=1):

            category = get_category(file)

            destination_folder = self.create_folder(category)

            destination_path = destination_folder / file.name

            duplicate_number = 1

            while destination_path.exists():

                destination_path = (
                    destination_folder /
                    f"{file.stem}_{duplicate_number}{file.suffix}"
                )

                duplicate_number += 1

            shutil.move(file, destination_path)

            self.statistics[category] += 1

            logger.info(
                f"Moved '{file.name}' -> '{category}'"
            )

            if progress_callback:

                progress_callback(index / total_files)

        logger.info("Organization completed successfully.")

        return self.statistics

    def preview(self) -> dict:

        preview_statistics = {
            "Images": 0,
            "Documents": 0,
            "Videos": 0,
            "Audio": 0,
            "Archives": 0,
            "Code": 0,
            "Programs": 0,
            "Others": 0
        }

        file_list = scan_folder(self.folder)

        for file in file_list:

            category = get_category(file)

            preview_statistics[category] += 1

        return preview_statistics