'''
Created on 13 Dec 2012

@author: shearer

dependencies:
    from http://pypi.python.org/pypi/txosc download txosc, unpack and "python setup.py install" it
    from http://www.lfd.uci.edu/~gohlke/pythonlibs/ download twisted and install
'''
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from txosc import osc
from txosc import dispatch
from txosc import async

from kivy.properties import BooleanProperty
    
class OscSender():
    
    def __init__(self, namespace_prefix, host, port, verbose=False):
        assert type(namespace_prefix) is str
        assert type(host) is str
        assert type(port) is int
        assert type(verbose) in [bool, BooleanProperty]
        
        self.verbose = verbose
        
        self.namespace_prefix = namespace_prefix
        self.host = host
        self.port = port
        
        self._oscBundle = osc.Bundle()
        
        self._oscSender = async.DatagramClientProtocol()
        global reactor
        self._sender_port = reactor.listenUDP(0, self._oscSender)
        
    def _sendBundle(self):
        #print 'Sending bundle with ' + str(len( self._oscBundle.elements)) + ' elements to ' + self.host + ':' + str(self.port)
        bundleString = ''
        for sub in self._oscBundle.elements:
            tmp = str(sub) + '\r\n'
            bundleString += tmp
            #print tmp
        self._oscSender.send(self._oscBundle, (self.host, self.port))
        self._oscBundle = osc.Bundle() #empty the bundle
        
    def sendMessage(self, message):
        
        assert type(message) is osc.Message
        
        if self.verbose: 
            print 'Sending Message: ' + str(message.getTypeTags()) + ' :: ' + str(message.getValues()) + ' to ' + str(message.address) + '@' + str(self.host) + ':' + str(self.port)
        #if bundle is empty or huge then we should schedule a bundle send
        bundleLength = len(self._oscBundle.elements)
        if bundleLength == 0 or bundleLength > 100:
            global reactor
            reactor.callLater(0.02, self._sendBundle)
        
        self._oscBundle.add(message)
            
    def send(self, commandString, commandValueOrValues=None):
        
        assert type(commandString) is str
        assert type(self.namespace_prefix) is str
        fullCommandString = '/' + self.namespace_prefix + '/' + commandString
        
        if type(commandValueOrValues) in [int, float, str]:
            message = osc.Message(fullCommandString, commandValueOrValues)
        elif type(commandValueOrValues) in [list, tuple]:
            message = osc.Message(fullCommandString, *commandValueOrValues)
        self.sendMessage(message)