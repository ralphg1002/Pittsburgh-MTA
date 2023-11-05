# importing libraries
import sys
import math
import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tcsw_tb import *
from tcsw_ui import *
from tcsw_time import *
from tcsw_train_attributes import *
from tcsw_functions import *

# create app
app = QApplication(sys.argv)

# create window instance
window = TrainControllerUI()

# run app
app.exec()
