# dbavisi.github.io
# Dwij Bavisi <dwij@dbavisi.net>

import os
import json
from scan import main as scan

ROOT_DIR: str = os.getcwd()
PREFIX: str = "dbavisi.github.io"

METADATA = scan(save_metadata=False)

def count_word(content: str) -> dict[str, int]:
    word_count: dict[str, int] = {}

    for word in content.split():
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

def parse() -> dict:
    files = METADATA["files"]
    metadata = {}

    for anonymous_file in files:
        file = anonymous_file.replace(PREFIX, ROOT_DIR)
        if not os.path.exists(file):
            continue
        if os.path.isfile(file):
            with open(file, "r") as f:
                print(f"Scanning {file}")
                content = f.read()
                word_count = count_word(content)
                metadata[file] = word_count

    return metadata

def main() -> None:
    metadata = parse()

    with open(f"{PREFIX}-word-cnt.json", "w") as f:
        json.dump(metadata, f, indent=4)

if __name__ == "__main__":
    main()
