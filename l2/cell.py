class Cell:
    '''That from which everything is made. A unit of "memory" that holds two values: left and right.'''
    
    def __init__(self,left,right,override=None):
        '''left and right can be anything. override will be used when converting
           to strings, if specified, to mask internal structure (recursion)'''
        self.left = left
        self.right = right
        self.override = override
        
    def __str__(self):
        return self.override if self.override is not None else '( '+str(self.left)+' . '+str(self.right)+' )'
