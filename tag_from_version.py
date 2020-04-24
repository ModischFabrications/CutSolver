import sys

if sys.version_info[0] == 2:
    sys.exit("You are using Python 2.7 , let it die already...")

from pathlib import Path
from sys import stderr

from git import Repo

from app import main


def process():
    repo = Repo(Path("."))
    assert not repo.bare

    version = main.version
    newest_tag = repo.tags[-1]
    newest_git_version = newest_tag.name
    print(f"code version: {version}, git version: {newest_git_version}")

    if newest_git_version == version:
        print("Everything up to date, job done")
        return 0

    if newest_git_version > version:
        print("Git was updated without updating the code version!", file=stderr)
        # TODO: edit code (this is very dangerous!)
        return 1

    if newest_git_version < version:
        print("git tag outdated, updating with newest version")
        # this could technically go back in history until the version change happened,
        #  but as long as nothing was pushed we can skip local only versions.
        repo.create_tag(version, message=f"autobump version from {newest_git_version} to {version}")


if __name__ == '__main__':
    sys.exit(process())
