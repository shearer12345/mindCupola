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
        
        self.property('debug').dispatch(self)
        self.property('paused').dispatch(self)
        self.property('fullscreen').dispatch(self)
        
        self.property('state').dispatch(self)
        
        self.property('boidType').dispatch(self)
        self.property('eyeLeftVisible').dispatch(self)
        self.property('eyeRightVisible').dispatch(self)
        self.property('pupilsVisible').dispatch(self)
        
        #self.property('attractorPosition').dispatch(self)

        self.property('calibrationTarget').dispatch(self)
        self.property('predatorCount').dispatch(self)
        self.property('migrateShapeNumber').dispatch(self)
        self.property('specialEffect').dispatch(self)
        
        self.property('cohesiveDistance').dispatch(self)
        self.property('cruisingSpeed').dispatch(self)
        self.property('maxVelocity').dispatch(self)
        self.property('attractionRate').dispatch(self)
        self.property('velocityRate').dispatch(self)
        self.property('migrateRate').dispatch(self)
        self.property('migrateOrbit').dispatch(self)
        self.property('blur').dispatch(self)
        
        
        
        
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
        
    blur = BoundedNumericProperty(0.0, min=0.0, max=1.0) #BUG BoundedNumericProperty appear to case min and max to INTS
    def on_blur(self, instance, value):
        assert type(value) in [int, float]
        self.oscSender.send('blur', float(value) )
        
    ##attractor
    attractorPositionX = BoundedNumericProperty(0.0, min=-2.0, max=2.0)
    attractorPositionY = BoundedNumericProperty(0.0, min=-2.0, max=2.0)
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
                    
    boidType = NumericProperty(0)
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
    
    migrateShapeDict = {        0: 'none',
                        1: 'planeTop',
                        2: 'planeSide',
                        3: 'hand',
                        4: 'fishStripes',
                        5: 'arrowLeft',
                        6: 'fishLeft',
                        7: 'fishLeftWithTails',
                        8: 'faceHappy',
                        9: 'faceSad',
                        10:'fishUp',
                        11:'circle',
                        12:'gunRight1',
                        13:'lightbulb',
                        14:'gunRight2',
                        15:'buddah',
                        16:'star',
                        17:'radioactive',
                        18:'ampersand',
                        19:'x',
                        20:'fishBones',
                        21:'squid',
                        22:'hourGlass',
                        23:'hexagons',
                        24:'cloud',
                        25:'wineGlass',
                        26:'shhh',
                        }
    
    migrateShapeNumber = NumericProperty(0)
    def on_migrateShapeNumber(self, instance, value):
        assert type(value) in [int, float]
        self.oscSender.send('flock/migrateShapeNumber', int(value))
        #Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + ' Line: ' + str(lineno()) + ']' + ' migrateShapeNumber changed to ' + str(int(value)))
    
    specialEffectList = ['none', 'matrixEffect', 'blurLookAtLocation', 'boidsFormingShape'] 
    specialEffect = StringProperty(specialEffectList[0])
    def on_specialEffect(self, instance, value):
        assert type(value) in [str]
        assert value in self.specialEffectList
        self.oscSender.send('specialEffectTriggered', value)
        #Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + ' Line: ' + str(lineno()) + ']') 
        #print 'send OSC specialEffectTriggered: ' + value
        
    cohesiveDistanceMin = 0.5
    cohesiveDistance = BoundedNumericProperty(7.5, min=cohesiveDistanceMin, max=200.0)
    def on_cohesiveDistance(self, instance, value):
        assert type(value) in [int, float]
        value = max(self.cohesiveDistanceMin, value
                    )
        self.oscSender.send('flock/cohesiveDistance', float(value) )
        
    cruisingSpeedMin = 0.5
    cruisingSpeed = BoundedNumericProperty(30.0, min=cruisingSpeedMin, max=200.0)
    def on_cruisingSpeed(self, instance, value):
        assert type(value) in [int, float]
        value = max(self.cruisingSpeedMin, value)
        self.oscSender.send('flock/cruisingSpeed', float(value) )    
    
    maxVelocityMin = 0.5
    maxVelocity = BoundedNumericProperty(60.0, min=maxVelocityMin, max=200.0)
    def on_maxVelocity(self, instance, value):
        assert type(value) in [int, float]
        value = max(self.maxVelocityMin, value)
        self.oscSender.send('flock/maxVelocity', float(value) )    
    
    attractionRateMin = 0.5
    attractionRate = BoundedNumericProperty(5000.0, min=attractionRateMin, max=5000.0)
    def on_attractionRate(self, instance, value):
        assert type(value) in [int, float]
        value = max(self.attractionRateMin, value)
        self.oscSender.send('flock/attractionRate', float(value) )    
    
    velocityRateMin = 0.5
    velocityRate = BoundedNumericProperty(200.0, min=velocityRateMin, max=2000.0)
    def on_velocityRate(self, instance, value):
        assert type(value) in [int, float]
        value = max(self.velocityRateMin, value)
        self.oscSender.send('flock/velocityRate', float(value) )    
    
    migrateRateMin = 0.5 #HACK, the return min value is always an int and so 0.5 gives 0
    migrateRate = BoundedNumericProperty(10.0, min=migrateRateMin, max=200.0)
    def on_migrateRate(self, instance, value):
        assert type(value) in [int, float]
        value = max(self.migrateRateMin, value)
        self.oscSender.send('flock/migrateRate', float(value) )    
    
    migrateOrbitMin = 0.5
    migrateOrbit = BoundedNumericProperty(10.0, min=migrateOrbitMin, max=200.0)
    def on_migrateOrbit(self, instance, value):
        assert type(value) in [int, float]
        value = max(self.migrateOrbitMin, value)
        self.oscSender.send('flock/migrateOrbit', float(value) )
            
    localMigrateOrbitMin = 0.5
    localMigrateOrbit = BoundedNumericProperty(25.0, min=localMigrateOrbitMin, max=200.0)
    def on_localMigrateOrbit(self, instance, value):
        assert type(value) in [int, float]
        value = max(self.localMigrateOrbitMin, value)
        self.oscSender.send('flock/localMigrateOrbit', float(value) )    
        
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivyUtils import LabeledSwitch, LabeledSlider, LabeledLabel, LabeledCheckBox, BoxLayoutOrientationRelativeToParent

class MindCupolaVisualizerGavinControllerMainWidget(BoxLayoutOrientationRelativeToParent):

    def __init__(self, mindCupolaVisualizerGavinController=None, **kwargs):
        super(MindCupolaVisualizerGavinControllerMainWidget, self).__init__(**kwargs)
        self.mindCupolaVisualizerGavinController = MindCupolaVisualizerGavinController() if mindCupolaVisualizerGavinController is None else mindCupolaVisualizerGavinController
        assert isinstance(self.mindCupolaVisualizerGavinController, MindCupolaVisualizerGavinController)
        
        box = BoxLayoutOrientationRelativeToParent(orientationInvertedFromParent=True)
        self.add_widget(box)
        

        fullscreen_widget = LabeledSwitch(labelingString='xx Fullscreen xx', active=self.mindCupolaVisualizerGavinController.fullscreen)
        fullscreen_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('fullscreen'))
        self.mindCupolaVisualizerGavinController.bind(fullscreen=fullscreen_widget.setter('active'))
        box.add_widget(fullscreen_widget)
        
        paused_widget = LabeledSwitch(labelingString='Paused', active=self.mindCupolaVisualizerGavinController.paused)
        paused_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('paused'))
        self.mindCupolaVisualizerGavinController.bind(paused=paused_widget.setter('active'))
        box.add_widget(paused_widget)
        
        debug_widget = LabeledSwitch(labelingString='Debug', active=self.mindCupolaVisualizerGavinController.debug)
        debug_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('debug'))
        self.mindCupolaVisualizerGavinController.bind(debug=debug_widget.setter('active'))
        box.add_widget(debug_widget)
        
        blur_widget = LabeledSlider(labelingString='blur',
                                                value=self.mindCupolaVisualizerGavinController.blur,
                                                min=self.mindCupolaVisualizerGavinController.property('blur').get_min(self.mindCupolaVisualizerGavinController),
                                                max=self.mindCupolaVisualizerGavinController.property('blur').get_max(self.mindCupolaVisualizerGavinController),
                                                orientationInvertedFromParent=False,
                                                )
        blur_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('blur'))
        self.mindCupolaVisualizerGavinController.bind(blur=blur_widget.setter('value'))
        box.add_widget(blur_widget)

        
        
        specialEffect_widget = LabeledLabel(labelingString='specialEffect', labelString=self.mindCupolaVisualizerGavinController.specialEffect)
        specialEffect_widget.bind(labelString=self.mindCupolaVisualizerGavinController.setter('specialEffect'))
        self.mindCupolaVisualizerGavinController.bind(specialEffect=specialEffect_widget.setter('labelString'))
        box.add_widget(specialEffect_widget)
        
        specialEffectBox = BoxLayoutOrientationRelativeToParent(orientationInvertedFromParent=False, size_hint_y=2)
        box.add_widget(specialEffectBox)
        
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
        box.add_widget(attractorBox)
        
        attractorPositionX_widget = LabeledSlider(labelingString='attractorPositionX', value=self.mindCupolaVisualizerGavinController.attractorPositionX, min=-1.0, max=1.0, orientationInvertedFromParent=False)
        attractorPositionX_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('attractorPositionX')),
        self.mindCupolaVisualizerGavinController.bind(attractorPositionX=attractorPositionX_widget.setter('value'))
        attractorBox.add_widget(attractorPositionX_widget)
        
        attractorPositionY_widget = LabeledSlider(labelingString='attractorPositionY', value=self.mindCupolaVisualizerGavinController.attractorPositionY, min=-1.0, max=1.0, orientationInvertedFromParent=True)
        attractorPositionY_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('attractorPositionY'))
        self.mindCupolaVisualizerGavinController.bind(attractorPositionY=attractorPositionY_widget.setter('value'))
        attractorBox.add_widget(attractorPositionY_widget)
        
        eyeVisibleBox = BoxLayoutOrientationRelativeToParent()
        box.add_widget(eyeVisibleBox)
        
        eyeLeftVisible_widget = LabeledCheckBox(labelingString='eyeLeftVisible', active=self.mindCupolaVisualizerGavinController.eyeLeftVisible)
        eyeLeftVisible_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('eyeLeftVisible'))
        self.mindCupolaVisualizerGavinController.bind(eyeLeftVisible=eyeLeftVisible_widget.setter('active'))
        eyeVisibleBox.add_widget(eyeLeftVisible_widget)
        
        eyeRightVisible_widget = LabeledCheckBox(labelingString='eyeRightVisible', active=self.mindCupolaVisualizerGavinController.eyeRightVisible)
        eyeRightVisible_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('eyeRightVisible'))
        self.mindCupolaVisualizerGavinController.bind(eyeRightVisible=eyeRightVisible_widget.setter('active'))
        eyeVisibleBox.add_widget(eyeRightVisible_widget)
        
        self.pupilsVisible_widget = LabeledSwitch(labelingString='pupilsVisible', active=mindCupolaVisualizerGavinController.pupilsVisible)
        self.pupilsVisible_widget.bind(active=self.mindCupolaVisualizerGavinController.setter('pupilsVisible'))
        self.mindCupolaVisualizerGavinController.bind(pupilsVisible=self.pupilsVisible_widget.setter('active'))
        eyeVisibleBox.add_widget(self.pupilsVisible_widget)
        
        
        #migrateShapeNumber
        
        migrateShapeNumberBox = BoxLayoutOrientationRelativeToParent(size_hint=[1,4])
        box.add_widget(migrateShapeNumberBox)
        migrateShapeNumberBox1 = BoxLayoutOrientationRelativeToParent()
        migrateShapeNumberBox.add_widget(migrateShapeNumberBox1)
        migrateShapeNumberBox2 = BoxLayoutOrientationRelativeToParent()
        migrateShapeNumberBox.add_widget(migrateShapeNumberBox2)
                                                                  
        migrateShapeNumber_widget = LabeledSlider(labelingString='migrateShapeNumber', value=self.mindCupolaVisualizerGavinController.migrateShapeNumber, min=0, max=len(self.mindCupolaVisualizerGavinController.migrateShapeDict))
        migrateShapeNumber_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('migrateShapeNumber'))
        self.mindCupolaVisualizerGavinController.bind(migrateShapeNumber=migrateShapeNumber_widget.setter('value'))
        migrateShapeNumberBox1.add_widget(migrateShapeNumber_widget)
        
        #shhh
        self.migrateShapeNumberTo26_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[26], active=False)
        self.migrateShapeNumberTo26_widget.bind(active=self.migrateShapeNumberTo26)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo26_widget)
        
        #wineGlass
        self.migrateShapeNumberTo25_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[25], active=False)
        self.migrateShapeNumberTo25_widget.bind(active=self.migrateShapeNumberTo25)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo25_widget)
        
        #cloud
        self.migrateShapeNumberTo24_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[24], active=False)
        self.migrateShapeNumberTo24_widget.bind(active=self.migrateShapeNumberTo24)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo24_widget)
        
        #hexagons
        self.migrateShapeNumberTo23_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[23], active=False)
        self.migrateShapeNumberTo23_widget.bind(active=self.migrateShapeNumberTo23)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo23_widget)
        
        #hourGlass
        self.migrateShapeNumberTo22_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[22], active=False)
        self.migrateShapeNumberTo22_widget.bind(active=self.migrateShapeNumberTo22)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo22_widget)
        
        #squid
        self.migrateShapeNumberTo21_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[21], active=False)
        self.migrateShapeNumberTo21_widget.bind(active=self.migrateShapeNumberTo21)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo21_widget)
        
        #fishBones
        self.migrateShapeNumberTo20_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[20], active=False)
        self.migrateShapeNumberTo20_widget.bind(active=self.migrateShapeNumberTo20)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo20_widget)
        
        #x
        self.migrateShapeNumberTo19_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[19], active=False)
        self.migrateShapeNumberTo19_widget.bind(active=self.migrateShapeNumberTo19)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo19_widget)
        
        #ampersand
        self.migrateShapeNumberTo18_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[18], active=False)
        self.migrateShapeNumberTo18_widget.bind(active=self.migrateShapeNumberTo18)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo18_widget)
        
        #radioactive
        self.migrateShapeNumberTo17_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[17], active=False)
        self.migrateShapeNumberTo17_widget.bind(active=self.migrateShapeNumberTo17)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo17_widget)
        
        #star
        self.migrateShapeNumberTo16_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[16], active=False)
        self.migrateShapeNumberTo16_widget.bind(active=self.migrateShapeNumberTo16)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo16_widget)
        
        #buddah
        self.migrateShapeNumberTo15_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[15], active=False)
        self.migrateShapeNumberTo15_widget.bind(active=self.migrateShapeNumberTo15)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo15_widget)
        
        #gunRight2
        self.migrateShapeNumberTo14_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[14], active=False)
        self.migrateShapeNumberTo14_widget.bind(active=self.migrateShapeNumberTo14)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo14_widget)
        
        #lightbulb
        self.migrateShapeNumberTo13_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[13], active=False)
        self.migrateShapeNumberTo13_widget.bind(active=self.migrateShapeNumberTo13)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo13_widget)
        
        #gunRight1
        self.migrateShapeNumberTo12_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[12], active=False)
        self.migrateShapeNumberTo12_widget.bind(active=self.migrateShapeNumberTo12)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo12_widget)
        
        #circle
        self.migrateShapeNumberTo11_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[11], active=False)
        self.migrateShapeNumberTo11_widget.bind(active=self.migrateShapeNumberTo11)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo11_widget)
        
        #fishUp
        self.migrateShapeNumberTo10_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[10], active=False)
        self.migrateShapeNumberTo10_widget.bind(active=self.migrateShapeNumberTo10)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo10_widget)
        
        #faceSad
        self.migrateShapeNumberTo9_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[9], active=False)
        self.migrateShapeNumberTo9_widget.bind(active=self.migrateShapeNumberTo9)
        migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo9_widget)
        
        #faceHappy
        self.migrateShapeNumberTo8_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[8], active=False)
        self.migrateShapeNumberTo8_widget.bind(active=self.migrateShapeNumberTo8)
        migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo8_widget)
        
        #fishLeftWithTails
        self.migrateShapeNumberTo7_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[7], active=False)
        self.migrateShapeNumberTo7_widget.bind(active=self.migrateShapeNumberTo7)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo7_widget)
        
        #fishLeft
        self.migrateShapeNumberTo6_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[6], active=False)
        self.migrateShapeNumberTo6_widget.bind(active=self.migrateShapeNumberTo6)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo6_widget)
        
        #arrowLeft
        self.migrateShapeNumberTo5_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[5], active=False)
        self.migrateShapeNumberTo5_widget.bind(active=self.migrateShapeNumberTo5)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo5_widget)
        
        #fishStripes
        self.migrateShapeNumberTo4_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[4], active=False)
        self.migrateShapeNumberTo4_widget.bind(active=self.migrateShapeNumberTo4)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo4_widget)
        
        #hand
        self.migrateShapeNumberTo3_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[3], active=False)
        self.migrateShapeNumberTo3_widget.bind(active=self.migrateShapeNumberTo3)
        migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo3_widget)
        
        #planeSide
        self.migrateShapeNumberTo2_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[2], active=False)
        self.migrateShapeNumberTo2_widget.bind(active=self.migrateShapeNumberTo2)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo2_widget)
        
        #planeTop
        self.migrateShapeNumberTo1_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[1], active=False)
        self.migrateShapeNumberTo1_widget.bind(active=self.migrateShapeNumberTo1)
        #migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo1_widget)
        
        self.migrateShapeNumberTo0_widget = LabeledSwitch(labelingString=self.mindCupolaVisualizerGavinController.migrateShapeDict[0], active=False)
        self.migrateShapeNumberTo0_widget.bind(active=self.migrateShapeNumberTo0)
        migrateShapeNumberBox2.add_widget(self.migrateShapeNumberTo0_widget)
        
        ##
        boidBox = BoxLayoutOrientationRelativeToParent(size_hint=[1,2])
        box.add_widget(boidBox)
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
        box.add_widget(self.predatorCountToZero_widget)
        
        self.predatorCountToOne_widget = LabeledSwitch(labelingString='set predatorCountToOne', active=False)
        self.predatorCountToOne_widget.bind(active=self.predatorCountToOne)
        box.add_widget(self.predatorCountToOne_widget)
        
        
        stateBox = BoxLayoutOrientationRelativeToParent(size_hint=[1,2])
        box.add_widget(stateBox)
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
        box.add_widget(calibrationTarget_widget)
        
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
        
                
    def migrateShapeNumberWidgetsToInactive(self):
        self.migrateShapeNumberTo0_widget.active = False
        self.migrateShapeNumberTo1_widget.active = False
        self.migrateShapeNumberTo2_widget.active = False
        self.migrateShapeNumberTo3_widget.active = False
        self.migrateShapeNumberTo4_widget.active = False
        self.migrateShapeNumberTo5_widget.active = False
        self.migrateShapeNumberTo6_widget.active = False
        self.migrateShapeNumberTo7_widget.active = False
        self.migrateShapeNumberTo8_widget.active = False
        self.migrateShapeNumberTo9_widget.active = False
        self.migrateShapeNumberTo10_widget.active = False
        self.migrateShapeNumberTo11_widget.active = False
        self.migrateShapeNumberTo12_widget.active = False
        self.migrateShapeNumberTo13_widget.active = False
        self.migrateShapeNumberTo14_widget.active = False
        self.migrateShapeNumberTo15_widget.active = False
        self.migrateShapeNumberTo16_widget.active = False
        self.migrateShapeNumberTo17_widget.active = False
        self.migrateShapeNumberTo18_widget.active = False
        self.migrateShapeNumberTo19_widget.active = False
        self.migrateShapeNumberTo20_widget.active = False
        self.migrateShapeNumberTo21_widget.active = False
        self.migrateShapeNumberTo22_widget.active = False
        self.migrateShapeNumberTo23_widget.active = False
        self.migrateShapeNumberTo24_widget.active = False
        self.migrateShapeNumberTo25_widget.active = False
        self.migrateShapeNumberTo26_widget.active = False
        
    def migrateShapeNumberTo0(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 0
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo1(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 1
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo2(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 2
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo3(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 3
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo4(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 4
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo5(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 5
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo6(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 6
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo7(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 7
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo8(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 8
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo9(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 9
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo10(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 10
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo11(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 11
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo12(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 12
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo13(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 13
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo14(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 14
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo15(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 15
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo16(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 16
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo17(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 17
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo18(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 18
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo19(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 19
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo20(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 20
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo21(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 21
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo22(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 22
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo23(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 23
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo24(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 24
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo25(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 25
            self.migrateShapeNumberWidgetsToInactive()
            
    def migrateShapeNumberTo26(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.migrateShapeNumber = 26
            self.migrateShapeNumberWidgetsToInactive()

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

    def predatorCountToZero(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.predatorCount = 0
            self.predatorCountToOne_widget.active = False
            
    def predatorCountToOne(self, instance, value):
        if value:
            self.mindCupolaVisualizerGavinController.predatorCount = 1
            self.predatorCountToZero_widget.active = False
    


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



class MindCupolaVisualizerGavinControllerFlockWidget(BoxLayoutOrientationRelativeToParent):

    def __init__(self, mindCupolaVisualizerGavinController=None, **kwargs):
        super(MindCupolaVisualizerGavinControllerFlockWidget, self).__init__(**kwargs)
        self.mindCupolaVisualizerGavinController = MindCupolaVisualizerGavinController() if mindCupolaVisualizerGavinController is None else mindCupolaVisualizerGavinController
        assert isinstance(self.mindCupolaVisualizerGavinController, MindCupolaVisualizerGavinController)

        #self.orientationInvertedFromParent = True
        box = BoxLayoutOrientationRelativeToParent(orientationInvertedFromParent=True)
        self.add_widget(box)
        
        cohesiveDistance_widget = LabeledSlider(labelingString='cohesiveDistance',
                                                value=self.mindCupolaVisualizerGavinController.cohesiveDistance,
                                                min=self.mindCupolaVisualizerGavinController.property('cohesiveDistance').get_min(self.mindCupolaVisualizerGavinController),
                                                max=self.mindCupolaVisualizerGavinController.property('cohesiveDistance').get_max(self.mindCupolaVisualizerGavinController),
                                                orientationInvertedFromParent=False,
                                                )
        cohesiveDistance_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('cohesiveDistance'))
        self.mindCupolaVisualizerGavinController.bind(cohesiveDistance=cohesiveDistance_widget.setter('value'))
        box.add_widget(cohesiveDistance_widget)

        cruisingSpeed_widget = LabeledSlider(labelingString='cruisingSpeed',
                                                value=self.mindCupolaVisualizerGavinController.cruisingSpeed,
                                                min=self.mindCupolaVisualizerGavinController.property('cruisingSpeed').get_min(self.mindCupolaVisualizerGavinController),
                                                max=self.mindCupolaVisualizerGavinController.property('cruisingSpeed').get_max(self.mindCupolaVisualizerGavinController),
                                                orientationInvertedFromParent=False,
                                                )
        cruisingSpeed_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('cruisingSpeed'))
        self.mindCupolaVisualizerGavinController.bind(cruisingSpeed=cruisingSpeed_widget.setter('value'))
        box.add_widget(cruisingSpeed_widget)

        maxVelocity_widget = LabeledSlider(labelingString='maxVelocity',
                                                value=self.mindCupolaVisualizerGavinController.maxVelocity,
                                                min=self.mindCupolaVisualizerGavinController.property('maxVelocity').get_min(self.mindCupolaVisualizerGavinController),
                                                max=self.mindCupolaVisualizerGavinController.property('maxVelocity').get_max(self.mindCupolaVisualizerGavinController),
                                                orientationInvertedFromParent=False,
                                                )
        maxVelocity_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('maxVelocity'))
        self.mindCupolaVisualizerGavinController.bind(maxVelocity=maxVelocity_widget.setter('value'))
        box.add_widget(maxVelocity_widget)
        
        attractionRate_widget = LabeledSlider(labelingString='attractionRate',
                                                value=self.mindCupolaVisualizerGavinController.attractionRate,
                                                min=self.mindCupolaVisualizerGavinController.property('attractionRate').get_min(self.mindCupolaVisualizerGavinController),
                                                max=self.mindCupolaVisualizerGavinController.property('attractionRate').get_max(self.mindCupolaVisualizerGavinController),
                                                orientationInvertedFromParent=False,
                                                )
        attractionRate_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('attractionRate'))
        self.mindCupolaVisualizerGavinController.bind(attractionRate=attractionRate_widget.setter('value'))
        box.add_widget(attractionRate_widget)
        
        velocityRate_widget = LabeledSlider(labelingString='velocityRate',
                                                value=self.mindCupolaVisualizerGavinController.velocityRate,
                                                min=self.mindCupolaVisualizerGavinController.property('velocityRate').get_min(self.mindCupolaVisualizerGavinController),
                                                max=self.mindCupolaVisualizerGavinController.property('velocityRate').get_max(self.mindCupolaVisualizerGavinController),
                                                orientationInvertedFromParent=False,
                                                )
        velocityRate_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('velocityRate'))
        self.mindCupolaVisualizerGavinController.bind(velocityRate=velocityRate_widget.setter('value'))
        box.add_widget(velocityRate_widget)
        
        migrateRate_widget = LabeledSlider(labelingString='migrateRate',
                                                value=self.mindCupolaVisualizerGavinController.migrateRate,
                                                min=self.mindCupolaVisualizerGavinController.property('migrateRate').get_min(self.mindCupolaVisualizerGavinController),
                                                max=self.mindCupolaVisualizerGavinController.property('migrateRate').get_max(self.mindCupolaVisualizerGavinController),
                                                orientationInvertedFromParent=False,
                                                )
        migrateRate_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('migrateRate'))
        self.mindCupolaVisualizerGavinController.bind(migrateRate=migrateRate_widget.setter('value'))
        box.add_widget(migrateRate_widget)
        
        migrateOrbit_widget = LabeledSlider(labelingString='migrateOrbit',
                                                value=self.mindCupolaVisualizerGavinController.migrateOrbit,
                                                min=self.mindCupolaVisualizerGavinController.property('migrateOrbit').get_min(self.mindCupolaVisualizerGavinController),
                                                max=self.mindCupolaVisualizerGavinController.property('migrateOrbit').get_max(self.mindCupolaVisualizerGavinController),
                                                orientationInvertedFromParent=False,
                                                )
        migrateOrbit_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('migrateOrbit'))
        self.mindCupolaVisualizerGavinController.bind(migrateOrbit=migrateOrbit_widget.setter('value'))
        box.add_widget(migrateOrbit_widget)
        
        localMigrateOrbit_widget = LabeledSlider(labelingString='localMigrateOrbit',
                                                value=self.mindCupolaVisualizerGavinController.localMigrateOrbit,
                                                min=self.mindCupolaVisualizerGavinController.property('localMigrateOrbit').get_min(self.mindCupolaVisualizerGavinController),
                                                max=self.mindCupolaVisualizerGavinController.property('localMigrateOrbit').get_max(self.mindCupolaVisualizerGavinController),
                                                orientationInvertedFromParent=False,
                                                )
        localMigrateOrbit_widget.bind(value=self.mindCupolaVisualizerGavinController.setter('localMigrateOrbit'))
        self.mindCupolaVisualizerGavinController.bind(localMigrateOrbit=localMigrateOrbit_widget.setter('value'))
        box.add_widget(localMigrateOrbit_widget)

           
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
        box = BoxLayoutOrientationRelativeToParent(orientationInvertedFromParent=False)
        mindCupolaVisualizerGavinControllerMainWidget = MindCupolaVisualizerGavinControllerMainWidget(mindCupolaVisualizerGavinController=self.mindCupolaVisualizerGavinController, orientation='horizontal')
        mindCupolaVisualizerGavinControllerFlockWidget = MindCupolaVisualizerGavinControllerFlockWidget(mindCupolaVisualizerGavinController=self.mindCupolaVisualizerGavinController, orientation='horizontal')
        box.add_widget(mindCupolaVisualizerGavinControllerMainWidget)
        box.add_widget(mindCupolaVisualizerGavinControllerFlockWidget)
        return box
                        
# self run, self test     
if __name__ == "__main__":
    Logger.info(__file__ + ': running from __name__')
    mcvgHost = '192.168.1.118'
    
    mindCupolaVisualizerGavinController = MindCupolaVisualizerGavinController(host=mcvgHost, verbose=True)
    mindCupolaVisualizerGavinControllerWidgetTestApp = MindCupolaVisualizerGavinControllerWidgetTestApp(mindCupolaVisualizerGavinController=mindCupolaVisualizerGavinController)
    mindCupolaVisualizerGavinControllerWidgetTestApp.run()
