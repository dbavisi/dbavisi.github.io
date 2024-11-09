# dbavisi.github.io
# Dwij Bavisi <dwij@dbavisi.net>

import os
import json

ROOT_DIR: str = os.getcwd()
PREFIX: str = "dbavisi.github.io"

HIDDEN_DIRS: list[str] = [
    os.path.join(ROOT_DIR, ".git"),
]

METADATA: dict = {
    "files": [],
    "folders": [],
    "file_size": [],
    "folder_size": [],
}

def scan(path: str) -> list[str]:
    next_folders: list[str] = []

    for root, dirs, files in os.walk(path):
        for file in files:
            METADATA["files"].append(os.path.join(root, file))
        for folder in dirs:
            METADATA["folders"].append(os.path.join(root, folder))
            next_folders.append(os.path.join(root, folder))
        break

    return next_folders

def get_file_size(file: str) -> int:
    return os.path.getsize(file)

def calculate_folder_size(folder: str) -> int:
    size: int = 0

    for (file, file_size) in METADATA["file_size"]:
        if file.startswith(folder):
            size += file_size

    return size

def anonymize() -> None:
    for hidden in HIDDEN_DIRS:
        for i, file in enumerate(METADATA["files"]):
            if file.startswith(hidden):
                METADATA["files"][i] = f"{hidden}/<anonymized>"
        for i, folder in enumerate(METADATA["folders"]):
            if folder.startswith(hidden) and folder != hidden:
                METADATA["folders"][i] = f"{hidden}/<anonymized>"
        for i, (file, size) in enumerate(METADATA["file_size"]):
            if file.startswith(hidden):
                METADATA["file_size"][i] = (f"{hidden}/<anonymized>", size)
        for i, (folder, size) in enumerate(METADATA["folder_size"]):
            if folder.startswith(hidden) and folder != hidden:
                METADATA["folder_size"][i] = (f"{hidden}/<anonymized>", size)

    for i, file in enumerate(METADATA["files"]):
        METADATA["files"][i] = file.replace(ROOT_DIR, PREFIX)
    for i, folder in enumerate(METADATA["folders"]):
        METADATA["folders"][i] = folder.replace(ROOT_DIR, PREFIX)

    for i, (file, size) in enumerate(METADATA["file_size"]):
        METADATA["file_size"][i] = (file.replace(ROOT_DIR, PREFIX), size)

    for i, (folder, size) in enumerate(METADATA["folder_size"]):
        METADATA["folder_size"][i] = (folder.replace(ROOT_DIR, PREFIX), size)

def save() -> None:
    with open("metadata.json", "w") as f:
        json.dump(METADATA, f, indent=4)

def main() -> None:
    next_folders: list[str] = scan(ROOT_DIR)

    while next_folders:
        folder = next_folders.pop(0)
        next_folders += scan(folder)

    for i, file in enumerate(METADATA["files"]):
        METADATA["file_size"].append((file, get_file_size(file)))
    for i, folder in enumerate(METADATA["folders"]):
        METADATA["folder_size"].append((folder, calculate_folder_size(folder)))

    anonymize()
    save()

if __name__ == "__main__":
    main()
