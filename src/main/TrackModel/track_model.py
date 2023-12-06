from .TrackData import TrackData
from .Station import Station
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from signals import masterSignals, trainModelToTrackModel, trackControllerToTrackModel

MTA_STYLING = {
    # font variables
    "textFontSize": 10,
    "labelFontSize": 12,
    "headerFontSize": 16,
    "titleFontSize": 22,
    "fontStyle": "Product Sans",
    # color variables
    "darkBlue": "#085394",
    "lightRed": "#EA9999",
    "lightBlue": "#9FC5F8",
    "lightGrey": "#CCCCCC",
    "mediumGrey": "#DDDDDD",
    "darkGrey": "#666666",
    "black": "#000000",
    "green": "#00FF00",
    "red": "#FF0000",
    # dimensions
    "w": 960,
    "h": 960,
    # "moduleName": 'CTC'
}


class TrackView(QGraphicsView):
    blocks = {}

    def __init__(self, parent):
        super().__init__(parent)
        self.greenTrack = QGraphicsScene(self)
        self.redTrack = QGraphicsScene(self)
        self.drawGreenLine()
        self.drawRedLine()
        self.setScene(self.greenTrack)

    def drawGreenLine(self):        
        yardImage = QPixmap("src/main/TrackModel/pngs/yard.jpg")
        yardImage = yardImage.scaledToWidth(100)
        yardScene = QGraphicsPixmapItem(yardImage)
        yardScene.setPos(100, 180)
        self.greenTrack.addItem(yardScene)

        path_0 = QPainterPath()
        path_0.moveTo(163, 250)
        path_0.lineTo(163, 330)
        block_0 = self.createTrackBlock(path_0, "Block 0")
        self.greenTrack.addItem(block_0)
        self.blocks[0] = block_0

        path_151 = QPainterPath()
        path_151.moveTo(96, 278)
        path_151.cubicTo(97, 278, 120, 251, 120, 250)
        block_151 = self.createTrackBlock(path_151, "Block 151")
        self.greenTrack.addItem(block_151)

        path_1 = QPainterPath()
        path_1.moveTo(0, 0)
        path_1.cubicTo(0, 0, 5, 0, 10, 10)
        block_1 = self.createTrackBlock(path_1, "Block 1")
        self.greenTrack.addItem(block_1)
        self.blocks[1] = block_1

        path_2 = QPainterPath()
        path_2.moveTo(14, 18)
        path_2.lineTo(21, 30)
        block_2 = self.createTrackBlock(path_2, "Block 2")
        self.greenTrack.addItem(block_2)
        self.blocks[2] = block_2

        path_3 = QPainterPath()
        path_3.moveTo(26, 38)
        path_3.cubicTo(26, 38, 28, 41, 38, 47)
        block_3 = self.createTrackBlock(path_3, "Block 3")
        self.greenTrack.addItem(block_3)
        self.blocks[3] = block_3

        path_4 = QPainterPath()
        path_4.moveTo(46, 52)
        path_4.cubicTo(46, 52, 52, 55, 59, 57)
        block_4 = self.createTrackBlock(path_4, "Block 4")
        self.greenTrack.addItem(block_4)
        self.blocks[4] = block_4

        path_5 = QPainterPath()
        path_5.moveTo(68, 60)
        path_5.cubicTo(68, 60, 73, 61, 82, 61)
        block_5 = self.createTrackBlock(path_5, "Block 5")
        self.greenTrack.addItem(block_5)
        self.blocks[5] = block_5

        path_6 = QPainterPath()
        path_6.moveTo(92, 61)
        path_6.cubicTo(92, 61, 103, 60, 104, 58)
        block_6 = self.createTrackBlock(path_6, "Block 6")
        self.greenTrack.addItem(block_6)
        self.blocks[6] = block_6

        path_7 = QPainterPath()
        path_7.moveTo(109, 50)
        path_7.cubicTo(109, 50, 112, 45, 112, 39)
        block_7 = self.createTrackBlock(path_7, "Block 7")
        self.greenTrack.addItem(block_7)
        self.blocks[7] = block_7

        path_8 = QPainterPath()
        path_8.moveTo(112, 29)
        path_8.cubicTo(112, 29, 112, 25, 102, 18)
        block_8 = self.createTrackBlock(path_8, "Block 8")
        self.greenTrack.addItem(block_8)
        self.blocks[8] = block_8

        path_9 = QPainterPath()
        path_9.moveTo(94, 14)
        path_9.cubicTo(94, 14, 86, 11, 81, 10)
        block_9 = self.createTrackBlock(path_9, "Block 9")
        self.greenTrack.addItem(block_9)
        self.blocks[9] = block_9

        path_10 = QPainterPath()
        path_10.moveTo(72, 8)
        path_10.cubicTo(72, 8, 58, 5, 57, 5)
        block_10 = self.createTrackBlock(path_10, "Block 10")
        self.greenTrack.addItem(block_10)
        self.blocks[10] = block_10

        path_11 = QPainterPath()
        path_11.moveTo(47, 4)
        path_11.cubicTo(47, 4, 35, 3, 33, 3)
        block_11 = self.createTrackBlock(path_11, "Block 11")
        self.greenTrack.addItem(block_11)
        self.blocks[11] = block_11

        path_12 = QPainterPath()
        path_12.moveTo(23, 2)
        path_12.cubicTo(23, 2, 13, 1, 10, 1)
        block_12 = self.createTrackBlock(path_12, "Block 12")
        self.greenTrack.addItem(block_12)
        self.blocks[12] = block_12

        path_13 = QPainterPath()
        path_13.moveTo(-10, 0)
        path_13.lineTo(-25, 0)
        block_13 = self.createTrackBlock(path_13, "Block 13")
        self.greenTrack.addItem(block_13)
        self.blocks[13] = block_13

        path_14 = QPainterPath()
        path_14.moveTo(-35, 0)
        path_14.lineTo(-50, 0)
        block_14 = self.createTrackBlock(path_14, "Block 14")
        self.greenTrack.addItem(block_14)
        self.blocks[14] = block_14

        path_15 = QPainterPath()
        path_15.moveTo(-60, 0)
        path_15.lineTo(-75, 0)
        block_15 = self.createTrackBlock(path_15, "Block 15")
        self.greenTrack.addItem(block_15)
        self.blocks[15] = block_15

        path_16 = QPainterPath()
        path_16.moveTo(-85, 0)
        path_16.lineTo(-100, 0)
        block_16 = self.createTrackBlock(path_16, "Block 16")
        self.greenTrack.addItem(block_16)
        self.blocks[16] = block_16

        path_17 = QPainterPath()
        path_17.moveTo(-110, 0)
        path_17.quadTo(-115, 0, -125, 5)
        block_17 = self.createTrackBlock(path_17, "Block 17")
        self.greenTrack.addItem(block_17)
        self.blocks[17] = block_17

        path_18 = QPainterPath()
        path_18.moveTo(-133, 9)
        path_18.quadTo(-141, 14, -145, 19)
        block_18 = self.createTrackBlock(path_18, "Block 18")
        self.greenTrack.addItem(block_18)
        self.blocks[18] = block_18

        path_19 = QPainterPath()
        path_19.moveTo(-151, 27)
        path_19.quadTo(-156, 33, -159, 40)
        block_19 = self.createTrackBlock(path_19, "Block 19")
        self.greenTrack.addItem(block_19)
        self.blocks[19] = block_19

        path_20 = QPainterPath()
        path_20.moveTo(-163, 49)
        path_20.cubicTo(-166, 55, -167, 58, -167, 63)
        block_20 = self.createTrackBlock(path_20, "Block 20")
        self.greenTrack.addItem(block_20)
        self.blocks[20] = block_20

        path_21 = QPainterPath()
        path_21.moveTo(-167, 73)
        path_21.lineTo(-167, 78)
        block_21 = self.createTrackBlock(path_21, "Block 21")
        self.greenTrack.addItem(block_21)
        self.blocks[21] = block_21

        path_22 = QPainterPath()
        path_22.moveTo(-167, 88)
        path_22.lineTo(-167, 93)
        block_22 = self.createTrackBlock(path_22, "Block 22")
        self.greenTrack.addItem(block_22)
        self.blocks[22] = block_22

        path_23 = QPainterPath()
        path_23.moveTo(-167, 103)
        path_23.lineTo(-167, 108)
        block_23 = self.createTrackBlock(path_23, "Block 23")
        self.greenTrack.addItem(block_23)
        self.blocks[23] = block_23

        path_24 = QPainterPath()
        path_24.moveTo(-167, 118)
        path_24.lineTo(-167, 123)
        block_24 = self.createTrackBlock(path_24, "Block 24")
        self.greenTrack.addItem(block_24)
        self.blocks[24] = block_24

        path_25 = QPainterPath()
        path_25.moveTo(-167, 133)
        path_25.lineTo(-167, 138)
        block_25 = self.createTrackBlock(path_25, "Block 25")
        self.greenTrack.addItem(block_25)
        self.blocks[25] = block_25

        path_26 = QPainterPath()
        path_26.moveTo(-167, 148)
        path_26.lineTo(-167, 153)
        block_26 = self.createTrackBlock(path_26, "Block 26")
        self.greenTrack.addItem(block_26)
        self.blocks[26] = block_26

        path_27 = QPainterPath()
        path_27.moveTo(-167, 163)
        path_27.lineTo(-167, 168)
        block_27 = self.createTrackBlock(path_27, "Block 27")
        self.greenTrack.addItem(block_27)
        self.blocks[27] = block_27

        path_28 = QPainterPath()
        path_28.moveTo(-167, 178)
        path_28.lineTo(-167, 183)
        block_28 = self.createTrackBlock(path_28, "Block 28")
        self.greenTrack.addItem(block_28)
        self.blocks[28] = block_28

        path_29 = QPainterPath()
        path_29.moveTo(-167, 193)
        path_29.lineTo(-167, 198)
        block_29 = self.createTrackBlock(path_29, "Block 29")
        self.greenTrack.addItem(block_29)
        self.blocks[29] = block_29

        path_30 = QPainterPath()
        path_30.moveTo(-167, 208)
        path_30.lineTo(-167, 213)
        block_30 = self.createTrackBlock(path_30, "Block 30")
        self.greenTrack.addItem(block_30)
        self.blocks[30] = block_30

        path_31 = QPainterPath()
        path_31.moveTo(-167, 223)
        path_31.lineTo(-167, 228)
        block_31 = self.createTrackBlock(path_31, "Block 31")
        self.greenTrack.addItem(block_31)
        self.blocks[31] = block_31

        path_32 = QPainterPath()
        path_32.moveTo(-167, 238)
        path_32.lineTo(-167, 243)
        block_32 = self.createTrackBlock(path_32, "Block 32")
        self.greenTrack.addItem(block_32)
        self.blocks[32] = block_32

        path_33 = QPainterPath()
        path_33.moveTo(-167, 253)
        path_33.quadTo(-167, 255, -166, 258)
        block_33 = self.createTrackBlock(path_33, "Block 33")
        self.greenTrack.addItem(block_33)
        self.blocks[33] = block_33

        path_34 = QPainterPath()
        path_34.moveTo(-162, 266)
        path_34.quadTo(-161, 268, -159, 270)
        block_34 = self.createTrackBlock(path_34, "Block 34")
        self.greenTrack.addItem(block_34)
        self.blocks[34] = block_34

        path_35 = QPainterPath()
        path_35.moveTo(-152, 277)
        path_35.quadTo(-151, 278, -147, 278)
        block_35 = self.createTrackBlock(path_35, "Block 35")
        self.greenTrack.addItem(block_35)
        self.blocks[35] = block_35

        path_36 = QPainterPath()
        path_36.moveTo(-137, 278)
        path_36.lineTo(-135, 278)
        block_36 = self.createTrackBlock(path_36, "Block 36")
        self.greenTrack.addItem(block_36)
        self.blocks[36] = block_36

        path_37 = QPainterPath()
        path_37.moveTo(-125, 278)
        path_37.lineTo(-124, 278)
        block_37 = self.createTrackBlock(path_37, "Block 37")
        self.greenTrack.addItem(block_37)
        self.blocks[37] = block_37

        path_38 = QPainterPath()
        path_38.moveTo(-114, 278)
        path_38.lineTo(-113, 278)
        block_38 = self.createTrackBlock(path_38, "Block 38")
        self.greenTrack.addItem(block_38)
        self.blocks[38] = block_38

        path_39 = QPainterPath()
        path_39.moveTo(-103, 278)
        path_39.lineTo(-102, 278)
        block_39 = self.createTrackBlock(path_39, "Block 39")
        self.greenTrack.addItem(block_39)
        self.blocks[39] = block_39

        path_40 = QPainterPath()
        path_40.moveTo(-92, 278)
        path_40.lineTo(-91, 278)
        block_40 = self.createTrackBlock(path_40, "Block 40")
        self.greenTrack.addItem(block_40)
        self.blocks[40] = block_40

        path_41 = QPainterPath()
        path_41.moveTo(-81, 278)
        path_41.lineTo(-80, 278)
        block_41 = self.createTrackBlock(path_41, "Block 41")
        self.greenTrack.addItem(block_41)
        self.blocks[41] = block_41

        path_42 = QPainterPath()
        path_42.moveTo(-70, 278)
        path_42.lineTo(-69, 278)
        block_42 = self.createTrackBlock(path_42, "Block 42")
        self.greenTrack.addItem(block_42)
        self.blocks[42] = block_42

        path_43 = QPainterPath()
        path_43.moveTo(-59, 278)
        path_43.lineTo(-58, 278)
        block_43 = self.createTrackBlock(path_43, "Block 43")
        self.greenTrack.addItem(block_43)
        self.blocks[43] = block_43

        path_44 = QPainterPath()
        path_44.moveTo(-48, 278)
        path_44.lineTo(-47, 278)
        block_44 = self.createTrackBlock(path_44, "Block 44")
        self.greenTrack.addItem(block_44)
        self.blocks[44] = block_44

        path_45 = QPainterPath()
        path_45.moveTo(-37, 278)
        path_45.lineTo(-36, 278)
        block_45 = self.createTrackBlock(path_45, "Block 45")
        self.greenTrack.addItem(block_45)
        self.blocks[45] = block_45

        path_46 = QPainterPath()
        path_46.moveTo(-26, 278)
        path_46.lineTo(-25, 278)
        block_46 = self.createTrackBlock(path_46, "Block 46")
        self.greenTrack.addItem(block_46)
        self.blocks[46] = block_46

        path_47 = QPainterPath()
        path_47.moveTo(-15, 278)
        path_47.lineTo(-14, 278)
        block_47 = self.createTrackBlock(path_47, "Block 47")
        self.greenTrack.addItem(block_47)
        self.blocks[47] = block_47

        path_48 = QPainterPath()
        path_48.moveTo(-4, 278)
        path_48.lineTo(-3, 278)
        block_48 = self.createTrackBlock(path_48, "Block 48")
        self.greenTrack.addItem(block_48)
        self.blocks[48] = block_48

        path_49 = QPainterPath()
        path_49.moveTo(7, 278)
        path_49.lineTo(8, 278)
        block_49 = self.createTrackBlock(path_49, "Block 49")
        self.greenTrack.addItem(block_49)
        self.blocks[49] = block_49

        path_50 = QPainterPath()
        path_50.moveTo(18, 278)
        path_50.lineTo(19, 278)
        block_50 = self.createTrackBlock(path_50, "Block 50")
        self.greenTrack.addItem(block_50)
        self.blocks[50] = block_50

        path_51 = QPainterPath()
        path_51.moveTo(29, 278)
        path_51.lineTo(30, 278)
        block_51 = self.createTrackBlock(path_51, "Block 51")
        self.greenTrack.addItem(block_51)
        self.blocks[51] = block_51

        path_52 = QPainterPath()
        path_52.moveTo(40, 278)
        path_52.lineTo(41, 278)
        block_52 = self.createTrackBlock(path_52, "Block 52")
        self.greenTrack.addItem(block_52)
        self.blocks[52] = block_52

        path_53 = QPainterPath()
        path_53.moveTo(51, 278)
        path_53.lineTo(52, 278)
        block_53 = self.createTrackBlock(path_53, "Block 53")
        self.greenTrack.addItem(block_53)
        self.blocks[53] = block_53

        path_54 = QPainterPath()
        path_54.moveTo(62, 278)
        path_54.lineTo(63, 278)
        block_54 = self.createTrackBlock(path_54, "Block 54")
        self.greenTrack.addItem(block_54)
        self.blocks[54] = block_54

        path_55 = QPainterPath()
        path_55.moveTo(73, 278)
        path_55.lineTo(74, 278)
        block_55 = self.createTrackBlock(path_55, "Block 55")
        self.greenTrack.addItem(block_55)
        self.blocks[55] = block_55

        path_56 = QPainterPath()
        path_56.moveTo(84, 278)
        path_56.lineTo(85, 278)
        block_56 = self.createTrackBlock(path_56, "Block 56")
        self.greenTrack.addItem(block_56)
        self.blocks[56] = block_56

        path_57 = QPainterPath()
        path_57.moveTo(95, 278)
        path_57.lineTo(96, 278)
        block_57 = self.createTrackBlock(path_57, "Block 57")
        self.greenTrack.addItem(block_57)
        self.blocks[57] = block_57

        path_58 = QPainterPath()
        path_58.moveTo(106, 278)
        path_58.quadTo(107, 278, 111, 279)
        block_58 = self.createTrackBlock(path_58, "Block 58")
        self.greenTrack.addItem(block_58)
        self.blocks[58] = block_58

        path_59 = QPainterPath()
        path_59.moveTo(120, 283)
        path_59.quadTo(125, 285, 128, 287)
        block_59 = self.createTrackBlock(path_59, "Block 59")
        self.greenTrack.addItem(block_59)
        self.blocks[59] = block_59

        path_60 = QPainterPath()
        path_60.moveTo(136, 293)
        path_60.quadTo(142, 297, 143, 298)
        block_60 = self.createTrackBlock(path_60, "Block 60")
        self.greenTrack.addItem(block_60)
        self.blocks[60] = block_60

        path_61 = QPainterPath()
        path_61.moveTo(150, 305)
        path_61.quadTo(156, 312, 157, 314)
        block_61 = self.createTrackBlock(path_61, "Block 61")
        self.greenTrack.addItem(block_61)
        self.blocks[61] = block_61

        path_62 = QPainterPath()
        path_62.moveTo(161, 322)
        path_62.cubicTo(162, 324, 163, 328, 163, 330)
        block_62 = self.createTrackBlock(path_62, "Block 62")
        self.greenTrack.addItem(block_62)
        self.blocks[62] = block_62

        path_63 = QPainterPath()
        path_63.moveTo(163, 340)
        path_63.lineTo(163, 350)
        block_63 = self.createTrackBlock(path_63, "Block 63")
        self.greenTrack.addItem(block_63)
        self.blocks[63] = block_63

        path_64 = QPainterPath()
        path_64.moveTo(163, 360)
        path_64.lineTo(163, 370)
        block_64 = self.createTrackBlock(path_64, "Block 64")
        self.greenTrack.addItem(block_64)
        self.blocks[64] = block_64

        path_65 = QPainterPath()
        path_65.moveTo(163, 380)
        path_65.lineTo(163, 400)
        block_65 = self.createTrackBlock(path_65, "Block 65")
        self.greenTrack.addItem(block_65)
        self.blocks[65] = block_65

        path_66 = QPainterPath()
        path_66.moveTo(163, 410)
        path_66.lineTo(163, 430)
        block_66 = self.createTrackBlock(path_66, "Block 66")
        self.greenTrack.addItem(block_66)
        self.blocks[66] = block_66

        path_67 = QPainterPath()
        path_67.moveTo(163, 440)
        path_67.lineTo(163, 450)
        block_67 = self.createTrackBlock(path_67, "Block 67")
        self.greenTrack.addItem(block_67)
        self.blocks[67] = block_67

        path_68 = QPainterPath()
        path_68.moveTo(163, 460)
        path_68.lineTo(163, 470)
        block_68 = self.createTrackBlock(path_68, "Block 68")
        self.greenTrack.addItem(block_68)
        self.blocks[68] = block_68

        path_69 = QPainterPath()
        path_69.moveTo(163, 480)
        path_69.quadTo(163, 486, 162, 491)
        block_69 = self.createTrackBlock(path_69, "Block 69")
        self.greenTrack.addItem(block_69)
        self.blocks[69] = block_69

        path_70 = QPainterPath()
        path_70.moveTo(160, 500)
        path_70.quadTo(159, 505, 157, 510)
        block_70 = self.createTrackBlock(path_70, "Block 70")
        self.greenTrack.addItem(block_70)
        self.blocks[70] = block_70

        path_71 = QPainterPath()
        path_71.moveTo(153, 519)
        path_71.quadTo(151, 524, 148, 529)
        block_71 = self.createTrackBlock(path_71, "Block 71")
        self.greenTrack.addItem(block_71)
        self.blocks[71] = block_71

        path_72 = QPainterPath()
        path_72.moveTo(143, 537)
        path_72.quadTo(139, 543, 137, 545)
        block_72 = self.createTrackBlock(path_72, "Block 72")
        self.greenTrack.addItem(block_72)
        self.blocks[72] = block_72

        path_73 = QPainterPath()
        path_73.moveTo(130, 551)
        path_73.cubicTo(126, 554, 121, 556, 120, 556)
        block_73 = self.createTrackBlock(path_73, "Block 73")
        self.greenTrack.addItem(block_73)
        self.blocks[73] = block_73

        path_74 = QPainterPath()
        path_74.moveTo(110, 556)
        path_74.lineTo(90, 556)
        block_74 = self.createTrackBlock(path_74, "Block 74")
        self.greenTrack.addItem(block_74)
        self.blocks[74] = block_74

        path_75 = QPainterPath()
        path_75.moveTo(80, 556)
        path_75.lineTo(60, 556)
        block_75 = self.createTrackBlock(path_75, "Block 75")
        self.greenTrack.addItem(block_75)
        self.blocks[75] = block_75

        path_76 = QPainterPath()
        path_76.moveTo(50, 556)
        path_76.lineTo(30, 556)
        block_76 = self.createTrackBlock(path_76, "Block 76")
        self.greenTrack.addItem(block_76)
        self.blocks[76] = block_76

        path_77 = QPainterPath()
        path_77.moveTo(20, 556)
        path_77.lineTo(12, 556)
        block_77 = self.createTrackBlock(path_77, "Block 77")
        self.greenTrack.addItem(block_77)
        self.blocks[77] = block_77

        path_78 = QPainterPath()
        path_78.moveTo(2, 556)
        path_78.lineTo(-6, 556)
        block_78 = self.createTrackBlock(path_78, "Block 78")
        self.greenTrack.addItem(block_78)
        self.blocks[78] = block_78

        path_79 = QPainterPath()
        path_79.moveTo(-16, 556)
        path_79.lineTo(-24, 556)
        block_79 = self.createTrackBlock(path_79, "Block 79")
        self.greenTrack.addItem(block_79)
        self.blocks[79] = block_79

        path_80 = QPainterPath()
        path_80.moveTo(-34, 556)
        path_80.lineTo(-42, 556)
        block_80 = self.createTrackBlock(path_80, "Block 80")
        self.greenTrack.addItem(block_80)
        self.blocks[80] = block_80

        path_81 = QPainterPath()
        path_81.moveTo(-52, 556)
        path_81.lineTo(-60, 556)
        block_81 = self.createTrackBlock(path_81, "Block 81")
        self.greenTrack.addItem(block_81)
        self.blocks[81] = block_81

        path_82 = QPainterPath()
        path_82.moveTo(-70, 556)
        path_82.lineTo(-78, 556)
        block_82 = self.createTrackBlock(path_82, "Block 82")
        self.greenTrack.addItem(block_82)
        self.blocks[82] = block_82

        path_83 = QPainterPath()
        path_83.moveTo(-88, 556)
        path_83.lineTo(-96, 556)
        block_83 = self.createTrackBlock(path_83, "Block 83")
        self.greenTrack.addItem(block_83)
        self.blocks[83] = block_83

        path_84 = QPainterPath()
        path_84.moveTo(-106, 556)
        path_84.lineTo(-114, 556)
        block_84 = self.createTrackBlock(path_84, "Block 84")
        self.greenTrack.addItem(block_84)
        self.blocks[84] = block_84

        path_85 = QPainterPath()
        path_85.moveTo(-124, 556)
        path_85.lineTo(-132, 556)
        block_85 = self.createTrackBlock(path_85, "Block 85")
        self.greenTrack.addItem(block_85)
        self.blocks[85] = block_85

        path_86 = QPainterPath()
        path_86.moveTo(-142, 556)
        path_86.lineTo(-149, 556)
        block_86 = self.createTrackBlock(path_86, "Block 86")
        self.greenTrack.addItem(block_86)
        self.blocks[86] = block_86

        path_87 = QPainterPath()
        path_87.moveTo(-159, 556)
        path_87.lineTo(-163, 556)
        block_87 = self.createTrackBlock(path_87, "Block 87")
        self.greenTrack.addItem(block_87)
        self.blocks[87] = block_87

        path_88 = QPainterPath()
        path_88.moveTo(-173, 556)
        path_88.lineTo(-180, 556)
        block_88 = self.createTrackBlock(path_88, "Block 88")
        self.greenTrack.addItem(block_88)
        self.blocks[88] = block_88

        path_89 = QPainterPath()
        path_89.moveTo(-190, 556)
        path_89.quadTo(-196, 556, -198, 555)
        block_89 = self.createTrackBlock(path_89, "Block 89")
        self.greenTrack.addItem(block_89)
        self.blocks[89] = block_89

        path_90 = QPainterPath()
        path_90.moveTo(-206, 551)
        path_90.quadTo(-212, 547, -213, 546)
        block_90 = self.createTrackBlock(path_90, "Block 90")
        self.greenTrack.addItem(block_90)
        self.blocks[90] = block_90

        path_91 = QPainterPath()
        path_91.moveTo(-220, 539)
        path_91.quadTo(-225, 533, -226, 531)
        block_91 = self.createTrackBlock(path_91, "Block 91")
        self.greenTrack.addItem(block_91)
        self.blocks[91] = block_91

        path_92 = QPainterPath()
        path_92.moveTo(-230, 523)
        path_92.quadTo(-232, 519, -233, 512)
        block_92 = self.createTrackBlock(path_92, "Block 92")
        self.greenTrack.addItem(block_92)
        self.blocks[92] = block_92

        path_93 = QPainterPath()
        path_93.moveTo(-234, 503)
        path_93.quadTo(-234, 499, -231, 491)
        block_93 = self.createTrackBlock(path_93, "Block 93")
        self.greenTrack.addItem(block_93)
        self.blocks[93] = block_93

        path_94 = QPainterPath()
        path_94.moveTo(-227, 482)
        path_94.quadTo(-224, 476, -218, 473)
        block_94 = self.createTrackBlock(path_94, "Block 94")
        self.greenTrack.addItem(block_94)
        self.blocks[94] = block_94

        path_95 = QPainterPath()
        path_95.moveTo(-210, 469)
        path_95.quadTo(-203, 466, -196, 469)
        block_95 = self.createTrackBlock(path_95, "Block 95")
        self.greenTrack.addItem(block_95)
        self.blocks[95] = block_95

        path_96 = QPainterPath()
        path_96.moveTo(-188, 473)
        path_96.quadTo(-182, 476, -179, 482)
        block_96 = self.createTrackBlock(path_96, "Block 96")
        self.greenTrack.addItem(block_96)
        self.blocks[96] = block_96

        path_97 = QPainterPath()
        path_97.moveTo(-175, 491)
        path_97.quadTo(-172, 499, -172, 503)
        block_97 = self.createTrackBlock(path_97, "Block 97")
        self.greenTrack.addItem(block_97)
        self.blocks[97] = block_97

        path_98 = QPainterPath()
        path_98.moveTo(-172, 512)
        path_98.quadTo(-171, 519, -168, 523)
        block_98 = self.createTrackBlock(path_98, "Block 98")
        self.greenTrack.addItem(block_98)
        self.blocks[98] = block_98

        path_99 = QPainterPath()
        path_99.moveTo(-163, 530)
        path_99.quadTo(-157, 537, -155, 539)
        block_99 = self.createTrackBlock(path_99, "Block 99")
        self.greenTrack.addItem(block_99)
        self.blocks[99] = block_99

        path_100 = QPainterPath()
        path_100.moveTo(-148, 546)
        path_100.quadTo(-147, 547, -142, 551)
        block_100 = self.createTrackBlock(path_100, "Block 100")
        self.greenTrack.addItem(block_100)
        self.blocks[100] = block_100

        path_101 = QPainterPath()
        path_101.moveTo(24, 546)
        path_101.cubicTo(24, 545, 34, 530, 35, 530)
        block_101 = self.createTrackBlock(path_101, "Block 101")
        self.greenTrack.addItem(block_101)
        self.blocks[101] = block_101

        path_102 = QPainterPath()
        path_102.moveTo(45, 530)
        path_102.lineTo(46, 530)
        block_102 = self.createTrackBlock(path_102, "Block 102")
        self.greenTrack.addItem(block_102)
        self.blocks[102] = block_102

        path_103 = QPainterPath()
        path_103.moveTo(56, 530)
        path_103.lineTo(57, 530)
        block_103 = self.createTrackBlock(path_103, "Block 103")
        self.greenTrack.addItem(block_103)
        self.blocks[103] = block_103

        path_104 = QPainterPath()
        path_104.moveTo(67, 530)
        path_104.lineTo(68, 530)
        block_104 = self.createTrackBlock(path_104, "Block 104")
        self.greenTrack.addItem(block_104)
        self.blocks[104] = block_104

        path_105 = QPainterPath()
        path_105.moveTo(88, 525)
        path_105.cubicTo(84, 528, 79, 530, 78, 530)
        block_105 = self.createTrackBlock(path_105, "Block 105")
        self.greenTrack.addItem(block_105)
        self.blocks[105] = block_105

        path_106 = QPainterPath()
        path_106.moveTo(101, 511)
        path_106.quadTo(97, 517, 95, 519)
        block_106 = self.createTrackBlock(path_106, "Block 106")
        self.greenTrack.addItem(block_106)
        self.blocks[106] = block_106

        path_107 = QPainterPath()
        path_107.moveTo(111, 493)
        path_107.quadTo(109, 498, 106, 503)
        block_107 = self.createTrackBlock(path_107, "Block 107")
        self.greenTrack.addItem(block_107)
        self.blocks[107] = block_107

        path_108 = QPainterPath()
        path_108.moveTo(118, 474)
        path_108.quadTo(117, 479, 115, 484)
        block_108 = self.createTrackBlock(path_108, "Block 108")
        self.greenTrack.addItem(block_108)
        self.blocks[108] = block_108

        path_109 = QPainterPath()
        path_109.moveTo(121, 455)
        path_109.quadTo(121, 460, 120, 464)
        block_109 = self.createTrackBlock(path_109, "Block 109")
        self.greenTrack.addItem(block_109)
        self.blocks[109] = block_109

        path_110 = QPainterPath()
        path_110.moveTo(121, 445)
        path_110.lineTo(121, 443)
        block_110 = self.createTrackBlock(path_110, "Block 110")
        self.greenTrack.addItem(block_110)
        self.blocks[110] = block_110

        path_111 = QPainterPath()
        path_111.moveTo(121, 433)
        path_111.lineTo(121, 431)
        block_111 = self.createTrackBlock(path_111, "Block 111")
        self.greenTrack.addItem(block_111)
        self.blocks[111] = block_111

        path_112 = QPainterPath()
        path_112.moveTo(121, 421)
        path_112.lineTo(121, 419)
        block_112 = self.createTrackBlock(path_112, "Block 112")
        self.greenTrack.addItem(block_112)
        self.blocks[112] = block_112

        path_113 = QPainterPath()
        path_113.moveTo(121, 409)
        path_113.lineTo(121, 407)
        block_113 = self.createTrackBlock(path_113, "Block 113")
        self.greenTrack.addItem(block_113)
        self.blocks[113] = block_113

        path_114 = QPainterPath()
        path_114.moveTo(121, 397)
        path_114.lineTo(121, 394)
        block_114 = self.createTrackBlock(path_114, "Block 114")
        self.greenTrack.addItem(block_114)
        self.blocks[114] = block_114

        path_115 = QPainterPath()
        path_115.moveTo(121, 384)
        path_115.lineTo(121, 382)
        block_115 = self.createTrackBlock(path_115, "Block 115")
        self.greenTrack.addItem(block_115)
        self.blocks[115] = block_115

        path_116 = QPainterPath()
        path_116.moveTo(121, 372)
        path_116.lineTo(121, 370)
        block_116 = self.createTrackBlock(path_116, "Block 116")
        self.greenTrack.addItem(block_116)
        self.blocks[116] = block_116

        path_117 = QPainterPath()
        path_117.moveTo(119, 352)
        path_117.cubicTo(120, 354, 121, 358, 121, 360)
        block_117 = self.createTrackBlock(path_117, "Block 117")
        self.greenTrack.addItem(block_117)
        self.blocks[117] = block_117

        path_118 = QPainterPath()
        path_118.moveTo(108, 335)
        path_118.quadTo(114, 342, 115, 344)
        block_118 = self.createTrackBlock(path_118, "Block 118")
        self.greenTrack.addItem(block_118)
        self.blocks[118] = block_118

        path_119 = QPainterPath()
        path_119.moveTo(94, 323)
        path_119.quadTo(100, 327, 101, 328)
        block_119 = self.createTrackBlock(path_119, "Block 119")
        self.greenTrack.addItem(block_119)
        self.blocks[119] = block_119

        path_120 = QPainterPath()
        path_120.moveTo(78, 313)
        path_120.quadTo(83, 315, 86, 317)
        block_120 = self.createTrackBlock(path_120, "Block 120")
        self.greenTrack.addItem(block_120)
        self.blocks[120] = block_120

        path_121 = QPainterPath()
        path_121.moveTo(64, 308)
        path_121.quadTo(65, 308, 69, 309)
        block_121 = self.createTrackBlock(path_121, "Block 121")
        self.greenTrack.addItem(block_121)
        self.blocks[121] = block_121

        path_122 = QPainterPath()
        path_122.moveTo(54, 308)
        path_122.lineTo(53, 308)
        block_122 = self.createTrackBlock(path_122, "Block 122")
        self.greenTrack.addItem(block_122)
        self.blocks[122] = block_122

        path_123 = QPainterPath()
        path_123.moveTo(43, 308)
        path_123.lineTo(42, 308)
        block_123 = self.createTrackBlock(path_123, "Block 123")
        self.greenTrack.addItem(block_123)
        self.blocks[123] = block_123

        path_124 = QPainterPath()
        path_124.moveTo(32, 308)
        path_124.lineTo(31, 308)
        block_124 = self.createTrackBlock(path_124, "Block 124")
        self.greenTrack.addItem(block_124)
        self.blocks[124] = block_124

        path_125 = QPainterPath()
        path_125.moveTo(21, 308)
        path_125.lineTo(20, 308)
        block_125 = self.createTrackBlock(path_125, "Block 125")
        self.greenTrack.addItem(block_125)
        self.blocks[125] = block_125

        path_126 = QPainterPath()
        path_126.moveTo(10, 308)
        path_126.lineTo(9, 308)
        block_126 = self.createTrackBlock(path_126, "Block 126")
        self.greenTrack.addItem(block_126)
        self.blocks[126] = block_126

        path_127 = QPainterPath()
        path_127.moveTo(-1, 308)
        path_127.lineTo(-2, 308)
        block_127 = self.createTrackBlock(path_127, "Block 127")
        self.greenTrack.addItem(block_127)
        self.blocks[127] = block_127

        path_128 = QPainterPath()
        path_128.moveTo(-12, 308)
        path_128.lineTo(-13, 308)
        block_128 = self.createTrackBlock(path_128, "Block 128")
        self.greenTrack.addItem(block_128)
        self.blocks[128] = block_128

        path_129 = QPainterPath()
        path_129.moveTo(-23, 308)
        path_129.lineTo(-24, 308)
        block_129 = self.createTrackBlock(path_129, "Block 129")
        self.greenTrack.addItem(block_129)
        self.blocks[129] = block_129

        path_130 = QPainterPath()
        path_130.moveTo(-34, 308)
        path_130.lineTo(-35, 308)
        block_130 = self.createTrackBlock(path_130, "Block 130")
        self.greenTrack.addItem(block_130)
        self.blocks[130] = block_130

        path_131 = QPainterPath()
        path_131.moveTo(-45, 308)
        path_131.lineTo(-46, 308)
        block_131 = self.createTrackBlock(path_131, "Block 131")
        self.greenTrack.addItem(block_131)
        self.blocks[131] = block_131

        path_132 = QPainterPath()
        path_132.moveTo(-56, 308)
        path_132.lineTo(-57, 308)
        block_132 = self.createTrackBlock(path_132, "Block 132")
        self.greenTrack.addItem(block_132)
        self.blocks[132] = block_132

        path_133 = QPainterPath()
        path_133.moveTo(-66, 308)
        path_133.lineTo(-67, 308)
        block_133 = self.createTrackBlock(path_133, "Block 133")
        self.greenTrack.addItem(block_133)
        self.blocks[133] = block_133

        path_134 = QPainterPath()
        path_134.moveTo(-77, 308)
        path_134.lineTo(-78, 308)
        block_134 = self.createTrackBlock(path_134, "Block 134")
        self.greenTrack.addItem(block_134)
        self.blocks[134] = block_134

        path_135 = QPainterPath()
        path_135.moveTo(-88, 308)
        path_135.lineTo(-89, 308)
        block_135 = self.createTrackBlock(path_135, "Block 135")
        self.greenTrack.addItem(block_135)
        self.blocks[135] = block_135

        path_136 = QPainterPath()
        path_136.moveTo(-99, 308)
        path_136.lineTo(-100, 308)
        block_136 = self.createTrackBlock(path_136, "Block 136")
        self.greenTrack.addItem(block_136)
        self.blocks[136] = block_136

        path_137 = QPainterPath()
        path_137.moveTo(-110, 308)
        path_137.lineTo(-111, 308)
        block_137 = self.createTrackBlock(path_137, "Block 137")
        self.greenTrack.addItem(block_137)
        self.blocks[137] = block_137

        path_138 = QPainterPath()
        path_138.moveTo(-121, 308)
        path_138.lineTo(-122, 308)
        block_138 = self.createTrackBlock(path_138, "Block 138")
        self.greenTrack.addItem(block_138)
        self.blocks[138] = block_138

        path_139 = QPainterPath()
        path_139.moveTo(-132, 308)
        path_139.lineTo(-133, 308)
        block_139 = self.createTrackBlock(path_139, "Block 139")
        self.greenTrack.addItem(block_139)
        self.blocks[139] = block_139

        path_140 = QPainterPath()
        path_140.moveTo(-143, 308)
        path_140.lineTo(-144, 308)
        block_140 = self.createTrackBlock(path_140, "Block 140")
        self.greenTrack.addItem(block_140)
        self.blocks[140] = block_140

        path_141 = QPainterPath()
        path_141.moveTo(-154, 308)
        path_141.lineTo(-155, 308)
        block_141 = self.createTrackBlock(path_141, "Block 141")
        self.greenTrack.addItem(block_141)
        self.blocks[141] = block_141

        path_142 = QPainterPath()
        path_142.moveTo(-165, 308)
        path_142.lineTo(-166, 308)
        block_142 = self.createTrackBlock(path_142, "Block 142")
        self.greenTrack.addItem(block_142)
        self.blocks[142] = block_142

        path_143 = QPainterPath()
        path_143.moveTo(-176, 308)
        path_143.lineTo(-177, 308)
        block_143 = self.createTrackBlock(path_143, "Block 143")
        self.greenTrack.addItem(block_143)
        self.blocks[143] = block_143

        path_144 = QPainterPath()
        path_144.moveTo(-192, 307)
        path_144.quadTo(-191, 308, -187, 308)
        block_144 = self.createTrackBlock(path_144, "Block 144")
        self.greenTrack.addItem(block_144)
        self.blocks[144] = block_144

        path_145 = QPainterPath()
        path_145.moveTo(-202, 296)
        path_145.quadTo(-201, 298, -199, 300)
        block_145 = self.createTrackBlock(path_145, "Block 145")
        self.greenTrack.addItem(block_145)
        self.blocks[145] = block_145

        path_146 = QPainterPath()
        path_146.moveTo(-207, 283)
        path_146.quadTo(-207, 285, -206, 288)
        block_146 = self.createTrackBlock(path_146, "Block 146")
        self.greenTrack.addItem(block_146)
        self.blocks[146] = block_146

        path_147 = QPainterPath()
        path_147.moveTo(-207, 273)
        path_147.lineTo(-207, 268)
        block_147 = self.createTrackBlock(path_147, "Block 147")
        self.greenTrack.addItem(block_147)
        self.blocks[147] = block_147

        path_148 = QPainterPath()
        path_148.moveTo(-207, 258)
        path_148.lineTo(-207, 240)
        block_148 = self.createTrackBlock(path_148, "Block 148")
        self.greenTrack.addItem(block_148)
        self.blocks[148] = block_148

        path_149 = QPainterPath()
        path_149.moveTo(-207, 230)
        path_149.lineTo(-207, 225)
        block_149 = self.createTrackBlock(path_149, "Block 149")
        self.greenTrack.addItem(block_149)
        self.blocks[149] = block_149

        path_150 = QPainterPath()
        path_150.moveTo(-207, 215)
        path_150.cubicTo(-207, 214, -179, 200, -177, 200)
        block_150 = self.createTrackBlock(path_150, "Block 150")
        self.greenTrack.addItem(block_150)
        self.blocks[150] = block_150

        #SWITCHES -> 0 by default, means continuation of number

        #CROSSING
        crossing = QPixmap("src/main/TrackModel/pngs/crossing.png")
        crossing = crossing.scaledToWidth(70)
        self.crossing = QGraphicsPixmapItem(crossing)
        self.crossing.setPos(-210, -20)
        self.greenTrack.addItem(self.crossing)

        #TRAFFIC LIGHTS
        lightPole1 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole1 = lightPole1.scaledToWidth(15)
        pole1 = QGraphicsPixmapItem(lightPole1)
        pole1.setPos(-5, 35)
        self.greenTrack.addItem(pole1)
        lightCircle1 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle1 = lightCircle1.scaledToWidth(17)
        circle1 = QGraphicsPixmapItem(lightCircle1)
        circle1.setPos(-6, 20)
        self.greenTrack.addItem(circle1)
        light1 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light1 = light1.scaledToWidth(35)
        self.signal1 = QGraphicsPixmapItem(light1)
        self.signal1.setPos(-15, 16)
        self.greenTrack.addItem(self.signal1)

        lightPole150 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole150 = lightPole150.scaledToWidth(15)
        pole150 = QGraphicsPixmapItem(lightPole150)
        pole150.setPos(-215, 180)
        self.greenTrack.addItem(pole150)
        lightCircle150 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle150 = lightCircle1.scaledToWidth(17)
        circle150 = QGraphicsPixmapItem(lightCircle150)
        circle150.setPos(-216, 165)
        self.greenTrack.addItem(circle150)
        light150 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light150 = light1.scaledToWidth(35)
        signal150 = QGraphicsPixmapItem(light150)
        signal150.setPos(-225, 161)
        self.greenTrack.addItem(signal150)

        lightPole0 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole0 = lightPole0.scaledToWidth(15)
        pole0 = QGraphicsPixmapItem(lightPole0)
        pole0.setPos(175, 310)
        self.greenTrack.addItem(pole0)
        lightCircle0 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle0 = lightCircle1.scaledToWidth(17)
        circle0 = QGraphicsPixmapItem(lightCircle0)
        circle0.setPos(174, 295)
        self.greenTrack.addItem(circle0)
        light0 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light0 = light1.scaledToWidth(35)
        signal0 = QGraphicsPixmapItem(light0)
        signal0.setPos(165, 291)
        self.greenTrack.addItem(signal0)

        lightPole76 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole76 = lightPole76.scaledToWidth(15)
        pole76 = QGraphicsPixmapItem(lightPole76)
        pole76.setPos(30, 580)
        self.greenTrack.addItem(pole76)
        lightCircle76 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle76 = lightCircle1.scaledToWidth(17)
        circle76 = QGraphicsPixmapItem(lightCircle76)
        circle76.setPos(29, 565)
        self.greenTrack.addItem(circle76)
        light76 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light76 = light1.scaledToWidth(35)
        signal76 = QGraphicsPixmapItem(light76)
        signal76.setPos(20, 561)
        self.greenTrack.addItem(signal76)

        lightPole100 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole100 = lightPole100.scaledToWidth(15)
        pole100 = QGraphicsPixmapItem(lightPole100)
        pole100.setPos(-142, 520)
        self.greenTrack.addItem(pole100)
        lightCircle100 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle100 = lightCircle1.scaledToWidth(17)
        circle100 = QGraphicsPixmapItem(lightCircle100)
        circle100.setPos(-143, 505)
        self.greenTrack.addItem(circle100)
        light100 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light100 = light1.scaledToWidth(35)
        signal100 = QGraphicsPixmapItem(light100)
        signal100.setPos(-152, 501)
        self.greenTrack.addItem(signal100)

    def drawRedLine(self):
        self.setScene(self.redTrack)

        path1 = QPainterPath()
        path1.moveTo(0, 0)
        path1.lineTo(20, 0)
        track_block1 = self.createTrackBlock(path1, "Block F")
        self.redTrack.addItem(track_block1)

        path2 = QPainterPath()
        path2.moveTo(-20, 20)
        path2.lineTo(-20, 160)
        track_block2 = self.createTrackBlock(path2, "Block H")
        self.redTrack.addItem(track_block2)

        path3 = QPainterPath()
        path3.moveTo(-10, 0)
        path3.cubicTo(-10, 0, -20, 0, -20, 10)
        track_block3 = self.createTrackBlock(path3, "Block G")
        self.redTrack.addItem(track_block3)

        path4 = QPainterPath()
        path4.moveTo(30, 0)
        path4.lineTo(50, 0)
        track_block4 = self.createTrackBlock(path4, "Block E")
        self.redTrack.addItem(track_block4)

        path5 = QPainterPath()
        path5.moveTo(60, 0)
        path5.cubicTo(60, 0, 80, 0, 80, -10)
        track_block5 = self.createTrackBlock(path5, "Block D")
        self.redTrack.addItem(track_block5)

        path6 = QPainterPath()
        path6.moveTo(80, -20)
        path6.cubicTo(80, -20, 80, -30, 70, -30)
        track_block6 = self.createTrackBlock(path6, "Block C")
        self.redTrack.addItem(track_block6)

        path7 = QPainterPath()
        path7.moveTo(60, -30)
        path7.cubicTo(60, -30, 50, -30, 50, -20)
        track_block7 = self.createTrackBlock(path7, "Block B")
        self.redTrack.addItem(track_block7)

        path8 = QPainterPath()
        path8.moveTo(48, -16)
        path8.cubicTo(48, -16, 40, -10, 20, -2)
        track_block8 = self.createTrackBlock(path8, "Block A")
        self.redTrack.addItem(track_block8)

        path9 = QPainterPath()
        path9.moveTo(-30, 30)
        path9.cubicTo(-30, 30, -40, 30, -40, 40)
        track_block9 = self.createTrackBlock(path9, "Block T")
        self.redTrack.addItem(track_block9)

        path10 = QPainterPath()
        path10.moveTo(-40, 50)
        path10.lineTo(-40, 60)
        track_block10 = self.createTrackBlock(path10, "Block S")
        self.redTrack.addItem(track_block10)

        path11 = QPainterPath()
        path11.moveTo(-40, 70)
        path11.cubicTo(-40, 70, -40, 80, -30, 80)
        track_block11 = self.createTrackBlock(path11, "Block R")
        self.redTrack.addItem(track_block11)

        path12 = QPainterPath()
        path12.moveTo(-30, 110)
        path12.cubicTo(-30, 110, -40, 110, -40, 120)
        track_block12 = self.createTrackBlock(path12, "Block Q")
        self.redTrack.addItem(track_block12)

        path13 = QPainterPath()
        path13.moveTo(-40, 130)
        path13.lineTo(-40, 140)
        track_block13 = self.createTrackBlock(path13, "Block P")
        self.redTrack.addItem(track_block13)

        path14 = QPainterPath()
        path14.moveTo(-40, 150)
        path14.cubicTo(-40, 150, -40, 160, -30, 160)
        track_block14 = self.createTrackBlock(path14, "Block O")
        self.redTrack.addItem(track_block14)

        path15 = QPainterPath()
        path15.moveTo(-20, 170)
        path15.cubicTo(-20, 170, -20, 190, -40, 190)
        track_block15 = self.createTrackBlock(path15, "Block I")
        self.redTrack.addItem(track_block15)

        path16 = QPainterPath()
        path16.moveTo(-50, 190)
        path16.lineTo(-80, 190)
        track_block16 = self.createTrackBlock(path16, "Block J")
        self.redTrack.addItem(track_block16)

        path17 = QPainterPath()
        path17.moveTo(-90, 190)
        path17.cubicTo(-90, 190, -110, 190, -110, 175)
        track_block17 = self.createTrackBlock(path17, "Block K")
        self.redTrack.addItem(track_block17)

        path18 = QPainterPath()
        path18.moveTo(-110, 165)
        path18.cubicTo(-110, 165, -110, 155, -100, 155)
        track_block18 = self.createTrackBlock(path18, "Block L")
        self.redTrack.addItem(track_block18)

        path19 = QPainterPath()
        path19.moveTo(-90, 155)
        path19.cubicTo(-90, 155, -85, 155, -85, 170)
        track_block19 = self.createTrackBlock(path19, "Block M")
        self.redTrack.addItem(track_block19)

        path20 = QPainterPath()
        path20.moveTo(-84, 175)
        path20.cubicTo(-84, 175, -83, 180, -70, 188)
        track_block20 = self.createTrackBlock(path20, "Block N")
        self.redTrack.addItem(track_block20)

    def createTrackBlock(self, path, number):
        track_block = TrackBlock(path, number)
        return track_block

    def showGreenLineLayout(self):
        self.setScene(self.greenTrack)

    def showRedLineLayout(self):
        self.setScene(self.redTrack)

    def change_color(self, on, off):
        print("works")
        if on == 999:
            on = 0
        onBlock = self.blocks.get(on)
        if onBlock:
            onBlock.toggle_occupancy(True)
        if off != 999:
            offBlock = self.blocks.get(off)
            if offBlock:
                offBlock.toggle_occupancy(False)


class TrackBlock(QGraphicsPathItem):
    def __init__(self, path, number):
        super().__init__(path)
        self.number = number
        self.original_pen = QPen(QColor(0, 0, 0))
        self.original_pen.setWidth(10)
        self.hover_pen = QPen(QColor(255, 255, 0))
        self.hover_pen.setWidth(10)
        self.occupied_pen = QPen(QColor(255, 0, 0))
        self.occupied_pen.setWidth(10)
        self.current_pen = None
        self.setPen(self.original_pen)
        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event):
        print(f"Clicked on {self.number}")
        # trackModeltoTrainModel.sendTest.emit(self.number)

    def hoverEnterEvent(self, event):
        self.current_pen = self.pen()
        self.setPen(self.hover_pen)

    def hoverLeaveEvent(self, event):
        if self.current_pen:
            self.setPen(self.current_pen)
        else:
            self.setPen(self.original_pen)

    def toggle_occupancy(self, occupied):
        if occupied:
            self.current_pen = self.occupied_pen
            self.setPen(self.occupied_pen)
        else:
            self.current_pen = self.original_pen
            self.setPen(self.original_pen)


class TrackModel:
    moduleName = "Track Model"
    simulationSpeed = 1.0
    selectedLine = "Red"
    temperature = 65
    allowableDirections = "EAST/WEST"
    blockTrackHeater = "OFF"
    failures = []
    maintenance = 0
    occupied = 0
    beacon = "---"
    ticketSales = 0
    waiting = 0
    signals = {}

    def __init__(self):
        self.block = TrackData()
        self.station = Station()
        self.load_data()

        trainModelToTrackModel.sendPolarity.connect(self.update_occupancy)
        # trackControllerToTrackModel.switchState.connect(self.update_switch_state)
        trackControllerToTrackModel.lightState.connect(self.update_light_state)
        trackControllerToTrackModel.crossingState.connect(self.update_crossing_state)

        self.setup_selection_window()

    def setup_selection_window(self):
        # app = QApplication(sys.argv) #Don't need for main.py
        self.mainWindow = QMainWindow()
        self.mainWindow.setGeometry(960, 35, 960, 1045)
        self.mainWindow.setWindowTitle(self.moduleName)
        self.mainWindow.setStyleSheet("background-color: white")
        # app.setWindowIcon(QIcon("src/main/TrackModel/pngs/MTA_logo.png"))

        # General layout
        self.set_clock()
        self.set_simulation_speed()
        # self.add_vline(mainWindow)
        # self.add_hline(mainWindow)
        self.add_header()
        self.add_mta_logo()
        # self.add_tabbar(mainWindow)
        self.add_module_name()
        self.add_testbench_button()

        # Map
        # self.add_line_panel(mainWindow)
        self.control_temperature()
        self.add_import_button()
        # The following are hidden initially and are shown upon an excel file import
        # self.display_file_path(mainWindow)
        # self.add_track_map(mainWindow)
        # self.add_map_zoom(mainWindow)
        # self.add_map_pngs(mainWindow)

        # self.add_block_info_display(mainWindow)
        # self.add_station_info(mainWindow)

        # Block Info Selection
        self.add_input_section()
        self.show_block_data()  # NEWWW
        self.add_failure_selection()  # NEWW
        # self.add_selectable_block_info(mainWindow)
        # self.add_change_failures_button(mainWindow)

        # NEW
        self.setup_content_widget()
        self.map_toggle()

        # Hide by default
        # self.mainWindow.show()
        # sys.exit(app.exec_())

    def load_data(self):
        # Preload track data
        self.redTrackData = self.block.read_track_data(
            "src\main\TrackModel\Track Layout & Vehicle Data vF2.xlsx", "Red Line"
        )
        self.greenTrackData = self.block.read_track_data(
            "src\main\TrackModel\Track Layout & Vehicle Data vF2.xlsx", "Green Line"
        )

    def add_header(self):
        headerBackground = QLabel(self.mainWindow)
        headerBackground.setGeometry(0, 0, 960, 80)
        headerBackground.setStyleSheet(f'background-color: {MTA_STYLING["darkBlue"]}')

        # Title
        windowWidth = self.mainWindow.width()
        labelWidth = 900
        titlePosition = int((windowWidth - labelWidth) / 2)

        titleLabel = QLabel(
            "Pittsburgh Metropolitan Transportation Authority", self.mainWindow
        )
        titleLabel.setGeometry(titlePosition, 20, labelWidth, 50)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["titleFontSize"])
        titleLabel.setStyleSheet(
            f'color: white; background-color: {MTA_STYLING["darkBlue"]}'
        )
        titleLabel.setFont(titleFont)

    def add_mta_logo(self):
        mtaPng = QPixmap("src/main/TrackModel/pngs/mta_logo.png")
        mtaPng = mtaPng.scaledToWidth(70)
        mtaLogo = QLabel(self.mainWindow)
        mtaLogo.setPixmap(mtaPng)
        mtaLogo.setGeometry(0, 0, mtaPng.width(), mtaPng.height())
        mtaLogo.setStyleSheet(f'background-color: {MTA_STYLING["darkBlue"]}')

    def add_module_name(self):
        moduleLabel = QLabel(self.moduleName, self.mainWindow)
        moduleFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])
        moduleLabel.setFont(moduleFont)
        moduleLabel.setGeometry(30, 80, 150, 60)
        moduleLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

    def add_testbench_button(self):
        # icon
        gearPng = QPixmap("src/main/TrackModel/pngs/gear.svg")
        gearPng = gearPng.scaledToWidth(20, 20)
        testbenchIcon = QLabel(self.mainWindow)
        testbenchIcon.setPixmap(gearPng)
        testbenchIcon.setGeometry(40, 135, gearPng.width(), gearPng.height())

        # button
        testbenchButton = QPushButton("Test Bench", self.mainWindow)
        testbenchFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        testbenchButton.setFont(testbenchFont)
        testbenchButton.setGeometry(60, 130, 100, 30)
        testbenchButton.setStyleSheet(
            f'color: {MTA_STYLING["darkBlue"]}; border: 1px solid white'
        )

        testbenchButton.clicked.connect(self.show_testbench)

    def control_temperature(self):
        setTemperature = QLabel("Set Temperature:", self.mainWindow)
        setTemperatureFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"]
        )
        setTemperature.setFont(setTemperatureFont)
        setTemperature.setGeometry(330, 80, 210, 60)
        setTemperature.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        self.temperatureInput = QLineEdit(self.mainWindow)
        temperatureInputFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        self.temperatureInput.setFont(temperatureInputFont)
        self.temperatureInput.setGeometry(365, 130, 40, 30)
        self.temperatureInput.setAlignment(Qt.AlignCenter)
        self.temperatureInput.setPlaceholderText("65")
        self.temperatureInput.setStyleSheet(
            f'color: {MTA_STYLING["darkBlue"]}; border: 1px solid {MTA_STYLING["darkBlue"]};'
        )

        fahrenheitUnit = QLabel("°F", self.mainWindow)
        fahrenheitFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])
        fahrenheitUnit.setFont(fahrenheitFont)
        fahrenheitUnit.setGeometry(405, 130, 30, 30)
        fahrenheitUnit.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        setTemperatureButton = QPushButton("Set", self.mainWindow)
        setTemperatureButtonFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        setTemperatureButton.setFont(setTemperatureButtonFont)
        setTemperatureButton.setGeometry(440, 130, 60, 30)
        setTemperatureButton.setStyleSheet(
            f'background-color: {MTA_STYLING["darkBlue"]}; color: white'
        )
        setTemperatureButton.clicked.connect(self.set_temperature)

    def set_temperature(self):
        tempInput = self.temperatureInput.text()
        if tempInput != "":
            self.temperature = self.temperatureInput.text()
            # If temperature is greater than 45 degrees F, then track heater will remain OFF
            if int(tempInput) > 45:
                self.blockTrackHeater = "OFF"
            else:
                self.blockTrackHeater = "ON"
        self.set_trackheater()
        self.temperatureInput.setPlaceholderText(str(self.temperature))
        print(self.temperature)

    def set_clock(self):
        # system time input
        systemTimeFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])

        clockLabel = QLabel("System Time:", self.mainWindow)
        clockLabel.setFont(systemTimeFont)
        clockLabel.setGeometry(650, 80, 170, 60)
        clockLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        self.clock = QLabel("00:00:00", self.mainWindow)
        self.clock.setFont(systemTimeFont)
        self.clock.setGeometry(830, 80, 150, 60)
        self.clock.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        # Timer from CTC
        self.timer = QTimer(self.mainWindow)
        self.timer.start(1000)
        self.timer.timeout.connect(self.get_CTC_timing)

        self.sysTime = QDateTime.currentDateTime()
        self.sysTime.setTime(QTime(0, 0, 0))

    def get_CTC_timing(self):
        masterSignals.timingMultiplier.connect(self.update_clock)

    def update_clock(self, period):
        time_interval = period
        masterSignals.clockSignal.connect(self.sysTime.setTime)
        self.timer.setInterval(time_interval)

        self.clock.setText(self.sysTime.toString("HH:mm:ss"))
        self.speedText.setText("x" + format(1 / (time_interval / 1000), ".3f"))

    def set_simulation_speed(self):
        systemSpeedFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])

        systemSpeedLabel = QLabel("System Speed:", self.mainWindow)
        systemSpeedLabel.setFont(systemSpeedFont)
        systemSpeedLabel.setGeometry(700, 130, 150, 30)
        systemSpeedLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')
        self.speedText = QLabel("x1.0", self.mainWindow)
        self.speedText.setFont(systemSpeedFont)
        self.speedText.setGeometry(850, 130, 50, 30)
        self.speedText.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

    def setup_content_widget(self):
        mapWidget = QWidget(self.mainWindow)
        mapWidget.setGeometry(30, 300, 500, 700)
        mapWidget.setStyleSheet(f'border: 20px solid {MTA_STYLING["darkBlue"]}')
        self.trackView = TrackView(mapWidget)
        self.trackView.setGeometry(0, 0, mapWidget.width(), mapWidget.height())

    def map_toggle(self):
        selectLine = QLabel("Select Line:", self.mainWindow)
        selectLineFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])
        selectLine.setFont(selectLineFont)
        selectLine.setGeometry(210, 260, 135, 30)
        selectLine.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        buttonStyle = f'background-color: white; color: {MTA_STYLING["darkBlue"]}; border: 1px solid {MTA_STYLING["darkBlue"]}; border-radius: 10px;'

        self.greenLineButton = QPushButton("Green Line", self.mainWindow)
        greenLineButtonFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        self.greenLineButton.setFont(greenLineButtonFont)
        self.greenLineButton.setGeometry(350, 260, 90, 30)
        self.greenLineButton.setStyleSheet(buttonStyle)
        self.greenLineButton.clicked.connect(self.toggle_green_data)

        self.redLineButton = QPushButton("Red Line", self.mainWindow)
        redLineButtonFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        self.redLineButton.setFont(redLineButtonFont)
        self.redLineButton.setGeometry(440, 260, 90, 30)
        self.redLineButton.setStyleSheet(buttonStyle)
        self.redLineButton.clicked.connect(self.toggle_red_data)

        # Set Base Line to Red
        self.change_button_color(MTA_STYLING["green"])
        self.toggle_green_data()  ################

        # Connect button click events to change the background color when selected
        self.greenLineButton.clicked.connect(
            lambda: self.change_button_color(MTA_STYLING["green"])
        )
        self.redLineButton.clicked.connect(
            lambda: self.change_button_color(MTA_STYLING["red"])
        )

    def toggle_green_data(self):
        self.trackView.showGreenLineLayout()
        self.trackData = self.greenTrackData
        self.selectedLine = "Green"

    def toggle_red_data(self):
        self.trackView.showRedLineLayout()
        self.trackData = self.redTrackData
        self.selectedLine = "Red"

    def change_button_color(self, color):
        buttonStyle = f'background-color: white; color: {MTA_STYLING["darkBlue"]}; border: 1px solid {MTA_STYLING["darkBlue"]}; border-radius: 10px;'
        if color == MTA_STYLING["green"]:
            self.redLineButton.setStyleSheet(buttonStyle)
            self.greenLineButton.setStyleSheet(
                f"background-color: {color}; color: white; border: 1px solid {color}; border-radius: 10px;"
            )
        else:
            self.greenLineButton.setStyleSheet(buttonStyle)
            self.redLineButton.setStyleSheet(
                f"background-color: {color}; color: white; border: 1px solid {color}; border-radius: 10px;"
            )

    def update_occupancy(self, _, curBlock, prevBlock):
        self.trackView.change_color(curBlock, prevBlock)
    
    def update_light_state(self, line, _, blockNum, state):
        lightBlocks = [0, 1, 62, 76, 100, 150]
        if line == 1:
            if state == "Green":
                if blockNum in lightBlocks:
                    self.trackView.greenTrack.removeItem(self.signals[blockNum])
                    del self.signals[blockNum]
                    print(self.signals)
            elif state == "Red":
                redLight = QPixmap("src/main/TrackModel/pngs/red-light.png")
                redLight = redLight.scaledToWidth(35)
                signal = QGraphicsPixmapItem(redLight)
                self.signals[blockNum] = signal
                if blockNum == 0:
                    signal.setPos(165, 291)
                if blockNum == 1:
                    signal.setPos(-15, 16)
                if blockNum == 76:
                    signal.setPos(20, 561)
                if blockNum == 100:
                    signal.setPos(-152, 501)
                if blockNum == 150:   
                    signal.setPos(-225, 161)              
                self.trackView.greenTrack.addItem(signal)

    def update_crossing_state(self, line, _, __, state):
        if line == 1:
            if state == 0:
                self.trackView.greenTrack.removeItem(self.signals[19.1])
                self.trackView.greenTrack.removeItem(self.signals[19.2])
                del self.signals[19.1]
                del self.signals[19.2]
                print(self.signals)
            elif state == 1:
                redLight = QPixmap("src/main/TrackModel/pngs/red-light.png")
                redLight = redLight.scaledToWidth(20)
                crossing = QGraphicsPixmapItem(redLight)
                crossing2 = QGraphicsPixmapItem(redLight)
                self.signals[19.1] = crossing
                self.signals[19.2] = crossing2
                crossing.setPos(-194, 12)
                crossing2.setPos(-175, 12)
                self.trackView.greenTrack.addItem(crossing)
                self.trackView.greenTrack.addItem(crossing2)
                
    def add_import_button(self):
        importButton = QPushButton("Import Track Data", self.mainWindow)
        importButtonFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        importButton.setFont(importButtonFont)
        importButton.setGeometry(30, 260, 150, 30)
        importButton.setStyleSheet(
            f'background-color: {MTA_STYLING["darkBlue"]}; color: white'
        )
        # Need to call lambda as parent_window is not accessible otherwise
        importButton.clicked.connect(lambda: self.import_track_data())

    # def update_gui(self, filePath):
        # self.update_file_path(filePath)
        # self.select_line("Blue Line")  # Sets label to blue as that is the only line
        # self.trackMap.show()
        # self.zoomInButton.show()
        # self.zoomOutButton.show()
        # self.zoomInButton.setDisabled(True)
        # self.zoomOutButton.setDisabled(True)
        # self.changeFailuresButton.setEnabled(True)
        # self.goButton.setEnabled(True)
        # for checkbox in self.trackInfoCheckboxes.values():
        #     checkbox.setDisabled(False)

    def import_track_data(self):
        options = QFileDialog.Options() | QFileDialog.ReadOnly
        # Opens file explorer in new customized window
        filePath, _ = QFileDialog.getOpenFileName(
            self.mainWindow,
            "Import Track Data",
            "",
            "Excel Files (*.xlsx *.xls)",
            options=options,
        )

        if filePath:
            # Update Gui
            # self.update_gui(filePath)

            self.trackData = self.block.read_track_data(filePath, "Green Line")
            print(self.trackData)

    def add_input_section(self):
        entryFieldLabel = QLabel("Enter Block #:", self.mainWindow)
        entryFieldLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"]
        )
        entryFieldLabel.setFont(entryFieldLabelFont)
        entryFieldLabel.setGeometry(570, 260, 170, 30)
        entryFieldLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        self.entryField = QLineEdit(self.mainWindow)
        entryFieldFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        self.entryField.setFont(entryFieldFont)
        self.entryField.setGeometry(750, 260, 120, 30)
        self.entryField.setPlaceholderText("Enter Block #")
        self.entryField.setStyleSheet(
            f'color: {MTA_STYLING["darkBlue"]}; border: 1px solid {MTA_STYLING["darkBlue"]};'
        )

        self.goButton = QPushButton("Go", self.mainWindow)
        goButtonFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        self.goButton.setFont(goButtonFont)
        self.goButton.setGeometry(880, 260, 60, 30)
        self.goButton.setStyleSheet(
            f'background-color: {MTA_STYLING["darkBlue"]}; color: white'
        )
        # Connect the button to the update_block_info_display method
        # self.goButton.clicked.connect(self.update_block_info_display)
        self.goButton.clicked.connect(self.update_blockinfo)
        # self.goButton.setEnabled(True)  # The button is disabled initially

        self.errorLabel = QLabel("", self.mainWindow)
        errorLabelFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        self.errorLabel.setFont(errorLabelFont)
        self.errorLabel.setGeometry(750, 290, 210, 30)
        self.errorLabel.setStyleSheet(f'color: {MTA_STYLING["red"]}; font-size: 14px')

        blockInfoLabel = QLabel("Block Information:", self.mainWindow)
        blockInfoFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])
        blockInfoLabel.setFont(blockInfoFont)
        blockInfoLabel.setGeometry(645, 350, 220, 30)
        blockInfoLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

    def show_block_data(self):
        infoFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["labelFontSize"])
        infoStyle = f'color: {MTA_STYLING["darkBlue"]}'

        self.add_blockinfo_labels(infoStyle, infoFont)
        self.add_blockinfo(infoStyle, infoFont)

    def add_blockinfo_labels(self, style, font):
        lengthLabel = QLabel("Length:", self.mainWindow)
        lengthLabel.setFont(font)
        lengthLabel.setGeometry(600, 400, 140, 25)
        lengthLabel.setStyleSheet(style)

        speedLimitLabel = QLabel("Speed Limit:", self.mainWindow)
        speedLimitLabel.setFont(font)
        speedLimitLabel.setGeometry(600, 435, 140, 25)
        speedLimitLabel.setStyleSheet(style)

        gradeLabel = QLabel("Grade:", self.mainWindow)
        gradeLabel.setFont(font)
        gradeLabel.setGeometry(600, 470, 140, 25)
        gradeLabel.setStyleSheet(style)

        elevationLabel = QLabel("Elevation:", self.mainWindow)
        elevationLabel.setFont(font)
        elevationLabel.setGeometry(600, 505, 140, 25)
        elevationLabel.setStyleSheet(style)

        cumElevationLabel = QLabel("Cum. Elevation:", self.mainWindow)
        cumElevationLabel.setFont(font)
        cumElevationLabel.setGeometry(600, 540, 140, 25)
        cumElevationLabel.setStyleSheet(style)

        trackHeaterLabel = QLabel("Track Heater:", self.mainWindow)
        trackHeaterLabel.setFont(font)
        trackHeaterLabel.setGeometry(600, 575, 140, 25)
        trackHeaterLabel.setStyleSheet(style)

    def add_blockinfo(self, style, font):
        self.blockLengthLabel = QLabel(self.mainWindow)
        self.blockLengthLabel.setFont(font)
        self.blockLengthLabel.setStyleSheet(style)
        self.blockLengthLabel.setGeometry(750, 400, 110, 25)

        self.speedLimitLabel = QLabel(self.mainWindow)
        self.speedLimitLabel.setFont(font)
        self.speedLimitLabel.setStyleSheet(style)
        self.speedLimitLabel.setGeometry(750, 435, 110, 25)

        self.gradeLabel = QLabel(self.mainWindow)
        self.gradeLabel.setFont(font)
        self.gradeLabel.setStyleSheet(style)
        self.gradeLabel.setGeometry(750, 470, 110, 25)

        self.elevationLabel = QLabel(self.mainWindow)
        self.elevationLabel.setFont(font)
        self.elevationLabel.setStyleSheet(style)
        self.elevationLabel.setGeometry(750, 505, 110, 25)

        self.cumElevationLabel = QLabel(self.mainWindow)
        self.cumElevationLabel.setFont(font)
        self.cumElevationLabel.setStyleSheet(style)
        self.cumElevationLabel.setGeometry(750, 540, 110, 25)

        self.trackHeaterLabel = QLabel(self.mainWindow)
        self.trackHeaterLabel.setFont(font)
        self.trackHeaterLabel.setStyleSheet(style)
        self.trackHeaterLabel.setGeometry(750, 575, 110, 25)

        # Station Labels:
        self.stationNameLabel = QLabel(self.mainWindow)
        self.stationNameLabel.setFont(font)
        self.stationNameLabel.setStyleSheet(style)
        self.stationNameLabel.setGeometry(650, 800, 250, 25)

        self.ticketSalesLabel = QLabel(self.mainWindow)
        self.ticketSalesLabel.setFont(font)
        self.ticketSalesLabel.setStyleSheet(style)
        self.ticketSalesLabel.setText("Ticket Sales:")
        self.ticketSalesLabel.setGeometry(600, 830, 200, 25)
        self.ticketSalesLabel.hide()

        self.ticketSalesOutput = QLabel(self.mainWindow)
        self.ticketSalesOutput.setFont(font)
        self.ticketSalesOutput.setStyleSheet(style)
        self.ticketSalesOutput.setGeometry(850, 830, 200, 25)

        self.waitingLabel = QLabel(self.mainWindow)
        self.waitingLabel.setFont(font)
        self.waitingLabel.setStyleSheet(style)
        self.waitingLabel.setText("Passengers Waiting:")
        self.waitingLabel.setGeometry(600, 860, 200, 25)
        self.waitingLabel.hide()

        self.waitingOutput = QLabel(self.mainWindow)
        self.waitingOutput.setFont(font)
        self.waitingOutput.setStyleSheet(style)
        self.waitingOutput.setGeometry(850, 860, 200, 25)

        self.boardingLabel = QLabel(self.mainWindow)
        self.boardingLabel.setFont(font)
        self.boardingLabel.setStyleSheet(style)
        self.boardingLabel.setText("Passengers Boarding:")
        self.boardingLabel.setGeometry(600, 890, 200, 25)
        self.boardingLabel.hide()

        self.boardingOutput = QLabel(self.mainWindow)
        self.boardingOutput.setFont(font)
        self.boardingOutput.setStyleSheet(style)
        self.boardingOutput.setGeometry(850, 890, 200, 25)

        self.leavingLabel = QLabel(self.mainWindow)
        self.leavingLabel.setFont(font)
        self.leavingLabel.setStyleSheet(style)
        self.leavingLabel.setText("Passengers Disembarking:")
        self.leavingLabel.setGeometry(600, 920, 200, 25)
        self.leavingLabel.hide()

        self.leavingOutput = QLabel(self.mainWindow)
        self.leavingOutput.setFont(font)
        self.leavingOutput.setStyleSheet(style)
        self.leavingOutput.setGeometry(850, 920, 200, 25)

    def update_blockinfo(self):
        if self.entryField.text() == "":
            self.errorLabel.setText("Please enter a block number")
        elif self.entryField.text().isnumeric() == False:
            self.errorLabel.setText("Please enter a valid block number")
        elif ((int(self.entryField.text()) > 150 or int(self.entryField.text()) < 1) and self.selectedLine == "Green") or (int(self.entryField.text()) > 75 and self.selectedLine == "Red"):
            self.errorLabel.setText("Block Number does not exist")
        else:
            self.errorLabel.setText("") #Clear error message
            if self.selectedLine == "Green":
                self.trackData = self.block.get_data("Green")
            elif self.selectedLine == "Red":
                self.trackData = self.block.get_data("Red")
            self.parse_block_info()
            self.set_blocklength()
            self.set_speedlimit()
            self.set_grade()
            self.set_elevation()
            self.set_cumelevation()
            self.set_trackheater()
            self.show_station_data()          

    def set_blocklength(self):
        self.blockLengthLabel.setText(f"{self.blockLength} m")

    def set_speedlimit(self):
        self.speedLimitLabel.setText(f"{self.blockSpeedLimit} Km/Hr")

    def set_grade(self):
        self.gradeLabel.setText(f"{self.blockGrade} %")

    def set_elevation(self):
        self.elevationLabel.setText(f"{self.blockElevation} M")

    def set_cumelevation(self):
        # Accept only up to certain numbers after decimal
        self.cumElevationLabel.setText(f"{self.blockCumElevation} M")

    def set_trackheater(self):
        self.trackHeaterLabel.setText(f"{self.blockTrackHeater}")

    def parse_block_info(self):
        # Obtain block number provided
        blockNumber = self.entryField.text()
        # Update the block info based on the block selected
        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                self.blockLength = str(data["Block Length (m)"])
                self.blockSpeedLimit = str(data["Speed Limit (Km/Hr)"])
                self.blockGrade = str(data["Block Grade (%)"])
                self.blockElevation = str(data["ELEVATION (M)"])
                self.blockCumElevation = str(data["CUMALTIVE ELEVATION (M)"])

                self.failures = data[
                    "Failures"
                ]  # Store new blocks data in self.failures
                print(self.failures)
                self.check_failures()

    def show_station_data(self):
        blockNumber = self.entryField.text()

        if self.selectedLine == "Green":
            for data in self.trackData:
                if data["Block Number"] == int(blockNumber):
                    if type(data["Infrastructure"]) == str and "STATION" in data["Infrastructure"]:
                        stationName = str(data["Infrastructure"])
                        stationName = stationName.split(";")[0]
                        print(stationName)
                        # if stationName in data["Infrastructure"]:
                        #     print(data["Infrasctructure"])#Left off here
                        self.stationNameLabel.setText(f"{stationName}")
                        self.ticketSalesLabel.show()
                        self.waitingLabel.show()
                        self.boardingLabel.show()
                        self.leavingLabel.show()
                        self.ticketSalesOutput.setText(f"{data['Ticket Sales']}")
                        self.ticketSalesOutput.show()
                        self.waitingOutput.setText(f"{data['Passengers Waiting']}")
                        self.waitingOutput.show()
                        self.boardingOutput.setText(f"{data['Passengers Boarding']}")
                        self.boardingOutput.show()
                        self.leavingOutput.setText(f"{data['Passengers Disembarking']}")
                        self.leavingOutput.show()
                    else:
                        self.stationNameLabel.setText(f"")
                        self.ticketSalesOutput.hide()
                        self.waitingOutput.hide()
                        self.boardingOutput.hide()
                        self.leavingOutput.hide()
                        self.ticketSalesLabel.hide()
                        self.waitingLabel.hide()
                        self.boardingLabel.hide()
                        self.leavingLabel.hide()

    def check_failures(self):
        if "Track Circuit Failure" in self.failures:
            self.circuitSelection.show()
        else:
            self.circuitSelection.hide()
        if "Power Failure" in self.failures:
            self.powerSelection.show()
        else:
            self.powerSelection.hide()
        if "Broken Rail" in self.failures:
            self.brokenSelection.show()
        else:
            self.brokenSelection.hide()

    def add_failure_selection(self):
        failuresLabel = QLabel("Set Failures:", self.mainWindow)
        failuresLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"]
        )
        failuresLabel.setFont(failuresLabelFont)
        failuresLabel.setGeometry(670, 630, 150, 30)
        failuresLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        circuitFailureLabel = QLabel("Circuit", self.mainWindow)
        circuitFailureLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        circuitFailureLabel.setFont(circuitFailureLabelFont)
        circuitFailureLabel.setGeometry(615, 665, 50, 30)
        circuitFailureLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        powerFailureLabel = QLabel("Power", self.mainWindow)
        powerFailureLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        powerFailureLabel.setFont(powerFailureLabelFont)
        powerFailureLabel.setGeometry(715, 665, 50, 30)
        powerFailureLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        brokenFailureLabel = QLabel("Broken", self.mainWindow)
        brokenFailureLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        brokenFailureLabel.setFont(brokenFailureLabelFont)
        brokenFailureLabel.setGeometry(815, 665, 50, 30)
        brokenFailureLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        circuitFailureSelector = QLabel(self.mainWindow)
        circuitFailureSelector.setGeometry(630, 695, 20, 20)
        circuitFailureSelector.setPixmap(
            QPixmap("src/main/TrackModel/pngs/circle_outline.png").scaled(20, 20)
        )
        circuitFailureSelector.mousePressEvent = self.set_circuit_failure

        powerFailureSelector = QLabel(self.mainWindow)
        powerFailureSelector.setGeometry(730, 695, 20, 20)
        powerFailureSelector.setPixmap(
            QPixmap("src/main/TrackModel/pngs/circle_outline.png").scaled(20, 20)
        )
        powerFailureSelector.mousePressEvent = self.set_power_failure

        brokenFailureSelector = QLabel(self.mainWindow)
        brokenFailureSelector.setGeometry(830, 695, 20, 20)
        brokenFailureSelector.setPixmap(
            QPixmap("src/main/TrackModel/pngs/circle_outline.png").scaled(20, 20)
        )
        brokenFailureSelector.mousePressEvent = self.set_broken_failure

        self.circuitSelection = QLabel(self.mainWindow)
        self.circuitSelection.setGeometry(630, 695, 20, 20)
        self.circuitSelection.setPixmap(
            QPixmap("src/main/TrackModel/pngs/red_circle.png").scaled(20, 20)
        )
        self.circuitSelection.hide()
        self.circuitSelection.mousePressEvent = self.set_circuit_failure

        self.powerSelection = QLabel(self.mainWindow)
        self.powerSelection.setGeometry(730, 695, 20, 20)
        self.powerSelection.setPixmap(
            QPixmap("src/main/TrackModel/pngs/red_circle.png").scaled(20, 20)
        )
        self.powerSelection.hide()
        self.powerSelection.mousePressEvent = self.set_power_failure

        self.brokenSelection = QLabel(self.mainWindow)
        self.brokenSelection.setGeometry(830, 695, 20, 20)
        self.brokenSelection.setPixmap(
            QPixmap("src/main/TrackModel/pngs/red_circle.png").scaled(20, 20)
        )
        self.brokenSelection.hide()
        self.brokenSelection.mousePressEvent = self.set_broken_failure

    def set_circuit_failure(self, event):
        # Obtain block number provided
        blockNumber = self.entryField.text()
        # Update the block info based on the block selected
        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                if self.circuitSelection.isHidden():
                    self.circuitSelection.show()
                    self.failures.append("Track Circuit Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should append failure to this block
                else:
                    self.circuitSelection.hide()
                    self.failures.remove("Track Circuit Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should remove failure to this block
        self.block.set_data(self.selectedLine, self.trackData)

    def set_power_failure(self, event):
        # Obtain block number provided
        blockNumber = self.entryField.text()
        # Update the block info based on the block selected
        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                if self.powerSelection.isHidden():
                    self.powerSelection.show()
                    self.failures.append("Power Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should append failure to this block
                else:
                    self.powerSelection.hide()
                    self.failures.remove("Power Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should remove failure to this block
        self.block.set_data(self.selectedLine, self.trackData)

    def set_broken_failure(self, event):
        # Obtain block number provided
        blockNumber = self.entryField.text()
        # Update the block info based on the block selected
        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                if self.brokenSelection.isHidden():
                    self.brokenSelection.show()
                    self.failures.append("Broken Rail")
                    data[
                        "Failures"
                    ] = self.failures  # Should append failure to this block
                else:
                    self.brokenSelection.hide()
                    self.failures.remove("Broken Rail")
                    data[
                        "Failures"
                    ] = self.failures  # Should remove failure to this block
        self.block.set_data(self.selectedLine, self.trackData)

    def update_switch_state(self, line, _, blockNum, state):
        # Initial Green Line Occupancy
        if blockNum == 62 and state == 1 and line == 1:
            self.update_occupancy("Green", 0, "")
        # # Initial Red Line Occupancy
        # elif blockNum == 9 and state == 1 and line == 2:
        #     self.update_occupancy("Red", 0, '')

    def show_testbench(self):
        testbenchWindow = TestbenchWindow()
        testbenchWindow.testbench.exec()


class TestbenchWindow:
    def __init__(self):
        self.testbench = QDialog()
        self.setup_testbench()

    def setup_testbench(self):
        self.testbench.setWindowTitle("Change Failures")
        self.testbench.setGeometry(450, 300, 960, 600)

        # General layout
        self.add_mta_logo()
        self.add_title()
        self.add_hline()

        # Inputs
        self.setup_inputs()
        self.setup_failure_inputs()

        # New
        self.add_occupancy_test()
        self.add_passenger_test()
        self.add_lightstate_test()
        self.add_crossingstate_test()

    def add_mta_logo(self):
        mtaLogo = QLabel(self.testbench)
        mtaLogo.setGeometry(0, 0, 80, 80)
        mtaLogo.setPixmap(
            QPixmap("src/main/TrackModel/pngs/MTA_logo.png").scaled(80, 80)
        )

    def add_title(self):
        windowWidth = self.testbench.width()
        labelWidth = 350
        titlePosition = int((windowWidth - labelWidth) / 2)

        titleLabel = QLabel("Track Model- Testbench", self.testbench)
        titleLabel.setGeometry(titlePosition, 25, labelWidth, 40)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleFont = QFont("Arial", 18, QFont.Bold)
        titleLabel.setFont(titleFont)

    def add_hline(self):
        thickness = 5
        line = QFrame(self.testbench)
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(0, 80, 960, thickness)
        line.setLineWidth(thickness)

    def setup_inputs(self):
        blueBackground = QWidget(self.testbench)
        blueBackground.setGeometry(10, 120, 400, 450)
        blueBackground.setStyleSheet("background-color: #A9D0F5;")

        whiteBackground = "background-color: white"

        inputsLabel = QLabel("Change Inputs:", blueBackground)
        inputsLabel.setGeometry(0, 0, 400, 30)
        inputsLabel.setStyleSheet(
            "background-color: blue; color: white; font-weight: bold"
        )
        inputsLabel.setAlignment(Qt.AlignCenter)

        selectBlock = QLabel("Select Block #:", blueBackground)
        selectBlock.setGeometry(10, 50, 150, 30)
        self.blockInput = QSpinBox(blueBackground)
        self.blockInput.setGeometry(120, 50, 50, 30)
        self.blockInput.setStyleSheet(whiteBackground)
        self.blockInput.setMinimum(1)
        self.blockInput.setMaximum(15)
        self.blockInput.setValue(1)
        goButton = QPushButton("Go", blueBackground)
        goButton.setGeometry(220, 50, 150, 30)
        goButton.setStyleSheet("background-color: blue; color: white")
        # Connect the button to the update_block_info_display method
        goButton.clicked.connect(self.update_display)

        speedLabel = QLabel("Set Commanded Speed (mph):", blueBackground)
        speedLabel.setGeometry(10, 90, 200, 30)
        self.speedInput = QLineEdit(blueBackground)
        self.speedInput.setGeometry(220, 90, 150, 30)
        self.speedInput.setStyleSheet(whiteBackground)
        self.speedInput.setEnabled(False)

        authorityLabel = QLabel("Set Authority (blocks):", blueBackground)
        authorityLabel.setGeometry(10, 130, 200, 30)
        self.authorityInput = QLineEdit(blueBackground)
        self.authorityInput.setGeometry(220, 130, 150, 30)
        self.authorityInput.setStyleSheet(whiteBackground)
        self.authorityInput.setEnabled(False)

        railwayLabel = QLabel("Set Railway Crossing (0/1):", blueBackground)
        railwayLabel.setGeometry(10, 170, 200, 30)
        self.railwayInput = QSpinBox(blueBackground)
        self.railwayInput.setGeometry(220, 170, 150, 30)
        self.railwayInput.setStyleSheet(whiteBackground)
        self.railwayInput.setMinimum(0)
        self.railwayInput.setMaximum(1)
        self.railwayInput.setValue(0)
        self.railwayInput.setEnabled(False)

        switchLabel = QLabel("Set Switch Position (0/1):", blueBackground)
        switchLabel.setGeometry(10, 210, 200, 30)
        self.switchInput = QSpinBox(blueBackground)
        self.switchInput.setGeometry(220, 210, 150, 30)
        self.switchInput.setStyleSheet(whiteBackground)
        self.switchInput.setMinimum(0)
        self.switchInput.setMaximum(1)
        self.switchInput.setValue(0)
        self.switchInput.setEnabled(False)

        heaterLabel = QLabel("Set Track Heater (0/1):", blueBackground)
        heaterLabel.setGeometry(10, 250, 200, 30)
        self.heaterInput = QSpinBox(blueBackground)
        self.heaterInput.setGeometry(220, 250, 150, 30)
        self.heaterInput.setStyleSheet(whiteBackground)
        self.heaterInput.setMinimum(0)
        self.heaterInput.setMaximum(1)
        self.heaterInput.setValue(0)
        self.heaterInput.setEnabled(False)

        trackStateLabel = QLabel("Set Track State:", blueBackground)
        trackStateLabel.setGeometry(10, 290, 200, 30)
        self.trackOpen = QRadioButton("Open", blueBackground)
        self.trackOpen.setGeometry(120, 290, 60, 30)
        self.trackOpen.setEnabled(False)
        self.trackOccupied = QRadioButton("Occupied", blueBackground)
        self.trackOccupied.setGeometry(190, 290, 80, 30)
        self.trackOccupied.setEnabled(False)
        self.trackMaintenance = QRadioButton("Maintenance", blueBackground)
        self.trackMaintenance.setGeometry(280, 290, 100, 30)
        self.trackMaintenance.setEnabled(False)
        self.trackStateButtons = QButtonGroup()
        self.trackStateButtons.addButton(self.trackOpen)
        self.trackStateButtons.addButton(self.trackOccupied)
        self.trackStateButtons.addButton(self.trackMaintenance)

        ticketSalesLabel = QLabel("Set Ticket Sales/Hr:", blueBackground)
        ticketSalesLabel.setGeometry(10, 330, 200, 30)
        self.ticketSalesInput = QLineEdit(blueBackground)
        self.ticketSalesInput.setGeometry(220, 330, 150, 30)
        self.ticketSalesInput.setStyleSheet(whiteBackground)
        self.ticketSalesInput.setEnabled(False)

        waitingLabel = QLabel("Set Waiting @ Station:", blueBackground)
        waitingLabel.setGeometry(10, 370, 200, 30)
        self.waitingInput = QLineEdit(blueBackground)
        self.waitingInput.setGeometry(220, 370, 150, 30)
        self.waitingInput.setStyleSheet(whiteBackground)
        self.waitingInput.setEnabled(False)

        lightLabel = QLabel("Set Light Color:", blueBackground)
        lightLabel.setGeometry(10, 410, 150, 30)
        self.greenRadio = QRadioButton("Green", blueBackground)
        self.greenRadio.setGeometry(170, 410, 70, 30)
        self.greenRadio.setEnabled(False)
        self.yellowRadio = QRadioButton("Yellow", blueBackground)
        self.yellowRadio.setGeometry(250, 410, 70, 30)
        self.yellowRadio.setEnabled(False)
        self.redRadio = QRadioButton("Red", blueBackground)
        self.redRadio.setGeometry(330, 410, 70, 30)
        self.redRadio.setEnabled(False)
        self.lightStateButtons = QButtonGroup()
        self.lightStateButtons.addButton(self.greenRadio)
        self.lightStateButtons.addButton(self.yellowRadio)
        self.lightStateButtons.addButton(self.redRadio)

    def setup_failure_inputs(self):
        redBackground = QWidget(self.testbench)
        redBackground.setGeometry(500, 120, 350, 80)
        redBackground.setStyleSheet("background-color: #ffd6d6;")

        failureLabel = QLabel("Set Failure Input:", redBackground)
        failureLabel.setGeometry(0, 0, 350, 30)
        failureLabel.setStyleSheet(
            "background-color: red; color: white; font-weight: bold"
        )
        failureLabel.setAlignment(Qt.AlignCenter)

        self.failureCheckboxes = []
        failures = ["Track Circuit Failure", "Power Failure", "Broken Rail"]
        xOffset = 0
        for failure in failures:
            option = QCheckBox(failure, redBackground)
            option.setGeometry(xOffset, 40, 150, 30)
            if failure == "Broken Rail":
                option.setGeometry(xOffset - 40, 40, 150, 30)
            option.setStyleSheet("background-color: #ffd6d6")
            self.failureCheckboxes.append(option)
            xOffset += 150

    def update_display(self):
        self.selectedBlock = self.blockInput.value()
        # Disable all input fields and buttons at the beginning
        self.speedInput.setEnabled(False)
        self.authorityInput.setEnabled(False)
        self.railwayInput.setEnabled(False)
        self.switchInput.setEnabled(False)
        self.heaterInput.setEnabled(False)
        self.ticketSalesInput.setEnabled(False)
        self.waitingInput.setEnabled(False)

        # Reset the radio button state
        self.trackOpen.setEnabled(False)
        self.trackOccupied.setEnabled(False)
        self.trackMaintenance.setEnabled(False)

        # Reset the radio button state
        self.greenRadio.setEnabled(False)
        self.yellowRadio.setEnabled(False)
        self.redRadio.setEnabled(False)
        # Enable the relevant input fields and buttons based on the selected block
        if self.selectedBlock == 5:
            self.switchInput.setEnabled(True)
        if self.selectedBlock == 10 or self.selectedBlock == 15:
            self.ticketSalesInput.setEnabled(True)
            self.waitingInput.setEnabled(True)

        self.heaterInput.setEnabled(True)
        self.speedInput.setEnabled(True)
        self.authorityInput.setEnabled(True)
        # Enable the radio buttons for track state and light state
        self.trackOpen.setEnabled(True)
        self.trackOccupied.setEnabled(True)
        self.trackMaintenance.setEnabled(True)
        self.greenRadio.setEnabled(True)
        self.yellowRadio.setEnabled(True)
        self.redRadio.setEnabled(True)

    def add_occupancy_test(self):
        selectLineLabel = QLabel("Select Line:", self.testbench)
        selectLineLabel.setGeometry(490, 210, 75, 30)
        selectLineLabel.setStyleSheet("font-weight: bold")
        self.occupancyLineInput = QLineEdit(self.testbench)
        self.occupancyLineInput.setGeometry(570, 210, 50, 30)
        self.occupancyLineInput.setStyleSheet("background-color: white")

        currentBlockLabel = QLabel("Current Block:", self.testbench)
        currentBlockLabel.setGeometry(625, 210, 100, 30)
        currentBlockLabel.setStyleSheet("font-weight: bold")
        self.occupancyCurrentBlock = QLineEdit(self.testbench)
        self.occupancyCurrentBlock.setGeometry(720, 210, 50, 30)
        self.occupancyCurrentBlock.setStyleSheet("background-color: white")

        nextBlockLabel = QLabel("Next Block:", self.testbench)
        nextBlockLabel.setGeometry(780, 210, 100, 30)
        nextBlockLabel.setStyleSheet("font-weight: bold")
        self.occupancyNextBlock = QLineEdit(self.testbench)
        self.occupancyNextBlock.setGeometry(860, 210, 50, 30)
        self.occupancyNextBlock.setStyleSheet("background-color: white")

        # self.lineInput.addItem("Green")
        # self.lineInput.addItem("Red")
        # self.lineInput.currentIndexChanged.connect(self.send_occupancy_signal)

        signalTest = QPushButton("Occupancy Test", self.testbench)
        signalTest.setGeometry(615, 250, 150, 30)
        signalTest.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        signalTest.clicked.connect(self.send_occupancy_signal)

    def send_occupancy_signal(self):
        line = self.occupancyLineInput.text()
        if self.occupancyCurrentBlock.text() != "":
            cur = int(self.occupancyCurrentBlock.text())
        else:
            cur = ""
        next = int(self.occupancyNextBlock.text())
        trainModelToTrackModel.sendPolarity.emit(line, next, cur)

    def add_passenger_test(self):
        selectLineLabel = QLabel("Select Line:", self.testbench)
        selectLineLabel.setGeometry(490, 300, 75, 30)
        selectLineLabel.setStyleSheet("font-weight: bold")
        self.passengerLineInput = QLineEdit(self.testbench)
        self.passengerLineInput.setGeometry(570, 300, 50, 30)
        self.passengerLineInput.setStyleSheet("background-color: white")

        stationNameLabel = QLabel("Station Name:", self.testbench)
        stationNameLabel.setGeometry(625, 300, 100, 30)
        stationNameLabel.setStyleSheet("font-weight: bold")
        self.passengerStationName = QLineEdit(self.testbench)
        self.passengerStationName.setGeometry(720, 300, 50, 30)
        self.passengerStationName.setStyleSheet("background-color: white")

        passengers = QLabel("Passengers:", self.testbench)
        passengers.setGeometry(780, 300, 100, 30)
        passengers.setStyleSheet("font-weight: bold")
        self.trainPassengers = QLineEdit(self.testbench)
        self.trainPassengers.setGeometry(860, 300, 50, 30)
        self.trainPassengers.setStyleSheet("background-color: white")

        signalTest = QPushButton("Passenger Test", self.testbench)
        signalTest.setGeometry(615, 340, 150, 30)
        signalTest.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        signalTest.clicked.connect(self.send_passenger_signal)

    def send_passenger_signal(self):
        line = self.passengerLineInput.text()
        station = self.passengerStationName.text()
        passengersOnBoard = int(self.trainPassengers.text())
        trainModelToTrackModel.sendCurrentPassengers.emit(
            line, station, passengersOnBoard
        )
    
    def add_lightstate_test(self):
        selectLineLabel = QLabel("Line Number:", self.testbench)
        selectLineLabel.setGeometry(490, 390, 85, 30)
        selectLineLabel.setStyleSheet("font-weight: bold")
        self.lightLineInput = QLineEdit(self.testbench)
        self.lightLineInput.setGeometry(580, 390, 50, 30)
        self.lightLineInput.setStyleSheet("background-color: white")

        blockLabel = QLabel("Select Block:", self.testbench)
        blockLabel.setGeometry(635, 390, 100, 30)
        blockLabel.setStyleSheet("font-weight: bold")
        self.lightBlock = QLineEdit(self.testbench)
        self.lightBlock.setGeometry(720, 390, 50, 30)
        self.lightBlock.setStyleSheet("background-color: white")

        lightColorLabel = QLabel("Light State:", self.testbench)
        lightColorLabel.setGeometry(780, 390, 100, 30)
        lightColorLabel.setStyleSheet("font-weight: bold")
        self.lightColor = QLineEdit(self.testbench)
        self.lightColor.setGeometry(860, 390, 50, 30)
        self.lightColor.setStyleSheet("background-color: white")

        lightTest = QPushButton("Light State Test", self.testbench)
        lightTest.setGeometry(615, 430, 150, 30)
        lightTest.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        lightTest.clicked.connect(self.send_light_signal)

    def send_light_signal(self):
        line = int(self.lightLineInput.text())
        blockNum = int(self.lightBlock.text())
        color = self.lightColor.text()
        trackControllerToTrackModel.lightState.emit(line, 1, blockNum, color)

    def add_crossingstate_test(self):
        selectLineLabel = QLabel("Line Number:", self.testbench)
        selectLineLabel.setGeometry(530, 480, 85, 30)
        selectLineLabel.setStyleSheet("font-weight: bold")
        self.crossingLineInput = QLineEdit(self.testbench)
        self.crossingLineInput.setGeometry(620, 480, 50, 30)
        self.crossingLineInput.setStyleSheet("background-color: white")

        stateLabel = QLabel("Crossing State:", self.testbench)
        stateLabel.setGeometry(680, 480, 100, 30)
        stateLabel.setStyleSheet("font-weight: bold")
        self.crossingState = QLineEdit(self.testbench)
        self.crossingState.setGeometry(780, 480, 50, 30)
        self.crossingState.setStyleSheet("background-color: white")

        crossingTest = QPushButton("Crossing State Test", self.testbench)
        crossingTest.setGeometry(615, 520, 150, 30)
        crossingTest.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        crossingTest.clicked.connect(self.send_crossing_signal)

    def send_crossing_signal(self):
        line = int(self.crossingLineInput.text())
        state = True
        if self.crossingState.text() == '0':
            state = False
        trackControllerToTrackModel.crossingState.emit(line, None, None, state)


if __name__ == "__main__":
    trackmodel = TrackModel()
