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
