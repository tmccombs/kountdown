# -*- coding: utf-8 -*-
# Copyright 2013 Thayne McCombs
from PyQt4.QtCore import *
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

from datetime import date

from model import KountdownModel
from configUI import ConfigPage

class Kountdown(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

 
    def init(self):
        self.setHasConfigurationInterface(True)

        config = self.config()

        self.model = KountdownModel(config)
        self.model.configChanged.connect(self.updatedConfig)
        if config.hasKey('Target') and config.hasKey('Event'):
            self.setupMainUI()
            'has both'
        else:
            self.setConfigurationRequired(True)
        self.resize(300,125)



    def setupMainUI(self):
        print 'setup'
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

        self.setBackgroundHints(Plasma.Applet.TranslucentBackground)

        self.layout = QGraphicsLinearLayout(Qt.Vertical,self.applet)
        self.label = Plasma.Label(self.applet)
        self.label.setText(self.model.message)
        self.label.setStyleSheet('''font-size: 18pt;''')
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addItem(self.label)
        self.applet.setLayout(self.layout)


        self.connectToEngine()
        self.model.messageChanged.connect(self.handleMessageChanged)

    def createConfigurationInterface(self, parent):
        '''Create the configuration UI'''
        plasmascript.Applet.createConfigurationInterface(self,parent)
        parent.addPage( ConfigPage(parent, self.model), 'Config')

    def updatedConfig(self):
        config = self.config()
        print 'updated'
        if self.configurationRequired() and config.hasKey('Target') and config.hasKey('Event'):
            self.setConfigurationRequired(False)
            self.setupMainUI()
        self.configNeedsSaving.emit()
        


    def connectToEngine(self):
        self.timeEngine = self.dataEngine("time")
        self.model.connectToEngine(self.timeEngine)

    def handleMessageChanged(self, newMessage):
        '''Update the view when the message changes.'''
        self.label.setText(newMessage)
        self.update()

def CreateApplet(parent):
    return Kountdown(parent)
