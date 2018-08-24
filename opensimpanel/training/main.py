import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.slider import Slider

from opensimpanel.gauges.altitude import AltitudeWidget
from kivy.app import App

kivy.require('1.10.1')


class SimVimDR400App(App):
    def build(self):
        def setScale(*ars):
            scatter.scale = sliderScale.value

        def setGaugeValue(*ars):
            alt.value = sliderValue.value

        def setPosition(*ars):
            scatter.pos = (sliderPositionX.value, sliderPositionY.value)

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        scatter = Scatter()

        alt = AltitudeWidget(value=0, size_gauge=300)

        scatter.add_widget(alt)

        box.add_widget(scatter)

        sliderValue = Slider(min=0, max=10000, value=0)
        sliderScale = Slider(min=0.5, max=3, value=1)
        sliderPositionX = Slider(min=0, max=1024, value=10)
        sliderPositionY = Slider(min=0, max=1024, value=10)

        sliderValue.bind(value=setGaugeValue)
        sliderScale.bind(value=setScale)

        sliderPositionX.bind(value=setPosition)
        sliderPositionY.bind(value=setPosition)

        box.add_widget(sliderValue)
        box.add_widget(sliderScale)
        box.add_widget(sliderPositionX)
        box.add_widget(sliderPositionY)

        return box


SimVimDR400 = SimVimDR400App()

SimVimDR400.run()
