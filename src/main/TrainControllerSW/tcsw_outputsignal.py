from PyQt5.QtCore import *


class TMSignals(QObject):
    pwrCmd = pyqtSignal(float)
    spSpd = 0
    self.anncmnt = ""
    self.hdlt = False
    self.ilt = False
    self.lDoor = False
    self.rDoor = False
    self.spTemp = 0
    self.ad = ""
