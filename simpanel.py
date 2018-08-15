from configparser import NoSectionError

import kivy
from kivy import Config
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.app import App

kivy.require('1.10.1')


# Main container
class SimPanel(Widget):

    def __init__(self, **kwargs):
        super(SimPanel, self).__init__(**kwargs)
        # Keyboard aware widget
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # Bind keyboard
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == '+':
            self._resizeScaleBox(keycode[1])
        elif keycode[1] == '=':  # Troubleshooting on MacOs
            self._resizeScaleBox('+')
        elif keycode[1] == '-':
            self._resizeScaleBox(keycode[1])
        elif keycode[1] == 'up':
            self._moveScaleBox(keycode[1])
        elif keycode[1] == 'down':
            self._moveScaleBox(keycode[1])
        elif keycode[1] == 'right':
            self._moveScaleBox(keycode[1])
        elif keycode[1] == 'left':
            self._moveScaleBox(keycode[1])
        elif keycode[1] == 'enter':
            self._saveConfiguration()
        elif keycode[1] == 'escape':
            # False sends back the key to the system and allow to quit
            return False
        # Accept the key and avoid to send it to the system
        return True

    def _getScaleBox(self):
        sim_scale_box = self.children[0]
        # Verifying we're on the good object
        if type(sim_scale_box).__name__ == 'SimScaleBox':
            return sim_scale_box

    def _moveScaleBox(self, side):
        sim_scale_box = self._getScaleBox()
        if side == 'right':
            sim_scale_box.pos = (sim_scale_box.pos[0] + 1, sim_scale_box.pos[1])
        elif side == 'left':
            sim_scale_box.pos = (sim_scale_box.pos[0] - 1, sim_scale_box.pos[1])
        elif side == 'up':
            sim_scale_box.pos = (sim_scale_box.pos[0], sim_scale_box.pos[1] + 1)
        else:  # 'down'
            sim_scale_box.pos = (sim_scale_box.pos[0], sim_scale_box.pos[1] - 1)

    def _resizeScaleBox(self, sign):
        sim_scale_box = self._getScaleBox()
        if sign == '+':
            sim_scale_box.scale = sim_scale_box.scale + .01
        else:  # '-'
            sim_scale_box.scale = sim_scale_box.scale - .01

    #  Save config to local simpanel.ini
    def _saveConfiguration(self):
        sim_scale_box = self._getScaleBox()
        Config.read('simpanel.ini')
        Config.set('simpanel', 'posX', round(sim_scale_box.pos[0], 1))
        Config.set('simpanel', 'posY', round(sim_scale_box.pos[1], 1))
        Config.set('simpanel', 'scale', round(sim_scale_box.scale, 3))
        Config.write()


# Scatter used to adjust position and size of the whole panel
class SimScaleBox(Scatter):
    def __init__(self, **kwargs):
        super(SimScaleBox, self).__init__(**kwargs)
        # set pre-saved data
        self.scale = eval(Config.get('simpanel', 'scale'))
        self.pos = (eval(Config.get('simpanel', 'posX')), eval(Config.get('simpanel', 'posY')))


# Sim App
class SimPanelApp(App):
    def build(self):
        return SimPanel()


#  Create config file at first use
Config.read('simpanel.ini')
try:
    Config.get('simpanel', 'posX')
except NoSectionError:
    Config.add_section('simpanel')
    Config.set('simpanel', 'posX', 0)
    Config.set('simpanel', 'posY', 0)
    Config.set('simpanel', 'scale', 1)
    Config.write()
    pass

Window.fullscreen = 'auto'

app = SimPanelApp()
app.run()
