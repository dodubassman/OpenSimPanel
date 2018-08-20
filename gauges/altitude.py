#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.uix.widget import Widget

import kivy

from kivy.properties import StringProperty, NumericProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image

kivy.require('1.10.1')


class AltitudeWidget(Widget):

    data_ref = ''
    units_per_revolution = 1000
    start_angle = 0
    value = BoundedNumericProperty(0, min=-1000, max=100000, errorvalue=-9999)
    file_gauge = StringProperty("gauges/assets/altitude_gear.png")
    file_needle = StringProperty("gauges/assets/altitude_dial_100.png")
    file_needle1k = StringProperty("gauges/assets/altitude_dial_1000.png")
    file_needle10k = StringProperty("gauges/assets/altitude_dial_10000.png")
    size_gauge = NumericProperty(300)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self._gauge = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        self._img_gauge = Image(source=self.file_gauge, size=(self.size_gauge, self.size_gauge))

        self._needle = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        self._needle1k = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        self._needle10k = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        _img_needle = Image(source=self.file_needle, size=(self.size_gauge, self.size_gauge))
        _img_needle1k = Image(source=self.file_needle1k, size=(self.size_gauge, self.size_gauge))
        _img_needle10k = Image(source=self.file_needle10k, size=(self.size_gauge, self.size_gauge))

        self._gauge.add_widget(self._img_gauge)

        self._needle.add_widget(_img_needle)
        self._needle1k.add_widget(_img_needle1k)
        self._needle10k.add_widget(_img_needle10k)

        self.add_widget(self._gauge)

        self.add_widget(self._needle10k)
        self.add_widget(self._needle1k)
        self.add_widget(self._needle)

        self.bind(pos=self._update)
        self.bind(size_gauge=self._update)
        self.bind(value=self._turn)

    def _update(self, *args):
        self._gauge.pos = self.pos

        self._needle.pos = (self.x, self.y)
        self._needle.center = self._gauge.center

        self._needle1k.pos = (self.x, self.y)
        self._needle1k.center = self._gauge.center

        self._needle10k.pos = (self.x, self.y)
        self._needle10k.center = self._gauge.center

        self._gauge.width = self.size_gauge
        self._img_gauge.width = self.size_gauge

    def _turn(self, *args):
        self._needle.center_x = self._gauge.center_x
        self._needle1k.center_x = self._gauge.center_x
        self._needle10k.center_x = self._gauge.center_x

        self._needle.center_y = self._gauge.center_y
        self._needle1k.center_y = self._gauge.center_y
        self._needle10k.center_y = self._gauge.center_y

        unit = 360 / self.units_per_revolution
        self._needle.rotation = unit - (self.value * unit)
        self._needle1k.rotation = unit - (self.value / 10 * unit)
        self._needle10k.rotation = unit - (self.value / 100 * unit)
