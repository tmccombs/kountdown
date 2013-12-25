# -*- coding: utf-8 -*-
# Copyright 2013 Thayne McCombs
from PyQt4.QtCore import *
from PyQt4.QtGui import QGraphicsLinearLayout,QWidget
from PyQt4 import uic
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

    def createConfigurationInterface(self,parent):
        plasmascript.Applet.createConfigurationInterface(self,parent)

        # add the general configuration tab
        generalWidget = QWidget(parent)
        uic.loadUi(self.package().filePath('ui','generalConfig.ui'),generalWidget)
        parent.addPage(generalWidget, self.configScheme(), 'Settings')


        # add the appearance configuration tab
        appearanceWidget = QWidget(parent)
        uic.loadUi(self.package().filePath('ui','appearanceConfig.ui'),appearanceWidget)
        parent.addPage(appearanceWidget, self.configScheme(), 'Appearance')


    def configChanged(self):
        '''handle changes in configuration'''
        plasmascript.Applet.configChanged(self)
        for item in self.configScheme().items():
            print('{0}: {1} in group: {2}'.format(item.name(), item.property().toPyObject(),item.group()))
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
