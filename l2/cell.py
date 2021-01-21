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
