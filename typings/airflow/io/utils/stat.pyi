"""
This type stub file was generated by pyright.
"""

class stat_result(dict):
    """
    stat_result: Result from stat, fstat, or lstat.

    This object provides a subset of os.stat_result attributes,
    for results returned from ObjectStoragePath.stat()

    It provides st_dev, st_ino, st_mode, st_nlink, st_uid, st_gid,
    st_size and st_mtime if they are available from the underlying
    storage. Extended attributes maybe accessed via dict access.

    See os.stat for more information.
    """

    st_dev = ...
    st_size = ...
    st_gid = ...
    st_uid = ...
    st_ino = ...
    st_nlink = ...
    @property
    def st_mtime(self):  # -> Literal[0] | None:
        """Time of most recent content modification."""
        ...

    @property
    def st_mode(self):  # -> Literal[40960, 16384, 32768, 0] | None:
        """Protection bits."""
        ...
