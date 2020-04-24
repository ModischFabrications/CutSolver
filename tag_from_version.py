import sys
from pathlib import Path
from sys import stderr

from git import Repo

from app import main


def process():
    repo = Repo(Path("."))
    assert not repo.bare

    version = main.version
    print(f"code version: {version}")
    newest_tag = repo.tags[-1]
    newest_git_version = newest_tag.name
    print(f"git version: {newest_git_version}")

    if newest_git_version == version:
        print("Everything up to date, job done")
        return 0

    if newest_git_version > version:
        print("You updated git without updating the code version!", file=stderr)
        # TODO: edit code (this is very dangerous!)
        return 1

    if newest_git_version < version:
        print("git version outdated, updating with newest tag")
        # FIXME: tag with new version
        # repo.create_tag()


if __name__ == '__main__':
    sys.exit(process())
