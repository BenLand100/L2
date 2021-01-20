class Symbol:
    '''The most primative atomic value; basically an upper case string.'''
    
    def __init__(self,name):
        self.name = name.upper()
    
    def __eq__(self,obj):
        if type(obj) != Symbol:
            raise Exception('Can not compare '+str(type(obj))+' to Symbol')
        return obj.name == self.name
    
    def __gt__(self,obj):
        if type(obj) != Symbol:
            raise Exception('Can not compare '+str(type(obj))+' to Symbol')
        return obj.name > self.name
    
    def __lt__(self,obj):
        if type(obj) != Symbol:
            raise Exception('Can not compare '+str(type(obj))+' to Symbol')
        return obj.name < self.name
    
    def __ge__(self,obj):
        if type(obj) != Symbol:
            raise Exception('Can not compare '+str(type(obj))+' to Symbol')
        return obj.name >= self.name
    
    def __le__(self,obj):
        if type(obj) != Symbol:
            raise Exception('Can not compare '+str(type(obj))+' to Symbol')
        return obj.name <= self.name
    
    def __ne__(self,obj):
        if type(obj) != Symbol:
            raise Exception('Can not compare '+str(type(obj))+' to Symbol')
        return obj.name != self.name
    
    def __str__(self):
        return self.name
