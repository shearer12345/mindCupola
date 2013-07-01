'''
Created on 21 Jul 2012

@author: shearer
'''

def stringReplace(sourceString, removalString, replacementString=''):
    """Remove any occurrences of characters in removalString, from string sourceString
    sourceString - string to be filtered, removalString - characters to filter"""
    
    assert type(sourceString) is str, 'sourceString is not a string: %s' % type(sourceString)
    assert type(removalString) is str, 'removalString is not a string: %s' % type(removalString)
    
    for a in removalString:
        sourceString = sourceString.replace(a,replacementString)
    return sourceString

def stringToBestType(stringToCast):
    
    try:
        stringToCast = int(stringToCast)
        try:
            stringToCast = bool(stringToCast)
        except ValueError:
            pass
    except ValueError:
        try:
            stringToCast = float(stringToCast)
        except ValueError:
            pass
    return stringToCast

def insertLineBreaks(logString):
        return stringReplace(logString, '[', '\r\n[')
