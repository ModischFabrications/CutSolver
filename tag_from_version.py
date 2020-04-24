import sys

if sys.version_info[0] == 2:
    sys.exit("You are using Python 2.7 , let it die already...")

from pathlib import Path
from sys import stderr

from git import Repo

from app import main


def compare_versions(left: str, right: str):
    # strip of "v"
    left = left[1:]
    right = right[1:]

    for left, right in zip(left.split("."), right.split(".")):
        l_version = int(left)
        r_version = int(right)

        if l_version == r_version:
            continue
        if l_version > r_version:
            return 1
        if l_version < r_version:
            return -1
        return

    return 0


def process():
    repo = Repo(Path("."))
    assert not repo.bare

    version = main.version

    version_tags_only = tuple(filter(lambda tag: tag.name[0] == "v", repo.tags))
    newest_tag = version_tags_only[-1]
    newest_git_version = newest_tag.name

    print(f"code version: {version}, git version: {newest_git_version}")

    if compare_versions(newest_git_version, version) == 0:
        print("Everything up to date, job done")
        return 0

    if compare_versions(newest_git_version, version) > 0:
        print("Git was updated without updating the code version!", file=stderr)
        # TODO: edit code (this is very dangerous!)
        return 1

    if compare_versions(newest_git_version, version) < 0:
        print("git tag outdated, updating with newest version")
        # this could technically go back in history until the version change happened,
        #  but as long as nothing was pushed we can skip local only versions.
        repo.create_tag(version, message=f"autobump version from {newest_git_version} to {version}")


if __name__ == '__main__':
    sys.exit(process())
