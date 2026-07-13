import hashlib
import shutil
from pathlib import Path

from modules.constants import DUPLICATE_FOLDER


def calculate_hash(file_path, chunk_size=8192):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()


def move_duplicates(folder_path):
    folder = Path(folder_path)
    duplicate_folder = folder / DUPLICATE_FOLDER
    duplicate_folder.mkdir(exist_ok=True)

    hashes = {}
    duplicate_count = 0

    for file in folder.iterdir():

        if not file.is_file():
            continue

        if file.parent.name == DUPLICATE_FOLDER:
            continue

        file_hash = calculate_hash(file)

        if file_hash in hashes:

            destination = duplicate_folder / file.name

            counter = 1

            while destination.exists():
                destination = (
                    duplicate_folder /
                    f"{file.stem}_{counter}{file.suffix}"
                )
                counter += 1

            shutil.move(str(file), str(destination))
            duplicate_count += 1

        else:
            hashes[file_hash] = file

    return duplicate_count