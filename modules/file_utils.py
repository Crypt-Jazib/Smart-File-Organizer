from pathlib import Path
from modules.constants import FILE_CATEGORIES, DEFAULT_CATEGORY


def get_extension(file_path):
    return Path(file_path).suffix.lower()


def get_category(file_path):
    extension = get_extension(file_path)

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return DEFAULT_CATEGORY


def get_file_size(file_path):
    size = Path(file_path).stat().st_size
    return round(size / (1024 * 1024), 2)


def scan_folder(folder_path):
    folder = Path(folder_path)

    return [
        file
        for file in folder.iterdir()
        if file.is_file()
    ]