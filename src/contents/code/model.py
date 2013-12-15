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

    def __init__(self,config):
        QObject.__init__(self)
        self.config = config
        #TODO: figure out how to get rid of all this toDate, toPyDate stuff
        self._targetDate = config.readEntry('Target',QDate()).toDate().toPyDate()
        self._event = str(config.readEntry('Event',QString()).toString())
        self._today = date.today()

    @property
    def message(self):
        '''get the message to display to the user'''
        return self.messageTemplate.format(self.daysRemaining, self._event)

    @property
    def targetDate(self):
        '''get the target date for the countdown'''
        return self._targetDate

    @targetDate.setter
    def targetDate(self, value):
        '''set the target date for the countdown'''
        self._targetDate = value
        self.config.writeEntry('Target',QDate(value))
        self.configChanged.emit()
        self.messageChanged.emit(self.message)

    @property
    def event(self):
        '''Get the name of the event counting down to'''
        return self._event

    @event.setter
    def event(self, value):
        '''set the name of the event counting down to'''
        self._event = value
        self.config.writeEntry('Event',value)
        self.configChanged.emit()
        self.messageChanged.emit(self.message)

    @property
    def daysRemaining(self):
        '''get the number of days remaining.'''
        return (self._targetDate - self._today).days

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
        

