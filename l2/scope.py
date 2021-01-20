from .cell import Cell
from . import binmap

'''Python logic for creating variable scope control out of Cells.
   Basically a linked list of BinMap that are searched in order.'''

def new(parent=None):
    return Cell(binmap.new(),parent)

def bind(root,sym,value):
    binmap.put(root.left,sym,value)

def reference(root,sym):
    ref = binmap.find(root.left,sym)
    if ref is None and root.right is not None:
        return reference(root.right,sym)
    else:
        return ref

def resolve(root,sym):
    ref = reference(root,sym)
    if ref is None:
        raise Exception(str(sym) + ' not defined')
    return ref.right
