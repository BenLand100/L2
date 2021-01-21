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

'''Python logic for creating a binary tree of (Symbol) keys that map to values out of Cells.'''
    
def new():
    return Cell(None,None)

def put(root,key,value):
    if root.left == None or root.left.left == key:
        root.left = Cell(key,value)
        root.right = Cell(new(),new())
    elif key < root.left.left:
        put(root.right.left,key,value)
    else:
        put(root.right.right,key,value)
    
def find(root,key):
    if root.left == None:
        return None
    elif root.left.left == key:
        return root.left
    elif key < root.left.left:
        return find(root.right.left,key)
    else:
        return find(root.right.right,key)
