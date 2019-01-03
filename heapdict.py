import collections

from typing import Tuple, Hashable, Any


def doc(s):
    if hasattr(s, '__call__'):
        s = s.__doc__

    def f(g):
        g.__doc__ = s
        return g
    return f


class HeapDict(collections.MutableMapping):
    __marker = object()

    @staticmethod
    def _parent(i):
        return (i - 1) >> 1

    @staticmethod
    def _left(i):
        return (i << 1) + 1

    @staticmethod
    def _right(i):
        return (i + 1) << 1
    
    def __init__(self, *args, **kw):
        self.heap = []
        self.d = {}
        self.update(*args, **kw)

    @doc(dict.clear)
    def clear(self):
        del self.heap[:]
        self.d.clear()

    @doc(dict.__setitem__)
    def __setitem__(self, key: Any, value: int):
        if key in self.d:
            self.pop(key)
        wrapper = [value, key, len(self)]
        self.d[key] = wrapper
        self.heap.append(wrapper)
        self._decrease_key(len(self.heap)-1)

    def _min_heapify(self, i):
        left = self._left(i)
        right = self._right(i)
        n = len(self.heap)
        if left < n and self.heap[left][0] < self.heap[i][0]:
            low = left
        else:
            low = i
        if right < n and self.heap[right][0] < self.heap[low][0]:
            low = right

        if low != i:
            self._swap(i, low)
            self._min_heapify(low)

    def _decrease_key(self, i):
        while i:
            parent = self._parent(i)
            if self.heap[parent][0] < self.heap[i][0]: break
            self._swap(i, parent)
            i = parent

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.heap[i][2] = i
        self.heap[j][2] = j

    @doc(dict.__delitem__)
    def __delitem__(self, key):
        wrapper = self.d[key]
        while wrapper[2]:
            parentpos = self._parent(wrapper[2])
            parent = self.heap[parentpos]
            self._swap(wrapper[2], parent[2])
        self.popitem()

    @doc(dict.__getitem__)
    def __getitem__(self, key):
        return self.d[key][0]

    @doc(dict.__iter__)
    def __iter__(self):
        return iter(self.d)

    def popitem(self) -> Tuple[Hashable, float]:
        """
        D.popitem() -> (k, v), remove and return the (key, value) pair with
        lowest value; but raise KeyError if D is empty.

        Remove and return the (key, value) pair with lowest value
        """
        if len(self.heap) == 0:
            raise KeyError('priority queue is empty')

        wrapper = self.heap[0]
        if len(self.heap) == 1:
            self.heap.pop()
        else:
            self.heap[0] = self.heap.pop(-1)
            self.heap[0][2] = 0
            self._min_heapify(0)
        del self.d[wrapper[1]]
        return wrapper[1], wrapper[0]

    def peekitem(self) -> Tuple[Hashable, float]:
        """
        D.peekitem() -> (k, v), return the (key, value) pair with lowest value;
        but raise KeyError if D is empty.
        """
        if len(self.heap) == 0:
            raise KeyError('priority queue is empty')

        return self.heap[0][1], self.heap[0][0]

    @doc(dict.__len__)
    def __len__(self):
        return len(self.d)


del doc
__all__ = ['HeapDict']
