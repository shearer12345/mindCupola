'''
Created on 21 Jul 2012

@author: shearer
'''

from kivy import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.switch import Switch
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

class BoxLayoutOrientationRelativeToParent(BoxLayout):
    def __init__(self, orientationInvertedFromParent=True, **kwargs):
        super(BoxLayoutOrientationRelativeToParent, self).__init__(**kwargs)
        self.orientationInvertedFromParent = orientationInvertedFromParent
        
    def on_parent(self, instance, value):
        if  hasattr(self, 'orientation') and \
            hasattr(self, 'parent') and \
            hasattr(self.parent, 'orientation') and \
            self.parent is not None:
                assert hasattr(self, 'orientationInvertedFromParent')
                if self.orientationInvertedFromParent:
                    self.orientation = 'horizontal' if self.parent.orientation is 'vertical' else 'vertical'
                else:
                    self.orientation = 'horizontal' if self.parent.orientation is 'horizontal' else 'vertical'
    
class SliderOrientationRelativeToParent(Slider):
    def __init__(self, orientationInvertedFromParent=True, **kwargs):
        super(SliderOrientationRelativeToParent, self).__init__(**kwargs)
        self.orientationInvertedFromParent = orientationInvertedFromParent
        
    def on_parent(self, instance, value):
        if  hasattr(self, 'orientation') and \
            hasattr(self, 'parent') and \
            hasattr(self.parent, 'orientation') and \
            self.parent is not None:
                assert hasattr(self, 'orientationInvertedFromParent')
                if self.orientationInvertedFromParent:
                    self.orientation = 'horizontal' if self.parent.orientation is 'vertical' else 'vertical'
                else:
                    self.orientation = 'horizontal' if self.parent.orientation is 'horizontal' else 'vertical'
    
class CheckBoxOrientationRelativeToParent(CheckBox):
    def __init__(self, orientationInvertedFromParent=True, **kwargs):
        super(CheckBoxOrientationRelativeToParent, self).__init__(**kwargs)
        self.orientationInvertedFromParent = orientationInvertedFromParent
        
    def on_parent(self, instance, value):
        if  hasattr(self, 'orientation') and \
            hasattr(self, 'parent') and \
            hasattr(self.parent, 'orientation') and \
            self.parent is not None:
                assert hasattr(self, 'orientationInvertedFromParent')
                if self.orientationInvertedFromParent:
                    self.orientation = 'horizontal' if self.parent.orientation is 'vertical' else 'vertical'
                else:
                    self.orientation = 'horizontal' if self.parent.orientation is 'horizontal' else 'vertical'
    
class SwitchOrientationRelativeToParent(Switch):
    def __init__(self, orientationInvertedFromParent=True, **kwargs):
        super(SwitchOrientationRelativeToParent, self).__init__(**kwargs)
        self.orientationInvertedFromParent = orientationInvertedFromParent
        
    def on_parent(self, instance, value):
        if  hasattr(self, 'orientation') and \
            hasattr(self, 'parent') and \
            hasattr(self.parent, 'orientation') and \
            self.parent is not None:
                assert hasattr(self, 'orientationInvertedFromParent')
                if self.orientationInvertedFromParent:
                    self.orientation = 'horizontal' if self.parent.orientation is 'vertical' else 'vertical'
                else:
                    self.orientation = 'horizontal' if self.parent.orientation is 'horizontal' else 'vertical'
    
class LabelOrientationRelativeToParent(Label):
    def __init__(self, orientationInvertedFromParent=True, **kwargs):
        super(LabelOrientationRelativeToParent, self).__init__(**kwargs)
        self.orientationInvertedFromParent = orientationInvertedFromParent
        
    def on_parent(self, instance, value):
        if  hasattr(self, 'orientation') and \
            hasattr(self, 'parent') and \
            hasattr(self.parent, 'orientation') and \
            self.parent is not None:
                assert hasattr(self, 'orientationInvertedFromParent')
                if self.orientationInvertedFromParent:
                    self.orientation = 'horizontal' if self.parent.orientation is 'vertical' else 'vertical'
                else:
                    self.orientation = 'horizontal' if self.parent.orientation is 'horizontal' else 'vertical'
    
class LabeledSlider(BoxLayoutOrientationRelativeToParent):
    
    labelingString = StringProperty('dummy slider label ')
    value = NumericProperty()
    labelingWidget = None
    sliderWidget = None
    
    def __init__(self, labelingString, value, **kwargs):
        super(LabeledSlider, self).__init__(**kwargs)

        assert type(labelingString) is str
        assert type(value) in [int, float]
        
        self.labelingWidget = LabelOrientationRelativeToParent(text=labelingString, **kwargs)
        self.sliderWidget = SliderOrientationRelativeToParent(value=value, **kwargs)
        
        # double bind labelText
        self.labelingWidget.bind(text=self.setter('labelingString'))
        self.bind(labelingString=self.labelingWidget.setter('text'))
        
        # double bind text
        self.sliderWidget.bind(value=self.setter('value'))
        self.bind(value=self.sliderWidget.setter('value'))
        
        self.add_widget(self.labelingWidget)
        self.add_widget(self.sliderWidget)
        
    
class LabeledCheckBox(BoxLayoutOrientationRelativeToParent):
    
    labelingString = StringProperty('dummy checkbox label ')
    active = BooleanProperty(False)
    labelingWidget = None
    checkBoxWidget = None
    
    def __init__(self, labelingString, active, **kwargs):
        super(LabeledCheckBox, self).__init__(**kwargs)
        
        assert type(labelingString) is str
        assert type(active) is bool
    
        #kwargs['orientationInvertedFromParent'] = True
        self.labelingWidget = LabelOrientationRelativeToParent(text=labelingString, **kwargs)
        self.checkBoxWidget = CheckBoxOrientationRelativeToParent(active=active, **kwargs)

        # double bind labelText
        self.labelingWidget.bind(text=self.setter('labelingString'))
        self.bind(labelingString=self.labelingWidget.setter('text'))
        
        # double bind text
        self.checkBoxWidget.bind(active=self.setter('active'))
        self.bind(active=self.checkBoxWidget.setter('active'))
        
        self.add_widget(self.labelingWidget)
        self.add_widget(self.checkBoxWidget)
        
class LabeledLabel(BoxLayoutOrientationRelativeToParent):
    
    labelingString = StringProperty('dummy label label ')
    labelString = StringProperty('dummy label')
    labelingWidget = None
    labelWidget = None
    
    def __init__(self, labelingString, labelString, **kwargs):
        super(LabeledLabel, self).__init__(**kwargs)
        assert type(labelingString) is str
        assert type(labelString) is str
        
        #kwargs['orientationInvertedFromParent'] = True
        self.labelingWidget = LabelOrientationRelativeToParent(text=labelingString, **kwargs)
        self.labelWidget = LabelOrientationRelativeToParent(text=labelString, **kwargs)

        # double bind labelText
        self.labelingWidget.bind(text=self.setter('labelingString'))
        self.bind(labelingString=self.labelingWidget.setter('text'))
        
        # double bind text
        self.labelWidget.bind(text=self.setter('labelString'))
        self.bind(labelString=self.labelWidget.setter('text'))
        
        self.add_widget(self.labelingWidget)
        self.add_widget(self.labelWidget)
        
class LabeledSwitch(BoxLayoutOrientationRelativeToParent):
    
    labelingString = StringProperty('dummy switch label')
    active = BooleanProperty(False)
    labelingWidget = None
    switchWidget = None
    
    def __init__(self, labelingString, active, **kwargs):
        super(LabeledSwitch, self).__init__(**kwargs)
        
        assert type(labelingString) is str
        assert type(active) in [bool, BooleanProperty]
               
        #kwargs['orientationInvertedFromParent'] = True
        self.labelingWidget = LabelOrientationRelativeToParent(text=labelingString, **kwargs)
        self.switchWidget = SwitchOrientationRelativeToParent(active=active, **kwargs)
        
        # double bind labelText
        self.labelingWidget.bind(text=self.setter('labelingString'))
        self.bind(labelingString=self.labelingWidget.setter('text'))
        
        # double bind text
        self.switchWidget.bind(active=self.setter('active'))
        self.bind(active=self.switchWidget.setter('active'))
        
        self.add_widget(self.labelingWidget)
        self.add_widget(self.switchWidget)




    
from kivy.app import App

class kivyUtilsTestApp(App):

    def build(self):
        
        layout = BoxLayout(orientation = 'vertical')
        
        layout.add_widget(LabeledSlider(labelingString='labeledSlider1', value=5.0, min = -3, max = 10, orientationInvertedFromParent = True))
        
        layout.add_widget(LabeledCheckBox(labelingString='labeledCheckBox', active=True))
        
        layout.add_widget(LabeledLabel(labelingString='labledLabel', labelString='a label'))
        
        layout.add_widget(LabeledSwitch(labelingString='labeledSwitch', active=False))
        
        return layout




# self run, self test     
if __name__ == "__main__":
    Logger.info(__file__ + ': running from __name__')
                
    kivyUtilsTestApp().run()
