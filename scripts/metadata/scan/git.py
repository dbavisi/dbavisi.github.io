# dbavisi.github.io
# Dwij Bavisi <dwij@dbavisi.net>

import os
import json

ROOT_DIR: str = os.getcwd()
PREFIX: str = "dbavisi.github.io"

CMDLine: str = 'git log --name-only --pretty=format:"%H%n%an%n%ae%n%at%n%s" --reverse > commit_history.txt'
GIT_HIST: dict = {}

def get_commit_history() -> list[dict]:
    os.system(CMDLine)

    with open("commit_history.txt", "r") as file:
        data: list[str] = file.read().split("\n")

    commits: list[dict] = []
    commit: dict = {}

    while data:
        line: str = data.pop(0)
        if not line:
            continue

        commit = {}
        commit["hash"] = line
        commit["author"] = data.pop(0)
        commit["email"] = data.pop(0)
        commit["timestamp"] = data.pop(0)
        commit["message"] = data.pop(0)
        commit["files"] = []

        line = data.pop(0)
        while line:
            commit["files"].append(line)
            line = data.pop(0)

        commits.append(commit)

    return commits

def save() -> None:
    with open("git_history.json", "w") as file:
        json.dump(GIT_HIST, file, indent=4)

def main() -> None:
    commits: list[dict] = get_commit_history()

    for commit in commits:
        GIT_HIST[commit["hash"]] = {
            "author": commit["author"],
            "email": commit["email"],
            "timestamp": commit["timestamp"],
            "message": commit["message"],
            "files": commit["files"]
        }

    save()

if __name__ == "__main__":
    main()
