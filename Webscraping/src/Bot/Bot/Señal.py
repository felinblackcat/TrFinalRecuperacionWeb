# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:27:24 2020

@author: Acer
"""

from PyQt5.QtCore import QObject, pyqtSignal
class Foo(QObject):

    # Define a new signal called 'trigger' that has no arguments.
    trigger = pyqtSignal(str)

    def connect_and_emit_trigger(self,value):
        # Connect the trigger signal to a slot.
        # Emit the signal.
        self.trigger.emit(value)

    def handle_trigger(self):
        # Show that the slot has been called.
        print(".")