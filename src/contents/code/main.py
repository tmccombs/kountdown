# -*- coding: utf-8 -*-
# Copyright 2013 Thayne McCombs
from PyQt4.QtCore import *
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

from datetime import date

from model import KountdownModel

class Kountdown(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

 
    def init(self):
        self.setHasConfigurationInterface(True)

        self.model = KountdownModel(self.configScheme())
        if self.model.needsConfiguration:
            self.setConfigurationRequired(True)
        else:
            self.setupMainUI()
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

    def configChanged(self):
        '''handle changes in configuration'''
        plasmascript.Applet.configChanged(self)
        self.updatedConfig()

    def updatedConfig(self):
        config = self.config()
        if self.configurationRequired() and not self.model.needsConfiguration:
            self.setConfigurationRequired(False)
            self.setupMainUI()
        


    def connectToEngine(self):
        self.timeEngine = self.dataEngine("time")
        self.model.connectToEngine(self.timeEngine)

    def handleMessageChanged(self, newMessage):
        '''Update the view when the message changes.'''
        self.label.setText(newMessage)
        self.update()

def CreateApplet(parent):
    return Kountdown(parent)
