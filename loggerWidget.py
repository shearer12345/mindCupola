'''
Created on 19 Aug 2012

@author: shearer
'''
from os.path import getmtime
from functools import partial

from kivy import Logger
from kivy.uix.rst import RstDocument
from kivy.clock import Clock
from stringUtils import stringReplace

class LoggerWidget(RstDocument):
    
    logLastModificationTime = 0
    logFileName = str(Logger.handlers[1].fd.name)
        
    def __init__(self, **kwargs):
        super(LoggerWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.onLoggerCheck, -1)
        
    def onLoggerCheck(self, dt):
        Logger.trace(self.__class__.__name__ + ': Checking Log')
        
        newLogLastModifiedTime = getmtime(self.logFileName)
        logTimeSinceLastCheckedModification = newLogLastModifiedTime - self.logLastModificationTime
        self.logLastModificationTime = newLogLastModifiedTime

        if logTimeSinceLastCheckedModification > 0:
            logtext = open(self.logFileName).read()
            logtext = stringReplace(logtext, '\r\n', '\r\n  ')
            logtext = '::\r\n\r\n  ' + logtext + '\r\n'
            self.title = self.logFileName.rpartition('/')[2]
            self.text = logtext
            Clock.schedule_once(self.gotoEnd, 0.3)
            Clock.schedule_once(self.onLoggerCheck, 1) # had a recent change so check aggresively
        else:
            Clock.schedule_once(self.onLoggerCheck, min(15, 16))
        
    def gotoEnd(self, dt=None):
        self.scroll_y = 0

from kivy.app import App
class LoggerWidgetTestApp(App):
    
    def build(self):
        loggerWidget = LoggerWidget()
        return loggerWidget
                        
# self run, self test     
if __name__ == "__main__":
    Logger.info(__file__ + ': running from __name__')

    eyeTrackerTestApp = LoggerWidgetTestApp()
    eyeTrackerTestApp.run()



 