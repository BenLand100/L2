from .cell import Cell
from .symbol import Symbol
from . import parser
from . import scope
from . import cell_ops

class L2Machine:
    '''Virtual machine that implements the L2 language.'''
    
    def __init__(self):
        self.static_scope = scope.new()
        scope.bind(self.static_scope,Symbol('NIL'),None)
        scope.bind(self.static_scope,Symbol('T'),Symbol('T'))
        self.scope = self.static_scope
        self.special = {
            'PRINT':self.spec_print,
            'LAMBDA':self.spec_lambda,
            'MACRO':self.spec_macro,
            'BIND':self.spec_bind,
            'REF':self.spec_ref,
            'TYPE':self.spec_type,
            'QUOTE':self.spec_quote,
            'SETL':self.spec_setl,
            'SETR':self.spec_setr,
            'GETL':self.spec_getl,
            'GETR':self.spec_getr,
            'CELL':self.spec_cell,
            'APPEND':self.spec_append, #tricky to define this in L2 w/o let (needed for let syntax)
            'COND':self.spec_cond
        }
        lang = parser.parse('''
            ; required basic functionality
            (bind list (lambda (&rest args) args)) ;no defun yet
            (macro set (symbol value) `(setr ,`(ref ,symbol) ,value) )
            (macro defun (symbol args &rest body) 
                (list 'bind symbol (cell 'lambda (cell args body)) ) )
            (macro call (func &rest args) (cell func args))
            (macro if (test-case true-form &optional false-form) (cond 
                    (false-form `(cond ,`(,test-case ,true-form) ,`(t ,false-form)) )
                    (t `(cond ,`(,test-case ,true-form)) )))
            (macro let (variables &rest forms) `(  
                ,`(lambda ,(map (lambda (variable) (getl variable)) variables) ,@forms)
                ,@(map (lambda (variable) (if (getr variable) (getl (getr variable)))) variables) ) )
            (defun map (func args-list) (if args-list 
                (cell (func (getl args-list)) (map func (getr args-list))) ) ) 
                
            ; utilities
            (defun copy-list (list) (map (lambda (x) x) list))
            (defun last (list) (let ((next (getr list))) (if next (last next) list)) )
        ''')
        for expr in cell_ops.to_iter(lang):
            self.evaluate(expr)
        
    def spec_print(self,head):
        args = cell_ops.eval_all(self,head)
        print(*args)
        return None
    
    def spec_lambda(self,head):
        closure = Cell(Symbol("LAMBDA"),Cell(self.scope,head),override='lambda')
        return closure
    
    def spec_macro(self,head):
        symbol = head.left
        closure = Cell(Symbol("MACRO"),Cell(self.scope,head.right),override='macro')
        scope.bind(self.scope,symbol,closure)
        return closure
    
    def spec_bind(self,head):
        sym,val = cell_ops.to_list(head)
        val = self.evaluate(val)
        print('Bind',val,'to',sym)
        scope.bind(self.scope,sym,val)
        return val
    
    def spec_ref(self,head):
        sym, = cell_ops.to_list(head)
        return scope.reference(self.scope,sym)
    
    def spec_type(self,head):
        val, = cell_ops.eval_all(self,head)
        if isinstance(val,Cell):
            return Symbol('CELL')
        elif isinstance(val,Symbol):
            return Symbol('SYMBOL')
        elif type(val) == str:
            return Symbol('STRING')
        elif type(val) == int:
            return Symbol('INTEGER')
        elif type(val) == float:
            return Symbol('REAL')
        elif val is None:
            return Symbol('NIL')
        else:
            raise Exception('Unknown type, somehow.')
    
    def spec_quote(self,head):
        return head.left
    
    def spec_setl(self,head):
        cell,val = cell_ops.eval_all(self,head)
        cell.left = val
        return val
    
    def spec_setr(self,head):
        cell,val = cell_ops.eval_all(self,head)
        cell.right = val
        return val
    
    def spec_getl(self,head):
        cell, = cell_ops.eval_all(self,head)
        return cell.left
    
    def spec_getr(self,head):
        cell, = cell_ops.eval_all(self,head)
        return cell.right
    
    def spec_cell(self,head):
        left,right = cell_ops.eval_all(self,head)
        return Cell(left,right)
    
    def spec_append(self,head):
        lists = cell_ops.eval_all(self,head)
        last = lists[-1]
        rest = lists[:-1]
        elems = []
        for l in rest:
            elems.extend(cell_ops.to_list(l))
        result = cell_ops.from_list(elems)
        cell_ops.tail(result).right = last
        return result
    
    def spec_cond(self,head):
        for cond in cell_ops.to_iter(head):
            test,body = cell_ops.to_list(cond)
            if self.evaluate(test) is not None:
                return self.evaluate(body)
        return None
        
    def bind_args(self,syms_list,args_list):
        isym = 0
        iarg = 0
        while isym < len(syms_list):
            if syms_list[isym] == Symbol('&REST'):
                isym = isym+1
                scope.bind(self.scope,syms_list[isym],cell_ops.from_list(args_list[iarg:]))
                break
            elif syms_list[isym] == Symbol('&OPTIONAL'):
                isym = isym+1
                if iarg >= len(args_list):
                    scope.bind(self.scope,syms_list[isym],None)
                else:
                    scope.bind(self.scope,syms_list[isym],args_list[iarg])
            else:
                if iarg >= len(args_list):
                    raise Exception('Not enough arguments to fill symbols')
                scope.bind(self.scope,syms_list[iarg],args_list[iarg])
            isym = isym+1
            iarg = iarg+1
        
    def evaluate(self,expr):
        print('Eval:',cell_ops.list_str(expr))
        if isinstance(expr,Cell): # CELLs are executed (head is OP)
            op = self.evaluate(expr.left)
            if callable(op): # primitives are callable and handle evaluation
                return op(expr.right)
            elif isinstance(op,Cell):
                if op.left == Symbol("LAMBDA"): # evaluates all arguments, result returned
                    args = cell_ops.eval_all(self,expr.right)
                    syms = cell_ops.to_list(op.right.right.left)
                    body = op.right.right.right 
                    last_scope = self.scope #save current scope to restore later
                    self.scope = scope.new(op.right.left) #parent scope is closure scope
                    self.bind_args(syms,args)
                    result = None
                    for form in cell_ops.to_iter(body):
                        result = self.evaluate(form)
                    self.scope = last_scope
                    return result
                elif op.left == Symbol("MACRO"): # evaluates no arguments, result evaluated
                    args = cell_ops.to_list(expr.right)
                    syms = cell_ops.to_list(op.right.right.left)
                    body = op.right.right.right 
                    last_scope = self.scope #save current scope to restore later
                    self.scope = scope.new(op.right.left) #parent scope is closure scope
                    self.bind_args(syms,args)
                    result = None
                    for form in cell_ops.to_iter(body):
                        result = self.evaluate(form)
                    self.scope = last_scope
                    print('Macro expanded:',cell_ops.list_str(result))
                    print('From expression:',cell_ops.list_str(expr))
                    #Store expanded macro
                    expr.left = result.left
                    expr.right = result.right
                    return self.evaluate(result)
                else:
                    raise Exception('CELL is not LAMBDA or MACRO')
            else:
                raise Exception('Head of list is not executable: '+str(op))
        elif isinstance(expr,Symbol): # SYMBOLs are resolved on evaluation (maybe special symbol)
            if expr.name in self.special:
                return self.special[expr.name]
            else:
                return scope.resolve(self.scope,expr)
        else: # everything else evaluates to itself
            return expr
