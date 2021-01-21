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
from .symbol import Symbol
from . import cell_ops 

import re

def is_string(tok):
    return tok[0] == '"' and tok[-1] == '"'

def is_integer(tok):
    try:
        int(tok)
        return True
    except ValueError:
        return False

def is_real(tok):
    try:
        float(tok)
        return True
    except ValueError:
        return False

def parse(expr_str):
    '''Converts a string into a Cell datastructure'''
    expr_str = re.sub(';[^\n]+','',expr_str) #remove comments
    toks = re.findall(r'''"(?:[\\].|[^\\"])*"|\(|\)|,@|'|`|,|[^\s\)\(]+''',expr_str)
    head = None
    prev_heads = []
    for tok in reversed(toks):
        if tok == ')':
            prev_heads.append(head)
            head = None
        elif tok == '(':
            head = Cell(head,prev_heads.pop())
        elif tok == "'":
            head = Cell(cell_ops.from_args(Symbol("QUOTE"),head.left),head.right)
        elif tok == "`": # Backquote is just syntatical sugar, but it's very sweet
            if not isinstance(head.left,Cell):
                raise Exception('Can only backquote a list')
            elems = cell_ops.to_list(head.left)
            rest = head.right
            if len(elems) > 0:
                ops = []
                temp = []
                for elem in elems:
                    if isinstance(elem,Symbol) and elem == Symbol(','):
                        ops.append('evaluate')
                    elif isinstance(elem,Symbol) and elem == Symbol(',@'):
                        ops.append('splice')
                    else:
                        if len(ops) == len(temp):
                            ops.append('quote')
                        temp.append(elem)
                new = None
                #If there are no splice, this could use LIST w/ args instead of nested CELL
                for op,elem in zip(reversed(ops),reversed(temp)):
                    if op == 'evaluate':
                        new = cell_ops.from_args(Symbol('CELL'),elem,new)
                    elif op == 'splice':
                        if new is None: # special case for splice at end of list
                            new = elem
                        else:
                            new = cell_ops.from_args(Symbol('APPEND'),elem,new)
                    else:
                        new = cell_ops.from_args(Symbol('CELL'),cell_ops.from_args(Symbol('QUOTE'),elem),new)
                head = Cell(new,rest)
            else:
                head = Cell(None,rest)
        else:
            if is_string(tok):
                head = Cell(tok[1:-1],head)
            elif is_integer(tok):
                head = Cell(int(tok),head)
            elif is_real(tok):
                head = Cell(float(tok),head)
            else:
                head = Cell(Symbol(tok),head)
            
    if len(prev_heads) != 0:
        raise Exception('Unbalanced parentheses detected')
    return head
