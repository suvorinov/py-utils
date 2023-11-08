# -*- coding: utf-8 -*-
# @Author: suvorinov
# @Date:   2023-05-18 10:06:55
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-05-18 10:26:44

import os
import tarfile
import zipfile
from typing import List


def extract_all(path, path_to=None) -> List:
    """Extract archive file.

    Parameters
    ----------
    path: str
        Path of archive file to be extracted.
    path_to: str, optional
        Directory to which the archive file will be extracted.
        If None, it will be set to the parent directory of the archive file.
    """
    if path_to is None:
        to = os.path.dirname(path)

    if path.endswith(".zip"):
        opener, mode = zipfile.ZipFile, "r"
    elif path.endswith(".tar"):
        opener, mode = tarfile.open, "r"
    elif path.endswith(".tar.gz") or path.endswith(".tgz"):
        opener, mode = tarfile.open, "r:gz"
    elif path.endswith(".tar.bz2") or path.endswith(".tbz"):
        opener, mode = tarfile.open, "r:bz2"
    else:
        raise ValueError(
            "Could not extract '%s' as no appropriate "
            "extractor is found" % path
        )

    def namelist(f):
        if isinstance(f, zipfile.ZipFile):
            return f.namelist()
        return [m.path for m in f.members]

    def filelist(f):
        files = []
        for fname in namelist(f):
            fname = os.path.join(to, fname)
            files.append(fname)
        return files

    with opener(path, mode) as f:
        f.extractall(path=path_to)

    return filelist(f)
