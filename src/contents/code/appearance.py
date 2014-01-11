# -*- coding: utf-8 -*-
# Copyright 2013 Thayne McCombs

from PyKDE4.kdeui import KConfigSkeleton
from PyKDE4.kdecore import KUrl, KCoreConfigSkeleton
from PyQt4.QtCore import *
from PyQt4.QtGui import QFont, QColor

class AppearanceModel(QObject):
    imageChanged = pyqtSignal('KUrl')
    stylesheetChanged = pyqtSignal('QString')

    def __init__(self,configLoader):
        QObject.__init__(self)
        self.config = configLoader
        self.config.configChanged.connect(self.configChanged)


    @property
    def color(self):
        return self.config.property('color').toPyObject()

    @property
    def font(self):
        return self.config.property('font').toPyObject()

    @property
    def imageUrl(self):
        return self.config.property('image').toPyObject()

    def stylesheet(self):
        return 'color: {0}; font: {1};'.format(self.color.name(), self._fontStyle())

    def _fontStyle(self):
        font = self.font
        boldItalic = ''
        if font.italic():
            boldItalic += ' italic'
        if font.bold():
            boldItalic += ' bold'
        return boldItalic + ' {0}pt {1}'.format(font.pointSize(), font.family())

    def configChanged(self):
        #for now don't do any checking
        self.imageChanged.emit(self.imageUrl)
        self.stylesheetChanged.emit(self.stylesheet())

