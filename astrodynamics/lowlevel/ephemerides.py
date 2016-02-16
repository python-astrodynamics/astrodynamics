# coding: utf-8
"""The astrodynamics.lowlevel.ephemerides module

This module contains a wrapper around the 'jplephem'
library by Brandon Rhodes.
"""

from __future__ import absolute_import, division, print_function

import jplephem.spk as spk
import networkx as nx
import numpy as np


class JPLEphemeris(object):
    def load_kernel(self, spk_file):
        self._kernel = spk.SPK.open(spk_file)
        self.generate_paths()

    def generate_paths(self):
        graph = nx.Graph()
        for edge in self.kernel.pairs:
            graph.add_edge(*edge)
        self.paths = nx.shortest_path(graph)

    @property
    def kernel(self):
        _kernel = getattr(self, '_kernel', None)
        if not _kernel:
            raise AttributeError("No SPICE kernel was loaded.")
        else:
            return self._kernel

    def _compute_segment(self, origin, target, tdb, tdb2):
        if (target, origin) in self.kernel.pairs:
            origin, target = target, origin
            factor = -1
        elif (origin, target) in self.kernel.pairs:
            factor = 1
        segment = self.kernel[origin, target]
        r, v = segment.compute_and_differentiate(tdb, tdb2)
        return factor * r, factor * v

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
        if origin not in self.paths or target not in self.paths:
            raise ValueError("Unknown pair({}, {}).".format(origin, target))
        path = self.paths[origin][target]
        r, v = self._compute_path(path, tdb, tdb2)
        return r, v
