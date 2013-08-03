'''
Created on 19 Aug 2012

@author: shearer
'''
import sys

from types import NoneType

from kivy.support import install_twisted_reactor
from mindCupolaArduinoController import MindCupolaArduinoController, MindCupolaArduinoControllerWidget
install_twisted_reactor() 

from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')
from kivy import Logger
from kivy.uix.settings import Settings
from kivy.clock import Clock
from mindCupolaPythonUtils import whoAmI, lineno

from kivy.core.audio import SoundLoader

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty, BoundedNumericProperty, StringProperty, OptionProperty

from eyeTracker import EyeTracker
from mindCupolaArduinoController import MindCupolaArduinoController
from mindCupolaVisualizerGavinController import MindCupolaVisualizerGavinController

from functools import partial

from oscSender import OscSender

class MindCupolaControllerSimple(EventDispatcher):
    
    #_configParser = jsConfigParser()
    #_settings = Settings()
    
    def testCallback(self, instance, value):
        print 'My callback is call from', instance,
        print 'and the a value changed to', value

    def __init__(self, eyeTracker=None, mindCupolaArduinoController=None, mindCupolaVisualizerGavinController=None, auralizerNamespace_prefix='mca', auralizerHost='192.168.1.118', auralizerPort=7001, auralizerVerbose=False):
        super(MindCupolaControllerSimple, self).__init__()
        
        self.eyeTracker = EyeTracker() if eyeTracker is None else eyeTracker
        assert isinstance(self.eyeTracker, EyeTracker)
        
        self.mindCupolaArduinoController = MindCupolaArduinoController() if mindCupolaArduinoController is None else mindCupolaArduinoController
        assert isinstance(self.mindCupolaArduinoController, MindCupolaArduinoController)
        
        self.mindCupolaVisualizerGavinController = MindCupolaVisualizerGavinController() if mindCupolaVisualizerGavinController is None else mindCupolaVisualizerGavinController 
        assert isinstance(self.mindCupolaVisualizerGavinController, MindCupolaVisualizerGavinController)
        
        self.auralizerVerbose = auralizerVerbose
        
        self.auralizerNamespace_prefix = auralizerNamespace_prefix
        self.auralizerHost = auralizerHost
        self.auralizerPort = auralizerPort
        self.auralizerOscSender = OscSender(namespace_prefix=auralizerNamespace_prefix, host=auralizerHost, port=auralizerPort, verbose=self.auralizerVerbose)
        
        Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] sending to auralizer on ' + str(auralizerHost) + ':' + str(auralizerPort))
        
        #binds, to monitor to update visualizer state
        self.mindCupolaVisualizerGavinController.bind(state=self.scheduleCheckState)
        self.mindCupolaArduinoController.bind(presenceState=self.scheduleCheckState)
        self.eyeTracker.bind(goodEyes=self.scheduleCheckState)
        self.eyeTracker.bind(goodCalibration=self.scheduleCheckState)
        self.eyeTracker.bind(badCalibration=self.scheduleCheckState)
        self.eyeTracker.bind(calibrationActivePoint=self.scheduleCheckState)
        self.eyeTracker.bind(pupilLeftValid=self.on_pupilLeftValid)
        self.eyeTracker.bind(pupilRightValid=self.on_pupilRightValid)
        
        self.eyeTracker.bind(fixation=self.on_fixation)
        
        self.mindCupolaVisualizerGavinController.bind(boidType=self.on_boidType)
        self.mindCupolaVisualizerGavinController.bind(state=self.on_state)
        
        self.mindCupolaVisualizerGavinController.bind(attractorPosition=self.on_attractorPosition)
        
        self.mindCupolaVisualizerGavinController.bind(calibrationTarget=self.on_calibrationTarget)
        self.mindCupolaVisualizerGavinController.bind(predatorCount=self.on_predatorCount)
        
        self.mindCupolaVisualizerGavinController.bind(specialEffect=self.on_specialEffect)
        
        self.eyeTracker.bind(badCalibration=self.on_badCalibration)
        self.eyeTracker.bind(goodCalibration=self.on_goodCalibration)
        
        self.mindCupolaArduinoController.bind(fanState=self.on_fanState)
        self.mindCupolaArduinoController.bind(heaterState=self.on_heaterState)
        
        self.boidStateSet('bird')
        
        #TODO ADAM 4 sound effect for entering state "running" - "/mca/interactionState running"
            #in progress by adam
        
        #TODO 1 visualiser aspect ratio to 16:9- 
        
        #TODO 1.1 message and sound effect for when enter running state - 

        #TODO 1 when/how should boidType be controlled/changed
        #random initially?? perhaps the AD model influences the chances of moving
        
        
                
        '''
            boidType includes:
                birds
                amoeba
                fish
                insects
            
            Pleasure - not using
            Arousal - more eye movement, controlling boidType
                very little eye movement -> amoeba
                some eye movement -> birds
                quite a lot of eye movement -> fish
                lots of movement -> insects
                
            Dominance - longer fixations, controlling predator count
        '''
        
        #TODO 1.1 When should of the visual effects happen: - do these need (at this point) accompanying sound effects
            #a. freezes the particle system - matrix effect, should only happen when boidType=fish
                #triggered by a random timer, reset on entry to state
                #reflecting managing to maintain a steady state. maybe trigger time increases over time
                
            #c. they build up on of the 6 shapes, a shape for each boid type.
                #TODO 1 Brigitta - setup mapping from boidType to shape
                #triggered by a random timer, reset on entry to state
                #reflecting managing to maintain a steady state. maybe trigger time increases over time
                 
            #d. effect that blurry where we look and sharp where we don't, should only happen when boidType=amoeba 
                #triggered by a random, reset on entry to state
                #reflecting managing to maintain a steady state. maybe trigger time increases over time
                
        #TODO 1.2 when should predators be introduced 
            #connected to dominance?
            
        #TODO 1.3 when should fan and heaters be used
        #TODO 1.4 should fan and heaters trigger sound effects? different in each boidType
        
        #TODO 1.5 when should LED screens be used, what should they do?
          #simple all LEDs on, and all LEDs off.
          #TODO 1.6 turn on when can't see eyes.
          
          
        #TODO 2 add pause between runs of eye tracking - move back to waiting for eyes?
        
        #TODO 2 goodEyesBuildUp Value should ONLY build up when in waitingForEyesState - need a new flag?
                
        
         
        #TODO 3 make all boid types except birds more attractive (maybe insects repulsive)
        
        #TODO 3.2 how should transitions happen etc? (between boids types?)
        
        #TODO 4 get MCC running on Alienware - as VM
        #TODO 4 control the eye blur??
        
        #TODO 5? in ComputerManagement->Services and Applications->Services. disable/stop desktop window manager session manager service - to stop the Boids game window to every 5 seconds flash up "not responding". probably doens't matter when in xen mode and seems new, so maybe just need to free windows up a little
        
        
        #TODO 5 insects run away from the eye?
        #TODO 5 flock speed - get from mindCupolaVisualizerGavinController? or set as modifier on mindCupolaVisualizerGavinController and send modifier?   
        #TODO 5 control calibration scale from here/UI, so can deal with different screens/projectors without needing to recompile
        
        
        
        #TODO 6 most of the fish seem to get 'stuck', ignoring the eye. Also occurs a little with insects and birds - perhaps the random selector consistently picks the same set?
         #the minCount (e.g. SbBoids.cpp line 1007) controls how many boids are selected to retarget. maybe increase?
        
        #TODO 7 resend full state every second or so
        #TODO 7 fade calibration points in and out 
        
        #TODO 8 show eye overlay if looses eyes during 'running' -maybe? we are changing the colour if we loose the eyes
        
        #TODO 9 fan state - controlled by boid or predator state. Initially controlled by boidType. When boidType=amoeba, cooling is on
        #TODO 9 heater state - controlled by boid state. Initially controlled by boidType. When boidType=insect, heating is on (with a duty cycle to not burn up/out)
        #TODO 9 refactor the auraliser into a new object
        
        #TODO DONE ADAM 1 MODIFICATION Cupola going down: bigger sound effect 
            #pitch/whine comes in faster 
            
        #TODO DONE ADAM 2  eyes appear on the screen for calibration: sound effect - message = "/mca/interactionState waitingForEyes"
        #TODO DONE ADAM 3 in progress - sound effect for calibration points. The message is getting to pd ("/mca/calibrationTarget") with values in range(0:8) inclusive
        
        #TODO DONE ADAM 5 NEW sound effect on failed calibration - message = "/mca/calibrationResult i" 
            #this works, in test, if eyetracker connected, manually triggering "goodCalibration" will start the eyetracker and so immediately after trigger a "badCalibration"
            
        #TODO DONE ADAM 6 when the person leaving the cupola - message = "/mca/interactionState ambient"
            #wind down
        
        #TODO DONE ADAM 7 when fans come on - message = "/mca/fanState"
        #TODO DONE ADAM 8 when heater come on - message= "/mca/heaterState"

        #TODO ADAM 9 sound effect when predators introduced to the system - message = "/mca/predatorCount"
            # works nicely
            
        #TODO ADAM x10 sound effect when matrix effect is triggered (freezes the particle system and rotate) - message = "/mca/specialEffectTriggered matrixEffect"
            # nice, I like it.
        
        #TODO DONE ADAM x11 sound effect when boids are following one of the 6 shapes - message = "/mca/specialEffectTriggeredormingShape"
            # yes, nice.
            
        #TODO DONE ADAM x12 sound effect when blur effect triggered - message = "/mca/specialEffectTriggered blurLookAtLocation"
            # goes quiet, with a squeak
           
        #TODO DONE 0 make boids less attractive to eyes in waitingForEyes State
        #TODO DONE 0 send message (/mca/calibrationResult) to auralizer when calibrationfinished
        #TODO DONE 0 send message (/mca/fanState) to auralizer when fanState changes
        #TODO DONE 0 send message (/mca/heaterState) to auralizer when heaterState changes
        
        #TODO DONE 1 Send message to auralizer when visual effect triggered - "/mca/specialEffectTriggered"
        
        #TODO DONE 2 test if works - always show the eyes for a little while - 1-5 seconds.
        #TODO DONE 2 send state etc to Auraliser
        #TODO DONE 2.1 something weird with the interaction state driving the auralizer - emailed Adam ... Adam has resolved it
        #TODO DONE 2.3 make the bright highlight a little brighter?
        #TODO DONE 3 bring calibration points in a little (and the left/right)
        #TODO DONE 3 enlarge calibration points a little
        
    #TODO DONE 1 send predator count to auralizer when it changes
    def on_predatorCount(self, instance, value):
        assert type(value) in [int, float]
        self.auralizerOscSender.send('predatorCount', int(value))
        
    def on_pupilLeftValid(self, instance, value):
        self.checkPupilValidity()
        
    def on_pupilRightValid(self, instance, value):
        self.checkPupilValidity()
    
    def on_specialEffect(self, instance, value):
        assert type(value) in [str]
        self.auralizerOscSender.send('specialEffectTriggered', value)
        
    def on_badCalibration(self, instance, value):
        self.auralizerOscSender.send('calibrationResult', 0)
    
    def on_goodCalibration(self, instance, value):
        self.auralizerOscSender.send('calibrationResult', 1)
    
    def on_fanState(self, instance, value):
        assert type(value) in [str,int,bool]
        if type(value) in [str, int]:
            value = bool(value)
        value = int(value)
        self.auralizerOscSender.send('fanState', value)
        
    def on_heaterState(self, instance, value):
        assert type(value) in [str,int,bool]
        if type(value) in [str, int]:
            value = bool(value)
        value = int(value)
        self.auralizerOscSender.send('heaterState', value)
        
    #TODO DONE 1 start in bird state
    def boidStateSet(self, boidString='bird'):
        for key, value in self.mindCupolaVisualizerGavinController.boidDict.iteritems():
            if value==boidString:
                self.mindCupolaVisualizerGavinController.boidType = key
                
    #TODO DONE 1 send auralizer message that eyes cannot be seen
    #TODO DONE 1 send mindCupolaVisualizerGavinController that eyes cannot be seen
    def checkPupilValidity(self):
        if self.eyeTracker.pupilLeftValid and self.eyeTracker.pupilRightValid:
            if self.mindCupolaVisualizerGavinController.pupilsVisible ==False:
                self.mindCupolaVisualizerGavinController.pupilsVisible = True
                self.auralizerOscSender.send('pupilsVisible', int(True))
        else:
            if self.mindCupolaVisualizerGavinController.pupilsVisible ==True:
                self.mindCupolaVisualizerGavinController.pupilsVisible = False
                self.auralizerOscSender.send('pupilsVisible', int(False))
            
    def on_boidType(self, instance, value):
        assert type(value) in [int, float]
        value = int(value)
        Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] Boidtype is ' + str(value) + ' meaning: ' + self.mindCupolaVisualizerGavinController.boidDict[value])
        if 0 <=  value < len(self.mindCupolaVisualizerGavinController.boidDict):
            #sending boidType as INT
            self.auralizerOscSender.send('boidType', self.mindCupolaVisualizerGavinController.boidDict[value])
            
        #do boidType change stuff
        Clock.unschedule(self.boidTypeTimeOut)
        Clock.schedule_interval(self.boidTypeTimeOut, 3) #TODO 0.5 choose appropriate boidTypeTimeOut timer value, and add variance
        
              
    def on_state(self, instance, value):
        assert type(value) in [int, float]
        value = int(value)
        if 1 <= value <= len(self.mindCupolaVisualizerGavinController.stateDict)+1: 
            #sending interactionState as STRING
            self.auralizerOscSender.send('interactionState', self.mindCupolaVisualizerGavinController.stateDict[value])

    def on_attractorPosition(self, instance, value):
        #print instance, value
        #print type(value)
        assert type(value) in [list]
        assert len(value) is 2
#        if value.attractorPositionX >= -1.0 and value.attractorPositionX <= 1.0 and value.attractorPositionY >= -1.0 and value.attractorPositionY <= 1.0:
        self.auralizerOscSender.send('flock/attractorLocation', value)

    #TODO DONE 1 send auralizer message calibration point change
    def on_calibrationTarget(self, instance, value):
        assert type(value) in [int, float]
        value = int(value)
        #sending INT
        self.auralizerOscSender.send('calibrationTarget', value)
        
    def on_fixation(self, instance, value):
        if instance.fixationValid:
            
            #scale from [0,1] to [-1,1]
            #TODO something is weird with this mapping, boids are moving always to upper right
            oldValue = instance.fixationX
            oldMin = 0.0
            oldMax = 1.0
            newMin = -1.0
            newMax = 1.0
            oldRange = (oldMax - oldMin)
            newRange = (newMax - newMin)
            rangeMultipler = newRange / oldRange
            rangeOffset = newMin - oldMin
            #newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
            newValue = (oldValue * rangeMultipler) +rangeOffset
            self.mindCupolaVisualizerGavinController.attractorPositionX = newValue
            
            #scale from [1,0] to [-1, 1]
            #TODO using scale [-0.5, 0.5] temporarily until mend mcvGavin to put calibration points wider
            oldValue = instance.fixationY
            oldMin = 0.0
            oldMax = 1.0
            newMin = 1.0
            newMax = -1.0
            oldRange = (oldMax - oldMin)
            newRange = (newMax - newMin)
            rangeMultipler = newRange / oldRange
            rangeOffset = newMin - oldMin
            #newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
            newValue = (oldValue * rangeMultipler) +rangeOffset
            self.mindCupolaVisualizerGavinController.attractorPositionY = newValue
            
    def scheduleCheckState(self, instance, value):
        Clock.schedule_once(self.checkState, 0) #TODO consider checking state on nextframe (0) or before nextframe (-1)
        
    def checkState(self, instance=None, value=None):
#        Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] visualizerState is ' + str(int(self.mindCupolaVisualizerGavinController.state)) + ' - ' + self.mindCupolaVisualizerGavinController.stateDict[int(self.mindCupolaVisualizerGavinController.state)])
        
        #Mode 1 - ambient
        if self.mindCupolaVisualizerGavinController.state == 1:
            self.eyeTracker.goodCalibration = False
            self.eyeTracker.goodCalibrationThresholdReset()  #TODO DONE 0 reset present calibration threshold on exit
            self.eyeTracker.badCalibration = False
            self.eyeTracker.calibrationActiveFlag = False
            self.eyeTracker.goodEyes = False
            
            #TODO DONE 0 switch to Birds on entry
            self.mindCupolaVisualizerGavinController.boidType = 0 #birds
                        
                        
            #TODO Done 0 in non-running states, drive the attractor points around to give random motion
            Clock.schedule_interval(self.retargetBoids, 2) #Schedule retargetBoids every 2 seconds
        
            if self.mindCupolaArduinoController.presenceState == 0: # movingDown, so move to entering
                self.mindCupolaVisualizerGavinController.state = 2 
            else:
                Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] Nothing to do.')
                
        #Mode 2 - entering
        elif self.mindCupolaVisualizerGavinController.state == 2:
            self.eyeTracker.goodCalibration = False
            self.eyeTracker.goodCalibrationThresholdReset()  #TODO DONE 0 reset present calibration threshold on exit
            self.eyeTracker.badCalibration = False
            self.eyeTracker.calibrationActiveFlag = False
            self.eyeTracker.goodEyes = False
            
            #self.mindCupolaVisualizerGavinController.boidType = 0 #birds
            
            #TODO DONE 0 in non-running states, drive the attractor points around to give random motion
            Clock.unschedule(self.retargetBoids) #clear retargetBoids from scheduler
            
        
            if self.mindCupolaArduinoController.presenceState == 1: # is down, so move to waiting for eyes
                self.mindCupolaVisualizerGavinController.state = 3
            elif self.mindCupolaArduinoController.presenceState == 2: #moved up, so person has left, so move to ambient
                self.mindCupolaVisualizerGavinController.state = 1 
            elif self.mindCupolaArduinoController.presenceState == 3: #powered off, so move to ambient 
                self.mindCupolaVisualizerGavinController.state = 1
            else:
                Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] Nothing to do.')    
                 
        #Mode 3 - waiting for eyes
        elif self.mindCupolaVisualizerGavinController.state == 3:
            self.eyeTracker.goodCalibration = False
            self.eyeTracker.badCalibration = False
            self.eyeTracker.calibrationActiveFlag = False
            
#            Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] presenceState is ' + str(int(self.mindCupolaArduinoController.presenceState)))
            if self.mindCupolaArduinoController.presenceState == 0: #moving down, so go back to entering
                self.mindCupolaVisualizerGavinController.state = 2 
            elif self.mindCupolaArduinoController.presenceState == 2: #moved up, so back to ambient
                self.mindCupolaVisualizerGavinController.state = 1 
            elif self.mindCupolaArduinoController.presenceState == 3: # powered off, so move to ambient
                self.mindCupolaVisualizerGavinController.state = 1
            elif self.eyeTracker.goodEyes: # goodEyes, so move to calibrating and clear goodEyesFlag
                self.mindCupolaVisualizerGavinController.state = 4
                self.eyeTracker.goodEyes = False
                self.eyeTracker.calibrationActiveFlag = True
            else:
                Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] Nothing to do.')
                
        #Mode 4 - calibrating
        elif self.mindCupolaVisualizerGavinController.state == 4:
            
            if self.mindCupolaArduinoController.presenceState == 0: #moving down, so go back to entering
                self.mindCupolaVisualizerGavinController.state = 2
            elif self.mindCupolaArduinoController.presenceState == 2: #moved up, so back to ambient
                self.mindCupolaVisualizerGavinController.state = 1
            elif self.mindCupolaArduinoController.presenceState == 3: #powered off, so move to ambient
                self.mindCupolaVisualizerGavinController.state = 1
            
            if self.eyeTracker.calibrationActivePoint >= 0:
                self.mindCupolaVisualizerGavinController.calibrationTarget = self.eyeTracker.calibrationActivePoint
                
            if self.eyeTracker.goodCalibration: #good calibration, so move to running
                self.mindCupolaVisualizerGavinController.state = 5
                Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] Got good calibration!!!.')
            elif self.eyeTracker.badCalibration: #bad calibration, so move to waiting for eyes
                self.mindCupolaVisualizerGavinController.state = 3
                Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] Got bad calibration.')
            else:
                Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] Nothing to do.')
                    
        #Mode 5 - running
        elif self.mindCupolaVisualizerGavinController.state == 5:
            
            self.eyeTracker.goodCalibration = False
            self.eyeTracker.badCalibration = False
            self.eyeTracker.calibrationActiveFlag = False

            if self.mindCupolaArduinoController.presenceState == 0: #moving down, so go back to entering
                self.mindCupolaVisualizerGavinController.state = 2 
            elif self.mindCupolaArduinoController.presenceState == 2: #moved up, so back to ambient
                self.mindCupolaVisualizerGavinController.state = 1
            elif self.mindCupolaArduinoController.presenceState == 3: #powered off, so move to ambient
                self.mindCupolaVisualizerGavinController.state = 1
            else:
                Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] Nothing to do.')
                
        else:
            Logger.warning(self.__class__.__name__ + ': in [' + whoAmI() + '] State is ' + str(self.mindCupolaVisualizerGavinController.state))
    
    def retargetBoids(self, dt=None):
        #TODO 1.1 drive the attractor points around to give random motion
        Logger.warning(self.__class__.__name__ + ': in [' + whoAmI() + '] Self targetting boids NOT implemented yet')
    
    def boidTypeTimeOut(self, dt=None):
        Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] Hit boidTypeTimeOut')
        
        boidTypeString = self.mindCupolaVisualizerGavinController.boidDict[self.mindCupolaVisualizerGavinController.boidType]
        predatorCount = self.mindCupolaVisualizerGavinController.predatorCount
        if boidTypeString == 'bird':
            if predatorCount < 1:
                pass
            pass #TODO 0
        elif boidTypeString == 'amoeba':
            pass
        elif boidTypeString == 'insect':
            pass
        elif boidTypeString == 'fish':
            pass



        
        
#UIX        
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label 

from kivyUtils import LabeledSwitch, LabeledSlider, LabeledLabel, LabeledCheckBox,\
    BoxLayoutOrientationRelativeToParent

from eyeTracker import EyeTrackerWidget
from mindCupolaVisualizerGavinController import  MindCupolaVisualizerGavinControllerMainWidget, MindCupolaVisualizerGavinControllerFlockWidget

class MindCupolaControllerSimpleWidget(BoxLayout):

    def __init__(self, mindCupolaControllerSimple=None, **kwargs):
        
        super(MindCupolaControllerSimpleWidget, self).__init__(**kwargs)
        self.orientation='horizontal'
        
        self.mindCupolaControllerSimple = MindCupolaControllerSimple() if mindCupolaControllerSimple is None else mindCupolaControllerSimple
        assert isinstance(self.mindCupolaControllerSimple, MindCupolaControllerSimple)
        
        ###########
        # Arduino #
        ###########
        
        self.arduinoBox = BoxLayout(orientation='vertical', size_hint_x=0.4)
        self.add_widget(self.arduinoBox)
        
        self.arduinoBoxLabel = Label(text='Arduino', size_hint_y=0.1)
        self.arduinoBox.add_widget(self.arduinoBoxLabel)
        
        self.arduinoWidget = MindCupolaArduinoControllerWidget(mindCupolaArduinoController=self.mindCupolaControllerSimple.mindCupolaArduinoController, orientation='horizontal')
        
        self.arduinoBox.add_widget(self.arduinoWidget)
        
        ###############
        # Eye Tracker #
        ###############
        
        self.auralizerBox = BoxLayout(orientation='vertical', size_hint_x=0.7)
        self.add_widget(self.auralizerBox)
        
        self.auralizerLabel = Label(text='EyeTracker', size_hint_y=0.1)
        self.auralizerBox.add_widget(self.auralizerLabel)
        
        self.eyeTrackerWidget = EyeTrackerWidget(eyeTracker=self.mindCupolaControllerSimple.eyeTracker)
        self.auralizerBox.add_widget(self.eyeTrackerWidget)
        
        ##############
        # Visualizer #
        ##############
        
        self.visualizerBox = BoxLayout(orientation='vertical', size_hint_x=1.4)
        self.add_widget(self.visualizerBox)
        
        self.visualizerLabel = Label(text='Visualiser', size_hint_y=0.1)
        self.visualizerBox.add_widget(self.visualizerLabel)
        
        self.visualizerSubBox = BoxLayoutOrientationRelativeToParent(orientationInvertedFromParent=True, size_hint_y=0.9)
        self.visualizerBox.add_widget(self.visualizerSubBox)
        
        self.mcvMainWidget = MindCupolaVisualizerGavinControllerMainWidget(mindCupolaVisualizerGavinController=mindCupolaControllerSimple.mindCupolaVisualizerGavinController, orientation='horizontal', size_hint_x=0.7)
        self.visualizerSubBox.add_widget(self.mcvMainWidget)
        
        self.mcvFlockWidget = MindCupolaVisualizerGavinControllerFlockWidget(mindCupolaVisualizerGavinController=mindCupolaControllerSimple.mindCupolaVisualizerGavinController, orientation='horizontal', size_hint_x=0.3)
        self.visualizerSubBox.add_widget(self.mcvFlockWidget)      
        
        #############
        # Auralizer #
        #############
        
        self.auralizerBox = BoxLayout(orientation='vertical', size_hint_x=0.4)
        #self.add_widget(self.auralizerBox)
        
        self.auralizerLabel = Label(text='Auralizer', size_hint_y=0.1)
        self.auralizerBox.add_widget(self.auralizerLabel)
        
        self.auralizerVerbose_widget = LabeledSwitch(labelingString='verbose?', active=self.mindCupolaControllerSimple.auralizerVerbose)
        #self.auralizerVerbose_widget.bind(active=self.mindCupolaControllerSimple.setter('auralizerVerbose'))
        #FIXME 3 generates a key error, so can't change the value from the UI self.mindCupolaControllerSimple.bind(auralizerVerbose=self.auralizerVerbose_widget.setter('active'))
        self.auralizerBox.add_widget(self.auralizerVerbose_widget)
        
        
    def tmp(self, **kwargs):
        print 'in tmp'
        
from kivy.app import App
class MindCupolaControllerSimpleWidgetTestApp(App):
    
    def __init__(self, mindCupolaControllerSimple=None):
        super(MindCupolaControllerSimpleWidgetTestApp, self).__init__()
        self.mindCupolaControllerSimple = MindCupolaControllerSimple() if mindCupolaControllerSimple is None else mindCupolaControllerSimple
        assert isinstance(self.mindCupolaControllerSimple, MindCupolaControllerSimple)
    
    def build(self):
        
        mindCupolaControllerSimpleWidget = MindCupolaControllerSimpleWidget(self.mindCupolaControllerSimple)
        
        #Clock.schedule_interval(self.connectEyeTracker, 1) #connect and keep reconnecting on loss
        return mindCupolaControllerSimpleWidget

    
        
# self run, self test     
if __name__ == "__main__":
    from mindCupolaPythonUtils import get_default_gateway_linux
    Logger.info(__file__ + ': running from __name__')
    
    #TODO 5 add command line options, according to http://kivy.org/docs/api-kivy.config.html    
    host = '192.168.1.118'#get_default_gateway_linux()
    
    etHost = host
    etPort = 4242
    etGoodCalibrationThresholdMax=8
    et = EyeTracker(host=etHost, port=etPort, goodCalibrationThresholdMax=etGoodCalibrationThresholdMax)
    et.wantToBeConnectedFlag = True
    
    mcar = MindCupolaArduinoController()
    mcar.manualMode = True
    
    mcvHost = host
    mcv = MindCupolaVisualizerGavinController(host=mcvHost, verbose=False)
    
    auralizerNamespace_prefix='mca'
    auralizerHost=host
    auralizerPort=7001
    auralizerVerbose=False
    
    mindCupolaControllerSimple = MindCupolaControllerSimple(eyeTracker=et,
                                                            mindCupolaArduinoController=mcar,
                                                            mindCupolaVisualizerGavinController=mcv, 
                                                            auralizerNamespace_prefix=auralizerNamespace_prefix,
                                                            auralizerHost=auralizerHost,
                                                            auralizerPort=auralizerPort,
                                                            auralizerVerbose=auralizerVerbose,
                                                            )
    mindCupolaControllerSimpleWidgetTestApp = MindCupolaControllerSimpleWidgetTestApp(mindCupolaControllerSimple=mindCupolaControllerSimple)
    mindCupolaControllerSimpleWidgetTestApp.run()
