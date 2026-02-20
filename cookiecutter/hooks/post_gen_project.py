import os
import shutil
from pathlib import Path


def remove_path(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

def main():
    platform = "{{ cookiecutter.platform }}".lower()
    project_dir = Path.cwd()

    if platform == "github":
        # Remove GitLab specific files
        remove_path(project_dir / ".gitlab-ci.yml")
    elif platform == "gitlab":
        # Remove GitHub specific files
        remove_path(project_dir / ".github")

if __name__ == "__main__":
    main()
