# -*- coding: utf-8 -*-
# Copyright 2013 Thayne McCombs

from PyQt4.QtGui import QFormLayout, QWidget
from PyQt4 import uic
from PyKDE4.kdeui import KDateComboBox, KLineEdit


class ConfigPage(QWidget):
    '''GUI for the configuration page for Kountdown'''

    def __init__(self, parent, model):
        '''Create a new ConfigPage backed by the supplied model.
        @param model The KountdownModel to update
        @param parent The parent GUI
        '''
        QWidget.__init__(self,parent)

        self.model = model
        self.dialog = parent

        self.setupUi()
        self.setupEvents()

    
    def setupUi(self):
        '''Set up the UI for the Page'''
        #Do this by hand for now since pykdeuic4 doesnt' work,
        #and it isn't too hard. Eventually move this into a UI file.
        self.setObjectName('ConfigPage')
        self.layout = QFormLayout(self)

        self.dateInput = KDateComboBox(self)
        self.layout.addRow('Event Date: ', self.dateInput)

        self.nameInput = KLineEdit(self)
        self.layout.addRow('Event Name: ', self.nameInput)

        self.loadConfig()


    def setupEvents(self):
        '''Add event handlers'''
        self.dialog.okClicked.connect(self.configAccepted)
        self.dialog.applyClicked.connect(self.configAccepted)


    def configAccepted(self):
        '''Apply the settings from the page.'''
        self.model.targetDate = self.dateInput.date().toPyDate()
        self.model.event = str(self.nameInput.text())


    def loadConfig(self):
        '''Load the values from the model.'''
        self.dateInput.setDate(self.model.targetDate)
        self.nameInput.setText(self.model.event)

