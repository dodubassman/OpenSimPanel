#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

'''
Gauge
=====

The :class:`Gauge` widget is a widget for displaying gauges.

.. note::

Source svg file provided for customing.

'''

__version__ = '0.2'
__author__ = 'julien@hautefeuille.eu, tcaron@umanit.fr'

import kivy

kivy.require('1.10.1')
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image


class AirspeedWidget(Widget):
    '''
    AirspeedWidget class

    '''

    unit = NumericProperty(1.8)
    value = BoundedNumericProperty(0, min=0, max=100000, errorvalue=-1)
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
        '''
        Update gauges and needle positions after sizing or positioning.

        '''
        self._gauge.pos = self.pos
        self._needle.pos = (self.x, self.y)
        self._needle.center = self._gauge.center
        self._gauge.width = self.size_gauge
        self._img_gauge.width = self.size_gauge

    def _turn(self, *args):
        '''
        Turn needle, 1 degree = 1 unit, 0 degree point start on 50 value.

        '''
        self._needle.center_x = self._gauge.center_x
        self._needle.center_y = self._gauge.center_y
        self._needle.rotation = self.unit - (self.value * self.unit)
