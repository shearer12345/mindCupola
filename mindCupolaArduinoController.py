'''
Created on 19 Aug 2012

@author: shearer
'''

#TODO setup input device permissions - http://sourceforge.net/apps/mediawiki/gizmod/index.php?title=HOWTO_-_Setting_Input_Device_Permissions_-_Creating_a_udev_Rule
import sys
from types import NoneType

from kivy.support import install_twisted_reactor
from traits.tests.test_property_notifications import on_anyvalue_changed
from kivy.uix.label import Label

install_twisted_reactor() 

try:
#    from twisted.internet.protocol import DatagramProtocol
    from twisted.internet import reactor
    from twisted.internet.serialport import SerialPort
    from twisted.internet.protocol import Protocol
    from serial.serialutil import SerialException
   
except:
    print '''Missing dependencies:
    from http://pypi.python.org/pypi/txosc download txosc, unpack and "python setup.py install" it
    from http://www.lfd.uci.edu/~gohlke/pythonlibs/ download twisted and install'''
    sys.exit(1)

from kivy import Logger
from mindCupolaPythonUtils import whoAmI

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty, BoundedNumericProperty, StringProperty, ReferenceListProperty

class MindCupolaArduinoProtocol(Protocol):
    
    matrixLeftRows         = [
                                [True,   True,  True,   True,  True,   True],
                                [True,  False,   False,  False,   False,  True],
                                [True,   False,  True,   True,  False,   True],
                                [True,  False,   False,  False,   False,  True],
                                [True,   True,  True,   True,  True,   True],
                                ]      
    
    matrixRightRows         = [
                                [True,   True,  True,   True,  True,   True],
                                [True,  False,   False,  False,   False,  True],
                                [True,   False,  True,   True,  False,   True],
                                [True,  False,   False,  False,   False,  True],
                                [True,   True,  True,   True,  True,   True],
                                ]      
      
    def __init__(self, mindCupolaArduinoController):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        
        #where data should persist and external methods 
        assert isinstance(mindCupolaArduinoController, MindCupolaArduinoController)
        self.mindCupolaArduinoController = mindCupolaArduinoController # protocol's factory, so can access persistent data (in the factory)
    
    def matrixRowsInvert(self, matrixRows):
        returnRows = []
        for row in matrixRows:
            newRow = []
            for value in row:
                newValue = False if value else True
                newRow.append(newValue)
            returnRows.append(newRow)
        return returnRows
                
    def matrixRowsToString(self, matrixRows):
        '''convert a list of LED matrix rows into a string to send to the LED controller
            string represents a bitwise representation of on/off states 
            string includes byte 
            assumes Least_Signifcant bit of the hexcode to send is the right-hand end of the first row, moving left
            assumes maximum of 32 LEDS (tested on 30 LEDS
            '''
        
        runningSum = 0;

        for row in reversed(matrixRows):
            for value in row:
                runningSum += 1 if value else 0
                runningSum = runningSum << 1
        runningSum = runningSum >> 1 #undo the last, needless bitshift
        return  (   chr(    (runningSum & 0x000000ff) >> 0) + 
                    chr(    (runningSum & 0x0000ff00) >> 8) +
                    chr(    (runningSum & 0x00ff0000) >> 16) +
                    chr(    (runningSum & 0xff000000) >> 24)
                )

    def dataReceived(self, data):
#        print data
        if len(data) == 1:
            i = int(data)
            assert 0 <= i 
            assert i <= 3
#             Logger.trace(self.__class__.__name__ + ': in ' + whoAmI() + '. ' + 'State is: ' + state)
            self.mindCupolaArduinoController.setModeAutomatically(i)
            
    def testOutput(self):
        #=======================================================================
        # The Cupola support output to 3 devices.
        # Each message is 7 bytes longer
        # starting with '<' and ending with '>'
        # central bytes are ABCDE
        # A = device bit
        #   '1' = Devices
        #   '2' = Left Matrix
        #   '3' = Right Matrix
        # For Devices:
        #   only the 3rd byte matters for the devices, and bit encodes which devices should be on. as:
        #     bit 7 (MSB) = 
        #     bit 6       = ?
        #     bit 5       = ?
        #     bit 4       = ?
        #     bit 3       = ?
        #     bit 2       = ?
        #     bit 1       = ?
        #     bit 0 (LSB) = ?
        #  then follow by '000'
        # 2 Left Matrix: 30 bytes <1?????????????????>
        # 3 Right Matrix: 30 bytes <2?????????????????>
        # 
        
        arduinoPrefix = '<'
        
        arduinoDevices = {'cupola': '3',
                          'leftMatrix': '1',
                          'rightMatrix': '2',}
        arduinoDevice = arduinoDevices['cupola']
        
        #cupolaItems = 
        cupolaString = '8000'
        arduinoSuffix = '>' 
        
        leftMatrixControlString = self.matrixRowsToString(self.matrixLeftRows)
        rightMatrixControlString = self.matrixRowsToString(self.matrixRightRows)
        
        cupolaArduinoString = arduinoPrefix + arduinoDevices['cupola'] + cupolaString + arduinoSuffix
        leftMatrixArduinoString = arduinoPrefix + arduinoDevices['leftMatrix'] + leftMatrixControlString + arduinoSuffix
        rightMatrixArduinoString = arduinoPrefix + arduinoDevices['rightMatrix'] + rightMatrixControlString + arduinoSuffix
        
        self.writeToTransport(cupolaArduinoString)
        self.writeToTransport(leftMatrixArduinoString)
        self.writeToTransport(rightMatrixArduinoString)
        
    def writeToTransport(self, writeString):
#        Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self.transport.write(writeString)

    def connectionMade(self):
        Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] Connected.')
    
    def connectionLost(self, reason='connectionDone'):
        print "Connection lost:", reason
    
class MindCupolaArduinoController(EventDispatcher):
    
    manualMode          = BooleanProperty(False)
    def on_manualMode(self, instance, value):
        assert type(value) in [bool]
        Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] manualMode is ' + str(self.manualMode) )
    
    presenceString      = StringProperty('default')
    presenceState       = BoundedNumericProperty(1, min=0, max=3)
    def on_presenceState(self, instance, value):
        assert type(value) in [int, float]
        self.presenceString = self.stateDictionary[int(round(self.presenceState))]
        Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] presenceState is ' + str(self.presenceState) + ' - ' + self.presenceString)
    
    #TODO DONE 0 add fan and heater state
    fanState = BooleanProperty(False)
    def on_fanState(self, instance, value):
        #TODO 3 send turn on/off fans to serial port
        Logger.exception(self.__class__.__name__ + ': in [' + whoAmI() + '] fanState is ' + str(self.fanState) + ' but NOT IMPLEMENTED YET')
        popup = Popup(title='fanState Not implemented yet',
                      content=Label(text='fanState Not implemented yet'),
                      size_hint=(0.4, 0.2) )
        popup.open()
        
    heaterState = BooleanProperty(False)
    def on_heaterState(self, instance, value):
        #TODO 3 set the heater duty cycle and make sure the duty cycle timer is running
        #also schedule a safety timer to force the heater off from time to time
        #TODO also add to initialisation and shutdown to force heater off
        Logger.exception(self.__class__.__name__ + ': in [' + whoAmI() + '] heaterState is ' + str(self.heaterState) + ' but NOT IMPLEMENTED YET')
        popup = Popup(title='heaterState Not implemented yet',
                      content=Label(text='heaterState Not implemented yet'),
                      size_hint=(0.4, 0.2) )
        popup.open()
        
    def __init__(self, serialPort=['/dev/ttyUSB0', '/dev/ttyUSB1'], baudrate=9600):
        super(MindCupolaArduinoController, self).__init__()
        assert type(serialPort) in [str, list]
        assert type(baudrate) in [int]
        
        self.serialPort = serialPort
        self.baudrate = baudrate
        self.protocol = MindCupolaArduinoProtocol(mindCupolaArduinoController=self)
        
        if type(self.serialPort) is str:
            self.serialPort = [self.serialPort]
        
        #check all values are ints
        for i in self.serialPort:
            assert type(i) in [str]
            try:
                self.serial = SerialPort(self.protocol, i, reactor, baudrate=self.baudrate)
                self.serialPort = i
                break
            except SerialException as error:
                pass
        
        if type(self.serialPort) is list:
            print 'SerialException. Cannot connect to any serial ports'
            print 'try: sudo chmod o+rw /dev/ttyUSB0'
            print 'you can test if can listen on the put by using "screen /dev/ttyUSB0" - using Ctrl-A, K to exit window'
            print 'running without arduino connected'
 
    stateDictionary = {0: 'movingDown',
                       1: 'down',
                       2: 'up',
                       3: 'movingUp',} 
    
    
    def setModeManually(self, mode):
        if self.manualMode:
            self.setMode(mode)
            
    def setModeAutomatically(self, mode):
        if not self.manualMode:
            self.setMode(mode)
            
    def setMode(self, mode):
        assert type(mode) in [int]
        self.presenceState = mode
                    
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivyUtils import LabeledSwitch, LabeledSlider, LabeledLabel, LabeledCheckBox, BoxLayoutOrientationRelativeToParent

class MindCupolaArduinoControllerWidget(BoxLayoutOrientationRelativeToParent):

    def __init__(self, mindCupolaArduinoController=None, **kwargs):
        super(MindCupolaArduinoControllerWidget, self).__init__(**kwargs)
        
        self.mindCupolaArduinoController = MindCupolaArduinoController() if mindCupolaArduinoController is None else mindCupolaArduinoController
        assert isinstance(self.mindCupolaArduinoController, MindCupolaArduinoController)
        
        mainBox = BoxLayoutOrientationRelativeToParent()
        self.add_widget(mainBox)
        
        fanState_widget = LabeledSwitch(labelingString='fanState', active=self.mindCupolaArduinoController.fanState, size_hint_y=0.2)
        fanState_widget.bind(active=self.mindCupolaArduinoController.setter('fanState'))
        self.mindCupolaArduinoController.bind(fanState=fanState_widget.setter('active'))
        mainBox.add_widget(fanState_widget)
        
        
        heaterState_widget = LabeledSwitch(labelingString='heaterState', active=self.mindCupolaArduinoController.heaterState, size_hint_y=0.2)
        heaterState_widget.bind(active=self.mindCupolaArduinoController.setter('heaterState'))
        self.mindCupolaArduinoController.bind(heaterState=heaterState_widget.setter('active'))
        mainBox.add_widget(heaterState_widget)
                
        manualMode_widget = LabeledSwitch(labelingString='manualMode', active=self.mindCupolaArduinoController.manualMode, size_hint_y=0.3)
        manualMode_widget.bind(active=self.mindCupolaArduinoController.setter('manualMode'))
        self.mindCupolaArduinoController.bind(manualMode=manualMode_widget.setter('active'))
        mainBox.add_widget(manualMode_widget)
        
        presenceBox = BoxLayoutOrientationRelativeToParent(size_hint_y=0.8)
        mainBox.add_widget(presenceBox)
        
        presenceState_widget = LabeledSlider(labelingString='presenceState', value=self.mindCupolaArduinoController.presenceState, min=0, max=3)
        presenceState_widget.bind(value=self.mindCupolaArduinoController.setter('presenceState'))
        self.mindCupolaArduinoController.bind(presenceState=presenceState_widget.setter('value'))
        presenceBox.add_widget(presenceState_widget)
         
        
        presenceButtonBox = BoxLayoutOrientationRelativeToParent()
        presenceBox.add_widget(presenceButtonBox)
        
        mode3_widget = Button(text='mode3: movingUp')
        mode3_widget.bind(on_press=self.setMode3)
        presenceButtonBox.add_widget(mode3_widget)
        
        mode2_widget = Button(text='mode2: up')
        mode2_widget.bind(on_press=self.setMode2)
        presenceButtonBox.add_widget(mode2_widget)
        
        mode1_widget = Button(text='mode1: down')
        mode1_widget.bind(on_press=self.setMode1)
        presenceButtonBox.add_widget(mode1_widget)
        
        mode0_widget = Button(text='mode0: movingDown')
        mode0_widget.bind(on_press=self.setMode0)
        presenceButtonBox.add_widget(mode0_widget)
        
    def setManualModeOn(self, instance):
        self.mindCupolaArduinoController.manualMode = True
        
    def setManualModeOff(self, instance):
        self.mindCupolaArduinoController.manualMode = False
    
    def setMode0(self, instance):
        self.mindCupolaArduinoController.setModeManually(0)
        
    def setMode1(self, instance):
        self.mindCupolaArduinoController.setModeManually(1)
        
    def setMode2(self, instance):
        self.mindCupolaArduinoController.setModeManually(2)
        
    def setMode3(self, instance):
        self.mindCupolaArduinoController.setModeManually(3)
        
    def presenceState_widget_labelStringSetter(self, instance, value):
        self.presenceStateText.text = value
        
from kivy.app import App
class MindCupolaArduinoControllerWidgetTestApp(App):
    
    def __init__(self, mindCupolaArduinoController=None):
        super(MindCupolaArduinoControllerWidgetTestApp, self).__init__()
        self.mindCupolaArduinoController = MindCupolaArduinoController() if mindCupolaArduinoController is None else mindCupolaArduinoController
        assert isinstance(self.mindCupolaArduinoController, MindCupolaArduinoController)
        
    def build(self):
        mindCupolaArduinoControllerWidget = MindCupolaArduinoControllerWidget(mindCupolaArduinoController=self.mindCupolaArduinoController, orientation='horizontal')
        return mindCupolaArduinoControllerWidget
                        
# self run, self test     
if __name__ == "__main__":
    Logger.info(__file__ + ': running from __name__')
    mindCupolaArduinoController=MindCupolaArduinoController()
    mindCupolaArduinoController.manualMode = False
    mindCupolaArduinoControllerWidgetTestApp = MindCupolaArduinoControllerWidgetTestApp(mindCupolaArduinoController=mindCupolaArduinoController)
    
    mindCupolaArduinoControllerWidgetTestApp.run()
