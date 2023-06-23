import os
import shutil
import sys
from tempfile import TemporaryDirectory

from git import Repo


def create_temp_repo(dirname, tempdir):
    # Copy all files from dirname to tempdir
    for item in os.listdir(dirname):
        s = os.path.join(dirname, item)
        d = os.path.join(tempdir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)

    # Copy .docs subdir to tempdir as 'docs'
    docs_src = os.path.join(dirname, ".docs")
    docs_dst = os.path.join(tempdir, "docs")
    shutil.copytree(docs_src, docs_dst, False, None)

    # Create a new git repo in tempdir
    repo = Repo.init(tempdir)

    # Add all copied files to the repo, excluding those with 'test' in the filename
    for item in os.listdir(tempdir):
        if "test" not in item:
            repo.git.add(item)

    # Commit with message "initial"
    repo.git.commit(m="initial")


def main(tempdir):
    if len(sys.argv) != 2:
        print("Usage: python benchmark.py <dirname>")
        sys.exit(1)

    dirname = sys.argv[1]

    create_temp_repo(dirname, tempdir)


if __name__ == "__main__":
    # with TemporaryDirectory() as tempdir:
    tempdir = "tmp.benchmark"
    main(tempdir)
