# -*- coding: utf-8 -*-
# Copyright 2013 Thayne McCombs

from PyQt4.QtCore import *
from PyKDE4.plasma import Plasma

from datetime import date

class KountdownModel(QObject):
    '''Model object to keep track of the state of a Kountdown instance
    and take care of reading and writing configuration values.'''

    messageTemplate = str(QCoreApplication.translate('kountdown','{0} days until {1}'))
    milliInHour = 3600000

    messageChanged = pyqtSignal('QString')
    configChanged = pyqtSignal()

    def __init__(self,configLoader):
        '''Create a Kountdown model backed by the supplied ConfigLoader'''
        QObject.__init__(self)
        self.config = configLoader
        self._today = date.today()
        self.config.configChanged.connect(self.configChanged)


    @property
    def needsConfiguration(self):
        return False

    @property
    def message(self):
        '''get the message to display to the user'''
        return self.messageTemplate.format(self.daysRemaining, self.event)

    @property
    def targetDate(self):
        '''get the target date for the countdown'''
        return self.config.property('target').toDate().toPyDate()

    @property
    def event(self):
        '''Get the name of the event counting down to'''
        return self.config.property('event').toPyObject()

    @property
    def daysRemaining(self):
        '''get the number of days remaining.'''
        return (self.targetDate - self._today).days

    def setCurrentDate(self, current):
        '''set the current date'''
        if current != self._today:
            self._today = current
            self.messageChanged.emit(self.message)

    @pyqtSignature("dataUpdated(const QString&, const Plasma::DataEngine::Data&)")
    def dataUpdated(self, sourceName, data):
        '''retrieve the current date from a dataengine.
        The Data must contain a Date key of type QDate.'''
        today = data[QString("Date")].toPyDate()
        self.setCurrentDate(today)

    def connectToEngine(self, engine):
        '''Connect this model to a Data Engine (specifically
         a time data engine).'''
        engine.connectSource("Local",self,self.milliInHour,Plasma.AlignToHour)

    def configChanged(self):
        '''Handle a configuration change.'''
        self.messageChanged.emit(self.message)
        

