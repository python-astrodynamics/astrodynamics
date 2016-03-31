# coding: utf-8
# The frames implementation in astrodynamics is a derivative work of the
# implementation in Orekit. It retains the original license (see
# licenses/OREKIT.txt)
from __future__ import absolute_import, division, print_function

import weakref
from abc import ABCMeta, abstractmethod, abstractproperty, abstractstaticmethod
from collections import Sequence
from functools import partial, wraps

import six
from represent import ReprHelper

from ..utils import read_only_property
from .transform import Transform


class AncestorsDescriptor(object):
    """Use :class:`AncestorsProxy` to add an ``ancestors`` attribute to a class."""
    def __init__(self, doc=None):
        self.instances = weakref.WeakKeyDictionary()
        if doc is not None:
            self.__doc__ = doc

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if instance not in self.instances:
            self.instances[instance] = AncestorsProxy(instance)

        return self.instances[instance]

    def __set__(self, instance, owner):
        # By providing __set__, we are a data descriptor and show up better
        # when calling help() on the owning class. This is because the docstring
        # of non-data descriptors isn't shown.
        raise AttributeError("can't set attribute")


class AncestorsProxy(Sequence):
    """Given an object with ``parent`` and ``depth`` attributes, provide lazy
    access to its ancestors using item access.

    Example:
        .. code-block:: python

            obj = MyObject(...)
            ancestors = AncestorsProxy(obj)
            assert ancestors[0] == obj
            assert ancestors[1] == obj.parent

    .. note::

        The recommended usage is adding :class:`AncestorsDescriptor` to a
        class with the ``parent`` attribute.
    """
    def __init__(self, instance):
        self._ancestor_refs = [weakref.ref(instance)]

    def __getitem__(self, item):
        # Calculate index of last item we need to return
        if isinstance(item, int):
            if item >= 0:
                last = item
            else:
                last = len(self) + item
        elif isinstance(item, slice):
            _, stop, _ = item.indices(len(self))
            last = stop - 1
        else:
            raise TypeError('Ancestor indices must be integers or slices.')

        # Try to lazily load any parents we don't have weak references to.
        if last > len(self._ancestor_refs) - 1:
            ref = self._ancestor_refs[-1]
            current = ref()

            for i in range(len(self._ancestor_refs), last + 1):
                if current.parent is None:
                    raise IndexError('{} has no parent.'.format(current))
                self._ancestor_refs.append(weakref.ref(current.parent))
                current = current.parent

        if isinstance(item, int):
            ref = self._ancestor_refs[item]
            return ref()
        elif isinstance(item, slice):
            return [ref() for ref in self._ancestor_refs[item]]

    def __len__(self):
        return self.depth + 1


@six.add_metaclass(ABCMeta)
class AbstractFrame(object):
    @abstractproperty
    def parent(self):
        raise NotImplementedError

    @abstractproperty
    def depth(self):
        raise NotImplementedError

    @abstractproperty
    def transform_provider(self):
        raise NotImplementedError

    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractproperty
    def pseudo_intertial(self):
        raise NotImplementedError

    @abstractproperty
    def ancestors(self):
        raise NotImplementedError

    @abstractmethod
    def get_transform_to(self, date):
        raise NotImplementedError

    @abstractstaticmethod
    def find_common_ancestor(from_, to):
        raise NotImplementedError


class Frame(AbstractFrame):
    """Reference frame class."""
    parent = read_only_property('_parent', 'Parent frame.')
    depth = read_only_property('_depth', 'Depth of frame in tree.')
    transform_provider = read_only_property('_transform_provider', 'Provides transform from parent to instance.')
    name = read_only_property('_name', 'Name of frame.')
    pseudo_intertial = read_only_property('_pseudo_intertial', 'Whether frame is pseudo-intertial.')
    ancestors = AncestorsDescriptor("An immutable sequence providing access to this frames' ancestors")

    def __init__(self, parent, transform_provider, name, pseudo_intertial):
        self._parent = parent
        self._depth = parent.depth + 1 if parent is not None else 0
        self._transform_provider = transform_provider
        self._name = name
        self._pseudo_intertial = pseudo_intertial

    def get_transform_to(self, destination_frame, date):
        if destination_frame is self:
            return Transform(date)

        common = Frame.find_common_ancestor(self, destination_frame)

        common_to_instance = Transform(date)
        for frame in self.ancestors:
            if frame is common:
                break
            common_to_instance = (
                frame.transform_provider.get_transform(date) +
                common_to_instance)

        common_to_destination = Transform(date)
        for frame in destination_frame.ancestors:
            if frame is common:
                break
            common_to_destination = (
                frame.transform_provider.get_transform(date) +
                common_to_destination)

        return ~common_to_instance + common_to_destination

    @staticmethod
    def find_common_ancestor(from_, to):
        if from_.depth > to.depth:
            current_from = from_.ancestors[from_.depth - to.depth]
            current_to = to
        else:
            current_from = from_
            current_to = to.ancestors[to.depth - from_.depth]

        while current_from != current_to:
            current_from = current_from.parent
            current_to = current_to.parent

        return current_from

    def __repr__(self):
        r = ReprHelper(self)
        r.parantheses = ('<', '>')
        r.keyword_from_attr('name')
        return str(r)


class FrameProxy(AbstractFrame):
    """Proxy a :class:`Frame` using a factory function for lazy initialisation."""

    def __init__(self):
        self._factory = None
        self._frame = None

    def register_factory(self, factory):
        if self._factory is not None:
            raise RuntimeError('This FrameProxy already has a registered factory.')
        self._factory = factory

    def _lazy_init(self):
        if self._frame is None:
            if self._factory is None:
                raise RuntimeError('Factory not registered with this FrameProxy')
            self._frame = self._factory()

    @property
    def parent(self):
        self._lazy_init()
        return self._frame.parent

    @property
    def depth(self):
        self._lazy_init()
        return self._frame.depth

    @property
    def transform_provider(self):
        self._lazy_init()
        return self._frame.transform_provider

    @property
    def name(self):
        self._lazy_init()
        return self._frame.name

    @property
    def pseudo_intertial(self):
        self._lazy_init()
        return self._frame.pseudo_intertial

    @property
    def ancestors(self):
        self._lazy_init()
        return self._frame.ancestors

    def get_transform_to(self, destination_frame, date):
        self._lazy_init()
        return self._frame.get_transform_to(destination_frame, date)

    def find_common_ancestor(self, from_, to):
        self._lazy_init()
        return self._frame.find_common_ancestor(from_, to)
