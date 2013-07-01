'''
Created on 19 Aug 2012

@author: shearer
'''

# install_twisted_rector must be called before importing  and using anything that uses twisted reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor() 

from kivy import Logger
from kivy.uix.settings import Settings
from kivy.clock import Clock
from mindCupolaPythonUtils import whoAmI, lineno

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty, BoundedNumericProperty, StringProperty, ReferenceListProperty

from oscSender import OscSender

class MindCupolaVisualizerGavinController(EventDispatcher):
    
    def __init__(self, namespace_prefix='mcv', host='localhost', port=7000, verbose=False):
        super(MindCupolaVisualizerGavinController, self).__init__()
        #self.oscSender.reactor.run()
        self.verbose = verbose
        
        self.namespace_prefix = namespace_prefix
        self.host = host
        self.port = port
        self.oscSender = OscSender(namespace_prefix=namespace_prefix, host=host, port=port, verbose=self.verbose)
        
        
        self.forceSendAllKivyProperties()
        
    def forceSendAllKivyProperties(self):
        pass #TODO not implemented yet
    
    fullscreen        = BooleanProperty(False)
    def on_fullscreen(self, instance, value):
        assert type(value) in [bool]
        self.oscSender.send('fullscreen', int(value) )
    
    paused = BooleanProperty(False)
    def on_paused(self, instance, value):
        assert type(value) in [bool]
        self.oscSender.send('paused', int(value) )
        
    debug = BooleanProperty(False)
    def on_debug(self, instance, value):
        assert type(value) in [bool]
        self.oscSender.send('debug', int(value) )
    ##attractor
    attractorPositionX = NumericProperty(0.0, min=-2.0, max=2.0)
    attractorPositionY = NumericProperty(0.0, min=-2.0, max=2.0)
    attractorPosition  = ReferenceListProperty(attractorPositionX, attractorPositionY)
    def on_attractorPosition(self, instance, value):
        #print instance, value
        #print type(value)
        assert type(value) in [list]
#        if value.attractorPositionX >= -1.0 and value.attractorPositionX <= 1.0 and value.attractorPositionY >= -1.0 and value.attractorPositionY <= 1.0:
        self.oscSender.send('attractorPosition', value )
    
    eyeLeftVisible          = BooleanProperty(False)
    def on_eyeLeftVisible(self, instance, value):
        assert type(value) in [bool]
        self.oscSender.send('eyeLeftVisible', int(value) )
        
    eyeRightVisible         = BooleanProperty(False)
    def on_eyeRightVisible(self, instance, value):
        assert type(value) in [bool]
        self.oscSender.send('eyeRightVisible', int(value) )
          
    boidDict = {        0: 'bird',
                            1: 'amoeba',
                            2: 'insect',
                            3: 'fish',}
                    
    boidType = NumericProperty(-1)
    def on_boidType(self, instance, value):
        assert type(value) in [int, float]
        if 0 <= value < len(self.boidDict):
            self.oscSender.send('boidType', int(value))
              
    stateDict = {       1: 'ambient',
                        2: 'entering',
                        3: 'waitingForEyes',
                        4: 'calibrating',
                        5: 'running',}
      
    state = NumericProperty(1)
    def on_state(self, instance, value):
        assert type(value) in [int, float]
        Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] State is ' + str(value) + ' [' + self.stateDict[int(value)] + ']')
        self.oscSender.send('state', int(value) )
        
    calibrationTarget = NumericProperty(-1)
    def on_calibrationTarget(self, instance, value):
        assert type(value) in [int, float]
        self.oscSender.send('calibrationTarget', int(value) )
        
    predatorCount = NumericProperty(0)
    def on_predatorCount(self, instance, value):
        assert type(value) in [int, float]
        if 0 <= value:
            self.oscSender.send('predatorCount', int(value))
        
    #TODO DONE 2 turn eyes red if can't see the eyes. light blue if it can. - need to add new things to MCgavinV for that?
    pupilsVisible = BooleanProperty(False)
    def on_pupilsVisible(self, instance, value):
        assert type(value) in [bool]
        #TODO 2 smooth out value and send on threshold changes
        #should only switch if Off for a while - perhaps move to float and smooth the value, and send only when above a threshold?
        
        self.oscSender.send('pupilsVisible', int(value))
        #Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + ' Line: ' + str(lineno()) + ']') 
        #print 'send OSC pupilVisible: ' + str(value)
        
    specialEffectList = ['none', 'matrixEffect', 'blurLookAtLocation', 'boidsFormingShape'] 
    specialEffect = StringProperty(specialEffectList[0])
    def on_specialEffect(self, instance, value):
        assert type(value) in [str]
        assert value in self.specialEffectList
        self.oscSender.send('specialEffectTriggered', value)
        #Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + ' Line: ' + str(lineno()) + ']') 
        #print 'send OSC specialEffectTriggered: ' + value
        
#    eyeCalibrationActive    = BooleanProperty(False)
#    def on_eyeCalibrationActive(self, instance, value):
#        assert type(value) in [bool]
#        self.oscSender.send('eyeCalibrationActive', int(value))
#        
#    eyeCalibrationPositionX = BoundedNumericProperty(0.0, min=0.0, max=1.0)
#    eyeCalibrationPositionY = BoundedNumericProperty(0.0, min=0.0, max=1.0)
#    eyeCalibrationPosition  = ReferenceListProperty(eyeCalibrationPositionX, eyeCalibrationPositionY)
#    def on_eyeCalibrationPosition(self, instance, value):
#        #print instance, value
#        #print type(value)
#        assert type(value) in [list]
#        self.oscSender.send('eyeCalibrationPosition', value )
    
    '''
        Yes you can completely replace the calibration with your own graphics.
        Check out the Tracker API (p6-8), just send:
        
        CALIBRATE_SHOW = FALSE  so our window doesn't show
        CALIBRATE_START = TRUE so the calibration starts
        
        Then watch for:
        
        <CAL ID="CALIB_START_PT" PT="1" CALX="0.10000" CALY="0.08000" />
        
        Which tells you the current point and position on the screen (pt1,
        X=.1*width, Y=.08*height) and
        
        <CAL ID="CALIB_RESULT_PT" PT="1" CALX="0.10000" CALY="0.08000" />
        
        which tells you when the current point is finished and it is time to
        move on to the next point
        
        The object you draw should be large enough to catch the viewers
        attention from their peripheral vision, with a higher contrast shape
        towards the center of the calibration marker to draw the eyes towards
        the true calibration point. Unfortunately at this point you cannot
        change the calibration positions though.
    '''
    
    
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivyUtils import LabeledSwitch, LabeledSlider, LabeledLabel, LabeledCheckBox, BoxLayoutOrientationRelativeToParent

class MindCupolaVisualizerGavinControllerWidget(BoxLayoutOrientationRelativeToParent):

    def __init__(self, mindCupolaVisualizerGavinController=None, **kwargs):
        super(MindCupolaVisualizerGavinControllerWidget, self).__init__(**kwargs)
        self.mindCupolaVisualizerGavinController = MindCupolaVisualizerGavinController() if mindCupolaVisualizerGavinController is None else mindCupolaVisualizerGavinController
        assert isinstance(self.mindCupolaVisualizerGavinController, MindCupolaVisualizerGavinController)
        
        mainBox = BoxLayoutOrientationRelativeToParent()
        self.add_widget(mainBox)
        
        fullscreen_widget = LabeledSwitch(labelingString='xx Fullscreen xx', active=self.mindCupolaVisualizerGavinController.fullscreen)
        fullscreen_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('fullscreen'))
        self.mindCupolaVisualizerGavinController.bind(fullscreen=fullscreen_widget.setter('active'))
        mainBox.add_widget(fullscreen_widget)
        
        paused_widget = LabeledSwitch(labelingString='Paused', active=self.mindCupolaVisualizerGavinController.paused)
        paused_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('paused'))
        self.mindCupolaVisualizerGavinController.bind(paused=paused_widget.setter('active'))
        mainBox.add_widget(paused_widget)
        
        debug_widget = LabeledSwitch(labelingString='Debug', active=self.mindCupolaVisualizerGavinController.debug)
        debug_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('debug'))
        self.mindCupolaVisualizerGavinController.bind(debug=debug_widget.setter('active'))
        mainBox.add_widget(debug_widget)
        
        specialEffect_widget = LabeledLabel(labelingString='specialEffect', labelString=self.mindCupolaVisualizerGavinController.specialEffect)
        specialEffect_widget.bind(labelString=self.mindCupolaVisualizerGavinController.setter('specialEffect'))
        self.mindCupolaVisualizerGavinController.bind(specialEffect=specialEffect_widget.setter('labelString'))
        mainBox.add_widget(specialEffect_widget)
        
        specialEffectBox = BoxLayoutOrientationRelativeToParent(orientationInvertedFromParent=False, size_hint_y=2)
        mainBox.add_widget(specialEffectBox)
        
        self.specialEffectToNone_widget = LabeledSwitch(labelingString='specialEffectToNone', active=False)
        self.specialEffectToNone_widget.bind(active=self.specialEffectToNone)
        specialEffectBox.add_widget(self.specialEffectToNone_widget)
        
        self.specialEffectToMatrixEffect_widget = LabeledSwitch(labelingString='specialEffectToMatrixEffect', active=False)
        self.specialEffectToMatrixEffect_widget.bind(active=self.specialEffectToMatrixEffect)
        specialEffectBox.add_widget(self.specialEffectToMatrixEffect_widget)
        
        
        self.specialEffectToBlurLookAtLocation_widget = LabeledSwitch(labelingString='specialEffectToBlurLookAtLocation', active=False)
        self.specialEffectToBlurLookAtLocation_widget.bind(active=self.specialEffectToBlurLookAtLocation)
        specialEffectBox.add_widget(self.specialEffectToBlurLookAtLocation_widget)
        
        self.specialEffectToBoidsFormingShape_widget = LabeledSwitch(labelingString='specialEffectToBoidsFormingShape', active=False)
        self.specialEffectToBoidsFormingShape_widget.bind(active=self.specialEffectToBoidsFormingShape)
        specialEffectBox.add_widget(self.specialEffectToBoidsFormingShape_widget)
        
       
        
        attractorBox = BoxLayoutOrientationRelativeToParent(size_hint=[1,4])
        mainBox.add_widget(attractorBox)
        
        attractorPositionX_widget = LabeledSlider(labelingString='attractorPositionX', value=self.mindCupolaVisualizerGavinController.attractorPositionX, min=-1.0, max=1.0, orientationInvertedFromParent=False)
        attractorPositionX_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('attractorPositionX')),
        self.mindCupolaVisualizerGavinController.bind(attractorPositionX=attractorPositionX_widget.setter('value'))
        attractorBox.add_widget(attractorPositionX_widget)
        
        attractorPositionY_widget = LabeledSlider(labelingString='attractorPositionY', value=self.mindCupolaVisualizerGavinController.attractorPositionY, min=-1.0, max=1.0, orientationInvertedFromParent=True)
        attractorPositionY_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('attractorPositionY'))
        self.mindCupolaVisualizerGavinController.bind(attractorPositionY=attractorPositionY_widget.setter('value'))
        attractorBox.add_widget(attractorPositionY_widget)
        
        eyeVisibleBox = BoxLayoutOrientationRelativeToParent()
        mainBox.add_widget(eyeVisibleBox)
        
        eyeLeftVisible_widget = LabeledCheckBox(labelingString='eyeLeftVisible', active=self.mindCupolaVisualizerGavinController.eyeLeftVisible)
        eyeLeftVisible_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('eyeLeftVisible'))
        self.mindCupolaVisualizerGavinController.bind(eyeLeftVisible=eyeLeftVisible_widget.setter('active'))
        eyeVisibleBox.add_widget(eyeLeftVisible_widget)
        
        eyeRightVisible_widget = LabeledCheckBox(labelingString='eyeRightVisible', active=self.mindCupolaVisualizerGavinController.eyeRightVisible)
        eyeRightVisible_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('eyeRightVisible'))
        self.mindCupolaVisualizerGavinController.bind(eyeRightVisible=eyeRightVisible_widget.setter('active'))
        eyeVisibleBox.add_widget(eyeRightVisible_widget)
        
        boidBox = BoxLayoutOrientationRelativeToParent(size_hint=[1,2])
        mainBox.add_widget(boidBox)
        boidBox1 = BoxLayoutOrientationRelativeToParent()
        boidBox.add_widget(boidBox1)
        boidBox2 = BoxLayoutOrientationRelativeToParent()
        boidBox.add_widget(boidBox2)
                                                                  
        boidType_widget = LabeledSlider(labelingString='boidType', value=self.mindCupolaVisualizerGavinController.boidType, min=0, max=len(self.mindCupolaVisualizerGavinController.boidDict)-1)
        boidType_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('boidType'))
        self.mindCupolaVisualizerGavinController.bind(boidType=boidType_widget.setter('value'))
        boidBox1.add_widget(boidType_widget)
        
        self.boidTypeTo3_widget = LabeledSwitch(labelingString='boidType to 3 - ' + self.mindCupolaVisualizerGavinController.boidDict[3], active=False)
        self.boidTypeTo3_widget.bind(active=self.boidTo3)
        boidBox2.add_widget(self.boidTypeTo3_widget)
        
        self.boidTypeTo2_widget = LabeledSwitch(labelingString='boidType to 2 - ' + self.mindCupolaVisualizerGavinController.boidDict[2], active=False)
        self.boidTypeTo2_widget.bind(active=self.boidTo2)
        boidBox2.add_widget(self.boidTypeTo2_widget)
        
        self.boidTypeTo1_widget = LabeledSwitch(labelingString='boidType to 1 - ' + self.mindCupolaVisualizerGavinController.boidDict[1], active=False)
        self.boidTypeTo1_widget.bind(active=self.boidTo1)
        boidBox2.add_widget(self.boidTypeTo1_widget)
        
        self.boidTypeTo0_widget = LabeledSwitch(labelingString='boidType to 0 - ' + self.mindCupolaVisualizerGavinController.boidDict[0], active=False)
        self.boidTypeTo0_widget.bind(active=self.boidTo0)
        boidBox2.add_widget(self.boidTypeTo0_widget)
        
        self.predatorCountToZero_widget = LabeledSwitch(labelingString='set predatorCountToZero', active=False)
        self.predatorCountToZero_widget.bind(active=self.predatorCountToZero)
        mainBox.add_widget(self.predatorCountToZero_widget)
        
        self.predatorCountToOne_widget = LabeledSwitch(labelingString='set predatorCountToOne', active=False)
        self.predatorCountToOne_widget.bind(active=self.predatorCountToOne)
        mainBox.add_widget(self.predatorCountToOne_widget)
        
        stateBox = BoxLayoutOrientationRelativeToParent(size_hint=[1,2])
        mainBox.add_widget(stateBox)
        stateBox1 = BoxLayoutOrientationRelativeToParent()
        stateBox.add_widget(stateBox1)
        stateBox2 = BoxLayoutOrientationRelativeToParent()
        stateBox.add_widget(stateBox2)
        
        state_widget = LabeledSlider(labelingString='state', value=self.mindCupolaVisualizerGavinController.state, min=1, max=5)
        state_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('state'))
        self.mindCupolaVisualizerGavinController.bind(state=state_widget.setter('value'))
        stateBox1.add_widget(state_widget)
        
        self.stateTo5_widget = LabeledSwitch(labelingString='State to 5 - running', active=False)
        self.stateTo5_widget.bind(active=self.stateTo5)
        stateBox2.add_widget(self.stateTo5_widget)
        
        self.stateTo4_widget = LabeledSwitch(labelingString='State to 4 - calibrating', active=False)
        self.stateTo4_widget.bind(active=self.stateTo4)
        stateBox2.add_widget(self.stateTo4_widget)
        
        self.stateTo3_widget = LabeledSwitch(labelingString='State to 3 - waiting for eyes', active=False)
        self.stateTo3_widget.bind(active=self.stateTo3)
        stateBox2.add_widget(self.stateTo3_widget)
        
        self.stateTo2_widget = LabeledSwitch(labelingString='State to 2 - entering', active=False)
        self.stateTo2_widget.bind(active=self.stateTo2)
        stateBox2.add_widget(self.stateTo2_widget)
        
        self.stateTo1_widget = LabeledSwitch(labelingString='State to 1 - ambient', active=False)
        self.stateTo1_widget.bind(active=self.stateTo1)
        stateBox2.add_widget(self.stateTo1_widget)
        
        calibrationTarget_widget = LabeledSlider(labelingString='calibrationTarget', value=self.mindCupolaVisualizerGavinController.calibrationTarget, min=0, max=8)
        calibrationTarget_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('calibrationTarget'))
        self.mindCupolaVisualizerGavinController.bind(calibrationTarget=calibrationTarget_widget.setter('value'))
        mainBox.add_widget(calibrationTarget_widget)
        
    def specialEffectWidgetsToInactive(self):
        self.specialEffectToNone_widget.active = False
        self.specialEffectToMatrixEffect_widget.active = False
        self.specialEffectToBlurLookAtLocation_widget.active = False
        self.specialEffectToBoidsFormingShape_widget.active = False
        
    def specialEffectToValue(self, value):
        if value:
            assert type(value) in [str]
            self.mindCupolaVisualizerGavinController.specialEffect = value
            self.specialEffectWidgetsToInactive()
    
    def specialEffectToNone(self, instance, value):
        self.specialEffectToValue('none')
        
    def specialEffectToMatrixEffect(self, instance, value):
        self.specialEffectToValue('matrixEffect')
        
    def specialEffectToBlurLookAtLocation(self, instance, value):
        self.specialEffectToValue('blurLookAtLocation')

    def specialEffectToBoidsFormingShape(self, instance, value):
        self.specialEffectToValue('boidsFormingShape')
        
        
    def predatorCountToZero(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.predatorCount = 0
            self.predatorCountToOne_widget.active = False
            
    def predatorCountToOne(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.predatorCount = 1
            self.predatorCountToZero_widget.active = False
    
    def boidTypeWidgetsToInactive(self):
        self.boidTypeTo0_widget.active = False
        self.boidTypeTo1_widget.active = False
        self.boidTypeTo2_widget.active = False
        self.boidTypeTo3_widget.active = False
        
           
    def boidTo0(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.boidType = 0
            self.boidTypeWidgetsToInactive()
            
    def boidTo1(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.boidType = 1
            self.boidTypeWidgetsToInactive()
            
    def boidTo2(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.boidType = 2
            self.boidTypeWidgetsToInactive()
            
    def boidTo3(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.boidType = 3
            self.boidTypeWidgetsToInactive()
     
    def stateWidgetsToInactive(self):
        self.stateTo1_widget.active = False
        self.stateTo2_widget.active = False
        self.stateTo3_widget.active = False
        self.stateTo4_widget.active = False
        self.stateTo5_widget.active = False
                 
    def stateTo1(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.state = 1
            self.stateWidgetsToInactive()
            
    def stateTo2(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.state = 2
            self.stateWidgetsToInactive()
            
    def stateTo3(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.state = 3
            self.stateWidgetsToInactive()
            
    def stateTo4(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.state = 4
            self.stateWidgetsToInactive()

    def stateTo5(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.state = 5
            self.stateWidgetsToInactive()
            
#        eyeCalibrationPositionX_widget = LabeledSlider(labelingString='eyeCalibrationPositionX', value=self.mindCupolaVisualizerGavinController.eyeCalibrationPositionX, min=0, max=1)
#        eyeCalibrationPositionX_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('eyeCalibrationPositionX'))
#        self.mindCupolaVisualizerGavinController.bind(eyeCalibrationPositionX=eyeCalibrationPositionX_widget.setter('value'))
#        mainBox.add_widget(eyeCalibrationPositionX_widget)
#        
#        eyeCalibrationPositionY_widget = LabeledSlider(labelingString='eyeCalibrationPositionY', value=self.mindCupolaVisualizerGavinController.eyeCalibrationPositionY, min=0, max=1)
#        eyeCalibrationPositionY_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('eyeCalibrationPositionY'))
#        self.mindCupolaVisualizerGavinController.bind(eyeCalibrationPositionY=eyeCalibrationPositionY_widget.setter('value'))
#        mainBox.add_widget(eyeCalibrationPositionY_widget)
        
        
        #TODO: make nice loop, to spin through properties and construct appropriate widgets for each
        
from kivy.app import App
class MindCupolaVisualizerGavinControllerWidgetTestApp(App):
    
    def __init__(self, mindCupolaVisualizerGavinController=None):
        super(MindCupolaVisualizerGavinControllerWidgetTestApp, self).__init__()
        self.mindCupolaVisualizerGavinController = MindCupolaVisualizerGavinController() if mindCupolaVisualizerGavinController is None else mindCupolaVisualizerGavinController
        assert isinstance(self.mindCupolaVisualizerGavinController, MindCupolaVisualizerGavinController)
    
    def build(self):
        mindCupolaVisualizerGavinControllerWidget = MindCupolaVisualizerGavinControllerWidget(mindCupolaVisualizerGavinController=self.mindCupolaVisualizerGavinController, orientation='horizontal')
        return mindCupolaVisualizerGavinControllerWidget
                        
# self run, self test     
if __name__ == "__main__":
    Logger.info(__file__ + ': running from __name__')
    mcvgHost = '192.168.1.119'
    
    mindCupolaVisualizerGavinController = MindCupolaVisualizerGavinController(host=mcvgHost, verbose=True)
    mindCupolaVisualizerGavinControllerWidgetTestApp = MindCupolaVisualizerGavinControllerWidgetTestApp(mindCupolaVisualizerGavinController=mindCupolaVisualizerGavinController)
    mindCupolaVisualizerGavinControllerWidgetTestApp.run()
