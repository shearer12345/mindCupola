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

class jsConfigParser(ConfigParser):
    
    def getdefault(self, section, option, defaultvalue):
        '''Get an option. If not found, it will return the default value
        '''
        if not self.has_section(section):
            return defaultvalue
        if not self.has_option(section, option):
            return defaultvalue
        return self.get(section, option)
    
    def getdefaultint(self, section, option, defaultvalue):
        '''Get an option. If not found, it will return the default value
        '''
        if not self.has_section(section):
            return defaultvalue
        if not self.has_option(section, option):
            return defaultvalue
        return self.getint(section, option)
    
    def getdefaultfloat(self, section, option, defaultvalue):
        '''Get an option. If not found, it will return the default value
        '''
        if not self.has_section(section):
            return defaultvalue
        if not self.has_option(section, option):
            return defaultvalue
        return self.getfloat(section, option)
    
    def getdefaultboolean(self, section, option, defaultvalue):
        '''Get an option. If not found, it will return the default value
        '''
        if not self.has_section(section):
            return defaultvalue
        if not self.has_option(section, option):
            return defaultvalue
        return self.getboolean(section, option)