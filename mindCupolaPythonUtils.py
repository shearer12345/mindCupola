'''
Created on 23 Jul 2012

@author: shearer
'''
import inspect
from kivy.config import ConfigParser
def whoAmI():
    return inspect.stack()[1][3]

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno
