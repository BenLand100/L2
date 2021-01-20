#!/usr/bin/env python3

import l2
import l2.cell_ops as ops
import sys
import readline

m = l2.L2Machine()

try:
    while True:
        expr_str = input('>> ')
        exprs = l2.parse(expr_str)
        for expr in ops.to_list(exprs): 
          result = m.evaluate(expr)
        print(ops.list_str(result))
except KeyboardInterrupt:
    sys.exit(0)
