"""Core logic for the prepare-commit-msg Git hook."""

import shutil
import subprocess
import sys
from pathlib import Path

from termcolor import colored

try:
    from colorama import init

    init()
except ImportError as error:
    print("could not import colorama:")
    print(error)
    raise SystemExit(1) from error

try:
    from commitizen.cz.utils import get_backup_file_path
except ImportError as error:
    print("could not import commitizen:")
    print(error)
    raise SystemExit(1) from error


def prepare_commit_msg(commit_msg_file: str) -> int:
    """Prepare or validate the commit message file; return process exit code."""
    path = Path(commit_msg_file)
    try:
        existing_content = path.read_text(encoding="utf-8").strip()
        non_comment_lines = [
            line
            for line in existing_content.split("\n")
            if not line.lstrip().startswith("#")
        ]
        existing_message = "\n".join(non_comment_lines).strip()
    except FileNotFoundError:
        existing_message = ""

    if existing_message:
        exit_code = subprocess.run(
            [
                "cz",
                "check",
                "--commit-msg-file",
                commit_msg_file,
            ],
            check=False,
            capture_output=True,
        ).returncode
        if exit_code == 0:
            return 0
        print(
            colored(
                "⚠️  Existing commit message detected (possibly from oco/opencommit). "
                "Skipping commitizen generation.",
                "yellow",
            ),
        )
        return 0

    backup_file = Path(get_backup_file_path())
    if backup_file.is_file():
        answer = input("retry with previous message? [y/N]: ")
        if answer.lower() == "y":
            shutil.copyfile(backup_file, commit_msg_file)
            return 0

    exit_code = subprocess.run(
        [
            "cz",
            "commit",
            "--dry-run",
            "--write-message-to-file",
            commit_msg_file,
        ],
        check=False,
        stdin=sys.stdin,
        stdout=sys.stdout,
    ).returncode
    if exit_code:
        return exit_code

    shutil.copyfile(commit_msg_file, backup_file)
    return 0
