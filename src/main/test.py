import sys
import math
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

from TrackController.trackcontrol import TrackControl





# create app
app = QApplication(sys.argv)

# create window instance
test = TrackControl()
test.show_gui()

# run app
app.exec()