#  This file is part of L2.
#
#  L2 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  L2 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with L2.  If not, see <https://www.gnu.org/licenses/>.

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
