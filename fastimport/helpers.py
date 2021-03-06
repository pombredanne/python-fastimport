# Copyright (C) 2008 Canonical Ltd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Miscellaneous useful stuff."""


def _common_path_and_rest(l1, l2, common=[]):
    # From http://code.activestate.com/recipes/208993/
    if len(l1) < 1: return (common, l1, l2)
    if len(l2) < 1: return (common, l1, l2)
    if l1[0] != l2[0]: return (common, l1, l2)
    return _common_path_and_rest(l1[1:], l2[1:], common+[l1[0]])


def common_path(path1, path2):
    """Find the common bit of 2 paths."""
    return ''.join(_common_path_and_rest(path1, path2)[0])


def common_directory(paths):
    """Find the deepest common directory of a list of paths.

    :return: if no paths are provided, None is returned;
      if there is no common directory, '' is returned;
      otherwise the common directory with a trailing / is returned.
    """
    import posixpath
    def get_dir_with_slash(path):
        if path == '' or path.endswith('/'):
            return path
        else:
            dirname, basename = posixpath.split(path)
            if dirname == '':
                return dirname
            else:
                return dirname + '/'

    if not paths:
        return None
    elif len(paths) == 1:
        return get_dir_with_slash(paths[0])
    else:
        common = common_path(paths[0], paths[1])
        for path in paths[2:]:
            common = common_path(common, path)
        return get_dir_with_slash(common)


def is_inside(dir, fname):
    """True if fname is inside dir.

    The parameters should typically be passed to osutils.normpath first, so
    that . and .. and repeated slashes are eliminated, and the separators
    are canonical for the platform.

    The empty string as a dir name is taken as top-of-tree and matches
    everything.
    """
    # XXX: Most callers of this can actually do something smarter by
    # looking at the inventory
    if dir == fname:
        return True

    if dir == '':
        return True

    if dir[-1] != '/':
        dir += '/'

    return fname.startswith(dir)


def is_inside_any(dir_list, fname):
    """True if fname is inside any of given dirs."""
    for dirname in dir_list:
        if is_inside(dirname, fname):
            return True
    return False
