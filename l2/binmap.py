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
