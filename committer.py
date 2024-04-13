import subprocess
import random
from datetime import datetime, timedelta
import os


def run_git_command(command, env=None):
    """Run a git command in the shell and return its output."""
    result = subprocess.run(command, shell=True, text=True,
                            capture_output=True, env=env)
    return result.stdout.strip()


def list_files(directory):
    """Recursively list all files in the directory."""
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files


def get_uncommitted_files():
    """Get a list of uncommitted files in the git repository."""
    tracked_files = run_git_command("git ls-files")
    all_files = list_files(".")
    uncommitted_files = [f for f in all_files if
                         f not in tracked_files and not os.path.isdir(f)]
    return uncommitted_files


def commit_files(start_date):
    """Commit files with a unique message on sequential dates with random times."""
    files = get_uncommitted_files()
    date = datetime.strptime(start_date, "%Y-%m-%d")

    for i, file in enumerate(files):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        timestamp = date.replace(hour=hour, minute=minute,
                                 second=second).isoformat()

        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = timestamp
        env['GIT_COMMITTER_DATE'] = timestamp

        run_git_command(f"git add '{file}'", env=env)
        run_git_command(f"git commit -m 'feat: adding file {file}'", env=env)

        if i < len(files) - 1 and random.random() > 0.7:
            date += timedelta(days=1)


if __name__ == "__main__":
    import sys

    start_date = sys.argv[1]  # Expecting date in YYYY-MM-DD format
    commit_files(start_date)
