#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gauge
=====
The :class:`GaugeWidget` is a widget for displaying gauges.

"""

__version__ = '0.2'
__author__ = 'julien@hautefeuille.eu, dodubassman@gmail.com'

import kivy

from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image

kivy.require('1.10.1')


class GaugeWidget(Widget):

    data_ref = ''
    unit_per_revolution = 220
    value = BoundedNumericProperty(0, min=0, max=10000, errorvalue=-1)
    file_gauge = StringProperty("gauges/assets/speed.png")
    file_needle = StringProperty("gauges/assets/speed-dial.png")
    size_gauge = NumericProperty(300)

    def __init__(self, **kwargs):
        super().__init__()

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

        _img_needle = Image(source=self.file_needle, size=(self.size_gauge, self.size_gauge))

        self._gauge.add_widget(self._img_gauge)
        self._needle.add_widget(_img_needle)

        self.add_widget(self._gauge)
        self.add_widget(self._needle)

        self.bind(pos=self._update)
        self.bind(size_gauge=self._update)
        self.bind(value=self._turn)

    def _update(self, *args):
        """
        Update gauges and needle positions after sizing or positioning.

        """
        self._gauge.pos = self.pos
        self._needle.pos = (self.x, self.y)
        self._needle.center = self._gauge.center
        self._gauge.width = self.size_gauge
        self._img_gauge.width = self.size_gauge

    def _turn(self, *args):
        """
        Needle Rotation

        """

        #  Set rotation unit depending of gauge actual unit
        unit = 360 / self.unit_per_revolution
        self._needle.center_x = self._gauge.center_x
        self._needle.center_y = self._gauge.center_y
        self._needle.rotation = unit - (self.value * unit)
