# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:37:40 2021

@author: Kristian
"""


import abc 

"""abc works by marking methods of the base class as abstract, 
and then registering concrete classes as implementations of the abstract base"""

import abc

class PluginBase(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def load(self, input):
        """Retrieve data from the input source and return an object."""
        return
    
    @abc.abstractmethod
    def save(self, output, data):
        """Save the data object to the output."""
        return
    "Registering a concrete class"
    
"""Two ways to indicate that a concrete class implements an abstract:
    1. register the class with the abc
    2. subclass directly from the abc"""
    

class SubclassImplementation(PluginBase):
    
    def load(self, input):
        return input.read()
    
    def save(self, output, data):
        return output.write(data)

if __name__ == '__main__':
    print('Subclass:', issubclass(SubclassImplementation, PluginBase))
    print('Instance:', isinstance(SubclassImplementation(), PluginBase))
    
'The other way (#1) does not work; specifically registering the class explicitly'

'A benfit of subclassing directly is that the subclass cannot be instantiated unless it fully implements the abstract portion of the API'
'Prevents half-baked implementations from triggering unexpected errors at run time'




    