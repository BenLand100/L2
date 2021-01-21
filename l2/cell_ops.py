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

def is_list(head):
    while head is not None:
        if not isinstance(head,Cell):
            return False
        head = head.right
    return True

def to_iter(head):
    while head is not None:
        if isinstance(head,Cell) and (head.right is None or isinstance(head.right,Cell)):
            yield head.left
            head = head.right
        else:
            yield head
            break
        
def to_list(head):
    return [x for x in to_iter(head)]

def length(head):
    i = 0
    while head is not None:
        i = i+1
        head = head.right
    return i

def tail(head):
    while head.right is not None:
        head = head.right
    return head

def from_args(*elems):
    return from_list(elems)

def from_list(elems):
    head = None
    for elem in reversed(elems):
        head = Cell(elem,head)
    return head
    
def list_str(head):
    if not isinstance(head,Cell):
        return str(head)
    if head.override is not None:
        return head.override
    if not is_list(head):
        return str(head) # a cons structure, not a list
    lists = [list_str(elem) if isinstance(elem,Cell) else str(elem) for elem in to_list(head)]
    return '('+(' '.join(lists))+')'
