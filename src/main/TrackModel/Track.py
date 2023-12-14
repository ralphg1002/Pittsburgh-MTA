from PyQt5.QtGui import QPixmap, QPainterPath, QPen, QColor, QFont, QBrush
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsPathItem, QGraphicsTextItem, QGraphicsRectItem

class TrackView(QGraphicsView):
    greenBlocks = {}
    redBlocks = {}
    greenSwitches = {}
    redSwitches = {}

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
        block_0 = self.createTrackBlock(path_0, "Block 0", "Green")
        self.greenTrack.addItem(block_0)
        self.greenBlocks[0] = block_0

        path_151 = QPainterPath()
        path_151.moveTo(96, 278)
        path_151.cubicTo(97, 278, 120, 251, 120, 250)
        block_151 = self.createTrackBlock(path_151, "Block 151", "Green")
        self.greenTrack.addItem(block_151)
        self.greenBlocks[151] = block_151

        #Hidden under block 1
        path_12 = QPainterPath()
        path_12.moveTo(23, 2)
        path_12.cubicTo(23, 2, 13, 1, 0, 0)
        block_12 = self.createTrackBlock(path_12, "Block 12", "Green")
        self.greenTrack.addItem(block_12)
        self.greenBlocks[12] = block_12

        path_1 = QPainterPath()
        path_1.moveTo(0, 0)
        path_1.cubicTo(0, 0, 5, 0, 10, 10)
        block_1 = self.createTrackBlock(path_1, "Block 1", "Green")
        self.greenTrack.addItem(block_1)
        self.greenBlocks[1] = block_1

        path_2 = QPainterPath()
        path_2.moveTo(14, 18)
        path_2.lineTo(21, 30)
        block_2 = self.createTrackBlock(path_2, "Block 2", "Green")
        self.greenTrack.addItem(block_2)
        self.greenBlocks[2] = block_2

        path_3 = QPainterPath()
        path_3.moveTo(26, 38)
        path_3.cubicTo(26, 38, 28, 41, 38, 47)
        block_3 = self.createTrackBlock(path_3, "Block 3", "Green")
        self.greenTrack.addItem(block_3)
        self.greenBlocks[3] = block_3

        path_4 = QPainterPath()
        path_4.moveTo(46, 52)
        path_4.cubicTo(46, 52, 52, 55, 59, 57)
        block_4 = self.createTrackBlock(path_4, "Block 4", "Green")
        self.greenTrack.addItem(block_4)
        self.greenBlocks[4] = block_4

        path_5 = QPainterPath()
        path_5.moveTo(68, 60)
        path_5.cubicTo(68, 60, 73, 61, 82, 61)
        block_5 = self.createTrackBlock(path_5, "Block 5", "Green")
        self.greenTrack.addItem(block_5)
        self.greenBlocks[5] = block_5

        path_6 = QPainterPath()
        path_6.moveTo(92, 61)
        path_6.cubicTo(92, 61, 103, 60, 104, 58)
        block_6 = self.createTrackBlock(path_6, "Block 6", "Green")
        self.greenTrack.addItem(block_6)
        self.greenBlocks[6] = block_6

        path_7 = QPainterPath()
        path_7.moveTo(109, 50)
        path_7.cubicTo(109, 50, 112, 45, 112, 39)
        block_7 = self.createTrackBlock(path_7, "Block 7", "Green")
        self.greenTrack.addItem(block_7)
        self.greenBlocks[7] = block_7

        path_8 = QPainterPath()
        path_8.moveTo(112, 29)
        path_8.cubicTo(112, 29, 112, 25, 102, 18)
        block_8 = self.createTrackBlock(path_8, "Block 8", "Green")
        self.greenTrack.addItem(block_8)
        self.greenBlocks[8] = block_8

        path_9 = QPainterPath()
        path_9.moveTo(94, 14)
        path_9.cubicTo(94, 14, 86, 11, 81, 10)
        block_9 = self.createTrackBlock(path_9, "Block 9", "Green")
        self.greenTrack.addItem(block_9)
        self.greenBlocks[9] = block_9

        path_10 = QPainterPath()
        path_10.moveTo(72, 8)
        path_10.cubicTo(72, 8, 58, 5, 57, 5)
        block_10 = self.createTrackBlock(path_10, "Block 10", "Green")
        self.greenTrack.addItem(block_10)
        self.greenBlocks[10] = block_10

        path_11 = QPainterPath()
        path_11.moveTo(47, 4)
        path_11.cubicTo(47, 4, 35, 3, 33, 3)
        block_11 = self.createTrackBlock(path_11, "Block 11", "Green")
        self.greenTrack.addItem(block_11)
        self.greenBlocks[11] = block_11

        path_13 = QPainterPath()
        path_13.moveTo(-10, 0)
        path_13.lineTo(-25, 0)
        block_13 = self.createTrackBlock(path_13, "Block 13", "Green")
        self.greenTrack.addItem(block_13)
        self.greenBlocks[13] = block_13

        path_14 = QPainterPath()
        path_14.moveTo(-35, 0)
        path_14.lineTo(-50, 0)
        block_14 = self.createTrackBlock(path_14, "Block 14", "Green")
        self.greenTrack.addItem(block_14)
        self.greenBlocks[14] = block_14

        path_15 = QPainterPath()
        path_15.moveTo(-60, 0)
        path_15.lineTo(-75, 0)
        block_15 = self.createTrackBlock(path_15, "Block 15", "Green")
        self.greenTrack.addItem(block_15)
        self.greenBlocks[15] = block_15

        path_16 = QPainterPath()
        path_16.moveTo(-85, 0)
        path_16.lineTo(-100, 0)
        block_16 = self.createTrackBlock(path_16, "Block 16", "Green")
        self.greenTrack.addItem(block_16)
        self.greenBlocks[16] = block_16

        path_17 = QPainterPath()
        path_17.moveTo(-110, 0)
        path_17.quadTo(-115, 0, -125, 5)
        block_17 = self.createTrackBlock(path_17, "Block 17", "Green")
        self.greenTrack.addItem(block_17)
        self.greenBlocks[17] = block_17

        path_18 = QPainterPath()
        path_18.moveTo(-133, 9)
        path_18.quadTo(-141, 14, -145, 19)
        block_18 = self.createTrackBlock(path_18, "Block 18", "Green")
        self.greenTrack.addItem(block_18)
        self.greenBlocks[18] = block_18

        path_19 = QPainterPath()
        path_19.moveTo(-151, 27)
        path_19.quadTo(-156, 33, -159, 40)
        block_19 = self.createTrackBlock(path_19, "Block 19", "Green")
        self.greenTrack.addItem(block_19)
        self.greenBlocks[19] = block_19

        path_20 = QPainterPath()
        path_20.moveTo(-163, 49)
        path_20.cubicTo(-166, 55, -167, 58, -167, 63)
        block_20 = self.createTrackBlock(path_20, "Block 20", "Green")
        self.greenTrack.addItem(block_20)
        self.greenBlocks[20] = block_20

        path_21 = QPainterPath()
        path_21.moveTo(-167, 73)
        path_21.lineTo(-167, 78)
        block_21 = self.createTrackBlock(path_21, "Block 21", "Green")
        self.greenTrack.addItem(block_21)
        self.greenBlocks[21] = block_21

        path_22 = QPainterPath()
        path_22.moveTo(-167, 88)
        path_22.lineTo(-167, 93)
        block_22 = self.createTrackBlock(path_22, "Block 22", "Green")
        self.greenTrack.addItem(block_22)
        self.greenBlocks[22] = block_22

        path_23 = QPainterPath()
        path_23.moveTo(-167, 103)
        path_23.lineTo(-167, 108)
        block_23 = self.createTrackBlock(path_23, "Block 23", "Green")
        self.greenTrack.addItem(block_23)
        self.greenBlocks[23] = block_23

        path_24 = QPainterPath()
        path_24.moveTo(-167, 118)
        path_24.lineTo(-167, 123)
        block_24 = self.createTrackBlock(path_24, "Block 24", "Green")
        self.greenTrack.addItem(block_24)
        self.greenBlocks[24] = block_24

        path_25 = QPainterPath()
        path_25.moveTo(-167, 133)
        path_25.lineTo(-167, 138)
        block_25 = self.createTrackBlock(path_25, "Block 25", "Green")
        self.greenTrack.addItem(block_25)
        self.greenBlocks[25] = block_25

        path_26 = QPainterPath()
        path_26.moveTo(-167, 148)
        path_26.lineTo(-167, 153)
        block_26 = self.createTrackBlock(path_26, "Block 26", "Green")
        self.greenTrack.addItem(block_26)
        self.greenBlocks[26] = block_26

        path_27 = QPainterPath()
        path_27.moveTo(-167, 163)
        path_27.lineTo(-167, 168)
        block_27 = self.createTrackBlock(path_27, "Block 27", "Green")
        self.greenTrack.addItem(block_27)
        self.greenBlocks[27] = block_27

        path_28 = QPainterPath()
        path_28.moveTo(-167, 178)
        path_28.lineTo(-167, 183)
        block_28 = self.createTrackBlock(path_28, "Block 28", "Green")
        self.greenTrack.addItem(block_28)
        self.greenBlocks[28] = block_28

        path_29 = QPainterPath()
        path_29.moveTo(-167, 193)
        path_29.lineTo(-167, 198)
        block_29 = self.createTrackBlock(path_29, "Block 29", "Green")
        self.greenTrack.addItem(block_29)
        self.greenBlocks[29] = block_29

        path_30 = QPainterPath()
        path_30.moveTo(-167, 208)
        path_30.lineTo(-167, 213)
        block_30 = self.createTrackBlock(path_30, "Block 30", "Green")
        self.greenTrack.addItem(block_30)
        self.greenBlocks[30] = block_30

        path_31 = QPainterPath()
        path_31.moveTo(-167, 223)
        path_31.lineTo(-167, 228)
        block_31 = self.createTrackBlock(path_31, "Block 31", "Green")
        self.greenTrack.addItem(block_31)
        self.greenBlocks[31] = block_31

        path_32 = QPainterPath()
        path_32.moveTo(-167, 238)
        path_32.lineTo(-167, 243)
        block_32 = self.createTrackBlock(path_32, "Block 32", "Green")
        self.greenTrack.addItem(block_32)
        self.greenBlocks[32] = block_32

        path_33 = QPainterPath()
        path_33.moveTo(-167, 253)
        path_33.quadTo(-167, 255, -166, 258)
        block_33 = self.createTrackBlock(path_33, "Block 33", "Green")
        self.greenTrack.addItem(block_33)
        self.greenBlocks[33] = block_33

        path_34 = QPainterPath()
        path_34.moveTo(-162, 266)
        path_34.quadTo(-161, 268, -159, 270)
        block_34 = self.createTrackBlock(path_34, "Block 34", "Green")
        self.greenTrack.addItem(block_34)
        self.greenBlocks[34] = block_34

        path_35 = QPainterPath()
        path_35.moveTo(-152, 277)
        path_35.quadTo(-151, 278, -147, 278)
        block_35 = self.createTrackBlock(path_35, "Block 35", "Green")
        self.greenTrack.addItem(block_35)
        self.greenBlocks[35] = block_35

        path_36 = QPainterPath()
        path_36.moveTo(-137, 278)
        path_36.lineTo(-135, 278)
        block_36 = self.createTrackBlock(path_36, "Block 36", "Green")
        self.greenTrack.addItem(block_36)
        self.greenBlocks[36] = block_36

        path_37 = QPainterPath()
        path_37.moveTo(-125, 278)
        path_37.lineTo(-124, 278)
        block_37 = self.createTrackBlock(path_37, "Block 37", "Green")
        self.greenTrack.addItem(block_37)
        self.greenBlocks[37] = block_37

        path_38 = QPainterPath()
        path_38.moveTo(-114, 278)
        path_38.lineTo(-113, 278)
        block_38 = self.createTrackBlock(path_38, "Block 38", "Green")
        self.greenTrack.addItem(block_38)
        self.greenBlocks[38] = block_38

        path_39 = QPainterPath()
        path_39.moveTo(-103, 278)
        path_39.lineTo(-102, 278)
        block_39 = self.createTrackBlock(path_39, "Block 39", "Green")
        self.greenTrack.addItem(block_39)
        self.greenBlocks[39] = block_39

        path_40 = QPainterPath()
        path_40.moveTo(-92, 278)
        path_40.lineTo(-91, 278)
        block_40 = self.createTrackBlock(path_40, "Block 40", "Green")
        self.greenTrack.addItem(block_40)
        self.greenBlocks[40] = block_40

        path_41 = QPainterPath()
        path_41.moveTo(-81, 278)
        path_41.lineTo(-80, 278)
        block_41 = self.createTrackBlock(path_41, "Block 41", "Green")
        self.greenTrack.addItem(block_41)
        self.greenBlocks[41] = block_41

        path_42 = QPainterPath()
        path_42.moveTo(-70, 278)
        path_42.lineTo(-69, 278)
        block_42 = self.createTrackBlock(path_42, "Block 42", "Green")
        self.greenTrack.addItem(block_42)
        self.greenBlocks[42] = block_42

        path_43 = QPainterPath()
        path_43.moveTo(-59, 278)
        path_43.lineTo(-58, 278)
        block_43 = self.createTrackBlock(path_43, "Block 43", "Green")
        self.greenTrack.addItem(block_43)
        self.greenBlocks[43] = block_43

        path_44 = QPainterPath()
        path_44.moveTo(-48, 278)
        path_44.lineTo(-47, 278)
        block_44 = self.createTrackBlock(path_44, "Block 44", "Green")
        self.greenTrack.addItem(block_44)
        self.greenBlocks[44] = block_44

        path_45 = QPainterPath()
        path_45.moveTo(-37, 278)
        path_45.lineTo(-36, 278)
        block_45 = self.createTrackBlock(path_45, "Block 45", "Green")
        self.greenTrack.addItem(block_45)
        self.greenBlocks[45] = block_45

        path_46 = QPainterPath()
        path_46.moveTo(-26, 278)
        path_46.lineTo(-25, 278)
        block_46 = self.createTrackBlock(path_46, "Block 46", "Green")
        self.greenTrack.addItem(block_46)
        self.greenBlocks[46] = block_46

        path_47 = QPainterPath()
        path_47.moveTo(-15, 278)
        path_47.lineTo(-14, 278)
        block_47 = self.createTrackBlock(path_47, "Block 47", "Green")
        self.greenTrack.addItem(block_47)
        self.greenBlocks[47] = block_47

        path_48 = QPainterPath()
        path_48.moveTo(-4, 278)
        path_48.lineTo(-3, 278)
        block_48 = self.createTrackBlock(path_48, "Block 48", "Green")
        self.greenTrack.addItem(block_48)
        self.greenBlocks[48] = block_48

        path_49 = QPainterPath()
        path_49.moveTo(7, 278)
        path_49.lineTo(8, 278)
        block_49 = self.createTrackBlock(path_49, "Block 49", "Green")
        self.greenTrack.addItem(block_49)
        self.greenBlocks[49] = block_49

        path_50 = QPainterPath()
        path_50.moveTo(18, 278)
        path_50.lineTo(19, 278)
        block_50 = self.createTrackBlock(path_50, "Block 50", "Green")
        self.greenTrack.addItem(block_50)
        self.greenBlocks[50] = block_50

        path_51 = QPainterPath()
        path_51.moveTo(29, 278)
        path_51.lineTo(30, 278)
        block_51 = self.createTrackBlock(path_51, "Block 51", "Green")
        self.greenTrack.addItem(block_51)
        self.greenBlocks[51] = block_51

        path_52 = QPainterPath()
        path_52.moveTo(40, 278)
        path_52.lineTo(41, 278)
        block_52 = self.createTrackBlock(path_52, "Block 52", "Green")
        self.greenTrack.addItem(block_52)
        self.greenBlocks[52] = block_52

        path_53 = QPainterPath()
        path_53.moveTo(51, 278)
        path_53.lineTo(52, 278)
        block_53 = self.createTrackBlock(path_53, "Block 53", "Green")
        self.greenTrack.addItem(block_53)
        self.greenBlocks[53] = block_53

        path_54 = QPainterPath()
        path_54.moveTo(62, 278)
        path_54.lineTo(63, 278)
        block_54 = self.createTrackBlock(path_54, "Block 54", "Green")
        self.greenTrack.addItem(block_54)
        self.greenBlocks[54] = block_54

        path_55 = QPainterPath()
        path_55.moveTo(73, 278)
        path_55.lineTo(74, 278)
        block_55 = self.createTrackBlock(path_55, "Block 55", "Green")
        self.greenTrack.addItem(block_55)
        self.greenBlocks[55] = block_55

        path_56 = QPainterPath()
        path_56.moveTo(84, 278)
        path_56.lineTo(85, 278)
        block_56 = self.createTrackBlock(path_56, "Block 56", "Green")
        self.greenTrack.addItem(block_56)
        self.greenBlocks[56] = block_56

        path_57 = QPainterPath()
        path_57.moveTo(95, 278)
        path_57.lineTo(96, 278)
        block_57 = self.createTrackBlock(path_57, "Block 57", "Green")
        self.greenTrack.addItem(block_57)
        self.greenBlocks[57] = block_57

        path_58 = QPainterPath()
        path_58.moveTo(106, 278)
        path_58.quadTo(107, 278, 111, 279)
        block_58 = self.createTrackBlock(path_58, "Block 58", "Green")
        self.greenTrack.addItem(block_58)
        self.greenBlocks[58] = block_58

        path_59 = QPainterPath()
        path_59.moveTo(120, 283)
        path_59.quadTo(125, 285, 128, 287)
        block_59 = self.createTrackBlock(path_59, "Block 59", "Green")
        self.greenTrack.addItem(block_59)
        self.greenBlocks[59] = block_59

        path_60 = QPainterPath()
        path_60.moveTo(136, 293)
        path_60.quadTo(142, 297, 143, 298)
        block_60 = self.createTrackBlock(path_60, "Block 60", "Green")
        self.greenTrack.addItem(block_60)
        self.greenBlocks[60] = block_60

        path_61 = QPainterPath()
        path_61.moveTo(150, 305)
        path_61.quadTo(156, 312, 157, 314)
        block_61 = self.createTrackBlock(path_61, "Block 61", "Green")
        self.greenTrack.addItem(block_61)
        self.greenBlocks[61] = block_61

        path_62 = QPainterPath()
        path_62.moveTo(161, 322)
        path_62.cubicTo(162, 324, 163, 328, 163, 330)
        block_62 = self.createTrackBlock(path_62, "Block 62", "Green")
        self.greenTrack.addItem(block_62)
        self.greenBlocks[62] = block_62

        path_63 = QPainterPath()
        path_63.moveTo(163, 340)
        path_63.lineTo(163, 350)
        block_63 = self.createTrackBlock(path_63, "Block 63", "Green")
        self.greenTrack.addItem(block_63)
        self.greenBlocks[63] = block_63

        path_64 = QPainterPath()
        path_64.moveTo(163, 360)
        path_64.lineTo(163, 370)
        block_64 = self.createTrackBlock(path_64, "Block 64", "Green")
        self.greenTrack.addItem(block_64)
        self.greenBlocks[64] = block_64

        path_65 = QPainterPath()
        path_65.moveTo(163, 380)
        path_65.lineTo(163, 400)
        block_65 = self.createTrackBlock(path_65, "Block 65", "Green")
        self.greenTrack.addItem(block_65)
        self.greenBlocks[65] = block_65

        path_66 = QPainterPath()
        path_66.moveTo(163, 410)
        path_66.lineTo(163, 430)
        block_66 = self.createTrackBlock(path_66, "Block 66", "Green")
        self.greenTrack.addItem(block_66)
        self.greenBlocks[66] = block_66

        path_67 = QPainterPath()
        path_67.moveTo(163, 440)
        path_67.lineTo(163, 450)
        block_67 = self.createTrackBlock(path_67, "Block 67", "Green")
        self.greenTrack.addItem(block_67)
        self.greenBlocks[67] = block_67

        path_68 = QPainterPath()
        path_68.moveTo(163, 460)
        path_68.lineTo(163, 470)
        block_68 = self.createTrackBlock(path_68, "Block 68", "Green")
        self.greenTrack.addItem(block_68)
        self.greenBlocks[68] = block_68

        path_69 = QPainterPath()
        path_69.moveTo(163, 480)
        path_69.quadTo(163, 486, 162, 491)
        block_69 = self.createTrackBlock(path_69, "Block 69", "Green")
        self.greenTrack.addItem(block_69)
        self.greenBlocks[69] = block_69

        path_70 = QPainterPath()
        path_70.moveTo(160, 500)
        path_70.quadTo(159, 505, 157, 510)
        block_70 = self.createTrackBlock(path_70, "Block 70", "Green")
        self.greenTrack.addItem(block_70)
        self.greenBlocks[70] = block_70

        path_71 = QPainterPath()
        path_71.moveTo(153, 519)
        path_71.quadTo(151, 524, 148, 529)
        block_71 = self.createTrackBlock(path_71, "Block 71", "Green")
        self.greenTrack.addItem(block_71)
        self.greenBlocks[71] = block_71

        path_72 = QPainterPath()
        path_72.moveTo(143, 537)
        path_72.quadTo(139, 543, 137, 545)
        block_72 = self.createTrackBlock(path_72, "Block 72", "Green")
        self.greenTrack.addItem(block_72)
        self.greenBlocks[72] = block_72

        path_73 = QPainterPath()
        path_73.moveTo(130, 551)
        path_73.cubicTo(126, 554, 121, 556, 120, 556)
        block_73 = self.createTrackBlock(path_73, "Block 73", "Green")
        self.greenTrack.addItem(block_73)
        self.greenBlocks[73] = block_73

        path_74 = QPainterPath()
        path_74.moveTo(110, 556)
        path_74.lineTo(90, 556)
        block_74 = self.createTrackBlock(path_74, "Block 74", "Green")
        self.greenTrack.addItem(block_74)
        self.greenBlocks[74] = block_74

        path_75 = QPainterPath()
        path_75.moveTo(80, 556)
        path_75.lineTo(60, 556)
        block_75 = self.createTrackBlock(path_75, "Block 75", "Green")
        self.greenTrack.addItem(block_75)
        self.greenBlocks[75] = block_75

        path_76 = QPainterPath()
        path_76.moveTo(50, 556)
        path_76.lineTo(30, 556)
        block_76 = self.createTrackBlock(path_76, "Block 76", "Green")
        self.greenTrack.addItem(block_76)
        self.greenBlocks[76] = block_76

        path_77 = QPainterPath()
        path_77.moveTo(20, 556)
        path_77.lineTo(12, 556)
        block_77 = self.createTrackBlock(path_77, "Block 77", "Green")
        self.greenTrack.addItem(block_77)
        self.greenBlocks[77] = block_77

        path_78 = QPainterPath()
        path_78.moveTo(2, 556)
        path_78.lineTo(-6, 556)
        block_78 = self.createTrackBlock(path_78, "Block 78", "Green")
        self.greenTrack.addItem(block_78)
        self.greenBlocks[78] = block_78

        path_79 = QPainterPath()
        path_79.moveTo(-16, 556)
        path_79.lineTo(-24, 556)
        block_79 = self.createTrackBlock(path_79, "Block 79", "Green")
        self.greenTrack.addItem(block_79)
        self.greenBlocks[79] = block_79

        path_80 = QPainterPath()
        path_80.moveTo(-34, 556)
        path_80.lineTo(-42, 556)
        block_80 = self.createTrackBlock(path_80, "Block 80", "Green")
        self.greenTrack.addItem(block_80)
        self.greenBlocks[80] = block_80

        path_81 = QPainterPath()
        path_81.moveTo(-52, 556)
        path_81.lineTo(-60, 556)
        block_81 = self.createTrackBlock(path_81, "Block 81", "Green")
        self.greenTrack.addItem(block_81)
        self.greenBlocks[81] = block_81

        path_82 = QPainterPath()
        path_82.moveTo(-70, 556)
        path_82.lineTo(-78, 556)
        block_82 = self.createTrackBlock(path_82, "Block 82", "Green")
        self.greenTrack.addItem(block_82)
        self.greenBlocks[82] = block_82

        path_83 = QPainterPath()
        path_83.moveTo(-88, 556)
        path_83.lineTo(-96, 556)
        block_83 = self.createTrackBlock(path_83, "Block 83", "Green")
        self.greenTrack.addItem(block_83)
        self.greenBlocks[83] = block_83

        path_84 = QPainterPath()
        path_84.moveTo(-106, 556)
        path_84.lineTo(-114, 556)
        block_84 = self.createTrackBlock(path_84, "Block 84", "Green")
        self.greenTrack.addItem(block_84)
        self.greenBlocks[84] = block_84

        #Hidden under blocks 85 & 86
        path_100 = QPainterPath()
        path_100.moveTo(-148, 546)
        path_100.quadTo(-147, 547, -142, 551)
        block_100 = self.createTrackBlock(path_100, "Block 100", "Green")
        self.greenTrack.addItem(block_100)
        self.greenBlocks[100] = block_100

        path_85 = QPainterPath()
        path_85.moveTo(-124, 556)
        path_85.lineTo(-132, 556)
        block_85 = self.createTrackBlock(path_85, "Block 85", "Green")
        self.greenTrack.addItem(block_85)
        self.greenBlocks[85] = block_85

        path_86 = QPainterPath()
        path_86.moveTo(-142, 556)
        path_86.lineTo(-149, 556)
        block_86 = self.createTrackBlock(path_86, "Block 86", "Green")
        self.greenTrack.addItem(block_86)
        self.greenBlocks[86] = block_86

        path_87 = QPainterPath()
        path_87.moveTo(-159, 556)
        path_87.lineTo(-163, 556)
        block_87 = self.createTrackBlock(path_87, "Block 87", "Green")
        self.greenTrack.addItem(block_87)
        self.greenBlocks[87] = block_87

        path_88 = QPainterPath()
        path_88.moveTo(-173, 556)
        path_88.lineTo(-180, 556)
        block_88 = self.createTrackBlock(path_88, "Block 88", "Green")
        self.greenTrack.addItem(block_88)
        self.greenBlocks[88] = block_88

        path_89 = QPainterPath()
        path_89.moveTo(-190, 556)
        path_89.quadTo(-196, 556, -198, 555)
        block_89 = self.createTrackBlock(path_89, "Block 89", "Green")
        self.greenTrack.addItem(block_89)
        self.greenBlocks[89] = block_89

        path_90 = QPainterPath()
        path_90.moveTo(-206, 551)
        path_90.quadTo(-212, 547, -213, 546)
        block_90 = self.createTrackBlock(path_90, "Block 90", "Green")
        self.greenTrack.addItem(block_90)
        self.greenBlocks[90] = block_90

        path_91 = QPainterPath()
        path_91.moveTo(-220, 539)
        path_91.quadTo(-225, 533, -226, 531)
        block_91 = self.createTrackBlock(path_91, "Block 91", "Green")
        self.greenTrack.addItem(block_91)
        self.greenBlocks[91] = block_91

        path_92 = QPainterPath()
        path_92.moveTo(-230, 523)
        path_92.quadTo(-232, 519, -233, 512)
        block_92 = self.createTrackBlock(path_92, "Block 92", "Green")
        self.greenTrack.addItem(block_92)
        self.greenBlocks[92] = block_92

        path_93 = QPainterPath()
        path_93.moveTo(-234, 503)
        path_93.quadTo(-234, 499, -231, 491)
        block_93 = self.createTrackBlock(path_93, "Block 93", "Green")
        self.greenTrack.addItem(block_93)
        self.greenBlocks[93] = block_93

        path_94 = QPainterPath()
        path_94.moveTo(-227, 482)
        path_94.quadTo(-224, 476, -218, 473)
        block_94 = self.createTrackBlock(path_94, "Block 94", "Green")
        self.greenTrack.addItem(block_94)
        self.greenBlocks[94] = block_94

        path_95 = QPainterPath()
        path_95.moveTo(-210, 469)
        path_95.quadTo(-203, 466, -196, 469)
        block_95 = self.createTrackBlock(path_95, "Block 95", "Green")
        self.greenTrack.addItem(block_95)
        self.greenBlocks[95] = block_95

        path_96 = QPainterPath()
        path_96.moveTo(-188, 473)
        path_96.quadTo(-182, 476, -179, 482)
        block_96 = self.createTrackBlock(path_96, "Block 96", "Green")
        self.greenTrack.addItem(block_96)
        self.greenBlocks[96] = block_96

        path_97 = QPainterPath()
        path_97.moveTo(-175, 491)
        path_97.quadTo(-172, 499, -172, 503)
        block_97 = self.createTrackBlock(path_97, "Block 97", "Green")
        self.greenTrack.addItem(block_97)
        self.greenBlocks[97] = block_97

        path_98 = QPainterPath()
        path_98.moveTo(-172, 512)
        path_98.quadTo(-171, 519, -168, 523)
        block_98 = self.createTrackBlock(path_98, "Block 98", "Green")
        self.greenTrack.addItem(block_98)
        self.greenBlocks[98] = block_98

        path_99 = QPainterPath()
        path_99.moveTo(-163, 530)
        path_99.quadTo(-157, 537, -155, 539)
        block_99 = self.createTrackBlock(path_99, "Block 99", "Green")
        self.greenTrack.addItem(block_99)
        self.greenBlocks[99] = block_99

        path_101 = QPainterPath()
        path_101.moveTo(24, 546)
        path_101.cubicTo(24, 545, 34, 530, 35, 530)
        block_101 = self.createTrackBlock(path_101, "Block 101", "Green")
        self.greenTrack.addItem(block_101)
        self.greenBlocks[101] = block_101

        path_102 = QPainterPath()
        path_102.moveTo(45, 530)
        path_102.lineTo(46, 530)
        block_102 = self.createTrackBlock(path_102, "Block 102", "Green")
        self.greenTrack.addItem(block_102)
        self.greenBlocks[102] = block_102

        path_103 = QPainterPath()
        path_103.moveTo(56, 530)
        path_103.lineTo(57, 530)
        block_103 = self.createTrackBlock(path_103, "Block 103", "Green")
        self.greenTrack.addItem(block_103)
        self.greenBlocks[103] = block_103

        path_104 = QPainterPath()
        path_104.moveTo(67, 530)
        path_104.lineTo(68, 530)
        block_104 = self.createTrackBlock(path_104, "Block 104", "Green")
        self.greenTrack.addItem(block_104)
        self.greenBlocks[104] = block_104

        path_105 = QPainterPath()
        path_105.moveTo(88, 525)
        path_105.cubicTo(84, 528, 79, 530, 78, 530)
        block_105 = self.createTrackBlock(path_105, "Block 105", "Green")
        self.greenTrack.addItem(block_105)
        self.greenBlocks[105] = block_105

        path_106 = QPainterPath()
        path_106.moveTo(101, 511)
        path_106.quadTo(97, 517, 95, 519)
        block_106 = self.createTrackBlock(path_106, "Block 106", "Green")
        self.greenTrack.addItem(block_106)
        self.greenBlocks[106] = block_106

        path_107 = QPainterPath()
        path_107.moveTo(111, 493)
        path_107.quadTo(109, 498, 106, 503)
        block_107 = self.createTrackBlock(path_107, "Block 107", "Green")
        self.greenTrack.addItem(block_107)
        self.greenBlocks[107] = block_107

        path_108 = QPainterPath()
        path_108.moveTo(118, 474)
        path_108.quadTo(117, 479, 115, 484)
        block_108 = self.createTrackBlock(path_108, "Block 108", "Green")
        self.greenTrack.addItem(block_108)
        self.greenBlocks[108] = block_108

        path_109 = QPainterPath()
        path_109.moveTo(121, 455)
        path_109.quadTo(121, 460, 120, 464)
        block_109 = self.createTrackBlock(path_109, "Block 109", "Green")
        self.greenTrack.addItem(block_109)
        self.greenBlocks[109] = block_109

        path_110 = QPainterPath()
        path_110.moveTo(121, 445)
        path_110.lineTo(121, 443)
        block_110 = self.createTrackBlock(path_110, "Block 110", "Green")
        self.greenTrack.addItem(block_110)
        self.greenBlocks[110] = block_110

        path_111 = QPainterPath()
        path_111.moveTo(121, 433)
        path_111.lineTo(121, 431)
        block_111 = self.createTrackBlock(path_111, "Block 111", "Green")
        self.greenTrack.addItem(block_111)
        self.greenBlocks[111] = block_111

        path_112 = QPainterPath()
        path_112.moveTo(121, 421)
        path_112.lineTo(121, 419)
        block_112 = self.createTrackBlock(path_112, "Block 112", "Green")
        self.greenTrack.addItem(block_112)
        self.greenBlocks[112] = block_112

        path_113 = QPainterPath()
        path_113.moveTo(121, 409)
        path_113.lineTo(121, 407)
        block_113 = self.createTrackBlock(path_113, "Block 113", "Green")
        self.greenTrack.addItem(block_113)
        self.greenBlocks[113] = block_113

        path_114 = QPainterPath()
        path_114.moveTo(121, 397)
        path_114.lineTo(121, 394)
        block_114 = self.createTrackBlock(path_114, "Block 114", "Green")
        self.greenTrack.addItem(block_114)
        self.greenBlocks[114] = block_114

        path_115 = QPainterPath()
        path_115.moveTo(121, 384)
        path_115.lineTo(121, 382)
        block_115 = self.createTrackBlock(path_115, "Block 115", "Green")
        self.greenTrack.addItem(block_115)
        self.greenBlocks[115] = block_115

        path_116 = QPainterPath()
        path_116.moveTo(121, 372)
        path_116.lineTo(121, 370)
        block_116 = self.createTrackBlock(path_116, "Block 116", "Green")
        self.greenTrack.addItem(block_116)
        self.greenBlocks[116] = block_116

        path_117 = QPainterPath()
        path_117.moveTo(119, 352)
        path_117.cubicTo(120, 354, 121, 358, 121, 360)
        block_117 = self.createTrackBlock(path_117, "Block 117", "Green")
        self.greenTrack.addItem(block_117)
        self.greenBlocks[117] = block_117

        path_118 = QPainterPath()
        path_118.moveTo(108, 335)
        path_118.quadTo(114, 342, 115, 344)
        block_118 = self.createTrackBlock(path_118, "Block 118", "Green")
        self.greenTrack.addItem(block_118)
        self.greenBlocks[118] = block_118

        path_119 = QPainterPath()
        path_119.moveTo(94, 323)
        path_119.quadTo(100, 327, 101, 328)
        block_119 = self.createTrackBlock(path_119, "Block 119", "Green")
        self.greenTrack.addItem(block_119)
        self.greenBlocks[119] = block_119

        path_120 = QPainterPath()
        path_120.moveTo(78, 313)
        path_120.quadTo(83, 315, 86, 317)
        block_120 = self.createTrackBlock(path_120, "Block 120", "Green")
        self.greenTrack.addItem(block_120)
        self.greenBlocks[120] = block_120

        path_121 = QPainterPath()
        path_121.moveTo(64, 308)
        path_121.quadTo(65, 308, 69, 309)
        block_121 = self.createTrackBlock(path_121, "Block 121", "Green")
        self.greenTrack.addItem(block_121)
        self.greenBlocks[121] = block_121

        path_122 = QPainterPath()
        path_122.moveTo(54, 308)
        path_122.lineTo(53, 308)
        block_122 = self.createTrackBlock(path_122, "Block 122", "Green")
        self.greenTrack.addItem(block_122)
        self.greenBlocks[122] = block_122

        path_123 = QPainterPath()
        path_123.moveTo(43, 308)
        path_123.lineTo(42, 308)
        block_123 = self.createTrackBlock(path_123, "Block 123", "Green")
        self.greenTrack.addItem(block_123)
        self.greenBlocks[123] = block_123

        path_124 = QPainterPath()
        path_124.moveTo(32, 308)
        path_124.lineTo(31, 308)
        block_124 = self.createTrackBlock(path_124, "Block 124", "Green")
        self.greenTrack.addItem(block_124)
        self.greenBlocks[124] = block_124

        path_125 = QPainterPath()
        path_125.moveTo(21, 308)
        path_125.lineTo(20, 308)
        block_125 = self.createTrackBlock(path_125, "Block 125", "Green")
        self.greenTrack.addItem(block_125)
        self.greenBlocks[125] = block_125

        path_126 = QPainterPath()
        path_126.moveTo(10, 308)
        path_126.lineTo(9, 308)
        block_126 = self.createTrackBlock(path_126, "Block 126", "Green")
        self.greenTrack.addItem(block_126)
        self.greenBlocks[126] = block_126

        path_127 = QPainterPath()
        path_127.moveTo(-1, 308)
        path_127.lineTo(-2, 308)
        block_127 = self.createTrackBlock(path_127, "Block 127", "Green")
        self.greenTrack.addItem(block_127)
        self.greenBlocks[127] = block_127

        path_128 = QPainterPath()
        path_128.moveTo(-12, 308)
        path_128.lineTo(-13, 308)
        block_128 = self.createTrackBlock(path_128, "Block 128", "Green")
        self.greenTrack.addItem(block_128)
        self.greenBlocks[128] = block_128

        path_129 = QPainterPath()
        path_129.moveTo(-23, 308)
        path_129.lineTo(-24, 308)
        block_129 = self.createTrackBlock(path_129, "Block 129", "Green")
        self.greenTrack.addItem(block_129)
        self.greenBlocks[129] = block_129

        path_130 = QPainterPath()
        path_130.moveTo(-34, 308)
        path_130.lineTo(-35, 308)
        block_130 = self.createTrackBlock(path_130, "Block 130", "Green")
        self.greenTrack.addItem(block_130)
        self.greenBlocks[130] = block_130

        path_131 = QPainterPath()
        path_131.moveTo(-45, 308)
        path_131.lineTo(-46, 308)
        block_131 = self.createTrackBlock(path_131, "Block 131", "Green")
        self.greenTrack.addItem(block_131)
        self.greenBlocks[131] = block_131

        path_132 = QPainterPath()
        path_132.moveTo(-56, 308)
        path_132.lineTo(-57, 308)
        block_132 = self.createTrackBlock(path_132, "Block 132", "Green")
        self.greenTrack.addItem(block_132)
        self.greenBlocks[132] = block_132

        path_133 = QPainterPath()
        path_133.moveTo(-66, 308)
        path_133.lineTo(-67, 308)
        block_133 = self.createTrackBlock(path_133, "Block 133", "Green")
        self.greenTrack.addItem(block_133)
        self.greenBlocks[133] = block_133

        path_134 = QPainterPath()
        path_134.moveTo(-77, 308)
        path_134.lineTo(-78, 308)
        block_134 = self.createTrackBlock(path_134, "Block 134", "Green")
        self.greenTrack.addItem(block_134)
        self.greenBlocks[134] = block_134

        path_135 = QPainterPath()
        path_135.moveTo(-88, 308)
        path_135.lineTo(-89, 308)
        block_135 = self.createTrackBlock(path_135, "Block 135", "Green")
        self.greenTrack.addItem(block_135)
        self.greenBlocks[135] = block_135

        path_136 = QPainterPath()
        path_136.moveTo(-99, 308)
        path_136.lineTo(-100, 308)
        block_136 = self.createTrackBlock(path_136, "Block 136", "Green")
        self.greenTrack.addItem(block_136)
        self.greenBlocks[136] = block_136

        path_137 = QPainterPath()
        path_137.moveTo(-110, 308)
        path_137.lineTo(-111, 308)
        block_137 = self.createTrackBlock(path_137, "Block 137", "Green")
        self.greenTrack.addItem(block_137)
        self.greenBlocks[137] = block_137

        path_138 = QPainterPath()
        path_138.moveTo(-121, 308)
        path_138.lineTo(-122, 308)
        block_138 = self.createTrackBlock(path_138, "Block 138", "Green")
        self.greenTrack.addItem(block_138)
        self.greenBlocks[138] = block_138

        path_139 = QPainterPath()
        path_139.moveTo(-132, 308)
        path_139.lineTo(-133, 308)
        block_139 = self.createTrackBlock(path_139, "Block 139", "Green")
        self.greenTrack.addItem(block_139)
        self.greenBlocks[139] = block_139

        path_140 = QPainterPath()
        path_140.moveTo(-143, 308)
        path_140.lineTo(-144, 308)
        block_140 = self.createTrackBlock(path_140, "Block 140", "Green")
        self.greenTrack.addItem(block_140)
        self.greenBlocks[140] = block_140

        path_141 = QPainterPath()
        path_141.moveTo(-154, 308)
        path_141.lineTo(-155, 308)
        block_141 = self.createTrackBlock(path_141, "Block 141", "Green")
        self.greenTrack.addItem(block_141)
        self.greenBlocks[141] = block_141

        path_142 = QPainterPath()
        path_142.moveTo(-165, 308)
        path_142.lineTo(-166, 308)
        block_142 = self.createTrackBlock(path_142, "Block 142", "Green")
        self.greenTrack.addItem(block_142)
        self.greenBlocks[142] = block_142

        path_143 = QPainterPath()
        path_143.moveTo(-176, 308)
        path_143.lineTo(-177, 308)
        block_143 = self.createTrackBlock(path_143, "Block 143", "Green")
        self.greenTrack.addItem(block_143)
        self.greenBlocks[143] = block_143

        path_144 = QPainterPath()
        path_144.moveTo(-192, 307)
        path_144.quadTo(-191, 308, -187, 308)
        block_144 = self.createTrackBlock(path_144, "Block 144", "Green")
        self.greenTrack.addItem(block_144)
        self.greenBlocks[144] = block_144

        path_145 = QPainterPath()
        path_145.moveTo(-202, 296)
        path_145.quadTo(-201, 298, -199, 300)
        block_145 = self.createTrackBlock(path_145, "Block 145", "Green")
        self.greenTrack.addItem(block_145)
        self.greenBlocks[145] = block_145

        path_146 = QPainterPath()
        path_146.moveTo(-207, 283)
        path_146.quadTo(-207, 285, -206, 288)
        block_146 = self.createTrackBlock(path_146, "Block 146", "Green")
        self.greenTrack.addItem(block_146)
        self.greenBlocks[146] = block_146

        path_147 = QPainterPath()
        path_147.moveTo(-207, 273)
        path_147.lineTo(-207, 268)
        block_147 = self.createTrackBlock(path_147, "Block 147", "Green")
        self.greenTrack.addItem(block_147)
        self.greenBlocks[147] = block_147

        path_148 = QPainterPath()
        path_148.moveTo(-207, 258)
        path_148.lineTo(-207, 240)
        block_148 = self.createTrackBlock(path_148, "Block 148", "Green")
        self.greenTrack.addItem(block_148)
        self.greenBlocks[148] = block_148

        path_149 = QPainterPath()
        path_149.moveTo(-207, 230)
        path_149.lineTo(-207, 225)
        block_149 = self.createTrackBlock(path_149, "Block 149", "Green")
        self.greenTrack.addItem(block_149)
        self.greenBlocks[149] = block_149

        path_150 = QPainterPath()
        path_150.moveTo(-207, 215)
        path_150.cubicTo(-207, 214, -179, 200, -177, 200)
        block_150 = self.createTrackBlock(path_150, "Block 150", "Green")
        self.greenTrack.addItem(block_150)
        self.greenBlocks[150] = block_150

        #SWITCHES -> 0 by default, means continuation of number
        switchPath13 = QPainterPath()
        switchPath13.moveTo(-25, 0)
        switchPath13.cubicTo(-10, 0, 10, 1, 23, 2)
        switch13 = self.createSwitch(switchPath13)
        self.greenTrack.addItem(switch13)
        self.greenSwitches[13] = switch13

        switchPath29 = QPainterPath()
        switchPath29.moveTo(-167, 193)
        switchPath29.lineTo(-167, 213)
        switch29 = self.createSwitch(switchPath29)
        self.greenTrack.addItem(switch29)
        self.greenSwitches[29] = switch29

        switchPath57 = QPainterPath()
        switchPath57.moveTo(95, 278)
        switchPath57.quadTo(107, 278, 111, 279)
        switch57 = self.createSwitch(switchPath57)
        self.greenTrack.addItem(switch57)
        self.greenSwitches[57] = switch57

        switchPath63 = QPainterPath()
        switchPath63.moveTo(163, 350)
        switchPath63.cubicTo(163, 340, 163, 330, 161, 322)
        switch63 = self.createSwitch(switchPath63)
        self.greenTrack.addItem(switch63)
        self.greenSwitches[63] = switch63

        switchPath77 = QPainterPath()
        switchPath77.moveTo(12, 556)
        switchPath77.lineTo(50, 556)
        switch77 = self.createSwitch(switchPath77)
        self.greenTrack.addItem(switch77)
        self.greenSwitches[77] = switch77

        switchpath85 = QPainterPath()
        switchpath85.moveTo(-124, 556)
        switchpath85.lineTo(-149, 556)
        switch85 = self.createSwitch(switchpath85)
        self.greenTrack.addItem(switch85)
        self.greenSwitches[85] = switch85        

        #CROSSING
        crossing = QPixmap("src/main/TrackModel/pngs/crossing.png")
        crossing = crossing.scaledToWidth(70)
        self.greenCrossing = QGraphicsPixmapItem(crossing)
        self.greenCrossing.setPos(-210, -20)
        self.greenTrack.addItem(self.greenCrossing)

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
        lightCircle150 = lightCircle150.scaledToWidth(17)
        circle150 = QGraphicsPixmapItem(lightCircle150)
        circle150.setPos(-216, 165)
        self.greenTrack.addItem(circle150)
        light150 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light150 = light150.scaledToWidth(35)
        signal150 = QGraphicsPixmapItem(light150)
        signal150.setPos(-225, 161)
        self.greenTrack.addItem(signal150)

        lightPole0 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole0 = lightPole0.scaledToWidth(15)
        pole0 = QGraphicsPixmapItem(lightPole0)
        pole0.setPos(175, 310)
        self.greenTrack.addItem(pole0)
        lightCircle0 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle0 = lightCircle0.scaledToWidth(17)
        circle0 = QGraphicsPixmapItem(lightCircle0)
        circle0.setPos(174, 295)
        self.greenTrack.addItem(circle0)
        light0 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light0 = light0.scaledToWidth(35)
        signal0 = QGraphicsPixmapItem(light0)
        signal0.setPos(165, 291)
        self.greenTrack.addItem(signal0)

        lightPole76 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole76 = lightPole76.scaledToWidth(15)
        pole76 = QGraphicsPixmapItem(lightPole76)
        pole76.setPos(30, 580)
        self.greenTrack.addItem(pole76)
        lightCircle76 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle76 = lightCircle76.scaledToWidth(17)
        circle76 = QGraphicsPixmapItem(lightCircle76)
        circle76.setPos(29, 565)
        self.greenTrack.addItem(circle76)
        light76 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light76 = light76.scaledToWidth(35)
        signal76 = QGraphicsPixmapItem(light76)
        signal76.setPos(20, 561)
        self.greenTrack.addItem(signal76)

        lightPole100 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole100 = lightPole100.scaledToWidth(15)
        pole100 = QGraphicsPixmapItem(lightPole100)
        pole100.setPos(-142, 520)
        self.greenTrack.addItem(pole100)
        lightCircle100 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle100 = lightCircle100.scaledToWidth(17)
        circle100 = QGraphicsPixmapItem(lightCircle100)
        circle100.setPos(-143, 505)
        self.greenTrack.addItem(circle100)
        light100 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light100 = light100.scaledToWidth(35)
        signal100 = QGraphicsPixmapItem(light100)
        signal100.setPos(-152, 501)
        self.greenTrack.addItem(signal100)
        
        #STATIONS AND BEACONS
        station = QPixmap("src/main/TrackModel/pngs/station.png")
        station = station.scaledToWidth(20)
        beacon = QPixmap("src/main/TrackModel/pngs/beacon.png")
        beacon = beacon.scaledToWidth(10)
        
        pioneer = QGraphicsPixmapItem(station)
        pioneer.setPos(30, 15)
        self.greenTrack.addItem(pioneer)
        pioneerBeacon = QGraphicsPixmapItem(beacon)
        pioneerBeacon.setPos(12, 18)
        self.greenTrack.addItem(pioneerBeacon)
        
        edgebrook = QGraphicsPixmapItem(station)
        edgebrook.setPos(86, -15)
        self.greenTrack.addItem(edgebrook)
        edgebrookBeacon = QGraphicsPixmapItem(beacon)
        edgebrookBeacon.setPos(83, 7)
        self.greenTrack.addItem(edgebrookBeacon)
        
        _station = QGraphicsPixmapItem(station)
        _station.setPos(-102, -27)
        self.greenTrack.addItem(_station)
        _stationBeacon = QGraphicsPixmapItem(beacon)
        _stationBeacon.setPos(-97, -5)
        self.greenTrack.addItem(_stationBeacon)
        
        whited = QGraphicsPixmapItem(station)
        whited.setPos(-160, 80)
        self.greenTrack.addItem(whited)
        whitedBeacon = QGraphicsPixmapItem(beacon)
        whitedBeacon.setPos(-172, 86)
        self.greenTrack.addItem(whitedBeacon)
        
        southbank = QGraphicsPixmapItem(station)
        southbank.setPos(-160, 215)
        self.greenTrack.addItem(southbank)
        southbankBeacon = QGraphicsPixmapItem(beacon)
        southbankBeacon.setPos(-172, 221)
        self.greenTrack.addItem(southbankBeacon)
        
        southbank = QGraphicsPixmapItem(station)
        southbank.setPos(-160, 215)
        self.greenTrack.addItem(southbank)
        southbankBeacon = QGraphicsPixmapItem(beacon)
        southbankBeacon.setPos(-172, 221)
        self.greenTrack.addItem(southbankBeacon)
        
        central = QGraphicsPixmapItem(station)
        central.setPos(-138, 283)
        self.greenTrack.addItem(central)
        centralBeacon1 = QGraphicsPixmapItem(beacon)
        centralBeacon1.setPos(-107, 273)
        centralBeacon2 = QGraphicsPixmapItem(beacon)
        centralBeacon2.setPos(-160, 303)
        self.greenTrack.addItem(centralBeacon1)
        self.greenTrack.addItem(centralBeacon2)
        
        inglewood = QGraphicsPixmapItem(station)
        inglewood.setPos(-40, 283)
        self.greenTrack.addItem(inglewood)
        inglewoodBeacon1 = QGraphicsPixmapItem(beacon)
        inglewoodBeacon1.setPos(-8, 273)
        inglewoodBeacon2 = QGraphicsPixmapItem(beacon)
        inglewoodBeacon2.setPos(-61, 303)
        self.greenTrack.addItem(inglewoodBeacon1)
        self.greenTrack.addItem(inglewoodBeacon2)
        
        overbrook = QGraphicsPixmapItem(station)
        overbrook.setPos(60, 283)
        self.greenTrack.addItem(overbrook)
        overbrookBeacon1 = QGraphicsPixmapItem(beacon)
        overbrookBeacon1.setPos(91, 273)
        overbrookBeacon2 = QGraphicsPixmapItem(beacon)
        overbrookBeacon2.setPos(38, 303)
        self.greenTrack.addItem(overbrookBeacon1)
        self.greenTrack.addItem(overbrookBeacon2)
        
        glenbury = QGraphicsPixmapItem(station)
        glenbury.setPos(133, 381)
        self.greenTrack.addItem(glenbury)
        glenburyBeacon1 = QGraphicsPixmapItem(beacon)
        glenburyBeacon1.setPos(158, 385)
        glenburyBeacon2 = QGraphicsPixmapItem(beacon)
        glenburyBeacon2.setPos(116, 390)
        self.greenTrack.addItem(glenburyBeacon1)
        self.greenTrack.addItem(glenburyBeacon2)
        
        dormont = QGraphicsPixmapItem(station)
        dormont.setPos(93, 530)
        self.greenTrack.addItem(dormont)
        dormontBeacon1 = QGraphicsPixmapItem(beacon)
        dormontBeacon1.setPos(121, 549)
        dormontBeacon2 = QGraphicsPixmapItem(beacon)
        dormontBeacon2.setPos(78, 523)
        self.greenTrack.addItem(dormontBeacon1)
        self.greenTrack.addItem(dormontBeacon2)
        
        mtlebanon = QGraphicsPixmapItem(station)
        mtlebanon.setPos(-5, 530)
        self.greenTrack.addItem(mtlebanon)
        mtlebanonBeacon = QGraphicsPixmapItem(beacon)
        mtlebanonBeacon.setPos(10, 551)
        self.greenTrack.addItem(mtlebanonBeacon)
        
        poplar = QGraphicsPixmapItem(station)
        poplar.setPos(-186, 530)
        self.greenTrack.addItem(poplar)
        poplarBeacon = QGraphicsPixmapItem(beacon)
        poplarBeacon.setPos(-181, 551)
        self.greenTrack.addItem(poplarBeacon)
        
        castleshannon = QGraphicsPixmapItem(station)
        castleshannon.setPos(-182, 450)
        self.greenTrack.addItem(castleshannon)
        castleshannonBeacon = QGraphicsPixmapItem(beacon)
        castleshannonBeacon.setPos(-188, 472)
        self.greenTrack.addItem(castleshannonBeacon)
        
        #Box where block numbers are displayed
        box = QGraphicsRectItem(-75, 150, 60, 20)
        box.setPen(QPen(QColor(0, 0, 0), 3))
        box.setBrush(QBrush(QColor(0, 255, 0, 20)))
        self.greenTrack.addItem(box)

    def drawRedLine(self):
        self.setScene(self.redTrack)

        yardImage = QPixmap("src/main/TrackModel/pngs/yard.jpg")
        yardImage = yardImage.scaledToWidth(100)
        yardScene = QGraphicsPixmapItem(yardImage)
        yardScene.setPos(50, 35)
        self.redTrack.addItem(yardScene)

        path_0 = QPainterPath()
        path_0.moveTo(119, -42)
        path_0.quadTo(118, -42, 110, 30)
        block_0 = self.createTrackBlock(path_0, "Block 0")
        self.redTrack.addItem(block_0)
        self.redBlocks[0] = block_0

        path_1 = QPainterPath()
        path_1.moveTo(7, -4)
        path_1.quadTo(20, -12, 22, -14)
        block_1 = self.createTrackBlock(path_1, "Block 1")
        self.redTrack.addItem(block_1)
        self.redBlocks[1] = block_1

        path_2 = QPainterPath()
        path_2.moveTo(29, -20)
        path_2.quadTo(34, -24, 36, -27)
        block_2 = self.createTrackBlock(path_2, "Block 2")
        self.redTrack.addItem(block_2)
        self.redBlocks[2] = block_2

        path_3 = QPainterPath()
        path_3.moveTo(41, -35)
        path_3.cubicTo(43, -38, 44, -41, 44, -42)
        block_3 = self.createTrackBlock(path_3, "Block 3")
        self.redTrack.addItem(block_3)
        self.redBlocks[3] = block_3

        path_4 = QPainterPath()
        path_4.moveTo(44, -52)
        path_4.cubicTo(44, -53, 45, -56, 47, -59)
        block_4 = self.createTrackBlock(path_4, "Block 4")
        self.redTrack.addItem(block_4)
        self.redBlocks[4] = block_4

        path_5 = QPainterPath()
        path_5.moveTo(51, -66)
        path_5.quadTo(53, -69, 58, -73)
        block_5 = self.createTrackBlock(path_5, "Block 5")
        self.redTrack.addItem(block_5)
        self.redBlocks[5] = block_5

        path_6 = QPainterPath()
        path_6.moveTo(65, -79)
        path_6.quadTo(67, -81, 75, -82)
        block_6 = self.createTrackBlock(path_6, "Block 6")
        self.redTrack.addItem(block_6)
        self.redBlocks[6] = block_6

        path_7 = QPainterPath()
        path_7.moveTo(84, -82)
        path_7.quadTo(95, -81, 97, -79)
        block_7 = self.createTrackBlock(path_7, "Block 7")
        self.redTrack.addItem(block_7)
        self.redBlocks[7] = block_7

        path_8 = QPainterPath()
        path_8.moveTo(105, -73)
        path_8.quadTo(111, -68, 112, -66)
        block_8 = self.createTrackBlock(path_8, "Block 8")
        self.redTrack.addItem(block_8)
        self.redBlocks[8] = block_8

        path_9 = QPainterPath()
        path_9.moveTo(116, -59)
        path_9.cubicTo(118, -56, 119, -53, 119, -52)
        block_9 = self.createTrackBlock(path_9, "Block 9")
        self.redTrack.addItem(block_9)
        self.redBlocks[9] = block_9

        path_10 = QPainterPath()
        path_10.moveTo(119, -42)
        path_10.cubicTo(119, -41, 116, -34, 114, -29)
        block_10 = self.createTrackBlock(path_10, "Block 10")
        self.redTrack.addItem(block_10)
        self.redBlocks[10] = block_10

        path_11 = QPainterPath()
        path_11.moveTo(109, -21)
        path_11.quadTo(105, -15, 96, -10)
        block_11 = self.createTrackBlock(path_11, "Block 11")
        self.redTrack.addItem(block_11)
        self.redBlocks[11] = block_11

        path_12 = QPainterPath()
        path_12.moveTo(88, -6)
        path_12.cubicTo(85, -5, 76, 0, 70, 0)
        block_12 = self.createTrackBlock(path_12, "Block 12")
        self.redTrack.addItem(block_12)
        self.redBlocks[12] = block_12

        path_13 = QPainterPath()
        path_13.moveTo(60, 0)
        path_13.lineTo(50, 0)
        block_13 = self.createTrackBlock(path_13, "Block 13")
        self.redTrack.addItem(block_13)
        self.redBlocks[13] = block_13

        path_14 = QPainterPath()
        path_14.moveTo(40, 0)
        path_14.lineTo(30, 0)
        block_14 = self.createTrackBlock(path_14, "Block 14")
        self.redTrack.addItem(block_14)
        self.redBlocks[14] = block_14

        path_15 = QPainterPath()
        path_15.moveTo(20, 0)
        path_15.lineTo(10, 0)
        block_15 = self.createTrackBlock(path_15, "Block 15")
        self.redTrack.addItem(block_15)
        self.redBlocks[15] = block_15

        path_16 = QPainterPath()
        path_16.moveTo(0, 0)
        path_16.lineTo(-1, 0)
        block_16 = self.createTrackBlock(path_16, "Block 16")
        self.redTrack.addItem(block_16)
        self.redBlocks[16] = block_16

        path_17 = QPainterPath()
        path_17.moveTo(-11, 0)
        path_17.lineTo(-13, 0)
        block_17 = self.createTrackBlock(path_17, "Block 17")
        self.redTrack.addItem(block_17)
        self.redBlocks[17] = block_17

        path_18 = QPainterPath()
        path_18.moveTo(-23, 0)
        path_18.lineTo(-27, 0)
        block_18 = self.createTrackBlock(path_18, "Block 18")
        self.redTrack.addItem(block_18)
        self.redBlocks[18] = block_18

        path_19 = QPainterPath()
        path_19.moveTo(-37, 0)
        path_19.lineTo(-41, 0)
        block_19 = self.createTrackBlock(path_19, "Block 19")
        self.redTrack.addItem(block_19)
        self.redBlocks[19] = block_19

        path_20 = QPainterPath()
        path_20.moveTo(-51, 0)
        path_20.lineTo(-53, 0)
        block_20 = self.createTrackBlock(path_20, "Block 20")
        self.redTrack.addItem(block_20)
        self.redBlocks[20] = block_20

        path_21 = QPainterPath()
        path_21.moveTo(-63, 0)
        path_21.cubicTo(-64, 0, -68, 1, -71, 3)
        block_21 = self.createTrackBlock(path_21, "Block 21")
        self.redTrack.addItem(block_21)
        self.redBlocks[21] = block_21

        path_22 = QPainterPath()
        path_22.moveTo(-79, 8)
        path_22.quadTo(-84, 12, -86, 14)
        block_22 = self.createTrackBlock(path_22, "Block 22")
        self.redTrack.addItem(block_22)
        self.redBlocks[22] = block_22

        path_23 = QPainterPath()
        path_23.moveTo(-91, 20)
        path_23.cubicTo(-93, 23, -94, 27, -94, 28)
        block_23 = self.createTrackBlock(path_23, "Block 23")
        self.redTrack.addItem(block_23)
        self.redBlocks[23] = block_23

        path_24 = QPainterPath()
        path_24.moveTo(-94, 38)
        path_24.lineTo(-94, 39)
        block_24 = self.createTrackBlock(path_24, "Block 24")
        self.redTrack.addItem(block_24)
        self.redBlocks[24] = block_24

        path_25 = QPainterPath()
        path_25.moveTo(-94, 49)
        path_25.lineTo(-94, 50)
        block_25 = self.createTrackBlock(path_25, "Block 25")
        self.redTrack.addItem(block_25)
        self.redBlocks[25] = block_25

        path_26 = QPainterPath()
        path_26.moveTo(-94, 60)
        path_26.lineTo(-94, 61)
        block_26 = self.createTrackBlock(path_26, "Block 26")
        self.redTrack.addItem(block_26)
        self.redBlocks[26] = block_26

        path_27 = QPainterPath()
        path_27.moveTo(-94, 71)
        path_27.lineTo(-94, 72)
        block_27 = self.createTrackBlock(path_27, "Block 27")
        self.redTrack.addItem(block_27)
        self.redBlocks[27] = block_27

        path_28 = QPainterPath()
        path_28.moveTo(-94, 82)
        path_28.lineTo(-94, 83)
        block_28 = self.createTrackBlock(path_28, "Block 28")
        self.redTrack.addItem(block_28)
        self.redBlocks[28] = block_28

        path_29 = QPainterPath()
        path_29.moveTo(-94, 93)
        path_29.lineTo(-94, 94)
        block_29 = self.createTrackBlock(path_29, "Block 29")
        self.redTrack.addItem(block_29)
        self.redBlocks[29] = block_29

        path_30 = QPainterPath()
        path_30.moveTo(-94, 104)
        path_30.lineTo(-94, 105)
        block_30 = self.createTrackBlock(path_30, "Block 30")
        self.redTrack.addItem(block_30)
        self.redBlocks[30] = block_30

        path_31 = QPainterPath()
        path_31.moveTo(-94, 115)
        path_31.lineTo(-94, 116)
        block_31 = self.createTrackBlock(path_31, "Block 31")
        self.redTrack.addItem(block_31)
        self.redBlocks[31] = block_31
        
        path_32 = QPainterPath()
        path_32.moveTo(-94, 126)
        path_32.lineTo(-94, 127)
        block_32 = self.createTrackBlock(path_32, "Block 32")
        self.redTrack.addItem(block_32)
        self.redBlocks[32] = block_32

        path_33 = QPainterPath()
        path_33.moveTo(-94, 137)
        path_33.lineTo(-94, 138)
        block_33 = self.createTrackBlock(path_33, "Block 33")
        self.redTrack.addItem(block_33)
        self.redBlocks[33] = block_33

        path_34 = QPainterPath()
        path_34.moveTo(-94, 148)
        path_34.lineTo(-94, 149)
        block_34 = self.createTrackBlock(path_34, "Block 34")
        self.redTrack.addItem(block_34)
        self.redBlocks[34] = block_34

        path_35 = QPainterPath()
        path_35.moveTo(-94, 159)
        path_35.lineTo(-94, 160)
        block_35 = self.createTrackBlock(path_35, "Block 35")
        self.redTrack.addItem(block_35)
        self.redBlocks[35] = block_35

        path_36 = QPainterPath()
        path_36.moveTo(-94, 170)
        path_36.lineTo(-94, 171)
        block_36 = self.createTrackBlock(path_36, "Block 36")
        self.redTrack.addItem(block_36)
        self.redBlocks[36] = block_36

        path_37 = QPainterPath()
        path_37.moveTo(-94, 181)
        path_37.lineTo(-94, 182)
        block_37 = self.createTrackBlock(path_37, "Block 37")
        self.redTrack.addItem(block_37)
        self.redBlocks[37] = block_37

        path_38 = QPainterPath()
        path_38.moveTo(-94, 192)
        path_38.lineTo(-94, 193)
        block_38 = self.createTrackBlock(path_38, "Block 38")
        self.redTrack.addItem(block_38)
        self.redBlocks[38] = block_38

        path_39 = QPainterPath()
        path_39.moveTo(-94, 203)
        path_39.lineTo(-94, 204)
        block_39 = self.createTrackBlock(path_39, "Block 39")
        self.redTrack.addItem(block_39)
        self.redBlocks[39] = block_39

        path_40 = QPainterPath()
        path_40.moveTo(-94, 214)
        path_40.lineTo(-94, 215)
        block_40 = self.createTrackBlock(path_40, "Block 40")
        self.redTrack.addItem(block_40)
        self.redBlocks[40] = block_40
        
        path_41 = QPainterPath()
        path_41.moveTo(-94, 225)
        path_41.lineTo(-94, 226)
        block_41 = self.createTrackBlock(path_41, "Block 41")
        self.redTrack.addItem(block_41)
        self.redBlocks[41] = block_41

        path_42 = QPainterPath()
        path_42.moveTo(-94, 236)
        path_42.lineTo(-94, 237)
        block_42 = self.createTrackBlock(path_42, "Block 42")
        self.redTrack.addItem(block_42)
        self.redBlocks[42] = block_42

        path_43 = QPainterPath()
        path_43.moveTo(-94, 247)
        path_43.lineTo(-94, 248)
        block_43 = self.createTrackBlock(path_43, "Block 43")
        self.redTrack.addItem(block_43)
        self.redBlocks[43] = block_43

        path_44 = QPainterPath()
        path_44.moveTo(-94, 258)
        path_44.lineTo(-94, 259)
        block_44 = self.createTrackBlock(path_44, "Block 44")
        self.redTrack.addItem(block_44)
        self.redBlocks[44] = block_44

        path_45 = QPainterPath()
        path_45.moveTo(-94, 269)
        path_45.lineTo(-94, 270)
        block_45 = self.createTrackBlock(path_45, "Block 45")
        self.redTrack.addItem(block_45)
        self.redBlocks[45] = block_45

        path_46 = QPainterPath()
        path_46.moveTo(-94, 280)
        path_46.cubicTo(-94, 282, -96, 290, -100, 296)
        block_46 = self.createTrackBlock(path_46, "Block 46")
        self.redTrack.addItem(block_46)
        self.redBlocks[46] = block_46

        path_47 = QPainterPath()
        path_47.moveTo(-105, 302)
        path_47.quadTo(-109, 307, -120, 316)
        block_47 = self.createTrackBlock(path_47, "Block 47")
        self.redTrack.addItem(block_47)
        self.redBlocks[47] = block_47

        path_48 = QPainterPath()
        path_48.moveTo(-127, 321)
        path_48.cubicTo(-133, 325, -141, 327, -143, 327)
        block_48 = self.createTrackBlock(path_48, "Block 48")
        self.redTrack.addItem(block_48)
        self.redBlocks[48] = block_48

        path_49 = QPainterPath()
        path_49.moveTo(-152, 327)
        path_49.lineTo(-160, 327)
        block_49 = self.createTrackBlock(path_49, "Block 49")
        self.redTrack.addItem(block_49)
        self.redBlocks[49] = block_49

        path_50 = QPainterPath()
        path_50.moveTo(-170, 327)
        path_50.lineTo(-178, 327)
        block_50 = self.createTrackBlock(path_50, "Block 50")
        self.redTrack.addItem(block_50)
        self.redBlocks[50] = block_50

        path_51 = QPainterPath()
        path_51.moveTo(-188, 327)
        path_51.lineTo(-196, 327)
        block_51 = self.createTrackBlock(path_51, "Block 51")
        self.redTrack.addItem(block_51)
        self.redBlocks[51] = block_51

        #Hide underneath block 52
        path_66 = QPainterPath()
        path_66.moveTo(-225, 314)
        path_66.quadTo(-223, 318, -220, 322)
        block_66 = self.createTrackBlock(path_66, "Block 66")
        self.redTrack.addItem(block_66)
        self.redBlocks[66] = block_66

        path_52 = QPainterPath()
        path_52.moveTo(-206, 327)
        path_52.lineTo(-214, 327)
        block_52 = self.createTrackBlock(path_52, "Block 52")
        self.redTrack.addItem(block_52)
        self.redBlocks[52] = block_52

        path_53 = QPainterPath()
        path_53.moveTo(-224, 327)
        path_53.lineTo(-232, 327)
        block_53 = self.createTrackBlock(path_53, "Block 53")
        self.redTrack.addItem(block_53)
        self.redBlocks[53] = block_53

        path_54 = QPainterPath()
        path_54.moveTo(-242, 327)
        path_54.lineTo(-250, 327)
        block_54 = self.createTrackBlock(path_54, "Block 54")
        self.redTrack.addItem(block_54)
        self.redBlocks[54] = block_54

        path_55 = QPainterPath()
        path_55.moveTo(-260, 327)
        path_55.cubicTo(-261, 327, -270, 325, -276, 317)
        block_55 = self.createTrackBlock(path_55, "Block 55")
        self.redTrack.addItem(block_55)
        self.redBlocks[55] = block_55

        path_56 = QPainterPath()
        path_56.moveTo(-282, 309)
        path_56.quadTo(-289, 300, -293, 292)
        block_56 = self.createTrackBlock(path_56, "Block 56")
        self.redTrack.addItem(block_56)
        self.redBlocks[56] = block_56

        path_57 = QPainterPath()
        path_57.moveTo(-297, 283)
        path_57.cubicTo(-301, 274, -302, 264, -302, 262)
        block_57 = self.createTrackBlock(path_57, "Block 57")
        self.redTrack.addItem(block_57)
        self.redBlocks[57] = block_57

        path_58 = QPainterPath()
        path_58.moveTo(-302, 252)
        path_58.cubicTo(-302, 250, -301, 243, -299, 237)
        block_58 = self.createTrackBlock(path_58, "Block 58")
        self.redTrack.addItem(block_58)
        self.redBlocks[58] = block_58

        path_59 = QPainterPath()
        path_59.moveTo(-296, 229)
        path_59.quadTo(-294, 223, -290, 219)
        block_59 = self.createTrackBlock(path_59, "Block 59")
        self.redTrack.addItem(block_59)
        self.redBlocks[59] = block_59

        path_60 = QPainterPath()
        path_60.moveTo(-286, 215)
        path_60.cubicTo(-282, 211, -276, 210, -275, 210)
        block_60 = self.createTrackBlock(path_60, "Block 60")
        self.redTrack.addItem(block_60)
        self.redBlocks[60] = block_60

        path_61 = QPainterPath()
        path_61.moveTo(-265, 210)
        path_61.cubicTo(-264, 210, -252, 214, -249, 220)
        block_61 = self.createTrackBlock(path_61, "Block 61")
        self.redTrack.addItem(block_61)
        self.redBlocks[61] = block_61

        path_62 = QPainterPath()
        path_62.moveTo(-245, 228)
        path_62.quadTo(-242, 234, -240, 243)
        block_62 = self.createTrackBlock(path_62, "Block 62")
        self.redTrack.addItem(block_62)
        self.redBlocks[62] = block_62

        path_63 = QPainterPath()
        path_63.moveTo(-238, 252)
        path_63.quadTo(-236, 261, -236, 268)
        block_63 = self.createTrackBlock(path_63, "Block 63")
        self.redTrack.addItem(block_63)
        self.redBlocks[63] = block_63

        path_64 = QPainterPath()
        path_64.moveTo(-236, 278)
        path_64.quadTo(-236, 279, -234, 288)
        block_64 = self.createTrackBlock(path_64, "Block 64")
        self.redTrack.addItem(block_64)
        self.redBlocks[64] = block_64

        path_65 = QPainterPath()
        path_65.moveTo(-232, 295)
        path_65.quadTo(-230, 304, -229, 306)
        block_65 = self.createTrackBlock(path_65, "Block 65")
        self.redTrack.addItem(block_65)
        self.redBlocks[65] = block_65

        path_67 = QPainterPath()
        path_67.moveTo(-104, 253)
        path_67.cubicTo(-105, 253, -120, 252, -120, 250)
        block_67 = self.createTrackBlock(path_67, "Block 67")
        self.redTrack.addItem(block_67)
        self.redBlocks[67] = block_67

        path_68 = QPainterPath()
        path_68.moveTo(-120, 240)
        path_68.lineTo(-120, 237)
        block_68 = self.createTrackBlock(path_68, "Block 68")
        self.redTrack.addItem(block_68)
        self.redBlocks[68] = block_68

        path_69 = QPainterPath()
        path_69.moveTo(-120, 227)
        path_69.lineTo(-120, 224)
        block_69 = self.createTrackBlock(path_69, "Block 69")
        self.redTrack.addItem(block_69)
        self.redBlocks[69] = block_69

        path_70 = QPainterPath()
        path_70.moveTo(-120, 214)
        path_70.lineTo(-120, 211)
        block_70 = self.createTrackBlock(path_70, "Block 70")
        self.redTrack.addItem(block_70)
        self.redBlocks[70] = block_70

        path_71 = QPainterPath()
        path_71.moveTo(-120, 201)
        path_71.cubicTo(-120, 199, -105, 198, -104, 198)
        block_71 = self.createTrackBlock(path_71, "Block 71")
        self.redTrack.addItem(block_71)
        self.redBlocks[71] = block_71

        path_72 = QPainterPath()
        path_72.moveTo(-104, 132)
        path_72.cubicTo(-105, 132, -120, 131, -120, 129)
        block_72 = self.createTrackBlock(path_72, "Block 72")
        self.redTrack.addItem(block_72)
        self.redBlocks[72] = block_72

        path_73 = QPainterPath()
        path_73.moveTo(-120, 119)
        path_73.lineTo(-120, 116)
        block_73 = self.createTrackBlock(path_73, "Block 73")
        self.redTrack.addItem(block_73)
        self.redBlocks[73] = block_73

        path_74 = QPainterPath()
        path_74.moveTo(-120, 106)
        path_74.lineTo(-120, 103)
        block_74 = self.createTrackBlock(path_74, "Block 74")
        self.redTrack.addItem(block_74)
        self.redBlocks[74] = block_74

        path_75 = QPainterPath()
        path_75.moveTo(-120, 93)
        path_75.lineTo(-120, 90)
        block_75 = self.createTrackBlock(path_75, "Block 75")
        self.redTrack.addItem(block_75)
        self.redBlocks[75] = block_75

        path_76 = QPainterPath()
        path_76.moveTo(-120, 80)
        path_76.cubicTo(-120, 78, -105, 77, -104, 77)
        block_76 = self.createTrackBlock(path_76, "Block 76")
        self.redTrack.addItem(block_76)
        self.redBlocks[76] = block_76

        #SWITCHES -> 0 by default, means continuation of number
        switchPath9 = QPainterPath()
        switchPath9.moveTo(116, -59)
        switchPath9.cubicTo(119, -52, 119, -42, 115, -29)
        switch9 = self.createSwitch(switchPath9)
        self.redTrack.addItem(switch9)
        self.redSwitches[9] = switch9

        switchPath27 = QPainterPath()
        switchPath27.moveTo(-94, 71)
        switchPath27.lineTo(-94, 83)
        switch27 = self.createSwitch(switchPath27)
        self.redTrack.addItem(switch27)
        self.redSwitches[27] = switch27

        switchPath33 = QPainterPath()
        switchPath33.moveTo(-94, 138)
        switchPath33.lineTo(-94, 126)
        switch33 = self.createSwitch(switchPath33)
        self.redTrack.addItem(switch33)
        self.redSwitches[33] = switch33

        switchPath38 = QPainterPath()
        switchPath38.moveTo(-94, 192)
        switchPath38.lineTo(-94, 204)
        switch38 = self.createSwitch(switchPath38)
        self.redTrack.addItem(switch38)
        self.redSwitches[38] = switch38

        switchPath44 = QPainterPath()
        switchPath44.moveTo(-94, 259)
        switchPath44.lineTo(-94, 247)
        switch44 = self.createSwitch(switchPath44)
        self.redTrack.addItem(switch44)
        self.redSwitches[44] = switch44

        switchPath52 = QPainterPath()
        switchPath52.moveTo(-206, 327)
        switchPath52.lineTo(-232, 327)
        switch52 = self.createSwitch(switchPath52)
        self.redTrack.addItem(switch52)
        self.redSwitches[52] = switch52

        #CROSSING
        crossing = QPixmap("src/main/TrackModel/pngs/crossing.png")
        crossing = crossing.scaledToWidth(70)
        self.redCrossing = QGraphicsPixmapItem(crossing)
        self.redCrossing.setPos(-120, 300)
        self.redTrack.addItem(self.redCrossing)

        #TRAFFIC LIGHTS
        lightPole0 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole0 = lightPole0.scaledToWidth(15)
        pole0 = QGraphicsPixmapItem(lightPole0)
        pole0.setPos(128, -25)
        self.redTrack.addItem(pole0)
        lightCircle0 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle0 = lightCircle0.scaledToWidth(17)
        circle0 = QGraphicsPixmapItem(lightCircle0)
        circle0.setPos(127, -40)
        self.redTrack.addItem(circle0)
        light0 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light0 = light0.scaledToWidth(35)
        signal0 = QGraphicsPixmapItem(light0)
        signal0.setPos(118, -44)
        self.redTrack.addItem(signal0)

        lightPole76 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole76 = lightPole76.scaledToWidth(15)
        pole76 = QGraphicsPixmapItem(lightPole76)
        pole76.setPos(-118, 48)
        self.redTrack.addItem(pole76)
        lightCircle76 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle76 = lightCircle76.scaledToWidth(17)
        circle76 = QGraphicsPixmapItem(lightCircle76)
        circle76.setPos(-119, 33)
        self.redTrack.addItem(circle76)
        light76 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light76 = light76.scaledToWidth(35)
        signal76 = QGraphicsPixmapItem(light76)
        signal76.setPos(-128, 29)
        self.redTrack.addItem(signal76)

        lightPole71 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole71 = lightPole71.scaledToWidth(15)
        pole71 = QGraphicsPixmapItem(lightPole71)
        pole71.setPos(-118, 169)
        self.redTrack.addItem(pole71)
        lightCircle71 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle71 = lightCircle71.scaledToWidth(17)
        circle71 = QGraphicsPixmapItem(lightCircle71)
        circle71.setPos(-119, 154)
        self.redTrack.addItem(circle71)
        light71 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light71 = light71.scaledToWidth(35)
        signal71 = QGraphicsPixmapItem(light71)
        signal71.setPos(-128, 150)
        self.redTrack.addItem(signal71)

        lightPole32 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole32 = lightPole32.scaledToWidth(15)
        pole32 = QGraphicsPixmapItem(lightPole32)
        pole32.setPos(-84, 110)
        self.redTrack.addItem(pole32)
        lightCircle32 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle32 = lightCircle32.scaledToWidth(17)
        circle32 = QGraphicsPixmapItem(lightCircle32)
        circle32.setPos(-85, 95)
        self.redTrack.addItem(circle32)
        light32 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light32 = light32.scaledToWidth(35)
        signal32 = QGraphicsPixmapItem(light32)
        signal32.setPos(-94, 91)
        self.redTrack.addItem(signal32)

        lightPole43 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole43 = lightPole43.scaledToWidth(15)
        pole43 = QGraphicsPixmapItem(lightPole43)
        pole43.setPos(-84, 231)
        self.redTrack.addItem(pole43)
        lightCircle43 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle43 = lightCircle43.scaledToWidth(17)
        circle43 = QGraphicsPixmapItem(lightCircle43)
        circle43.setPos(-85, 216)
        self.redTrack.addItem(circle43)
        light43 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light43 = light43.scaledToWidth(35)
        signal43 = QGraphicsPixmapItem(light43)
        signal43.setPos(-94, 212)
        self.redTrack.addItem(signal43)

        lightPole66 = QPixmap("src/main/TrackModel/pngs/light-pole.png")
        lightPole66 = lightPole66.scaledToWidth(15)
        pole66 = QGraphicsPixmapItem(lightPole66)
        pole66.setPos(-220, 290)
        self.redTrack.addItem(pole66)
        lightCircle66 = QPixmap("src/main/TrackModel/pngs/light-circle.png")
        lightCircle66 = lightCircle66.scaledToWidth(17)
        circle66 = QGraphicsPixmapItem(lightCircle66)
        circle66.setPos(-221, 275)
        self.redTrack.addItem(circle66)
        light66 = QPixmap("src/main/TrackModel/pngs/green-light.png")
        light66 = light66.scaledToWidth(35)
        signal66 = QGraphicsPixmapItem(light66)
        signal66.setPos(-230, 271)
        self.redTrack.addItem(signal66)
        
        #STATIONS AND BEACONS
        station = QPixmap("src/main/TrackModel/pngs/station.png")
        station = station.scaledToWidth(20)
        beacon = QPixmap("src/main/TrackModel/pngs/beacon.png")
        beacon = beacon.scaledToWidth(10)
        
        shadyside = QGraphicsPixmapItem(station)
        shadyside.setPos(91, -107)
        self.redTrack.addItem(shadyside)
        shadysideBeacon = QGraphicsPixmapItem(beacon)
        shadysideBeacon.setPos(86, -86)
        self.redTrack.addItem(shadysideBeacon)
        
        herron = QGraphicsPixmapItem(station)
        herron.setPos(-10, 10)
        self.redTrack.addItem(herron)
        herronBeacon = QGraphicsPixmapItem(beacon)
        herronBeacon.setPos(-5, -5)
        self.redTrack.addItem(herronBeacon)
        
        #Over beacon
        switchPath16 = QPainterPath()
        switchPath16.moveTo(0, 0)
        switchPath16.lineTo(20, 0)
        switch16 = self.createSwitch(switchPath16)
        self.redTrack.addItem(switch16)
        self.redSwitches[16] = switch16
        
        swissville = QGraphicsPixmapItem(station)
        swissville.setPos(-80, -26)
        self.redTrack.addItem(swissville)
        swissvilleBeacon = QGraphicsPixmapItem(beacon)
        swissvilleBeacon.setPos(-71, -4)
        self.redTrack.addItem(swissvilleBeacon)
        
        pennstation = QGraphicsPixmapItem(station)
        pennstation.setPos(-87, 40)
        self.redTrack.addItem(pennstation)
        pennstationBeacon = QGraphicsPixmapItem(beacon)
        pennstationBeacon.setPos(-99, 45)
        self.redTrack.addItem(pennstationBeacon)
        
        steelplaza = QGraphicsPixmapItem(station)
        steelplaza.setPos(-87, 150)
        self.redTrack.addItem(steelplaza)
        steelplazaBeacon = QGraphicsPixmapItem(beacon)
        steelplazaBeacon.setPos(-99, 155)
        self.redTrack.addItem(steelplazaBeacon)
        
        firstave = QGraphicsPixmapItem(station)
        firstave.setPos(-87, 260)
        self.redTrack.addItem(firstave)
        firstaveBeacon = QGraphicsPixmapItem(beacon)
        firstaveBeacon.setPos(-99, 265)
        self.redTrack.addItem(firstaveBeacon)
        
        stationsquare = QGraphicsPixmapItem(station)
        stationsquare.setPos(-154, 298)
        self.redTrack.addItem(stationsquare)
        stationsquareBeacon = QGraphicsPixmapItem(beacon)
        stationsquareBeacon.setPos(-140, 320)
        self.redTrack.addItem(stationsquareBeacon)
        
        southhills = QGraphicsPixmapItem(station)
        southhills.setPos(-294, 184)
        self.redTrack.addItem(southhills)
        southhillsBeacon = QGraphicsPixmapItem(beacon)
        southhillsBeacon.setPos(-286, 208)
        self.redTrack.addItem(southhillsBeacon)
        
        #Box where block numbers are displayed
        box = QGraphicsRectItem(-225, 0, 60, 20)
        box.setPen(QPen(QColor(0, 0, 0), 3))
        box.setBrush(QBrush(QColor(255, 0, 0, 20)))
        self.redTrack.addItem(box)

    def createTrackBlock(self, path, number, line= "Red"):
        track_block = TrackBlock(path, number, line)
        return track_block

    def createSwitch(self, path):
        switch = QGraphicsPathItem(path)
        switchPen = QPen(QColor(220, 83, 0))
        switchPen.setWidth(5)
        switch.setPen(switchPen)
        return switch
    
    def showGreenLineLayout(self):
        self.setScene(self.greenTrack)

    def showRedLineLayout(self):
        self.setScene(self.redTrack)

    def change_color(self, line, curBlock, prevBlock):
        if line == "Green":
            if prevBlock == None:
                onBlock = self.greenBlocks.get(curBlock)
                onBlock.toggle_occupancy(True)
            elif curBlock == None:
                offBlock = self.greenBlocks.get(prevBlock)
                offBlock.toggle_occupancy(False)
            #To turn off occupancy of previous block based on back of the train
            elif curBlock == -1:
                offBlock = self.greenBlocks.get(prevBlock)
                offBlock.toggle_occupancy(False)
            elif curBlock == 151:
                offBlock = self.greenBlocks.get(curBlock)
                offBlock.toggle_occupancy(False)
            #Turn on occupancy
            elif curBlock != -1:
                #First yard block
                if curBlock == 999:
                    onBlock = self.greenBlocks.get(0)
                    onBlock.toggle_occupancy(True)
                #After first yard block
                elif curBlock == 0:
                    onBlock = self.greenBlocks.get(63)
                    onBlock.toggle_occupancy(True)
                #Q -> N
                elif curBlock == 100:
                    onBlock = self.greenBlocks.get(85)
                    onBlock.toggle_occupancy(True)
                #N -> R
                elif curBlock == 77 and prevBlock == 78:
                    onBlock = self.greenBlocks.get(101)
                    onBlock.toggle_occupancy(True)
                #Z -> F
                elif curBlock == 150:
                    onBlock = self.greenBlocks.get(28)
                    onBlock.toggle_occupancy(True)
                #A -> D
                elif curBlock == 1:
                    onBlock = self.greenBlocks.get(13)
                    onBlock.toggle_occupancy(True)
                #For last yard block
                elif curBlock == 57:
                    onBlock = self.greenBlocks.get(151)
                    onBlock.toggle_occupancy(True)
                elif curBlock > prevBlock:
                    nextBlock = curBlock + 1
                    onBlock = self.greenBlocks.get(nextBlock)
                    onBlock.toggle_occupancy(True)
                elif curBlock < prevBlock:
                    nextBlock = curBlock - 1
                    onBlock = self.greenBlocks.get(nextBlock)
                    onBlock.toggle_occupancy(True)
        elif line == "Red":
            if prevBlock == None:
                onBlock = self.redBlocks.get(curBlock)
                onBlock.toggle_occupancy(True)
            elif curBlock == None:
                offBlock = self.redBlocks.get(prevBlock)
                offBlock.toggle_occupancy(False)
            #To turn off occupancy of previous block based on back of the train
            elif curBlock == -1:
                offBlock = self.redBlocks.get(prevBlock)
                offBlock.toggle_occupancy(False)
            elif curBlock == 0 and prevBlock == 9:
                offBlock = self.redBlocks.get(prevBlock)
                offBlock.toggle_occupancy(False)
            #Turn on occupancy
            elif curBlock != -1:
                #Yard block
                if curBlock == 999:
                    onBlock = self.redBlocks.get(0)
                    onBlock.toggle_occupancy(True)
                #Yard -> C
                elif curBlock == 0 and prevBlock == 999:
                    onBlock = self.redBlocks.get(9)
                    onBlock.toggle_occupancy(True)
                #C -> Yard
                elif curBlock == 9 and prevBlock == 8:
                    onBlock = self.redBlocks.get(0)
                    onBlock.toggle_occupancy(True)
                #9 -> 8
                elif curBlock == 9 and prevBlock == 0:
                    onBlock = self.redBlocks.get(8)
                    onBlock.toggle_occupancy(True)
                                #1 -> 2
                elif curBlock == 1 and prevBlock == 16:
                    onBlock = self.redBlocks.get(2)
                    onBlock.toggle_occupancy(True)
                #A -> F
                elif curBlock == 1:
                    onBlock = self.redBlocks.get(16)
                    onBlock.toggle_occupancy(True)
                #F -> A
                elif curBlock == 16 and prevBlock == 17:
                    onBlock = self.redBlocks.get(1)
                    onBlock.toggle_occupancy(True)
                #N -> J
                elif curBlock == 66:
                    onBlock = self.redBlocks.get(52)
                    onBlock.toggle_occupancy(True)
                #H -> O
                elif curBlock == 44 and prevBlock == 45:
                    onBlock = self.redBlocks.get(67)
                    onBlock.toggle_occupancy(True)
                #Q -> H
                elif curBlock == 71:
                    onBlock = self.redBlocks.get(38)
                    onBlock.toggle_occupancy(True)
                #H -> R
                elif curBlock == 33 and prevBlock == 34:
                    onBlock = self.redBlocks.get(72)
                    onBlock.toggle_occupancy(True)
                #T -> H
                elif curBlock == 76:
                    onBlock = self.redBlocks.get(27)
                    onBlock.toggle_occupancy(True)
                elif curBlock > prevBlock:
                    nextBlock = curBlock + 1
                    onBlock = self.redBlocks.get(nextBlock)
                    onBlock.toggle_occupancy(True)
                elif curBlock < prevBlock:
                    nextBlock = curBlock - 1
                    onBlock = self.redBlocks.get(nextBlock)
                    onBlock.toggle_occupancy(True)
        
    def change_switch(self, line, switchNum, state):
        switch = QPainterPath()
        if line == 1:
            self.greenTrack.removeItem(self.greenSwitches[switchNum])
            if switchNum == 13:
                if state == 0:
                    # 13 -> 12
                    switch.moveTo(-25, 0)
                    switch.cubicTo(-10, 0, 10, 1, 23, 2)
                    switch13 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch13)
                elif state == 1:
                    # 13 -> 1
                    switch.moveTo(-25, 0)
                    switch.cubicTo(-10, 0, 0, 0, 10, 10)
                    switch13 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch13)
                self.greenSwitches[switchNum] = switch13
            elif switchNum == 29:
                if state == 0:
                    # 29 -> 30
                    switch.moveTo(-167, 193)
                    switch.lineTo(-167, 213)
                    switch29 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch29)  
                elif state == 1:
                    # 29 -> 150
                    switch.moveTo(-167, 193)
                    switch.cubicTo(-167, 198, -177, 200, -204, 214)
                    switch29 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch29)
                self.greenSwitches[switchNum] = switch29
            elif switchNum == 57:
                if state == 0:
                    # 57 -> 58
                    switch.moveTo(95, 278)
                    switch.quadTo(107, 278, 111, 279)
                    switch57 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch57)
                elif state == 1:
                    # 57 -> 151
                    switch.moveTo(95, 278)
                    switch.quadTo(97, 278, 112, 260)
                    switch57 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch57)
                self.greenSwitches[switchNum] = switch57
            elif switchNum == 63:
                if state == 0:
                    # 63 -> 62
                    switch.moveTo(163, 350)
                    switch.cubicTo(163, 340, 163, 330, 161, 322)
                    switch63 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch63)
                elif state == 1:
                    # 63 -> 0
                    switch.moveTo(163, 350)
                    switch.lineTo(163, 310)
                    switch63 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch63)
                self.greenSwitches[switchNum] = switch63
            elif switchNum == 77:
                if state == 0:
                    # 77 -> 76
                    switch.moveTo(12, 556)
                    switch.lineTo(50, 556)
                    switch77 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch77)
                elif state == 1:
                    # 77 -> 101
                    switch.moveTo(12, 556)
                    switch.cubicTo(20, 556, 24, 546, 28, 540)
                    switch77 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch77)
                self.greenSwitches[switchNum] = switch77
            elif switchNum == 85:
                if state == 0:
                    # 85 -> 86
                    switch.moveTo(-124, 556)
                    switch.lineTo(-149, 556)
                    switch85 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch85)
                elif state == 1:
                    # 85 -> 100
                    switch.moveTo(-124, 556)
                    switch.cubicTo(-132, 556, -142, 551, -148, 546)
                    switch85 = self.createSwitch(switch)
                    self.greenTrack.addItem(switch85)
                self.greenSwitches[switchNum] = switch85
        elif line == 2:
            self.redTrack.removeItem(self.redSwitches[switchNum])
            if switchNum == 9:
                if state == 0:
                    # 9 -> 10
                    switch.moveTo(116, -59)
                    switch.cubicTo(119, -52, 119, -42, 115, -29)
                    switch9 = self.createSwitch(switch)
                    self.redTrack.addItem(switch9)
                elif state == 1:
                    # 9 -> 0
                    switch.moveTo(116, -59)
                    switch.cubicTo(119, -52, 119, -42, 115, -10)
                    switch9 = self.createSwitch(switch)
                    self.redTrack.addItem(switch9)
                self.redSwitches[switchNum] = switch9
            elif switchNum == 16:
                if state == 0:
                    # 16 -> 15
                    switch.moveTo(0, 0)
                    switch.lineTo(20, 0)
                    switch16 = self.createSwitch(switch)
                    self.redTrack.addItem(switch16)
                elif state == 1:
                    # 16 -> 1
                    switch.moveTo(0, 0)
                    switch.cubicTo(-1, 0, 7, -4, 22, -14)
                    switch16 = self.createSwitch(switch)
                    self.redTrack.addItem(switch16)
                self.redSwitches[switchNum] = switch16
            elif switchNum == 27:
                if state == 0:
                    # 27 -> 28
                    switch.moveTo(-94, 71)
                    switch.lineTo(-94, 83)
                    switch27 = self.createSwitch(switch)
                    self.redTrack.addItem(switch27)
                elif state == 1:
                    # 27 -> 76
                    switch.moveTo(-94, 71)
                    switch.cubicTo(-94, 77, -105, 77, -110, 78)
                    switch27 = self.createSwitch(switch)
                    self.redTrack.addItem(switch27)
                self.redSwitches[switchNum] = switch27
            elif switchNum == 33:
                if state == 0:
                    # 33 -> 32
                    switch.moveTo(-94, 138)
                    switch.lineTo(-94, 126)
                    switch33 = self.createSwitch(switch)
                    self.redTrack.addItem(switch33)
                elif state == 1:
                    # 33 -> 72
                    switch.moveTo(-94, 138)
                    switch.cubicTo(-94, 132, -105, 132, -110, 131)
                    switch33 = self.createSwitch(switch)
                    self.redTrack.addItem(switch33)
                self.redSwitches[switchNum] = switch33
            elif switchNum == 38:
                if state == 0:
                    # 38 -> 39
                    switch.moveTo(-94, 192)
                    switch.lineTo(-94, 204)
                    switch38 = self.createSwitch(switch)
                    self.redTrack.addItem(switch38)
                elif state == 1:
                    # 38 -> 71
                    switch.moveTo(-94, 192)
                    switch.cubicTo(-94, 198, -105, 198, -110, 199)
                    switch38 = self.createSwitch(switch)
                    self.redTrack.addItem(switch38)
                self.redSwitches[switchNum] = switch38
            elif switchNum == 44:
                if state == 0:
                    # 44 -> 43
                    switch.moveTo(-94, 259)
                    switch.lineTo(-94, 247)
                    switch44 = self.createSwitch(switch)
                    self.redTrack.addItem(switch44)
                elif state == 1:
                    # 44 -> 67
                    switch.moveTo(-94, 259)
                    switch.cubicTo(-94, 253, -105, 253, -110, 252)
                    switch44 = self.createSwitch(switch)
                    self.redTrack.addItem(switch44)
                self.redSwitches[switchNum] = switch44
            elif switchNum == 52:
                if state == 0:
                    # 52 -> 53
                    switch.moveTo(-206, 327)
                    switch.lineTo(-232, 327)
                    switch52 = self.createSwitch(switch)
                    self.redTrack.addItem(switch52)
                elif state == 1:
                    # 52 -> 66
                    switch.moveTo(-206, 327)
                    switch.cubicTo(-214, 327, -220, 322, -225, 314)
                    switch52 = self.createSwitch(switch)
                    self.redTrack.addItem(switch52)
                self.redSwitches[switchNum] = switch52
        

class TrackBlock(QGraphicsPathItem):
    def __init__(self, path, number, line):
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
        
        self.text_item = QGraphicsTextItem(str(number), parent=self)
        
        if line == "Green":
            self.text_item.setPos(-75, 150)
            self.text_item.setDefaultTextColor(QColor(3, 200, 29))
        else:
            self.text_item.setPos(-225, 0)
            self.text_item.setDefaultTextColor(QColor(255, 0, 0))
        
        font = self.text_item.font()
        font.setWeight(QFont.Bold)
        self.text_item.setFont(font)
        self.text_item.setVisible(False)

    def mousePressEvent(self, event):
        print(f"Clicked on {self.number}")

    def hoverEnterEvent(self, event):
        self.current_pen = self.pen()
        self.setPen(self.hover_pen)
        self.text_item.setVisible(True)

    def hoverLeaveEvent(self, event):
        if self.current_pen:
            self.setPen(self.current_pen)
        else:
            self.setPen(self.original_pen)
        self.text_item.setVisible(False)

    def toggle_occupancy(self, occupied):
        if occupied:
            self.current_pen = self.occupied_pen
            self.setPen(self.occupied_pen)
        else:
            self.current_pen = self.original_pen
            self.setPen(self.original_pen)
