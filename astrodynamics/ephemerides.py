# coding: utf-8
from __future__ import absolute_import, division, print_function

import jplephem.spk as spk
import numpy as np


def parent(id):
    if len(id) == 1:
        return '0'
    else:
        return id[0]


def parents(id):
    if len(id) == 3:
        return [0, int(id[0]), int(id)]
    else:
        return [0, int(id)]


def is_child(origin, target):
    return origin == parent(target)


def is_grandchild(origin, target):
    return origin == parent(parent(target))


def is_sibling(origin, target):
    return parent(origin) == parent(target)


def paths(origin, target):
    if is_child(origin, target):
        return [int(origin), int(target)], []
    elif is_sibling(origin, target):
        p = int(parent(origin))
        return [p, int(origin)], [p, int(target)]
    elif is_grandchild(origin, target):
        return [int(origin), int(parent(target)), int(target)], []
    else:
        return parents(origin), parents(target)


class JPLEphemeris(object):
    def __init__(self, spk_file):
        self.kernel = spk.SPK.open(spk_file)

    def _compute_segment(self, origin, target, tdb, tdb2):
        if (origin, target) not in self.kernel.pairs:
            raise ValueError("Unknown pair({}, {}).".format(origin, target))
        segment = self.kernel[origin, target]
        return segment.compute_and_differentiate(tdb, tdb2)

    def _compute_path(self, path, tdb, tdb2):
        if len(path) == 2:
            r, v = self._compute_segment(path[0], path[1], tdb, tdb2)
        else:
            r = np.zeros(3)
            v = np.zeros(3)
            for origin, target in zip(path, path[1:]):
                rs, vs = self._compute_segment(origin, target, tdb, tdb2)
                r += rs
                v += vs
        return r, v

    def rv(self, origin, target, tdb, tdb2=0.0):
        opath, tpath = paths(str(origin), str(target))
        ro, vo = self._compute_path(opath, tdb, tdb2)
        if tpath:
            rt, vt = self._compute_path(tpath, tdb, tdb2)
            return rt - ro, vt - vo
        else:
            return ro, vo
