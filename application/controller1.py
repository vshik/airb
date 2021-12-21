import os
import json
import shutil
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from model.interfaces import IData
from model.Model import Model
from gui.dashboard_View import MainWindow
import logger
import datetime


class Controller(object):
    def __init__(self):
        """
        Initializer
        @param adamant: instantiates the Controller
        @type adamant:
        """

        # app = QApplication(sys.argv)
        self._model = Model()
        self._view = MainWindow(controller=self)
        self._view.resize(1645,7000)
        self._view.show()

        # app.exec_()


    @property
    def model(self):
        return self._model

    def onModeChangedtoSTR(self):
        if self._view.STRradioButton_2.isChecked() == True:
            print("STRradioButton was clicked")
            df=self._model.db1_str.flow_df.df
            Hovnames=set(df.index.tolist())
            self._view.populate_HOV(Hovnames)
            return True
        else:
            return False

    def onModeChangedtoLTR(self):
        if self._view.LTRradioButton_2.isChecked() == True:
            print("LTRradioButton was clicked")
            #df=self._model.db2_ltr.flow_df.df
            #Hovnames=set(df.index.tolist())
            #self._view.populate_HOV(Hovnames)
            return True
        else:
            return False

    def onModeChangedtoGTR4(self):
        if self._view.GTR4radioButton_2.isChecked() == True:
            print("GTR4radioButton was clicked")
            df=self._model.db3_gtr4.flow_df.df
            Hovnames=set(df.index.tolist())
            self._view.populate_HOV(Hovnames)
            return True
        else:
            return False

    def onModeChangedtoGTR8(self):
        if self._view.GTR8radioButton_2.isChecked() == True:
            print("GTR8radioButton was clicked")
            df=self._model.db4_gtr8.flow_df.df
            Hovnames=set(df.index.tolist())
            self._view.populate_HOV(Hovnames)
            return True
        else:
            return False


#if __name__ == "__main__":
#    controller = Controller()



    '''
    def set_configFile(self, configFile):
        """
        Sets the Adamant configFile (on model) and adjust mainWindow title accordingly

        @param configFile: path to the configuration file to use
        @type configFile: str
        """
        try:
            self._model.set_configFile(configFile)
            self._view.setWindowTitle(configFile)  # the config file appears in window title
        except:
            pass
                        

    def new(self):
        """
        Have the Adamant default displayed and model re-generated from scratch

        """
        # asks confirmation on whether user really wants to lose current settings
        answerIsYes = self._view.popUpYesNo(title='New configuration',
                                            message='If you continue all the configuration will be lost.\n'
                                                    'Do you wish to continue ?')

        if answerIsYes:
            if self._model:
                del self._model  # this step is necesssay to instantiate a new Adamant Model
                self._model = Model()
            self._view.reset()
            self._view.setWindowTitle(self._model.configFile)
            self.refresh()
            

    def populate_HoVCombo(self):
        # self._view.aircraftVersion_comboBox.clear()
        # print("aircraftVersion_comboBox was clicked")
        if self.isSTRradioButton_2_Checked():
            STR1Flow = self._model.db1_str.flow_df
            STR1Flow.importAllFilesinFolders(r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\1-STR")
            hovlist = set(STR1Flow.df.index.tolist())
            # for hov in set(STR1Flow.df.index.tolist()):
            #    self._view.populate_HOV(hovlist) # aircraftHOV_comboBox.addItem(hov)
            self._view.populate_HOV(hovlist)
        elif self.isLTRradioButton_2_Checked():
            LTR2Flow = self._model.db2_ltr.flow_df
            LTR2Flow.importAllFiles(r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\2-LTR")
            for hov in set(LTR2Flow.df.index.tolist()):
                self._view.aircraftHOV_comboBox.addItem(hov)
        elif self.isGTR4radioButton_2_Checked():
            for hov in sorted(Model.db3_gtr4.flow_df.headdf()[0]):
                self.aircraftHOV_comboBox.addItem(hov)
        elif self.isGTR8radioButton_2_Checked():
            for hov in sorted(Model.db4_gtr8.flow_df.headdf()[0]):
                self.aircraftHOV_comboBox.addItem(hov)    


    def import_new_file(self):
        excel_file = QFileDialog.getOpenFileName(self, "Select Excel file to import", "", "Excel (*.xls *.xlsx)")
        if excel_file[0]:
            shutil.copy2(excel_file[0], destPath)
            # self._model.process.importing.interfaces.LTR2.importmultiplefiles(self, destPath)
        else:
            self.invalid_importfile_alert_message()


    def invalid_importfile_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Invalid file")
        messageBox.setText("Selected filename or path is not valid. Please select a valid file.")
        messageBox.exec()


    def text_changed(self, s):  # s is a str
        self._model.actionsQ.append((True, s))
        self.save()


    def save(self):
        with open('actionsQ.db', 'w') as f:
            actionsQ = json.dump(self._model.actionsQ, f)


    def engUpdated_DB(self):
        pass


    def openXml(self):
        """
        Actions when the Open button has been pressed
        Show Open dialog and update Monica with data of the xml file
        """
        pass


    def loadFromXml(self, xmlConfigfile):
        """
        Loads configuration from xml file

        @param xmlConfigfile: path to the xml Monica configuration file to load
        @type xmlConfigfile: str
        """
        pass


    def saveToXml(self):
        """
        Save configuration to xml file

        """
        pass


    def pushButtonXYZ_clicked(self):
        # open XYZ and get the information
        pass


    def updated_aircraft_combo(self):
        """
        Update the aircraft comboBox

        """
        pass


    def refresh(self):
        """
        Have the Adamant interface refreshed in accordance with model contents
        """
        pass
    '''
