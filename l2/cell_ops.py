from .cell import Cell

def is_list(head):
    while head is not None:
        if not isinstance(head,Cell):
            return False
        head = head.right
    return True

def to_iter(head):
    while head is not None:
        if isinstance(head,Cell):
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
    
def eval_all(machine,head):
    return [machine.evaluate(elem) for elem in to_iter(head)]

def list_str(head):
    if not isinstance(head,Cell):
        return str(head)
    lists = [list_str(elem) if isinstance(elem,Cell) else str(elem) for elem in to_list(head)]
    return '('+(' '.join(lists))+')'
