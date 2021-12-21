import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import matplotlib.pyplot as plot
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.pyui.ui_dashboard import Ui_MainWindow
import pandas as pd
import sys, random

from PyQt5.QtWidgets import QGraphicsScene, QApplication, QGraphicsView, QGraphicsEllipseItem
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from pylab import *



import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import FigureCanvas


COLUMN_COUNT_TABLE=5
ROW_COUNT_TABLE=43
COLUMN_COUNT_TABLE_LH_1=5
ROW_COUNT_TABLE_LH_1=43
RES_ROW_COUNT=124
RES_COL_COUNT = 24
TZ_ROW_COUNT=6
TZ_COL_COUNT=11
CLR_RANGE_ROW_COUNT=6
CLR_RANGE_COL_COUNT=3



class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    def __init__(self):
        """
        Constructor of the MainWindow class
        """
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("ADAMANTv1.5")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.pieDiagram_groupBox.setLayout(layout)
    '''

    def __init__(self, controller=None, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.controller = controller

        '''
        self.STRradioButton_2.toggled.connect(self.contoller.onModeChangedtoSTR)
        self.LTRradioButton_2.toggled.connect(self.controller.onModeChangedtoLTR)
        self.GTR4radioButton_2.toggled.connect(self.controller.onModeChangedtoGTR4)
        self.GTR8radioButton_2.toggled.connect(self.controller.onModeChangedtoGTR8)
        #print("currentIndex:", self.aircraftHOV_comboBox.currentIndex())
        self.aircraftHOV_comboBox.addItem("")
        self.aircraftHOV_comboBox.currentIndexChanged[str].connect(self._controller.populate_HoVCombo)
        self.aircraftHOV_comboBox.activated[str].connect(self.controller.populate_HoVCombo)
        '''

        '''
        # Setting up Signals and slots for the Widgets
        self.STRradioButton_2.toggled.connect(self.controller.isSTRradioButton_2_Checked)
        self.LTRradioButton_2.toggled.connect(self.controller.isLTRradioButton_2_Checked)
        self.GTR4radioButton_2.toggled.connect(self.controller.isGTR4radioButton_2_Checked)
        self.GTR8radioButton_2.toggled.connect(self.controller.isGTR8radioButton_2_Checked)
        #print("currentIndex:", self.aircraftHOV_comboBox.currentIndex())
        self.aircraftHOV_comboBox.addItem("")
        #self.aircraftHOV_comboBox.currentIndexChanged[str].connect(self._controller.populate_HoVCombo)
        self.aircraftHOV_comboBox.activated[str].connect(self.controller.populate_HoVCombo)
        '''

        try:
            self.signalSlotUI()
        except Exception as e:
            pass


    def signalSlotUI(self):
        """
        Called at the beginning to signal slot evry widget
        Called only once
        :return:
        """
        self.STRradioButton.toggled.connect(self.controller.onModeChangedtoSTR)
        self.LTRradioButton.toggled.connect(self.controller.onModeChangedtoLTR)
        self.GTR4radioButton.toggled.connect(self.controller.onModeChangedtoGTR4)
        self.GTR8radioButton.toggled.connect(self.controller.onModeChangedtoGTR8)
        #print("currentIndex:", self.aircraftHOV_comboBox.currentIndex())
        #self.aircraftHOV_comboBox.addItem("")
        self.aircraftHOV_comboBox.currentTextChanged.connect(self.controller.on_aircraftHOV_comboBox_changed)
        #self.aircraftHOV_comboBox.currentIndexChanged[str].connect(self.controller.onModeChangedtoLTR)
        #self.aircraftHOV_comboBox.currentIndexChanged[str].connect(self.controller.onModeChangedtoGTR4)
        #self.aircraftHOV_comboBox.currentIndexChanged[str].connect(self.controller.onModeChangedtoGTR8)
        #self.aircraftHOV_comboBox.activated[str].connect(self.controller.onModeChangedtoSTR)
        #self.aircraftHOV_comboBox.activated[str].connect(self.controller.onModeChangedtoLTR)
        #self.aircraftHOV_comboBox.activated[str].connect(self.controller.onModeChangedtoGTR4)
        #self.aircraftHOV_comboBox.activated[str].connect(self.controller.onModeChangedtoGTR8)


    def populate_HOV(self, hovlist):
        """
        Function to populate the list
        :param hovlist:
        :return:
        """
        #self.aircraftHOV_comboBox.clear()
        self.reset_HOV()
        for hov in sorted(hovlist):
            self.aircraftHOV_comboBox.addItem(hov)

    def populate_AC(self, aclist):
        self.aircraftcomboBox.clear()
        for ac in sorted(aclist):
            self.aircraftcomboBox.addItem(ac)

    def populate_SYSTEM(self, systemlist):
        self.systemcomboBox.clear()
        for system in sorted(systemlist):
            self.systemcomboBox.addItem(system)

    def populate_TEST(self, testlist):
        self.test_comboBox.clear()
        for test in sorted(testlist):
            self.test_comboBox.addItem(test)

    def populate_COMB(self, comblist):
        self.combination_comboBox.clear()
        for comb in sorted(comblist):
            self.combination_comboBox.addItem(comb)

    def populate_LOOP(self, looplist):
        self.loop_comboBox.clear()
        for loop in sorted(looplist):
            self.loop_comboBox.addItem(loop)
    def populate_TEST_DATE(self,testdate):
        self.testdate_lineEdit.clear()
        self.testdate_lineEdit.setText(testdate)

    def populate_IMPORT_DATE(self, importdate):
        self.importdate_lineEdit.clear()
        self.importdate_lineEdit.setText(importdate)

    def populate_EXPORT_DATE(self, exportdate):
        self.importedby_lineEdit.clear()
        self.importedby_lineEdit.setText(exportdate)


    def populate_ACV(self, acvlist):
        self.aircraftVersion_comboBox.clear()
        for acv in sorted(acvlist):
            self.aircraftVersion_comboBox.addItem(acv)

    def populate_MSN(self, msnlist):
        self.aircraftMSN_comboBox.clear()
        for msn in sorted(msnlist):
            self.aircraftMSN_comboBox.addItem(msn)

    def reset_HOV(self):
        self.aircraftHOV_comboBox.clear()

    def reset_ACV(self):
        self.aircraftVersion_comboBox.clear()

    def reset_MSN(self):
        self.aircraftMSN_comboBox.clear()

    # common function for tables

    def set_TableRowCount(self,tableWidget, count):
        tableWidget.setRowCount(count)

    def set_TableColumnCount(self,tableWidget, count):
        tableWidget.setColumnCount(count)

    # def setCellValuePercentage(self, tableWidget, row, column, value, format = '%'):
    #      tableWidget.setItem(row, column, QTableWidgetItem(str(value)))


    def setCellValueInt(self, tableWidget, row, column, value, format='.2f'):
        tableWidget.setItem(row, column, QTableWidgetItem(str(value)))


    # LH Table 1

    # ----- AC Version 350-1000
    def resetTable_LH_LAO(self, tableWidget,row_count,col_count):

        self.set_TableRowCount(tableWidget=tableWidget, count=row_count)
        self.set_TableColumnCount(tableWidget=tableWidget, count=col_count)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        tableWidget.setStyleSheet("border : 2px solid black")
        tableWidget.setStyleSheet("border-style : outset")
        tableWidget.setStyleSheet("gridline-color: black")
        deligate = self.Set_deligate_for_Flow_LAO_table()
        tableWidget.setItemDelegate(deligate)

    def adjustColWidthOf_LH_LAO(self, tableWidget):
        for i in range(tableWidget.columnCount()):
            if i == 4:
                tableWidget.setColumnWidth(i, 65)
            else:
                tableWidget.setColumnWidth(i, 50)
    def adjustColWidthOf_RH_LAO(self, tableWidget):
        for i in range(tableWidget.columnCount()):
            if i == 0:
                tableWidget.setColumnWidth(i, 65)
            else:
                tableWidget.setColumnWidth(i, 50)

    def adjustRowHeightOf_LH_LAO(self, tableWidget,df):
        for row in range(tableWidget.rowCount()-1):
            diff = self._sectionDifference(df.iloc[row, 4])
            if diff == 1:
                tableWidget.setRowHeight(row, 15)
            else:
                tableWidget.setRowHeight(row, 30)

    def adjustRowHeightOf_RH_LAO(self, tableWidget,df):
        for row in range(tableWidget.rowCount()-1):
            diff = self._sectionDifference(df.iloc[row, 0])
            if diff == 1:
                tableWidget.setRowHeight(row, 15)
            else:
                tableWidget.setRowHeight(row, 30)

    def populateTable_LH_LAO(self, tableWidget, df, commentdf):
        commentdf = commentdf.replace(np.nan, " ")
        commentdf = commentdf.astype(str)
        for row in range(len(df.index)):
            for col in range(len(df.columns)):
                self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=df.iloc[row, col])
                tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
                if pd.notnull(commentdf.iloc[row, col]):
                    tableWidget.item(row, col).setToolTip(commentdf.iloc[row, col])
                    # tableWidget.setItem(row,col,icon)

    def resizeTableWidget_LH_LAO(self, tableWidget,df):
        setTableWidth = 0
        for i in range(len(df.columns)):
            setTableWidth += tableWidget.columnWidth(i)
        tableWidget.setFixedWidth(setTableWidth + 2)
        setTableHeight = 0
        for i in range(len(df.index)):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight + 2)

    def LH_LAO_Table(self,df):
        self.resetTable_LH_LAO(tableWidget=self.flowValueLAOLH_tableWidget , row_count=len(df.index),col_count=len(df.columns))
        self.adjustColWidthOf_LH_LAO(tableWidget=self.flowValueLAOLH_tableWidget)
        self.adjustRowHeightOf_LH_LAO(tableWidget=self.flowValueLAOLH_tableWidget,df=df)
        self.populateTable_LH_LAO(tableWidget=self.flowValueLAOLH_tableWidget,df=df , commentdf= df)
        self.resizeTableWidget_LH_LAO(tableWidget=self.flowValueLAOLH_tableWidget,df=df)
        self.scrollArea.setGeometry(50,40,1189,self.flowValueLAOLH_tableWidget.height())
        # self.flowValueLAOLH_tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def RH_LAO_Table(self,df):
        self.resetTable_LH_LAO(tableWidget=self.flowValueLAORH_tableWidget , row_count=len(df.index),col_count=len(df.columns))
        self.adjustColWidthOf_RH_LAO(tableWidget=self.flowValueLAORH_tableWidget)
        self.adjustRowHeightOf_RH_LAO(tableWidget=self.flowValueLAORH_tableWidget,df=df)
        self.populateTable_LH_LAO(tableWidget=self.flowValueLAORH_tableWidget,df=df , commentdf= df)
        self.resizeTableWidget_LH_LAO(tableWidget=self.flowValueLAORH_tableWidget,df=df)
        self.scrollArea.setGeometry(50,40,1189,self.flowValueLAORH_tableWidget.height())
        # self.flowValueLAOLH_tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    # -------------------------

    class Set_deligate_for_Flow_LAO_table(QtWidgets.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            return size

        def paint(self, painter, option, index):
            painter.save()
            painter.setRenderHint(painter.Antialiasing)
            painter.setClipping(True)
            painter.setClipRect(option.rect)

            super().paint(painter, option, index)
            pen = painter.pen()
            pen.setColor(Qt.black)
            pen.setWidth(2)
            painter.setPen(pen)

            option.rect.adjust(0, 0, 0, 0)
            row_bottom_border_thick = [0,7,12,16,20,26,33,37,41]
            for i in row_bottom_border_thick:
                if index.row() == i:
                    painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

            painter.restore()
    class Set_deligate_for_Flow_CAO_table(QtWidgets.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            return size

        def paint(self, painter, option, index):
            painter.save()
            painter.setRenderHint(painter.Antialiasing)
            painter.setClipping(True)
            painter.setClipRect(option.rect)

            super().paint(painter, option, index)
            pen = painter.pen()
            pen.setColor(Qt.black)
            pen.setWidth(2)
            painter.setPen(pen)

            option.rect.adjust(0, 0, 0, 0)
            row_bottom_border_thick = [0,7,12,16,20,26,32,37,41]
            for i in row_bottom_border_thick:
                if index.row() == i:
                    painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

            painter.restore()

    def resetTable_LH_first(self, tableWidget):

        self.set_TableRowCount(tableWidget=tableWidget, count=ROW_COUNT_TABLE_LH_1)
        self.set_TableColumnCount(tableWidget=tableWidget, count=COLUMN_COUNT_TABLE_LH_1)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        tableWidget.setStyleSheet("border : 2px solid black")
        tableWidget.setStyleSheet("border-style : outset")
        tableWidget.setStyleSheet("gridline-color: black")
        deligate = self.Set_deligate_for_Flow_LAO_table()
        tableWidget.setItemDelegate(deligate)

    def adjustColWidthOf_LH_firstTable(self,tableWidget):
        for i in range(tableWidget.columnCount()):
            if i == 4:
                tableWidget.setColumnWidth(i, 65)
            else:
                tableWidget.setColumnWidth(i, 50)

    def adjustRowHeightOf_LH_firstTable(self, tableWidget):
        for i in range(tableWidget.rowCount()):
           tableWidget.setRowHeight(i, 30)
        smallRowWidth = [1,2,3,27,28,39,40]
        for i in smallRowWidth:
            tableWidget.setRowHeight(i,15)

    def populateTable_LH_first(self, tableWidget, df,commentdf):
        commentdf = commentdf.replace(np.nan," ")
        commentdf = commentdf.astype(str)
        for row in range(ROW_COUNT_TABLE_LH_1):
            for col in range(COLUMN_COUNT_TABLE_LH_1):
                self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value= df.iloc[row, col])
                tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row,col).setFlags(tableWidget.item(row,col).flags() & ~Qt.ItemIsEditable)
                #if pd.notnull(commentdf.iloc[row,col]):
                #    tableWidget.item(row, col).setToolTip(commentdf.iloc[row,col])
                    # tableWidget.setItem(row,col,icon)


    def resizeTableWidget_LH_first(self,tableWidget):
        setTableWidth=0
        for i in range(COLUMN_COUNT_TABLE_LH_1):
            setTableWidth += tableWidget.columnWidth(i)
        tableWidget.setFixedWidth(setTableWidth+2)
        setTableHeight = 0
        for i in range(ROW_COUNT_TABLE_LH_1):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight+2)

    # LH Table 2

    #  AC version 350-1000
    def resetTable_LH_CAO(self,tableWidget,row_count , col_count):

        self.set_TableRowCount(tableWidget=tableWidget,count=row_count)
        self.set_TableColumnCount(tableWidget=tableWidget, count=col_count)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        tableWidget.setStyleSheet("border-top : 1px solid black")
        tableWidget.setStyleSheet("border-bottom : 1px solid black")
        tableWidget.setStyleSheet("gridline-color: black")
        deligate = self.Set_deligate_for_Flow_CAO_table()
        tableWidget.setItemDelegate(deligate)

    def adjustColWidth_LH_CAO(self, tableWidget):
        for i in range(tableWidget.columnCount()):
            if i == 4:
                tableWidget.setColumnWidth(i, 65)
            else:
                tableWidget.setColumnWidth(i, 50)
    def adjustColWidth_RH_CAO(self, tableWidget):
        for i in range(tableWidget.columnCount()):
            if i == 0:
                tableWidget.setColumnWidth(i, 65)
            else:
                tableWidget.setColumnWidth(i, 50)

    def _sectionDifference(self,val):
        diff =[]
        val = str(val)
        if len(val)>3 :
            val = val.split("-")
            val = list(map(lambda x: x.replace('C', ''), val))
            diff = float(val[1]) - float(val[0])
            return diff
        else:
            return diff == 2

    def adjustRowHeight_LH_CAO(self, tableWidget,df):

        for row in range(tableWidget.rowCount()):
            diff = self._sectionDifference(df.iloc[row,4])
            if diff == 1 :
                tableWidget.setRowHeight(row, 15)
            else:
                tableWidget.setRowHeight(row, 30)

    def adjustRowHeight_RH_CAO(self, tableWidget,df):

        for row in range(tableWidget.rowCount()):
            diff = self._sectionDifference(df.iloc[row,0])
            if diff == 1 :
                tableWidget.setRowHeight(row, 15)
            else:
                tableWidget.setRowHeight(row, 30)



    def populateTable_LH_CAO(self, tableWidget, df , commentdf):
        commentdf = commentdf.replace(np.nan, " ")
        commentdf = commentdf.astype(str)
        for row in range(len(df.index)):
            for col in range(len(df.columns)):
                self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=df.iloc[row, col])
                tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
                if pd.notnull(commentdf.iloc[row,col]):
                    tableWidget.item(row, col).setToolTip(commentdf.iloc[row,col])

    def resizeTableWidget_LH_CAO(self,tableWidget,df):
        setTableWidth=0
        for i in range(len(df.columns)):
            setTableWidth += tableWidget.columnWidth(i)
        tableWidget.setFixedWidth(setTableWidth+2)
        setTableHeight = 0
        for i in range(len(df.index)):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight+2)

    def LH_CAO_Table(self,df):
        self.resetTable_LH_CAO(tableWidget=self.flowValueCAOLH_tableWidget, row_count=len(df.index),
                                 col_count=len(df.columns))
        self.adjustColWidth_LH_CAO(tableWidget=self.flowValueCAOLH_tableWidget)
        self.adjustRowHeight_LH_CAO(tableWidget=self.flowValueCAOLH_tableWidget,df=df)
        self.populateTable_LH_CAO(tableWidget=self.flowValueCAOLH_tableWidget, df=df, commentdf=df)
        self.resizeTableWidget_LH_CAO(tableWidget=self.flowValueCAOLH_tableWidget, df=df)
        # self.scrollArea.setGeometry(50, 40, 1189, self.LH_LAO_tableWidget.height())
        # self.flowValueCAOLH_tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def RH_CAO_Table(self,df):
        self.resetTable_LH_CAO(tableWidget=self.flowValueCAORH_tableWidget, row_count=len(df.index),
                                 col_count=len(df.columns))
        self.adjustColWidth_RH_CAO(tableWidget=self.flowValueCAORH_tableWidget)
        self.adjustRowHeight_RH_CAO(tableWidget=self.flowValueCAORH_tableWidget,df=df)
        self.populateTable_LH_CAO(tableWidget=self.flowValueCAORH_tableWidget, df=df, commentdf=df)
        self.resizeTableWidget_LH_CAO(tableWidget=self.flowValueCAORH_tableWidget, df=df)
    # ----------------------
    def resetTable(self,tableWidget):

        self.set_TableRowCount(tableWidget=tableWidget,count=ROW_COUNT_TABLE)
        self.set_TableColumnCount(tableWidget=tableWidget, count=COLUMN_COUNT_TABLE)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        tableWidget.setStyleSheet("border-top : 1px solid black")
        tableWidget.setStyleSheet("border-bottom : 1px solid black")
        tableWidget.setStyleSheet("gridline-color: black")
        deligate = self.Set_deligate_for_Flow_CAO_table()
        tableWidget.setItemDelegate(deligate)

    def adjustColWidth(self, tableWidget):
        for i in range(tableWidget.columnCount()):
            if i == 4:
                tableWidget.setColumnWidth(i, 65)
            else:
                tableWidget.setColumnWidth(i, 50)

    def adjustRowHeight(self, tableWidget):
        for i in range(tableWidget.rowCount()):
            tableWidget.setRowHeight(i, 30)
        smallRowWidth = [1, 2, 4, 33, 34, 39, 40]
        for i in smallRowWidth:
            tableWidget.setRowHeight(i, 15)

    def populateTable(self, tableWidget, df , commentdf):
        commentdf = commentdf.replace(np.nan, " ")
        commentdf = commentdf.astype(str)
        for row in range(ROW_COUNT_TABLE):
            for col in range(COLUMN_COUNT_TABLE):
                self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=df.iloc[row, col])
                tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
                #if pd.notnull(commentdf.iloc[row,col]):
                #    tableWidget.item(row, col).setToolTip(commentdf.iloc[row,col])

    def resizeTableWidget(self,tableWidget):
        setTableWidth=0
        for i in range(COLUMN_COUNT_TABLE):
            setTableWidth += tableWidget.columnWidth(i)
        tableWidget.setFixedWidth(setTableWidth+2)
        setTableHeight = 0
        for i in range(ROW_COUNT_TABLE):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight+2)

    # RH Table 1
    def resetTable_RH_first(self, tableWidget):

        self.set_TableRowCount(tableWidget=tableWidget, count=ROW_COUNT_TABLE)
        self.set_TableColumnCount(tableWidget=tableWidget, count=COLUMN_COUNT_TABLE)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        tableWidget.setStyleSheet("border-top : 1px solid black")
        tableWidget.setStyleSheet("border-bottom : 1px solid black")
        tableWidget.setStyleSheet("gridline-color: black")
        deligate = self.Set_deligate_for_Flow_CAO_table()
        tableWidget.setItemDelegate(deligate)


    def adjustColWidthOf_RH_firstTable(self, tableWidget):
        for i in range(tableWidget.columnCount()):
            if i == 0:
                tableWidget.setColumnWidth(i,65)
            else:
                tableWidget.setColumnWidth(i,50)

    def adjustRowHeightOf_RH_firstTable(self, tableWidget):
        for i in range(tableWidget.rowCount()):
            tableWidget.setRowHeight(i, 30)
        smallRowWidth = [1, 2, 4, 33, 34, 39, 40]
        for i in smallRowWidth:
            tableWidget.setRowHeight(i, 15)

    def populateTable_RH_first(self, tableWidget, df , commentdf):
        commentdf = commentdf.replace(np.nan, " ")
        commentdf = commentdf.astype(str)
        for row in range(ROW_COUNT_TABLE):
            for col in range(COLUMN_COUNT_TABLE):
                self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=df.iloc[row, col])
                tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
                #if pd.notnull(commentdf.iloc[row,col]):
                #    tableWidget.item(row, col).setToolTip(commentdf.iloc[row,col])

    def resizeTableWidget_RH_first(self, tableWidget):
        setTableWidth = 0
        for i in range(COLUMN_COUNT_TABLE):
            setTableWidth += tableWidget.columnWidth(i)
        tableWidget.setFixedWidth(setTableWidth + 2)
        setTableHeight = 0
        for i in range(ROW_COUNT_TABLE):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight + 2)

    # RH table 2
    def resetTable_RH_second(self, tableWidget):

        self.set_TableRowCount(tableWidget=tableWidget, count=ROW_COUNT_TABLE_LH_1)
        self.set_TableColumnCount(tableWidget=tableWidget, count=COLUMN_COUNT_TABLE_LH_1)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        tableWidget.setStyleSheet("border-top : 1px solid black")
        tableWidget.setStyleSheet("border-bottom : 1px solid black")
        tableWidget.setStyleSheet("gridline-color: black")
        deligate = self.Set_deligate_for_Flow_LAO_table()
        tableWidget.setItemDelegate(deligate)

    def adjustColWidthOf_RH_secondTable(self,tableWidget):
        for i in range(tableWidget.columnCount()):
            if i == 0:
                tableWidget.setColumnWidth(i, 65)
            else:
                tableWidget.setColumnWidth(i, 50)

    def adjustRowWidthOf_RH_secondTable(self, tableWidget):
        for i in range(tableWidget.rowCount()):
           tableWidget.setRowHeight(i, 30)
        smallRowWidth = [1,2,3,27,28,39,40]
        for i in smallRowWidth:
            tableWidget.setRowHeight(i,15)

    def populateTable_RH_second(self, tableWidget, df , commentdf):
        commentdf = commentdf.replace(np.nan, " ")
        commentdf = commentdf.astype(str)
        for row in range(ROW_COUNT_TABLE_LH_1):
            for col in range(COLUMN_COUNT_TABLE_LH_1):
                self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value= df.iloc[row, col])
                tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
                #if pd.notnull(commentdf.iloc[row,col]):
                #    tableWidget.item(row, col).setToolTip(commentdf.iloc[row,col])

    def resizeTableWidget_RH_second(self,tableWidget):
        setTableWidth=0
        for i in range(COLUMN_COUNT_TABLE_LH_1):
            setTableWidth += tableWidget.columnWidth(i)
        tableWidget.setFixedWidth(setTableWidth+2)
        setTableHeight = 0
        for i in range(ROW_COUNT_TABLE_LH_1):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight+2)


    #  Restrictor Table
    def resetTable_restrictor(self, tableWidget):

        self.set_TableRowCount(tableWidget=tableWidget, count=RES_ROW_COUNT)
        self.set_TableColumnCount(tableWidget=tableWidget, count=RES_COL_COUNT)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        tableWidget.setStyleSheet("border-style: outset;\n"
            "border-width: 2px;\n"
            "border-color: black;\n")
        tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        delegate = self.Set_deligate_for_restrictor_table()
        tableWidget.setItemDelegate(delegate)
        # tableWidget.setFont(QtGui.QFont('Arial', 10))

    def populateTable_restrictor_table(self, tableWidget, df):
        for row in range(RES_ROW_COUNT):
            for col in range(RES_COL_COUNT):
                self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value= df.iloc[row, col])
                tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)

    def resizeTableWidget_restrictor(self, tableWidget):

        setTableWidth = 0
        for i in range(RES_COL_COUNT):
            setTableWidth += tableWidget.columnWidth(i)
        tableWidget.setFixedWidth(setTableWidth + 2)
        setTableHeight = 0
        for i in range(RES_ROW_COUNT):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight+2)

    def adjustRowWidthOf_restrictor_table(self, tableWidget):
        for i in range(RES_ROW_COUNT):
            tableWidget.setRowHeight(i, 30)
        # for i in range(RES_COL_COUNT):
        #     tableWidget.setColumnWidth(i, 50)
        # tableWidget.setRowHeight(0,60)
        # tableWidget.setRowHeight(1,50)

    def adjustColWidthOf_restrictor_table(self, tableWidget):
        for i in range(tableWidget.columnCount()):
            if i == 1:
                tableWidget.setColumnWidth(i,100)
            else:
                tableWidget.setColumnWidth(i,50)

    # def set_res_col_label(self,tableWidget):
    #     tableWidget.setRowCount(2)  # row count = 43
    #     tableWidget.setColumnCount(26)
    #     #  set col width
    #     for i in range(tableWidget.columnCount()):
    #         if i == 0 :
    #             tableWidget.setColumnWidth(i,28)
    #         else:
    #             tableWidget.setColumnWidth(i, 60)
    #         tableWidget.setColumnWidth(2, 100)
    #
    #     tableWidget.setSpan(0,0,1,5)
    #     tableWidget.setSpan(0,5,1,4)
    #     tableWidget.setItem(0, 5, QTableWidgetItem("Type Limits"))
    #     tableWidget.setSpan(0,9,1,4)
    #     tableWidget.setItem(0, 9, QTableWidgetItem("Caliberation"))
    #     tableWidget.setSpan(0, 13, 1, 4)
    #     tableWidget.setItem(0, 13, QTableWidgetItem("Open Ratio"))
    #     tableWidget.setSpan(0, 17, 1, 4)
    #     tableWidget.setItem(0, 17, QTableWidgetItem("Compare Calib."))
    #     tableWidget.setSpan(0, 21, 1, 4)
    #     tableWidget.setItem(0, 21, QTableWidgetItem("Compare ratio"))
    #     tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #     tableWidget.verticalHeader().hide()
    #     # tableWidget.horizontalHeader().hide()

    def alignHeadingRes(self,tableWidget):
        col = [4, 8, 12, 16, 20]
        for i in col:
            tableWidget.item(0,i).setTextAlignment(Qt.AlignCenter)

    def backgroundColorForRes(self, tableWidget):
        for i in range(2, tableWidget.rowCount()):
            for j in [12, 13, 14, 15, 20, 21, 22, 23]:
                c = tableWidget.item(i, j).text()
                if len(c) > 0:
                    d = float(c.strip('%')) / 100
                    if d > 0.5:
                        tableWidget.item(i, j).setBackground(QColor(0, 80, 0))
                        tableWidget.item(i, j).setForeground(Qt.white)
                    if d == 0:
                        tableWidget.item(i, j).setBackground(Qt.darkGreen)
                        tableWidget.item(i, j).setForeground(Qt.white)
                    if d < 0.5 and d > 0:
                        tableWidget.item(i, j).setBackground(QColor(0, 0, 128))
                        tableWidget.item(i, j).setForeground(Qt.white)

    def tableHeadBoldRes(self,tableWidget):
        col = [4, 8, 12, 16, 20]
        for i in col:
            font = QFont('Arial', 12)
            font.setBold(True)
            tableWidget.item(0,i).setFont(font)
        for i in range(tableWidget.columnCount()):
            font = QFont('Arial', 10)
            font.setBold(True)
            tableWidget.item(1,i).setFont(font)
    def resSpan(self,tableWidget):
        col = [0, 4, 8, 12, 16, 20]
        for i in col:
            tableWidget.setSpan(0,i,1,4)

    # def resizeTable_res_header(self,tableWidget):
    #     setTableWidth = 0
    #     for i in range(26):
    #         setTableWidth += tableWidget.columnWidth(i)
    #     tableWidget.setFixedWidth(setTableWidth + 2)
    #     setTableHeight = 0
    #     for i in range(2):
    #         setTableHeight += tableWidget.rowHeight(i)
    #     tableWidget.setFixedHeight(setTableHeight + 2)

    class Set_deligate_for_restrictor_table(QtWidgets.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            return size

        def paint(self, painter, option, index):
            painter.save()
            painter.setRenderHint(painter.Antialiasing)
            painter.setClipping(True)
            painter.setClipRect(option.rect)

            super().paint(painter, option, index)
            pen = painter.pen()
            pen.setColor(Qt.black)
            pen.setWidth(2)
            painter.setPen(pen)

            option.rect.adjust(0, 0, 0, 0)

            if index.row()==0:
                painter.drawLine(option.rect.topRight(),option.rect.bottomRight())
                painter.drawLine(option.rect.bottomLeft(),option.rect.bottomRight())
            if index.row()==1:
                painter.drawLine(option.rect.topRight(),option.rect.bottomRight())
                painter.drawLine(option.rect.bottomLeft(),option.rect.bottomRight())
            tz_row=[20,38,55,70,85,104]
            for i in tz_row:
                if index.row()==i:
                    painter.drawLine(option.rect.bottomLeft(),option.rect.bottomRight())
            tz_col = [3,7,11,15,19]
            for i in tz_col:
                if index.column() == i:
                    painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
            painter.restore()

    # TZ Table of flow data

    class Set_deligate_for_Flow_TZ_table(QtWidgets.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            return size

        def paint(self, painter, option, index):
            painter.save()
            painter.setRenderHint(painter.Antialiasing)
            painter.setClipping(True)
            painter.setClipRect(option.rect)

            super().paint(painter, option, index)
            pen = painter.pen()
            pen.setColor(Qt.black)
            pen.setWidth(2)
            painter.setPen(pen)

            option.rect.adjust(0, 0, 0, 0)
            row_bottom_border_thick = [1,8,13,17,21,27,34,38]
            for i in row_bottom_border_thick:
                if index.row() == i:
                    painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

            painter.restore()

    def setRowSpanOfTZ_table(self,tableWidget):
        tableWidget.setRowCount(ROW_COUNT_TABLE_LH_1)  # row count = 43
        tableWidget.setColumnCount(1)
        TZ_list=['TZ','TZ1','TZ2','TZ3','TZ4','TZ5','TZ6','TZ7','AFT','TZ']
        row_list = [0,42,1,8,13,17,21,27,34,38]
        row_span_list = [0,0,7,5,4,4,6,7,4,4]
        tableWidget.setItem(0, 0, QTableWidgetItem('TZ'))
        tableWidget.setItem(42, 0, QTableWidgetItem('TZ'))
        tableWidget.setSpan(1, 0, 7, 1)
        tableWidget.setItem(1, 0, QTableWidgetItem('TZ1'))

        tableWidget.setSpan(8, 0, 5, 1)
        tableWidget.setItem(8, 0, QTableWidgetItem("TZ2"))

        tableWidget.setSpan(13, 0, 4, 1)
        tableWidget.setItem(13, 0, QTableWidgetItem("TZ3"))

        tableWidget.setSpan(17, 0, 4, 1)
        tableWidget.setItem(17, 0, QTableWidgetItem("TZ4"))

        tableWidget.setSpan(21, 0, 6, 1)
        tableWidget.setItem(21, 0, QTableWidgetItem("TZ5"))

        tableWidget.setSpan(27, 0, 7, 1)
        tableWidget.setItem(27, 0, QTableWidgetItem("TZ6"))

        tableWidget.setSpan(34, 0, 4, 1)
        tableWidget.setItem(34, 0, QTableWidgetItem("TZ7"))

        tableWidget.setSpan(38, 0, 4, 1)
        tableWidget.setItem(38, 0, QTableWidgetItem("AFT"))
        tableWidget.setStyleSheet("border-color :  solid black")
        tableWidget.setStyleSheet("border-width:2px")
        tableWidget.setStyleSheet("border-style:outset")
        tableWidget.setStyleSheet("gridline-color: black")

    def resizeTableWidget_LH_TZ_first(self, tableWidget):

        setTableHeight = 0
        for i in range(ROW_COUNT_TABLE_LH_1):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight+2)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        tableWidget.setFixedWidth(30)
        deligate = self.Set_deligate_for_Flow_TZ_table()
        tableWidget.setItemDelegate(deligate)
        # tableWidget.resizeColumnsToContents()


    #  TZ Table of restrictor

    class Set_deligate_for_restrictor_TZ_table(QtWidgets.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            return size

        def paint(self, painter, option, index):
            painter.save()
            painter.setRenderHint(painter.Antialiasing)
            painter.setClipping(True)
            painter.setClipRect(option.rect)

            super().paint(painter, option, index)
            pen = painter.pen()
            pen.setColor(Qt.black)
            pen.setWidth(2)
            painter.setPen(pen)

            option.rect.adjust(0, 0, 0, 0)
            tz_row = [0,2,21,39,56,71,86,105]
            for i in tz_row:
                if index.row() == i:
                    painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
            painter.restore()

    def setRowSpanOf_res_TZ_table(self,tableWidget):
        tableWidget.setRowCount(RES_ROW_COUNT)
        tableWidget.setColumnCount(1)

        tableWidget.setSpan(0, 0, 2, 1)
        tableWidget.setItem(0, 0, QTableWidgetItem('TZ'))
        # tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)

        tableWidget.setSpan(2, 0, 19, 1)
        tableWidget.setItem(2, 0, QTableWidgetItem('TZ1'))
        # tableWidget.item(2, 0).setTextAlignment(Qt.AlignCenter)

        tableWidget.setSpan(21, 0, 18, 1)
        tableWidget.setItem(21, 0, QTableWidgetItem("TZ2"))
        # tableWidget.item(21, 0).setTextAlignment(Qt.AlignCenter)

        tableWidget.setSpan(39, 0, 17, 1)
        tableWidget.setItem(39, 0, QTableWidgetItem("TZ3"))
        # tableWidget.item(39, 0).setTextAlignment(Qt.AlignCenter)

        tableWidget.setSpan(56, 0, 15, 1)
        tableWidget.setItem(56, 0, QTableWidgetItem("TZ4"))
        # tableWidget.item(56, 0).setTextAlignment(Qt.AlignCenter)

        tableWidget.setSpan(71, 0, 15, 1)
        tableWidget.setItem(71, 0, QTableWidgetItem("TZ5"))
        # tableWidget.item(71,0).setTextAlignment(Qt.AlignCenter)

        tableWidget.setSpan(86, 0, 19, 1)
        tableWidget.setItem(86, 0, QTableWidgetItem("TZ6"))
        # tableWidget.item(86, 0).setTextAlignment(Qt.AlignCenter)

        tableWidget.setSpan(105, 0, 19, 1)
        tableWidget.setItem(105, 0, QTableWidgetItem("TZ7"))
        # tableWidget.item(105,0).setTextAlignment(Qt.AlignCenter)

        tableWidget.setStyleSheet("border-style: outset;\n"
                                  "border-width: 2px;\n"
                                  "border-color: black;\n")
        tableWidget.setShowGrid(False)
        tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        delegate = self.Set_deligate_for_restrictor_TZ_table()
        tableWidget.setItemDelegate(delegate)
        # for row in range(tableWidget.rowCount()):
        #     tableWidget.item(row, 0).setTextAlignment(Qt.AlignCenter)


    def resizeTableWidget_res_TZ(self, tableWidget):

        setTableHeight = 0
        for i in range(RES_ROW_COUNT):
            setTableHeight += tableWidget.rowHeight(i)
        print('TZ height',setTableHeight)
        tableWidget.setFixedHeight(setTableHeight+2)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        tableWidget.setFixedWidth(30)

        # tableWidget.setFixedHeight(610)

    def adjustRowSize_res_TZ(self, tableWidget):
        for i in range(RES_ROW_COUNT):
            tableWidget.setRowHeight(i,30)
        # tableWidget.setRowHeight(0, 60)
        # tableWidget.setRowHeight(1, 50)

    def tableHeadBoldResTZ(self,tableWidget):
        font = QFont()
        font.setBold(True)
        tableWidget.item(0, 0).setFont(font)
        tableWidget.item(0,0)


    #  colour cells
    def colourCells(self, tableWidget, listofTuple_colorLimits ):
        """

        :param tableWidget:
        :param listofTuple_colorLimits:
        listofTuple_colorLimits= [(-20, -10, "RGB" ),(-10,"RGB" ) ]
        :return:
        """
        pass
    def colour(self,tableWidget,colorList):
        for i in range(1,tableWidget.rowCount()):
            for j in range(tableWidget.columnCount()):
                a = tableWidget.item(i,j).text()
                if a != 'AVG':
                    b = float(a.strip('%')) / 100
                    if b >= 0.02:
                        tableWidget.item(i,j).setBackground(Qt.gray)

                else:
                    b = a


    def backgroundColorForLH(self, tableWidget,colorlimits):
         for i in range(1,tableWidget.rowCount()-1):

                c = tableWidget.item(i, 3).text()
                d = float(c.strip('%')) / 100
                if d == -1.0:
                    tableWidget.item(i, 3).setBackground(QColor(255,204,0))
                if d > colorlimits[0][0] and d < colorlimits[0][1]:
                    tableWidget.item(i, 3).setBackground(QColor(0,102,204))
                if d >= colorlimits[1][0] and d < colorlimits[1][1] :
                    tableWidget.item(i, 3).setBackground(QColor(58, 190, 246))
                if d >= colorlimits[2][0] and d <= colorlimits[2][1]:
                    tableWidget.item(i, 3).setBackground(Qt.darkGreen)
                if d > colorlimits[3][0] and d <= colorlimits[3][1]:
                    tableWidget.item(i, 3).setBackground(QColor(234, 160, 160))
                if d > colorlimits[4][0] and d < colorlimits[4][1]:
                    tableWidget.item(i, 3).setBackground(Qt.red)



    def backgroundColorForRH(self, tableWidget,colorlimits):
        for i in range(1,tableWidget.rowCount()-1):
            c = tableWidget.item(i, 1).text()
            d =  float(c.strip('%')) /100
            if d == -1.0:
                tableWidget.item(i, 1).setBackground(QColor(255,204,0))
            if d > colorlimits[0][0] and d < colorlimits[0][1]:
                tableWidget.item(i, 1).setBackground(QColor(0, 102, 204))
            if d >= colorlimits[1][0] and d < colorlimits[1][1]:
                tableWidget.item(i, 1).setBackground(QColor(58, 190, 246))
            if d >= colorlimits[2][0] and d <= colorlimits[2][1]:
                tableWidget.item(i, 1).setBackground(Qt.darkGreen)
            if d > colorlimits[3][0] and d <= colorlimits[3][1]:
                tableWidget.item(i, 1).setBackground(QColor(234, 160, 160))
            if d > colorlimits[4][0] and d < colorlimits[4][1]:
                tableWidget.item(i, 1).setBackground(Qt.red)


    def setCellColor(self,tableWidget):
        for i in range(tableWidget.rowCount()):
            for j in range(tableWidget.columnCount()):
                if tableWidget.item(i,j).text()=='0':
                    tableWidget.item(i, j).setForeground(QColor(255,204,0))
                    # tableWidget.item(i, j).setForeground(QColor(255,204,0))


    def tableHeadBold(self,tableWidget):
        for i in range(tableWidget.columnCount()):
            font = QFont()
            font.setBold(True)
            tableWidget.item(0,i).setFont(font)
            tableWidget.item(42, i).setFont(font)

    def setSpanLH(self,tableWidget):
        tableWidget.setSpan(0,3,1,2)
        tableWidget.setSpan(42, 3, 1, 2)

    def setSpanRH(self,tableWidget):
        tableWidget.setSpan(0,0,1,2)
        tableWidget.setSpan(42, 0, 1, 2)

    def alignHeadingLH(self,tableWidget):
        tableWidget.item(0, 3).setTextAlignment(Qt.AlignCenter)

    def alignHeadingRH(self,tableWidget):
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)

    def setGeometryOFflowTZ1(self,tableWidget):
        tableWidget.setGeometry(5, 10, tableWidget.width(), tableWidget.height())

    def setGeometryOFflowLH1(self,tableWidget,tableWidgetTZ1):
        tableWidget.setGeometry(5+ tableWidgetTZ1.width(), 10, tableWidget.width(), tableWidget.height())

    def setGeometryOFflowLH2(self, tableWidget,tableWidgetTZ1,tableWidget1):
        tableWidget.setGeometry(5+ tableWidgetTZ1.width() + tableWidget1.width(), 10, tableWidget.width(),
                                 tableWidget.height())

    def setGeometryOFflowTZ2(self,tableWidget):
        tableWidget.setGeometry(1480, 10, tableWidget.width(), tableWidget.height())

    def setGeometryOFflowRH2(self,tableWidget):
        tableWidget.setGeometry(1480 - tableWidget.width(), 10, tableWidget.width(), tableWidget.height())

    def setGeometryOFflowRH1(self,tableWidget,tableWidget4):
        tableWidget.setGeometry(1480 - tableWidget.width() - tableWidget4.width(), 10, tableWidget.width(),
                                 tableWidget.height())

    # TZ Table

    class Set_deligate_for_TZ_table(QtWidgets.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            return size

        def paint(self, painter, option, index):
            painter.save()
            painter.setRenderHint(painter.Antialiasing)
            painter.setClipping(True)
            painter.setClipRect(option.rect)

            super().paint(painter, option, index)
            pen = painter.pen()
            pen.setColor(Qt.black)
            pen.setWidth(1)
            painter.setPen(pen)

            option.rect.adjust(0, 0, 0, 0)
            painter.drawLine(option.rect.topLeft(),option.rect.topRight())
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
            painter.drawLine(option.rect.topRight(),option.rect.bottomRight())
            painter.drawLine(option.rect.topLeft(),option.rect.bottomLeft())
            painter.restore()
    def resetTable_TZ(self,tableWidget):
        self.set_TableRowCount(tableWidget=tableWidget, count=TZ_ROW_COUNT)
        self.set_TableColumnCount(tableWidget=tableWidget, count=TZ_COL_COUNT)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        # tableWidget.setStyleSheet("Border-style:outset;\n" "Border-width:2px;\n" "Border-color:solid black;\n")
        deligate = self.Set_deligate_for_TZ_table()
        tableWidget.setItemDelegate(deligate)

    def populateTable_TZ_table(self, tableWidget, df,commentdf):
        commentdf = commentdf.replace(np.nan, " ")
        commentdf = commentdf.astype(str)
        for row in range(TZ_ROW_COUNT):
            for col in range(TZ_COL_COUNT):
                self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value= df.iloc[row, col])
                tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
                if pd.notnull(commentdf.iloc[row,col]):
                    tableWidget.item(row, col).setToolTip(commentdf.iloc[row,col])

        font = QFont()
        font.setBold(True)
        for row in range(4,TZ_ROW_COUNT):
            for col in range(TZ_COL_COUNT):
                tableWidget.item(row, col).setFont(font)

        tableWidget.setStyleSheet("border : 1px solid black")
        tableWidget.setStyleSheet("gridline-color: black")
        # tableWidget.setSpan(0,0,2,1)

    def resizeTableWidget_TZ(self, tableWidget):

        setTableWidth = 0
        for i in range(TZ_COL_COUNT):
            setTableWidth += tableWidget.columnWidth(i)
        tableWidget.setFixedWidth(setTableWidth + 2)
        setTableHeight = 0
        for i in range(TZ_ROW_COUNT):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight + 2)

    def adjustRowWidthOf_TZ_table(self, tableWidget):
        for i in range(TZ_ROW_COUNT):
            tableWidget.setRowHeight(i, 30)
        for i in range(TZ_COL_COUNT):
            tableWidget.setColumnWidth(i, 50)


    def adjustColWidthOf_TZ_table(self, tableWidget):
        for i in range(tableWidget.columnCount()):
            tableWidget.setColumnWidth(i,45)

    def set_TZ_col_label(self,tableWidget):

        tableWidget.setSpan(0,1,1,9)
        tableWidget.setItem(0, 1, QTableWidgetItem("TEMPERATURE ZONE ANALYSIS"))

        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)


    def tableHeadBoldTZ(self,tableWidget):
        font = QFont()
        font.setBold(True)
        tableWidget.item(0, 1).setFont(font)
        tableWidget.item(2, 0).setFont(font)
        tableWidget.item(3, 0).setFont(font)
        tableWidget.item(5, 0).setFont(font)
        tableWidget.item(1, 1).setFont(font)
        tableWidget.item(1, 2).setFont(font)
        tableWidget.item(1, 3).setFont(font)
        tableWidget.item(1, 4).setFont(font)
        tableWidget.item(1, 5).setFont(font)
        tableWidget.item(1, 6).setFont(font)
        tableWidget.item(1, 7).setFont(font)
        tableWidget.item(1, 8).setFont(font)
        tableWidget.item(1, 9).setFont(font)
        tableWidget.item(1,10).setFont(font)

    def backgroundColorForTZ(self, tableWidget, colorlimits):
        for i in range(1, tableWidget.columnCount()):

            c = tableWidget.item(4, i).text()
            if len(c)>0:
                d = float(c.strip('%')) / 100
                if d == -1.0:
                    tableWidget.item(4, i).setBackground(QColor(255,204,0))
                if d > colorlimits[0][0] and d < colorlimits[0][1]:
                    tableWidget.item(4, i).setBackground(QColor(0,102,204))
                if d >= colorlimits[1][0] and d < colorlimits[1][1]:
                    tableWidget.item(4, i).setBackground(QColor(58,190,246))
                if d >= colorlimits[2][0] and d <= colorlimits[2][1]:
                    tableWidget.item(4, i).setBackground(Qt.darkGreen)
                if d > colorlimits[3][0] and d <= colorlimits[3][1]:
                    tableWidget.item(4, i).setBackground(QColor(234, 160, 160))
                if d > colorlimits[4][0] and d < colorlimits[4][1]:
                    tableWidget.item(4, i).setBackground(Qt.red)

    def setEmptyCellBackgroungGray_TZ(self,tableWidget):
        for row in range(1,tableWidget.rowCount()):
            for col in range(1,tableWidget.columnCount()-1):
                c = tableWidget.item(row, col).text()
                if len(c)==0:
                    tableWidget.item(row,col).setBackground(Qt.gray)

    # colour range table widget
    def resetTable_ColourRange(self,tableWidget):
        self.set_TableRowCount(tableWidget=tableWidget, count=CLR_RANGE_ROW_COUNT)
        self.set_TableColumnCount(tableWidget=tableWidget, count=CLR_RANGE_COL_COUNT)
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()

    def resizeTableWidget_ColourRange(self, tableWidget):

        setTableWidth = 0
        for i in range(CLR_RANGE_COL_COUNT):
            setTableWidth += tableWidget.columnWidth(i)
        tableWidget.setFixedWidth(setTableWidth + 2)
        setTableHeight = 0
        for i in range(CLR_RANGE_ROW_COUNT):
            setTableHeight += tableWidget.rowHeight(i)
        tableWidget.setFixedHeight(setTableHeight + 2)

    def adjustColWidthOf_ColourRange_table(self, tableWidget):
        for i in range(tableWidget.columnCount()):
            tableWidget.setColumnWidth(i,49)

    def populateTable_ColourRange_table(self, tableWidget,count,percentage):
        col_1 = ['<20%','<10%','OK','>10%','>20%','N/A']
        colours = [ QColor(0, 102, 204), QColor(58, 190, 246),Qt.darkGreen, QColor(234, 160, 160), Qt.red, QColor(255,204,0)]
        for row in range(TZ_ROW_COUNT):

                self.setCellValueInt(tableWidget=tableWidget, row=row, column=0, value=col_1[row])
                tableWidget.item(row, 0).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, 0).setFlags(tableWidget.item(row, 0).flags() & ~Qt.ItemIsEditable)
                tableWidget.item(row,0).setBackground(colours[row])
                font = QFont()
                font.setBold(True)
                tableWidget.item(row, 0).setFont(font)

                self.setCellValueInt(tableWidget=tableWidget, row=row, column=1, value=count[row])
                tableWidget.item(row, 1).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, 1).setFlags(tableWidget.item(row, 1).flags() & ~Qt.ItemIsEditable)

                self.setCellValueInt(tableWidget=tableWidget, row=row, column=2, value=percentage[row])
                tableWidget.item(row, 2).setTextAlignment(Qt.AlignCenter)
                tableWidget.item(row, 2).setFlags(tableWidget.item(row, 2).flags() & ~Qt.ItemIsEditable)

                tableWidget.setStyleSheet("border : 1px solid black")
                tableWidget.setStyleSheet("gridline-color: black")

    def populateTable_AMBIENT_PRESSURE_TEMP_table(self, tableWidget,AmbP,AmbT):
          self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=AmbP)
          tableWidget.item(0,0 ).setTextAlignment(Qt.AlignCenter)
          tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)


          self.setCellValueInt(tableWidget=tableWidget, row=0, column=3, value=AmbT)
          tableWidget.item(0,3).setTextAlignment(Qt.AlignCenter)
          tableWidget.item(0, 3).setFlags(tableWidget.item(0, 3).flags() & ~Qt.ItemIsEditable)

    def populateTable_Mx1_table(self, tableWidget, Mx1):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=1, value=Mx1[0])
        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 1).setFlags(tableWidget.item(0, 1).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=1, value=Mx1[1])
        tableWidget.item(1,1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,1).setFlags(tableWidget.item(1,1).flags() & ~Qt.ItemIsEditable)

    def populateTable_Mx2_table(self, tableWidget, Mx2):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=1, value=Mx2[0])
        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 1).setFlags(tableWidget.item(0, 1).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=1, value=Mx2[1])
        tableWidget.item(1,1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,1).setFlags(tableWidget.item(1,1).flags() & ~Qt.ItemIsEditable)

    def populateTable_Mx3_table(self, tableWidget, Mx3):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=1, value=Mx3[0])
        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 1).setFlags(tableWidget.item(0, 1).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=1, value=Mx3[1])
        tableWidget.item(1,1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,1).setFlags(tableWidget.item(1,1).flags() & ~Qt.ItemIsEditable)

    def populateTable_Mx4_table(self, tableWidget, Mx4):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=1, value=Mx4[0])
        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 1).setFlags(tableWidget.item(0, 1).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=1, value=Mx4[1])
        tableWidget.item(1,1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,1).setFlags(tableWidget.item(1,1).flags() & ~Qt.ItemIsEditable)

    def populateTable_Mx5_table(self, tableWidget, Mx5):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=1, value=Mx5[0])
        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 1).setFlags(tableWidget.item(0, 1).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=1, value=Mx5[1])
        tableWidget.item(1,1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,1).setFlags(tableWidget.item(1,1).flags() & ~Qt.ItemIsEditable)

    def populateTable_Mx6_table(self, tableWidget, Mx6):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=1, value=Mx6[0])
        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 1).setFlags(tableWidget.item(0, 1).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=1, value=Mx6[1])
        tableWidget.item(1,1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,1).setFlags(tableWidget.item(1,1).flags() & ~Qt.ItemIsEditable)
    def populateTable_Mx7_table(self, tableWidget, Mx7):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=1, value=Mx7[0])
        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 1).setFlags(tableWidget.item(0, 1).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=1, value=Mx7[1])
        tableWidget.item(1,1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,1).setFlags(tableWidget.item(1,1).flags() & ~Qt.ItemIsEditable)

    def populateTable_Mx8_table(self, tableWidget, Mx8):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=1, value=Mx8[0])
        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 1).setFlags(tableWidget.item(0, 1).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=1, value=Mx8[1])
        tableWidget.item(1,1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,1).setFlags(tableWidget.item(1,1).flags() & ~Qt.ItemIsEditable)

    def populateTable_MxAG_table(self, tableWidget, MxAG):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=1, value=MxAG[0])
        tableWidget.item(0, 1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 1).setFlags(tableWidget.item(0, 1).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=1, value=MxAG[1])
        tableWidget.item(1,1).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,1).setFlags(tableWidget.item(1,1).flags() & ~Qt.ItemIsEditable)
    def populateTable_Cb1_table(self, tableWidget, Cb1):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=Cb1[0])
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=0, value=Cb1[1])
        tableWidget.item(1,0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,0).setFlags(tableWidget.item(1,0).flags() & ~Qt.ItemIsEditable)
    def populateTable_Cb2_table(self, tableWidget, Cb2):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=Cb2[0])
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=0, value=Cb2[1])
        tableWidget.item(1,0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,0).setFlags(tableWidget.item(1,0).flags() & ~Qt.ItemIsEditable)
    def populateTable_Cb3_table(self, tableWidget, Cb3):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=Cb3[0])
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=0, value=Cb3[1])
        tableWidget.item(1,0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,0).setFlags(tableWidget.item(1,0).flags() & ~Qt.ItemIsEditable)
    def populateTable_Cb4_table(self, tableWidget, Cb4):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=Cb4[0])
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=0, value=Cb4[1])
        tableWidget.item(1,0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,0).setFlags(tableWidget.item(1,0).flags() & ~Qt.ItemIsEditable)
    def populateTable_Cb5_table(self, tableWidget, Cb5):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=Cb5[0])
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=0, value=Cb5[1])
        tableWidget.item(1,0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,0).setFlags(tableWidget.item(1,0).flags() & ~Qt.ItemIsEditable)
    def populateTable_Cb6_table(self, tableWidget, Cb6):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=Cb6[0])
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=0, value=Cb6[1])
        tableWidget.item(1,0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,0).setFlags(tableWidget.item(1,0).flags() & ~Qt.ItemIsEditable)
    def populateTable_Cb7_table(self, tableWidget, Cb7):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=Cb7[0])
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=0, value=Cb7[1])
        tableWidget.item(1,0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,0).setFlags(tableWidget.item(1,0).flags() & ~Qt.ItemIsEditable)
    def populateTable_Cb8_table(self, tableWidget, Cb8):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=Cb8[0])
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)

        self.setCellValueInt(tableWidget=tableWidget, row=1, column=0, value=Cb8[1])
        tableWidget.item(1,0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(1,0).setFlags(tableWidget.item(1,0).flags() & ~Qt.ItemIsEditable)
    def populateTable_CbAG_table(self, tableWidget, CbAG):

        self.setCellValueInt(tableWidget=tableWidget, row=0, column=0, value=CbAG[0])
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        tableWidget.item(0, 0).setFlags(tableWidget.item(0, 0).flags() & ~Qt.ItemIsEditable)

    # Pressure Port TZ
    # def resetTable_PP_TZ1(self, tableWidget,):
    #     self.set_TableRowCount(tableWidget=tableWidget, count=CLR_RANGE_ROW_COUNT)
    #     self.set_TableColumnCount(tableWidget=tableWidget, count=CLR_RANGE_COL_COUNT)
    #     tableWidget.verticalHeader().hide()
    #     tableWidget.horizontalHeader().hide()
    def populateTable_PP_TZ1_table(self, tableWidget, TZ1_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0, 0, 1, 2)
        tableWidget.setItem(0, 0, QTableWidgetItem("TZ1"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height = 0
        if len(TZ1_df) > 0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(TZ1_df) + 1)
            for row in range(1, tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=TZ1_df.iloc[row - 1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0, 40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def populateTable_PP_TZ2_table(self, tableWidget, TZ2_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0, 0, 1, 2)
        tableWidget.setItem(0, 0, QTableWidgetItem("TZ2"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height = 0
        if len(TZ2_df) > 0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(TZ2_df) + 1)
            for row in range(1, tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=TZ2_df.iloc[row - 1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0, 40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def populateTable_PP_TZ3_table(self, tableWidget, TZ3_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0,0,1,2)
        tableWidget.setItem(0, 0, QTableWidgetItem("TZ3"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height =0
        if len(TZ3_df)>0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(TZ3_df)+1)
            for row in range(1,tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=TZ3_df.iloc[row-1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0,40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def populateTable_PP_TZ4_table(self, tableWidget, TZ4_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0,0,1,2)
        tableWidget.setItem(0, 0, QTableWidgetItem("TZ4"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height =0
        if len(TZ4_df)>0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(TZ4_df)+1)
            for row in range(1,tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=TZ4_df.iloc[row-1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0,40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def populateTable_PP_TZ5_table(self, tableWidget, TZ5_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0,0,1,2)
        tableWidget.setItem(0, 0, QTableWidgetItem("TZ5"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height =0
        if len(TZ5_df)>0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(TZ5_df)+1)
            for row in range(1,tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=TZ5_df.iloc[row-1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0,40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def populateTable_PP_TZ6_table(self, tableWidget, TZ6_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0,0,1,2)
        tableWidget.setItem(0, 0, QTableWidgetItem("TZ6"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height =0
        if len(TZ6_df)>0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(TZ6_df)+1)
            for row in range(1,tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=TZ6_df.iloc[row-1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0,40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def populateTable_PP_TZ7_table(self, tableWidget, TZ7_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0,0,1,2)
        tableWidget.setItem(0, 0, QTableWidgetItem("TZ7"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height =0
        if len(TZ7_df)>0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(TZ7_df)+1)
            for row in range(1,tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=TZ7_df.iloc[row-1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0,40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def populateTable_PP_TZ8_table(self, tableWidget, TZ8_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0,0,1,2)
        tableWidget.setItem(0, 0, QTableWidgetItem("TZ8"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height =0
        if len(TZ8_df)>0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(TZ8_df)+1)
            for row in range(1,tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=TZ8_df.iloc[row-1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0,40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def populateTable_FCRC_table(self, tableWidget, FCRC_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0, 0, 1, 2)
        tableWidget.setItem(0, 0, QTableWidgetItem("FCRC"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height = 0
        if len(FCRC_df) > 0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(FCRC_df) + 1)
            for row in range(1, tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=FCRC_df.iloc[row - 1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0, 40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def populateTable_CCRC_table(self, tableWidget, CCRC_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0, 0, 1, 2)
        tableWidget.setItem(0, 0, QTableWidgetItem("CCRC"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height = 0
        if len(CCRC_df) > 0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(CCRC_df) + 1)
            for row in range(1, tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=CCRC_df.iloc[row - 1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0, 40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def populateTable_CVS_table(self, tableWidget, CVS_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0, 0, 1, 2)
        tableWidget.setItem(0, 0, QTableWidgetItem("CVS"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height = 0
        if len(CVS_df) > 0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(CVS_df) + 1)
            for row in range(1, tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=CVS_df.iloc[row - 1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0, 40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def populateTable_AVS_table(self, tableWidget, AVS_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0, 0, 1, 2)
        tableWidget.setItem(0, 0, QTableWidgetItem("AVS"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height = 0
        if len(AVS_df) > 0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(AVS_df) + 1)
            for row in range(1, tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=AVS_df.iloc[row - 1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0, 40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def populateTable_CAX_table(self, tableWidget, CAX_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0, 0, 1, 2)
        tableWidget.setItem(0, 0, QTableWidgetItem("CAX"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height = 0
        if len(CAX_df) > 0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(CAX_df) + 1)
            for row in range(1, tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=CAX_df.iloc[row - 1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0, 40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def populateTable_CC_table(self, tableWidget, CC_df):
        tableWidget.verticalHeader().hide()
        tableWidget.horizontalHeader().hide()
        self.set_TableRowCount(tableWidget=tableWidget, count=2)
        self.set_TableColumnCount(tableWidget=tableWidget, count=2)
        tableWidget.setSpan(0, 0, 1, 2)
        tableWidget.setItem(0, 0, QTableWidgetItem("CC"))
        tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        row_height = 0
        if len(CC_df) > 0:
            self.set_TableRowCount(tableWidget=tableWidget, count=len(CC_df) + 1)
            for row in range(1, tableWidget.rowCount()):
                row_height += tableWidget.rowHeight(row)
                for col in range(2):
                    self.setCellValueInt(tableWidget=tableWidget, row=row, column=col, value=CC_df.iloc[row - 1, col])
                    tableWidget.resizeColumnToContents(col)
                    tableWidget.item(row, col).setTextAlignment(Qt.AlignCenter)
                    tableWidget.item(row, col).setFlags(tableWidget.item(row, col).flags() & ~Qt.ItemIsEditable)
            tableWidget.setFixedWidth(tableWidget.columnWidth(0) + tableWidget.columnWidth(1) + 2)
            tableWidget.setFixedHeight(row_height + 32)
        else:
            tableWidget.setSpan(1, 0, 1, 2)
            tableWidget.setItem(1, 0, QTableWidgetItem("NO DATA"))
            tableWidget.item(1, 0).setTextAlignment(Qt.AlignCenter)
            tableWidget.rowHeight(30)
            tableWidget.setColumnWidth(0, 40)
            tableWidget.setColumnWidth(1, 40)
            tableWidget.setFixedWidth(80)
            tableWidget.setFixedHeight(62)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


    def populateTable_PP_TZ(self,tableWidget1,df1,tableWidget2,df2,tableWidget3,df3,tableWidget4,df4,tableWidget5,df5,tableWidget6,df6,tableWidget7,df7,tableWidget8,df8,tableWidget9,df9,
                            tableWidget10,df10,tableWidget11,df11,tableWidget12,df12,tableWidget13,df13,tableWidget14,df14):
        self.populateTable_PP_TZ1_table(tableWidget=tableWidget1,TZ1_df=df1)
        self.populateTable_PP_TZ2_table(tableWidget2,df2)
        self.populateTable_PP_TZ3_table(tableWidget3,df3)
        self.populateTable_PP_TZ4_table(tableWidget4, df4)
        self.populateTable_PP_TZ5_table(tableWidget5, df5)
        self.populateTable_PP_TZ6_table(tableWidget6, df6)
        self.populateTable_PP_TZ7_table(tableWidget7, df7)
        self.populateTable_PP_TZ8_table(tableWidget8, df8)
        max_ht = max(len(df1),len(df2),len(df3),len(df4),len(df5),len(df6),len(df7),len(df8))
        print('max_ht: ',max_ht)
        self.populateTable_FCRC_table(tableWidget9,df9)
        tableWidget9.setGeometry(80, (max_ht*40 )+ 100, tableWidget9.width(), tableWidget9.height())
        self.populateTable_CCRC_table(tableWidget10,df10)
        tableWidget10.setGeometry(230, (max_ht*40 )+ 100, tableWidget10.width(), tableWidget10.height())
        self.populateTable_CVS_table(tableWidget11,df11)
        tableWidget11.setGeometry(390,(max_ht*40 )+ 100, tableWidget11.width(), tableWidget11.height())
        self.populateTable_AVS_table(tableWidget12,df12)
        tableWidget12.setGeometry(540, (max_ht*40 )+ 100, tableWidget12.width(), tableWidget12.height())
        self.populateTable_CAX_table(tableWidget13,df13)
        tableWidget13.setGeometry(690, (max_ht*40 )+ 100, tableWidget13.width(), tableWidget13.height())
        self.populateTable_CC_table(tableWidget14,df14)
        tableWidget14.setGeometry(850, (max_ht*40 )+ 100, tableWidget14.width(), tableWidget14.height())
        if max_ht==0:
            tableWidget9.setGeometry(80, 200, tableWidget9.width(), tableWidget9.height())
            tableWidget10.setGeometry(230, 200, tableWidget10.width(), tableWidget10.height())
            tableWidget11.setGeometry(390, 200, tableWidget11.width(), tableWidget11.height())
            tableWidget12.setGeometry(540, 200, tableWidget12.width(), tableWidget12.height())
            tableWidget13.setGeometry(690, 200, tableWidget13.width(), tableWidget13.height())
            tableWidget14.setGeometry(850, 200, tableWidget14.width(), tableWidget14.height())

    #  load Image
    def loadImage(self):
        pixmap = QPixmap('X:/Aditi/Work_Done/ADAMANT_code/aircraft.jpg')
        self.aircraftImage_label.setPixmap(pixmap)

    #   load ADAMANT logo image
    def loadImage_ADAMANT_Logo(self):
        pixmap = QPixmap('X:/Aditi/Work_Done/ADAMANT_code/ADAMANT_Logo.jpg')
        self.adamant_logo_label.setPixmap(pixmap)


#     pie chart

    def create_piechart(self,pieDiagram_groupBox,data_count):

        # scene = QGraphicsScene()
        # families = [1, 2, 3, 4, 5, 6]
        # total = 0
        # set_angle = 0
        # count1 = 0
        # colours = [ QColor(0, 102, 204), QColor(58, 190, 246),Qt.darkGreen, QColor(234, 160, 160), Qt.red, QColor(255,204,0)]
        # total = sum(families)
        # for family in families:
        #     angle = round(float(family * 5760) / total)
        #     ellipse = QGraphicsEllipseItem(0, 0, 150, 150)
        #     ellipse.setPos(0, 0)
        #     ellipse.setStartAngle(set_angle)
        #     ellipse.setSpanAngle(angle)
        #     ellipse.setBrush(colours[count1])
        #     set_angle += angle
        #     count1 += 1
        #     scene.addItem(ellipse)
        #
        # chartview = QGraphicsView(scene)
        # vbox = QVBoxLayout()
        # self.pieDiagram_groupBox.setLayout(vbox)
        # vbox.addWidget(chartview)


        # figure(1, figsize=(10, 3))
        # ax = axes([0.1, 0.1, 0.8, 0.8])
        # labels = ['Python', 'C++', 'Ruby', 'Java']
        # count = [215, 130, 245, 210]
        # explode = (0, 0.15, 0, 0)
        # # Plot
        # plt.pie(sizes,labels=labels,
        #         autopct='%1.2f%%', shadow=True, explode=explode)
        # self.canvas.draw()

        labels =['<20%','<10%','OK','>10%','>20%']
        explode = (0.0, 0.1, 0.0, 0.0, 0.0)
        colr = [QColor(0, 102, 204), QColor(58, 190, 246), Qt.darkGreen, QColor(234, 160, 160), Qt.red,Qt.yellow]
        # wp = {'linewidth': 1, 'edgecolor': Qt.green}
        explode = (0, 0.15, 0, 0,0)
        # plt.pie(data_count,autopct='%1.2f%%', shadow=True, explode=explode)
        plt.pie(data_count,  shadow=True, explode=explode)
        # data_count.plt(kind ='pie',color = colr)



        self.canvas.draw()

    def plotTRanalysis(self):
        # df = pd.read_excel('TRanalysis_data.xlsx')
        # x = list(df.iloc[2,:])
        # plt.figure(figsize=(10, 10))
        # plt.style.use('seaborn')
        # plt.scatter(x, marker="*", s=100, edgecolors="black", c="yellow")
        # plt.title("Excel sheet to Scatter Plot")
        # plt.show()
        pass


'''
def test6(app):
    """
    testing restrictor table
    :param app:
    :return:
    """

    import pandas as pd
    # LH First table
    df_res = pd.read_excel("restrictor.xlsx")
    df_res = df_res.fillna("0-0")
    tableWidget_res=app.tableWidget_2
    app.resetTable_restrictor(tableWidget_res)
    app.adjustRowWidthOf_restrictor_table(tableWidget_res)
    app.adjustColWidthOf_restrictor_table(tableWidget_res)
    app.populateTable_restrictor_table(tableWidget=tableWidget_res, df=df_res)
    app.resizeTableWidget_restrictor(tableWidget=tableWidget_res)
    tableWidget_res.setFont(QtGui.QFont('Arial', 10))

    #  restrictor TZ tables

    tableWidget_res_TZ1 = app.tableWidget
    app.setRowSpanOf_res_TZ_table(tableWidget_res_TZ1)
    app.adjustRowSize_res_TZ(tableWidget_res_TZ1)
    app.resizeTableWidget_res_TZ(tableWidget_res_TZ1)


    tableWidget_res_TZ2 = app.tableWidget_3
    app.setRowSpanOf_res_TZ_table(tableWidget_res_TZ2)
    app.adjustRowSize_res_TZ(tableWidget_res_TZ2)
    app.resizeTableWidget_res_TZ(tableWidget_res_TZ2)

    app.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    app.tableWidget_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    app.tableWidget_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    app.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    app.tableWidget_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    app.tableWidget_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    app.tableWidget_2.setHorizontalHeaderLabels(str("AVG;REF;GTR8;LAO").split(";"))


    # tableWidget_res_header = app.res_col_tableWidget
    # app.set_res_col_label(tableWidget_res_header)
    # app.resizeTable_res_header(tableWidget_res_header)

    # tableWidget_res.setFixedWidth(1250)
    # tableWidget_res.setFixedHeight(1500)
    # app.res_col_tableWidget.setGeometry(20,30,tableWidget_res_TZ1.width()+tableWidget_res.width()+tableWidget_res_TZ2.width(),70)
    app.tableWidget.setGeometry(20, 40, tableWidget_res_TZ1.width(), tableWidget_res_TZ1.height()+50)
    app.tableWidget_2.setGeometry(20 + tableWidget_res_TZ1.width(), 40, tableWidget_res.width(),
                                  tableWidget_res.height()+2)
    app.tableWidget_3.setGeometry(20 + tableWidget_res_TZ1.width() + tableWidget_res.width(), 40,
                                  tableWidget_res_TZ2.width(), tableWidget_res_TZ2.height()+2)

    app.groupBox_9.setGeometry(10, 110, tableWidget_res.width() +270,tableWidget_res.height()+180 )
    app.flow_value.setGeometry(10, 10, tableWidget_res.width() + 300, tableWidget_res.height()+260 )
    print('groupBox_9 height', app.groupBox_9.height())
    print('flow height', app.flow_value.height())

    app.scrollArea.setGeometry(9,9,1600,5000)

    app.calculation_groupBox.setGeometry(9, 583 ,tableWidget_res.width() + 340, tableWidget_res.height()+5000 )
    print(app.calculation_groupBox.height())
    print(app.scrollArea.height())
def test7(app):
    hovlist = ["AAL01", "D0006"]
    msnlist = ["MSN24", "MSN64"]
    acvlist = ["A350-900", "A350-900 Step7", "A350-1000", "A350-1000 Step7", ]
    aclist = ['A350']
    systemlist = ['ATA21-21VCS']
    testlist = ['In Test']
    comblist =['Combination']
    looplist = ['-3(2)']
    testdate = '12/9/2020'
    importdate= '12/9/2020'
    exportdate = '12/9/2020'
    colorlimlts = [(-0.4,-0.2),(-0.2,-0.1),(-0.1,0.1),(0.1,0.2),(0.2,0.4)]
    valueCount = [0,6,86,11,0,33]
    percentageCount = ['0.0%','5.8%','83.5%','10.7%','0.0%','']
    AmbP='0'
    AmbT = '0'
    Mx1=['0','0']
    Mx2 = ['0', '0']
    Mx3 = ['0', '0']
    Mx4 = ['0', '0']
    Mx5 = ['0', '0']
    Mx6 = ['0', '0']
    Mx7 = ['0', '0']
    Mx8 = ['0', '0']
    MxAG = ['0', '0']
    Cb1 = ['0', '0']
    Cb2 = ['0', '0']
    Cb3 = ['0', '0']
    Cb4 = ['0', '0']
    Cb5 = ['0', '0']
    Cb6 = ['0', '0']
    Cb7 = ['0', '0']
    Cb8 = ['0', '0']
    CbAG = ['0']
    PP_TZ1 = [[2101,18.7],[2143,12.5],[2135,13.4],[2136,31.5]]
    PP_TZ2 = [[2101, 18.7], [2143, 12.5], [2135, 13.4], [2136, 31.5],[0,0],[2463,24.5],[2456,31.2],[2210,36.5]]
    # PP_TZ1=[]
    # PP_TZ2=[]
    PP_TZ3=[]
    PP_TZ4 = []
    PP_TZ5 = []
    PP_TZ6 = []
    PP_TZ7 = []
    PP_TZ8 = []
    PP_FCRC = [[3120,21.5],[3251,32.65]]
    PP_CCRC=[]
    PP_AVS=[]
    PP_CVS=[]
    PP_CAX=[]
    PP_CC=[]

    data_for_piechart = [2,6,84,11,5]

    app.reset_HOV()
    app.reset_MSN()
    app.reset_ACV()
    app.populate_HOV(hovlist=hovlist)
    app.populate_ACV(acvlist=acvlist)
    app.populate_MSN(msnlist=msnlist)
    app.populate_AC(aclist=aclist)
    app.populate_SYSTEM(systemlist=systemlist)
    app.populate_TEST(testlist=testlist)
    app.populate_COMB(comblist=comblist)
    app.populate_LOOP(looplist=looplist)
    app.populate_TEST_DATE(testdate=testdate)
    app.populate_IMPORT_DATE(importdate=importdate)
    app.populate_EXPORT_DATE(exportdate=exportdate)

    import pandas as pd
    # LH First table
    df1 = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_GitHub/tests/OUT/UI/LH_Table1.xlsx")
    comment_df1 = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_GitHub/tests/OUT/UI/LH_Table1.xlsx")
    df1 = df1.fillna("")
    def getPercentageValues(val):
        if type(val) == str:
            return val
        else:
            return (f"{val:.1%}")
    df1.iloc[:,0] = df1.iloc[:,0].apply(getPercentageValues)
    df1.iloc[:, 3] = df1.iloc[:, 3].apply(getPercentageValues)
    tableWidget1 = app.flowValueLAOLH_tableWidget
    app.resetTable_LH_first(tableWidget1)
    app.adjustColWidthOf_LH_firstTable(tableWidget1)
    app.adjustRowHeightOf_LH_firstTable(tableWidget1)
    app.populateTable_LH_first(tableWidget=tableWidget1, df=df1,commentdf=comment_df1)
    app.resizeTableWidget_LH_first(tableWidget=tableWidget1)
    app.backgroundColorForLH(tableWidget=tableWidget1,colorlimits=colorlimlts)
    app.tableHeadBold(tableWidget=tableWidget1)
    app.setSpanLH(tableWidget=tableWidget1)
    app.setCellColor(tableWidget=tableWidget1)
    app.alignHeadingLH(tableWidget=tableWidget1)


    # LH Second table
    df2 = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_GitHub/tests/OUT/UI/LH_Table2.xlsx")
    df2 = df2.fillna("")
    df2.iloc[:, 0] = df2.iloc[:, 0].apply(getPercentageValues)
    df2.iloc[:, 3] = df2.iloc[:, 3].apply(getPercentageValues)
    tableWidget2 = app.flowValueCAOLH_tableWidget
    app.resetTable(tableWidget2)
    app.adjustColWidth(tableWidget2)
    app.adjustRowHeight(tableWidget2)
    app.populateTable(tableWidget=tableWidget2, df=df2,commentdf=df2)
    app.resizeTableWidget(tableWidget=tableWidget2)
    app.backgroundColorForLH(tableWidget=tableWidget2,colorlimits=colorlimlts)
    app.tableHeadBold(tableWidget=tableWidget2)
    app.setSpanLH(tableWidget=tableWidget2)
    app.setCellColor(tableWidget=tableWidget2)
    app.alignHeadingLH(tableWidget=tableWidget2)

    #      TZ LH flow table
    tableWidgetTZ1 = app.TZ_LH_tableWidget
    app.setRowSpanOfTZ_table(tableWidgetTZ1)
    app.adjustRowHeightOf_LH_firstTable(tableWidgetTZ1)
    app.resizeTableWidget_LH_TZ_first(tableWidgetTZ1)
    app.tableHeadBold(tableWidget=tableWidgetTZ1)


    #     RH table 2
    df4 = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_GitHub/tests/OUT/UI/RH_Table2.xlsx")
    df4 = df4.fillna("")
    df4.iloc[:, 1] = df4.iloc[:, 1].apply(getPercentageValues)
    df4.iloc[:, 4] = df4.iloc[:, 4].apply(getPercentageValues)
    tableWidget4 = app.flowValueLAORH_tableWidget
    app.resetTable_RH_second(tableWidget4)
    app.adjustColWidthOf_RH_secondTable(tableWidget4)
    app.adjustRowWidthOf_RH_secondTable(tableWidget4)
    app.populateTable_RH_second(tableWidget=tableWidget4, df=df4 , commentdf=df4)
    app.resizeTableWidget_RH_second(tableWidget=tableWidget4)
    app.backgroundColorForRH(tableWidget=tableWidget4,colorlimits=colorlimlts)
    app.tableHeadBold(tableWidget=tableWidget4)
    app.setSpanRH(tableWidget=tableWidget4)
    app.setCellColor(tableWidget=tableWidget4)
    app.alignHeadingRH(tableWidget=tableWidget4)

    # rH first table
    df3 = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_GitHub/tests/OUT/UI/RH_Table1.xlsx")
    df3 = df3.fillna("")
    df3.iloc[:, 1] = df3.iloc[:, 1].apply(getPercentageValues)
    df3.iloc[:, 4] = df3.iloc[:, 4].apply(getPercentageValues)
    tableWidget3 = app.flowValueCAORH_tableWidget
    app.resetTable_RH_first(tableWidget3)
    app.adjustColWidthOf_RH_firstTable(tableWidget3)
    app.adjustRowHeightOf_RH_firstTable(tableWidget3)
    app.populateTable_RH_first(tableWidget=tableWidget3, df=df3, commentdf=df3)
    app.resizeTableWidget_RH_first(tableWidget=tableWidget3)
    app.backgroundColorForRH(tableWidget=tableWidget3,colorlimits=colorlimlts)
    app.tableHeadBold(tableWidget=tableWidget3)
    app.setSpanRH(tableWidget=tableWidget3)
    app.setCellColor(tableWidget=tableWidget3)
    app.alignHeadingRH(tableWidget=tableWidget3)

    #      TZ table RH Flow
    tableWidgetTZ2 = app.TZ_RH_tableWidget
    app.setRowSpanOfTZ_table(tableWidgetTZ2)
    app.adjustRowHeightOf_LH_firstTable(tableWidgetTZ2)
    app.resizeTableWidget_LH_TZ_first(tableWidgetTZ2)
    app.tableHeadBold(tableWidget=tableWidgetTZ2)


    app.setGeometryOFflowTZ1(tableWidget=tableWidgetTZ1)
    app.setGeometryOFflowLH1(tableWidget=tableWidget1,tableWidgetTZ1=tableWidgetTZ1)
    app.setGeometryOFflowLH2(tableWidget=tableWidget2,tableWidgetTZ1=tableWidgetTZ1,tableWidget1=tableWidget1)


    app.setGeometryOFflowTZ2(tableWidget=tableWidgetTZ2)
    app.setGeometryOFflowRH2(tableWidget=tableWidget4)
    app.setGeometryOFflowRH1(tableWidget=tableWidget3,tableWidget4=tableWidget4)


    app.flowValues_groupBox.setGeometry(10, 260, tableWidget4.width() * 5 + 180, tableWidget4.height() + 20)
    app.flow_value.setGeometry(10, 10, tableWidget4.width() * 5 + 250, tableWidget4.height() + 3010)

#     res table


    df_res = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_GitHub/tests/OUT/UI/restrictor.xlsx")
    df_res = df_res.fillna("")
    df_res.iloc[:, 12] = df_res.iloc[:, 12].apply(getPercentageValues)
    df_res.iloc[:, 13] = df_res.iloc[:, 13].apply(getPercentageValues)
    df_res.iloc[:, 14] = df_res.iloc[:, 14].apply(getPercentageValues)
    df_res.iloc[:, 15] = df_res.iloc[:, 15].apply(getPercentageValues)
    df_res.iloc[:, 20] = df_res.iloc[:, 20].apply(getPercentageValues)
    df_res.iloc[:, 21] = df_res.iloc[:, 21].apply(getPercentageValues)
    df_res.iloc[:, 22] = df_res.iloc[:, 22].apply(getPercentageValues)
    df_res.iloc[:, 23] = df_res.iloc[:, 23].apply(getPercentageValues)
    tableWidget_res = app.restrictor_tableWidget
    app.resetTable_restrictor(tableWidget_res)
    app.adjustRowWidthOf_restrictor_table(tableWidget_res)
    app.adjustColWidthOf_restrictor_table(tableWidget_res)
    app.populateTable_restrictor_table(tableWidget=tableWidget_res, df=df_res )
    app.resizeTableWidget_restrictor(tableWidget=tableWidget_res)
    # tableWidget_res.setFont(QtGui.QFont('Arial', 10))
    app.backgroundColorForRes(tableWidget_res)
    app.resSpan(tableWidget=tableWidget_res)
    app.tableHeadBoldRes(tableWidget=tableWidget_res)
    app.alignHeadingRes(tableWidget=tableWidget_res)
    # delegate = app.MyStyledItem()
    # tableWidget_res.setItemDelegate(delegate)

    #  restrictor TZ tables

    tableWidget_res_TZ1 = app.restrictor_TZ_LH_tableWidget
    app.setRowSpanOf_res_TZ_table(tableWidget_res_TZ1)
    app.adjustRowSize_res_TZ(tableWidget_res_TZ1)
    app.resizeTableWidget_res_TZ(tableWidget_res_TZ1)
    app.tableHeadBoldResTZ(tableWidget=tableWidget_res_TZ1)

    tableWidget_res_TZ2 = app.restrictor_RH_TZ_tableWidget
    app.setRowSpanOf_res_TZ_table(tableWidget_res_TZ2)
    app.adjustRowSize_res_TZ(tableWidget_res_TZ2)
    app.resizeTableWidget_res_TZ(tableWidget_res_TZ2)
    app.tableHeadBoldResTZ(tableWidget_res_TZ2)

    app.restrictor_TZ_LH_tableWidget.setGeometry(60, 15, tableWidget_res_TZ1.width(), tableWidget_res_TZ1.height() + 50)
    app.restrictor_tableWidget.setGeometry(60 + tableWidget_res_TZ1.width(), 15, tableWidget_res.width(),
                                           tableWidget_res.height() + 2)
    app.restrictor_RH_TZ_tableWidget.setGeometry(60 + tableWidget_res_TZ1.width() + tableWidget_res.width(), 15,
                                                 tableWidget_res_TZ2.width(), tableWidget_res_TZ2.height() + 2)

    app.restrictor_groupBox.setGeometry(20, 140, tableWidget_res.width() + 245, tableWidget_res.height() + 2000)
    app.flow_value.setGeometry(10, 10, tableWidget_res.width() + 390, tableWidget_res.height() + 5000)

    app.scrollArea.setGeometry(9, 9, 1600, 10000)

    app.calculation_groupBox.setGeometry(9, 583, tableWidget_res.width() + 340, tableWidget_res.height() + 3000)

    #      load image
    app.loadImage()
    app.loadImage_ADAMANT_Logo()
    app.aircraftImage_label.setGeometry(5+ tableWidgetTZ1.width() + tableWidget1.width()+tableWidget2.width() ,14,600,tableWidget1.height())


    # TZ Table
    tableWidget_TZ= app.TZ_tableWidget
    app.resetTable_TZ(tableWidget=tableWidget_TZ)
    df_TZ = pd.read_excel('X:/Aditi/Work_Done/ADAMANT_code/TZ_table.xlsx')
    df_TZ = df_TZ.fillna("")
    df_TZ.iloc[4, :] = df_TZ.iloc[4, :].apply(getPercentageValues)
    df_TZ.iloc[5, :] = df_TZ.iloc[5, :].apply(getPercentageValues)
    app.adjustRowWidthOf_TZ_table(tableWidget_TZ)
    app.adjustColWidthOf_TZ_table(tableWidget_TZ)
    app.populateTable_TZ_table(tableWidget=tableWidget_TZ, df=df_TZ,commentdf=df_TZ)
    app.resizeTableWidget_TZ(tableWidget=tableWidget_TZ)
    app.set_TZ_col_label(tableWidget_TZ)
    app.tableHeadBoldTZ(tableWidget_TZ)
    app.backgroundColorForTZ(tableWidget=tableWidget_TZ,colorlimits=colorlimlts)
    app.setEmptyCellBackgroungGray_TZ(tableWidget_TZ)

    # pie chart
    pieChart = app.pieDiagram_groupBox
    app.create_piechart(pieChart,data_count=data_for_piechart)

    # colour range table
    tableWidget_ColorRange = app.colorRange_tableWidget
    app.resetTable_ColourRange(tableWidget_ColorRange)
    app.adjustColWidthOf_ColourRange_table(tableWidget_ColorRange)
    app.resizeTableWidget_ColourRange(tableWidget_ColorRange)
    app.populateTable_ColourRange_table(tableWidget_ColorRange,count=valueCount , percentage=percentageCount)

    # ambient/mixer/pressure
    ambientPT = app.Ambient_P_T_tableWidget
    app.populateTable_AMBIENT_PRESSURE_TEMP_table(tableWidget=ambientPT,AmbP=AmbP,AmbT=AmbT)

    # Mx1
    Mx1_tablewidget = app.MxP1_tableWidget
    app.populateTable_Mx1_table(tableWidget=Mx1_tablewidget,Mx1=Mx1)
    # Mx2
    Mx2_tablewidget = app.MxP2_tableWidget
    app.populateTable_Mx2_table(tableWidget=Mx2_tablewidget, Mx2=Mx2)
    # Mx3
    Mx3_tablewidget = app.MxP3_tableWidget
    app.populateTable_Mx3_table(tableWidget=Mx3_tablewidget, Mx3=Mx3)
    # Mx4
    Mx4_tablewidget = app.MxP4_tableWidget
    app.populateTable_Mx4_table(tableWidget=Mx4_tablewidget, Mx4=Mx4)
    # Mx5
    Mx5_tablewidget = app.MxP5_tableWidget
    app.populateTable_Mx5_table(tableWidget=Mx5_tablewidget, Mx5=Mx5)
    # Mx6
    Mx6_tablewidget = app.MxP6_tableWidget
    app.populateTable_Mx6_table(tableWidget=Mx6_tablewidget, Mx6=Mx6)
    # Mx7
    Mx7_tablewidget = app.MxP7_tableWidget
    app.populateTable_Mx7_table(tableWidget=Mx7_tablewidget, Mx7=Mx7)
    # Mx8
    Mx8_tablewidget = app.MxP8_tableWidget
    app.populateTable_Mx8_table(tableWidget=Mx8_tablewidget, Mx8=Mx8)
    # MxAG
    MxAG_tablewidget = app.MxPAG_tableWidget
    app.populateTable_MxAG_table(tableWidget=MxAG_tablewidget, MxAG=MxAG)
    # Cb1
    Cb1_tablewidget = app.CbP1_tableWidget
    app.populateTable_Cb1_table(tableWidget=Cb1_tablewidget, Cb1=Cb1)
    # Cb2
    Cb2_tablewidget = app.CbP2_tableWidget
    app.populateTable_Cb2_table(tableWidget=Cb2_tablewidget, Cb2=Cb2)
    # Cb3
    Cb3_tablewidget = app.CbP3_tableWidget
    app.populateTable_Cb3_table(tableWidget=Cb3_tablewidget, Cb3=Cb3)
    # Cb4
    Cb4_tablewidget = app.CbP4_tableWidget
    app.populateTable_Cb4_table(tableWidget=Cb4_tablewidget, Cb4=Cb4)
    # Cb5
    Cb5_tablewidget = app.CbP5_tableWidget
    app.populateTable_Cb5_table(tableWidget=Cb5_tablewidget, Cb5=Cb5)
    # Cb6
    Cb6_tablewidget = app.CbP6_tableWidget
    app.populateTable_Cb6_table(tableWidget=Cb6_tablewidget, Cb6=Cb6)
    # Cb7
    Cb7_tablewidget = app.CbP7_tableWidget
    app.populateTable_Cb7_table(tableWidget=Cb7_tablewidget, Cb7=Cb7)
    # Cb8
    Cb8_tablewidget = app.CbP8_tableWidget
    app.populateTable_Cb8_table(tableWidget=Cb8_tablewidget, Cb8=Cb8)
    # CbAG
    CbAG_tablewidget = app.CbPAG_tableWidget
    app.populateTable_CbAG_table(tableWidget=CbAG_tablewidget, CbAG=CbAG)

    # # PPTZ1
    # PP_TZ1_tableWidget = app.PP_TZ1_tableWidget
    # app.populateTable_PP_TZ1_table(tableWidget=PP_TZ1_tableWidget,TZ1_df=pd.DataFrame(PP_TZ1))
    # # PPTZ2
    # PP_TZ2_tableWidget = app.PP_TZ2_tableWidget
    # app.populateTable_PP_TZ2_table(tableWidget=PP_TZ2_tableWidget,TZ2_df=pd.DataFrame(PP_TZ2))
    # # app.fun(tab=app.PP_TZ2_tableWidget,df=pd.DataFrame(PP_TZ2))
    # # PPTZ3
    # PP_TZ3_tableWidget = app.PP_TZ3_tableWidget
    # app.populateTable_PP_TZ3_table(tableWidget=PP_TZ3_tableWidget, TZ3_df=pd.DataFrame(PP_TZ3))
    # # PPTZ4
    # PP_TZ4_tableWidget = app.PP_TZ4_tableWidget
    # app.populateTable_PP_TZ4_table(tableWidget=PP_TZ4_tableWidget, TZ4_df=pd.DataFrame(PP_TZ4))
    # # PPTZ5
    # PP_TZ5_tableWidget = app.PP_TZ5_tableWidget
    # app.populateTable_PP_TZ5_table(tableWidget=PP_TZ5_tableWidget, TZ5_df=pd.DataFrame(PP_TZ5))
    # # PPTZ6
    # PP_TZ6_tableWidget = app.PP_TZ6_tableWidget
    # app.populateTable_PP_TZ6_table(tableWidget=PP_TZ6_tableWidget, TZ6_df=pd.DataFrame(PP_TZ6))
    # # PPTZ7
    # PP_TZ7_tableWidget = app.PP_TZ7_tableWidget
    # app.populateTable_PP_TZ7_table(tableWidget=PP_TZ7_tableWidget, TZ7_df=pd.DataFrame(PP_TZ7))
    # # PPTZ8
    # PP_TZ8_tableWidget = app.PP_TZ8_tableWidget
    # app.populateTable_PP_TZ8_table(tableWidget=PP_TZ8_tableWidget, TZ8_df=pd.DataFrame(PP_TZ8))
    app.populateTable_PP_TZ(app.PP_TZ1_tableWidget,pd.DataFrame(PP_TZ1),app.PP_TZ2_tableWidget,pd.DataFrame(PP_TZ2),app.PP_TZ3_tableWidget,pd.DataFrame(PP_TZ3),app.PP_TZ4_tableWidget,pd.DataFrame(PP_TZ4),
                            app.PP_TZ5_tableWidget,pd.DataFrame(PP_TZ5),app.PP_TZ6_tableWidget,pd.DataFrame(PP_TZ6),app.PP_TZ7_tableWidget,pd.DataFrame(PP_TZ7),
                            app.PP_TZ8_tableWidget,pd.DataFrame(PP_TZ8),app.PP_FCRC_tableWidget,pd.DataFrame(PP_FCRC),app.PP_CCRC_tableWidget,pd.DataFrame(PP_CCRC),
                            app.PP_AVS_tableWidget,pd.DataFrame(PP_AVS),app.PP_CVS_tableWidget,pd.DataFrame(PP_CVS),
                            app.PP_CAX_tableWidget,pd.DataFrame(PP_CAX),app.PP_CC_tableWidget,pd.DataFrame(PP_CC))
    # FCRC
    # app.populateTable_FCRC_table(app.PP_FCRC_tableWidget,pd.DataFrame(PP_FCRC))

    print('flow height', app.flow_value.height())
    print('scroll area height', app.scrollArea.height())
    print('calculation group box height', app.calculation_groupBox.height())
    print('restrictor height', app.restrictor_groupBox.height())
    print('first table height', app.restrictor_TZ_LH_tableWidget.height())
    print('second table height', app.restrictor_tableWidget.height())
    print('third table height', app.restrictor_RH_TZ_tableWidget.height())
    # app.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: app.scrollArea.verticalScrollBar().setValue(app.scrollArea.verticalScrollBar().maximum()))
    print('scroll area height', app.scrollArea.height())
    print(MainWindow.height)

#     TR analysis plot
    app.plotTRanalysis()

def test8(app):
    hovlist = ["AAL01", "D0006"]
    msnlist = ["MSN24", "MSN64"]
    acvlist = ["A350-900", "A350-900 Step7", "A350-1000", "A350-1000 Step7", ]
    aclist = ['A350']
    systemlist = ['ATA21-21VCS']
    testlist = ['In Test']
    comblist =['Combination']
    looplist = ['-3(2)']
    testdate = '12/9/2020'
    importdate= '12/9/2020'
    exportdate = '12/9/2020'
    colorlimlts = [(-0.4,-0.2),(-0.2,-0.1),(-0.1,0.1),(0.1,0.2),(0.2,0.4)]
    valueCount = [0,6,86,11,0,33]
    percentageCount = ['0.0%','5.8%','83.5%','10.7%','0.0%','']
    AmbP='0'
    AmbT = '0'
    Mx1=['0','0']
    Mx2 = ['0', '0']
    Mx3 = ['0', '0']
    Mx4 = ['0', '0']
    Mx5 = ['0', '0']
    Mx6 = ['0', '0']
    Mx7 = ['0', '0']
    Mx8 = ['0', '0']
    MxAG = ['0', '0']
    Cb1 = ['0', '0']
    Cb2 = ['0', '0']
    Cb3 = ['0', '0']
    Cb4 = ['0', '0']
    Cb5 = ['0', '0']
    Cb6 = ['0', '0']
    Cb7 = ['0', '0']
    Cb8 = ['0', '0']
    CbAG = ['0']
    PP_TZ1 = [[2101,18.7],[2143,12.5],[2135,13.4],[2136,31.5]]
    PP_TZ2 = [[2101, 18.7], [2143, 12.5], [2135, 13.4], [2136, 31.5],[0,0],[2463,24.5],[2456,31.2],[2210,36.5]]
    # PP_TZ1=[]
    # PP_TZ2=[]
    PP_TZ3=[]
    PP_TZ4 = []
    PP_TZ5 = []
    PP_TZ6 = []
    PP_TZ7 = []
    PP_TZ8 = []
    PP_FCRC = [[3120,21.5],[3251,32.65]]
    PP_CCRC=[]
    PP_AVS=[]
    PP_CVS=[]
    PP_CAX=[]
    PP_CC=[]

    data_for_piechart = [2,6,84,11,5]

    app.reset_HOV()
    app.reset_MSN()
    app.reset_ACV()
    app.populate_HOV(hovlist=hovlist)
    app.populate_ACV(acvlist=acvlist)
    app.populate_MSN(msnlist=msnlist)
    app.populate_AC(aclist=aclist)
    app.populate_SYSTEM(systemlist=systemlist)
    app.populate_TEST(testlist=testlist)
    app.populate_COMB(comblist=comblist)
    app.populate_LOOP(looplist=looplist)
    app.populate_TEST_DATE(testdate=testdate)
    app.populate_IMPORT_DATE(importdate=importdate)
    app.populate_EXPORT_DATE(exportdate=exportdate)


    # LH LAO table

    df1 = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_code/tablewidgetAdjustment_Data/LH_LAO.xlsx")

    df1 = df1.fillna("")

    def getPercentageValues(val):
        if type(val) == str:
            return val
        else:
            return (f"{val:.1%}")
    def getValues(val):
        if type(val) == str:
            return val
        else:
            return (f"{val:.2f}")

    df1.iloc[:, 0] = df1.iloc[:, 0].apply(getPercentageValues)
    df1.iloc[:, 3] = df1.iloc[:, 3].apply(getPercentageValues)
    df1.iloc[:, 2] = df1.iloc[:, 2].apply(getValues)


    df2 = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_code/tablewidgetAdjustment_Data/LH_CAO.xlsx")
    df2 = df2.fillna("")
    df2.iloc[:, 0] = df2.iloc[:, 0].apply(getPercentageValues)
    df2.iloc[:, 3] = df2.iloc[:, 3].apply(getPercentageValues)
    df2.iloc[:, 2] = df2.iloc[:, 2].apply(getValues)
    app.LH_CAO_Table(df=df2)

    extra_row_LH_LAO = set(df1.iloc[:, 4]) - set(df2.iloc[:, 4])
    print(extra_row_LH_LAO)

    extra_row_LH_CAO = set(df2.iloc[:, 4]) - set(df1.iloc[:, 4])
    print(extra_row_LH_CAO)

    LH_LAO = list(df1.iloc[:, 4])

    for i in extra_row_LH_CAO:
        if i != 'CAS':
            LH_LAO.append(i)
    xtra_LAO = {'Unnamed: 4': pd.Series(LH_LAO)}

    df1 = df1.append(pd.DataFrame(xtra_LAO), sort=True)
    cor = df1.loc[df1['Unnamed: 4'] == 'CORNER']
    df1 = df1[df1.iloc[:, 4] != 'CORNER']
    df1 = df1.append(cor)
    df1 = df1.drop_duplicates(subset='Unnamed: 4')
    app.LH_LAO_Table(df=df1)

    df3 = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_code/tablewidgetAdjustment_Data/RH_CAO.xlsx")
    df3 = df3.fillna("")
    df3.iloc[:, 1] = df3.iloc[:, 1].apply(getPercentageValues)
    df3.iloc[:, 4] = df3.iloc[:, 4].apply(getPercentageValues)
    df3.iloc[:, 2] = df3.iloc[:, 2].apply(getValues)

    df3.to_excel('df3.xlsx')
    app.RH_CAO_Table(df=df3)

    df4 = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_code/tablewidgetAdjustment_Data/RH_LAO.xlsx")

    df4 = df4.fillna("")
    df4.iloc[:, 1] = df4.iloc[:, 1].apply(getPercentageValues)
    df4.iloc[:, 4] = df4.iloc[:, 4].apply(getPercentageValues)
    df4.iloc[:, 2] = df4.iloc[:, 2].apply(getValues)

    extra_row_RH_LAO = set(df4.iloc[:, 0]) - set(df3.iloc[:, 0])
    print("df4",extra_row_RH_LAO)

    extra_row_RH_CAO = set(df3.iloc[:, 0]) - set(df4.iloc[:, 0])
    print(extra_row_RH_CAO)

    RH_LAO = list(df4.iloc[:, 0])
    #
    for i in extra_row_RH_CAO:
         if i != 'CAS' and i!= 'CA0':
            RH_LAO.append(i)

    xtra_LAO_ = {'Unnamed: 0': pd.Series(RH_LAO)}
    #
    df4 = df4.append(pd.DataFrame(xtra_LAO_), sort=True)
    cor_ = df4.loc[df4['Unnamed: 0'] == 'CORNER']
    df4 = df4[df4.iloc[:, 0] != 'CORNER']
    df4 = df4[df4.iloc[:, 0] != 'CAO']
    df4 = df4.append(cor_)
    df4 = df4.drop_duplicates(subset='Unnamed: 0')
    df4 = df4.sort_values(by=['Unnamed: 0'])
    df4.to_excel('df4.xlsx')
    df4_last_row = df4.iloc[len(df4)-1,:]
    print(df4_last_row)
    df4_shifted = df4.shift(1)
    df4_shifted.iloc[0,:] = df4_last_row
    df4_shifted.to_excel('df4_shifted.xlsx')
    app.RH_LAO_Table(df=df4_shifted)



    #      TZ LH flow table
    tableWidgetTZ1 = app.TZ_LH_tableWidget
    app.setRowSpanOfTZ_table(tableWidgetTZ1)
    app.adjustRowHeightOf_LH_firstTable(tableWidgetTZ1)
    app.resizeTableWidget_LH_TZ_first(tableWidgetTZ1)
    app.tableHeadBold(tableWidget=tableWidgetTZ1)



    #      TZ table RH Flow
    tableWidgetTZ2 = app.TZ_RH_tableWidget
    app.setRowSpanOfTZ_table(tableWidgetTZ2)
    app.adjustRowHeightOf_LH_firstTable(tableWidgetTZ2)
    app.resizeTableWidget_LH_TZ_first(tableWidgetTZ2)
    app.tableHeadBold(tableWidget=tableWidgetTZ2)


    app.setGeometryOFflowTZ1(tableWidget=tableWidgetTZ1)
    app.setGeometryOFflowLH1(tableWidget=app.flowValueLAOLH_tableWidget,tableWidgetTZ1=tableWidgetTZ1)
    app.setGeometryOFflowLH2(tableWidget=app.flowValueCAOLH_tableWidget,tableWidgetTZ1=tableWidgetTZ1,tableWidget1=app.flowValueLAOLH_tableWidget)


    app.setGeometryOFflowTZ2(tableWidget=tableWidgetTZ2)
    app.setGeometryOFflowRH2(tableWidget=app.flowValueLAORH_tableWidget)
    app.setGeometryOFflowRH1(tableWidget=app.flowValueCAORH_tableWidget,tableWidget4=app.flowValueLAORH_tableWidget)


    app.flowValues_groupBox.setGeometry(10, 260, app.flowValueLAORH_tableWidget.width() * 5 + 180, app.flowValueLAOLH_tableWidget.height() + 20)
    app.flow_value.setGeometry(10, 10, app.flowValueLAORH_tableWidget.width() * 5 + 250, app.flowValueLAORH_tableWidget.height() + 3010)

#     res table


    df_res = pd.read_excel("X:/Aditi/Work_Done/ADAMANT_GitHub/tests/OUT/UI/restrictor.xlsx")
    df_res = df_res.fillna("")
    df_res.iloc[:, 12] = df_res.iloc[:, 12].apply(getPercentageValues)
    df_res.iloc[:, 13] = df_res.iloc[:, 13].apply(getPercentageValues)
    df_res.iloc[:, 14] = df_res.iloc[:, 14].apply(getPercentageValues)
    df_res.iloc[:, 15] = df_res.iloc[:, 15].apply(getPercentageValues)
    df_res.iloc[:, 20] = df_res.iloc[:, 20].apply(getPercentageValues)
    df_res.iloc[:, 21] = df_res.iloc[:, 21].apply(getPercentageValues)
    df_res.iloc[:, 22] = df_res.iloc[:, 22].apply(getPercentageValues)
    df_res.iloc[:, 23] = df_res.iloc[:, 23].apply(getPercentageValues)
    tableWidget_res = app.restrictor_tableWidget
    app.resetTable_restrictor(tableWidget_res)
    app.adjustRowWidthOf_restrictor_table(tableWidget_res)
    app.adjustColWidthOf_restrictor_table(tableWidget_res)
    app.populateTable_restrictor_table(tableWidget=tableWidget_res, df=df_res )
    app.resizeTableWidget_restrictor(tableWidget=tableWidget_res)
    # tableWidget_res.setFont(QtGui.QFont('Arial', 10))
    app.backgroundColorForRes(tableWidget_res)
    app.resSpan(tableWidget=tableWidget_res)
    app.tableHeadBoldRes(tableWidget=tableWidget_res)
    app.alignHeadingRes(tableWidget=tableWidget_res)
    # delegate = app.MyStyledItem()
    # tableWidget_res.setItemDelegate(delegate)

    #  restrictor TZ tables

    tableWidget_res_TZ1 = app.restrictor_TZ_LH_tableWidget
    app.setRowSpanOf_res_TZ_table(tableWidget_res_TZ1)
    app.adjustRowSize_res_TZ(tableWidget_res_TZ1)
    app.resizeTableWidget_res_TZ(tableWidget_res_TZ1)
    app.tableHeadBoldResTZ(tableWidget=tableWidget_res_TZ1)

    tableWidget_res_TZ2 = app.restrictor_RH_TZ_tableWidget
    app.setRowSpanOf_res_TZ_table(tableWidget_res_TZ2)
    app.adjustRowSize_res_TZ(tableWidget_res_TZ2)
    app.resizeTableWidget_res_TZ(tableWidget_res_TZ2)
    app.tableHeadBoldResTZ(tableWidget_res_TZ2)

    app.restrictor_TZ_LH_tableWidget.setGeometry(60, 15, tableWidget_res_TZ1.width(), tableWidget_res_TZ1.height() + 50)
    app.restrictor_tableWidget.setGeometry(60 + tableWidget_res_TZ1.width(), 15, tableWidget_res.width(),
                                           tableWidget_res.height() + 2)
    app.restrictor_RH_TZ_tableWidget.setGeometry(60 + tableWidget_res_TZ1.width() + tableWidget_res.width(), 15,
                                                 tableWidget_res_TZ2.width(), tableWidget_res_TZ2.height() + 2)

    app.restrictor_groupBox.setGeometry(20, 140, tableWidget_res.width() + 245, tableWidget_res.height() + 2000)
    app.flow_value.setGeometry(10, 10, tableWidget_res.width() + 390, tableWidget_res.height() + 5000)

    app.scrollArea.setGeometry(9, 9, 1600, 10000)

    app.calculation_groupBox.setGeometry(9, 583, tableWidget_res.width() + 340, tableWidget_res.height() + 3000)

    #      load image
    app.loadImage()
    app.loadImage_ADAMANT_Logo()
    app.aircraftImage_label.setGeometry(5+ tableWidgetTZ1.width() + app.flowValueLAOLH_tableWidget.width()+app.flowValueCAOLH_tableWidget.width() ,14,600,app.flowValueLAOLH_tableWidget.height())


    # TZ Table
    tableWidget_TZ= app.TZ_tableWidget
    app.resetTable_TZ(tableWidget=tableWidget_TZ)
    df_TZ = pd.read_excel('X:/Aditi/Work_Done/ADAMANT_code/TZ_table.xlsx')
    df_TZ = df_TZ.fillna("")
    df_TZ.iloc[4, :] = df_TZ.iloc[4, :].apply(getPercentageValues)
    df_TZ.iloc[5, :] = df_TZ.iloc[5, :].apply(getPercentageValues)
    app.adjustRowWidthOf_TZ_table(tableWidget_TZ)
    app.adjustColWidthOf_TZ_table(tableWidget_TZ)
    app.populateTable_TZ_table(tableWidget=tableWidget_TZ, df=df_TZ,commentdf=df_TZ)
    app.resizeTableWidget_TZ(tableWidget=tableWidget_TZ)
    app.set_TZ_col_label(tableWidget_TZ)
    app.tableHeadBoldTZ(tableWidget_TZ)
    app.backgroundColorForTZ(tableWidget=tableWidget_TZ,colorlimits=colorlimlts)
    app.setEmptyCellBackgroungGray_TZ(tableWidget_TZ)

    # pie chart
    pieChart = app.pieDiagram_groupBox
    app.create_piechart(pieChart,data_count=data_for_piechart)

    # colour range table
    tableWidget_ColorRange = app.colorRange_tableWidget
    app.resetTable_ColourRange(tableWidget_ColorRange)
    app.adjustColWidthOf_ColourRange_table(tableWidget_ColorRange)
    app.resizeTableWidget_ColourRange(tableWidget_ColorRange)
    app.populateTable_ColourRange_table(tableWidget_ColorRange,count=valueCount , percentage=percentageCount)

    # ambient/mixer/pressure
    ambientPT = app.Ambient_P_T_tableWidget
    app.populateTable_AMBIENT_PRESSURE_TEMP_table(tableWidget=ambientPT,AmbP=AmbP,AmbT=AmbT)

    # Mx1
    Mx1_tablewidget = app.MxP1_tableWidget
    app.populateTable_Mx1_table(tableWidget=Mx1_tablewidget,Mx1=Mx1)
    # Mx2
    Mx2_tablewidget = app.MxP2_tableWidget
    app.populateTable_Mx2_table(tableWidget=Mx2_tablewidget, Mx2=Mx2)
    # Mx3
    Mx3_tablewidget = app.MxP3_tableWidget
    app.populateTable_Mx3_table(tableWidget=Mx3_tablewidget, Mx3=Mx3)
    # Mx4
    Mx4_tablewidget = app.MxP4_tableWidget
    app.populateTable_Mx4_table(tableWidget=Mx4_tablewidget, Mx4=Mx4)
    # Mx5
    Mx5_tablewidget = app.MxP5_tableWidget
    app.populateTable_Mx5_table(tableWidget=Mx5_tablewidget, Mx5=Mx5)
    # Mx6
    Mx6_tablewidget = app.MxP6_tableWidget
    app.populateTable_Mx6_table(tableWidget=Mx6_tablewidget, Mx6=Mx6)
    # Mx7
    Mx7_tablewidget = app.MxP7_tableWidget
    app.populateTable_Mx7_table(tableWidget=Mx7_tablewidget, Mx7=Mx7)
    # Mx8
    Mx8_tablewidget = app.MxP8_tableWidget
    app.populateTable_Mx8_table(tableWidget=Mx8_tablewidget, Mx8=Mx8)
    # MxAG
    MxAG_tablewidget = app.MxPAG_tableWidget
    app.populateTable_MxAG_table(tableWidget=MxAG_tablewidget, MxAG=MxAG)
    # Cb1
    Cb1_tablewidget = app.CbP1_tableWidget
    app.populateTable_Cb1_table(tableWidget=Cb1_tablewidget, Cb1=Cb1)
    # Cb2
    Cb2_tablewidget = app.CbP2_tableWidget
    app.populateTable_Cb2_table(tableWidget=Cb2_tablewidget, Cb2=Cb2)
    # Cb3
    Cb3_tablewidget = app.CbP3_tableWidget
    app.populateTable_Cb3_table(tableWidget=Cb3_tablewidget, Cb3=Cb3)
    # Cb4
    Cb4_tablewidget = app.CbP4_tableWidget
    app.populateTable_Cb4_table(tableWidget=Cb4_tablewidget, Cb4=Cb4)
    # Cb5
    Cb5_tablewidget = app.CbP5_tableWidget
    app.populateTable_Cb5_table(tableWidget=Cb5_tablewidget, Cb5=Cb5)
    # Cb6
    Cb6_tablewidget = app.CbP6_tableWidget
    app.populateTable_Cb6_table(tableWidget=Cb6_tablewidget, Cb6=Cb6)
    # Cb7
    Cb7_tablewidget = app.CbP7_tableWidget
    app.populateTable_Cb7_table(tableWidget=Cb7_tablewidget, Cb7=Cb7)
    # Cb8
    Cb8_tablewidget = app.CbP8_tableWidget
    app.populateTable_Cb8_table(tableWidget=Cb8_tablewidget, Cb8=Cb8)
    # CbAG
    CbAG_tablewidget = app.CbPAG_tableWidget
    app.populateTable_CbAG_table(tableWidget=CbAG_tablewidget, CbAG=CbAG)


    app.populateTable_PP_TZ(app.PP_TZ1_tableWidget,pd.DataFrame(PP_TZ1),app.PP_TZ2_tableWidget,pd.DataFrame(PP_TZ2),app.PP_TZ3_tableWidget,pd.DataFrame(PP_TZ3),app.PP_TZ4_tableWidget,pd.DataFrame(PP_TZ4),
                            app.PP_TZ5_tableWidget,pd.DataFrame(PP_TZ5),app.PP_TZ6_tableWidget,pd.DataFrame(PP_TZ6),app.PP_TZ7_tableWidget,pd.DataFrame(PP_TZ7),
                            app.PP_TZ8_tableWidget,pd.DataFrame(PP_TZ8),app.PP_FCRC_tableWidget,pd.DataFrame(PP_FCRC),app.PP_CCRC_tableWidget,pd.DataFrame(PP_CCRC),
                            app.PP_AVS_tableWidget,pd.DataFrame(PP_AVS),app.PP_CVS_tableWidget,pd.DataFrame(PP_CVS),
                            app.PP_CAX_tableWidget,pd.DataFrame(PP_CAX),app.PP_CC_tableWidget,pd.DataFrame(PP_CC))
    # FCRC
    # app.populateTable_FCRC_table(app.PP_FCRC_tableWidget,pd.DataFrame(PP_FCRC))



#     TR analysis plot
    app.plotTRanalysis()

#     heading 2
#     app.aircraftHoV_label.hide()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    myapp = MainWindow()
    test7(app=myapp)
    print(myapp.size())
    myapp.show()
    sys.exit(app.exec_())
'''

