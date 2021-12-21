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
import pandas as pd


class Controller(object):
    def __init__(self):
        """
        Initializer
        @param adamant: instantiates the Controller
        @type adamant:
        """
        # app = QApplication(sys.argv)
        self._model = Model()
        self._setupDataframes()
        self._view = MainWindow(controller=self)
        self._view.resize(1645,7000)
        self._view.show()
        # app.exec_()

    @property
    def model(self):
        return self._model


    def _setupDataframes(self):
        self.df_db1_flow = self._model.db1_str.flow_df.df
        self.df_db2_flow = self._model.db2_ltr.flow_df.df
        self.df_db3_flow = self._model.db3_gtr4.flow_df.df
        self.df_db4_flow = self._model.db4_gtr8.flow_df.df
        #self.df_db5_flow = self._model.db5_ftr.flow_df.df
        #self.df_db6_flow = self._model.db6_csird.flow_df.df
        self.df_db1_mixrecamb = self._model.db1_str.mix_rec_amb_df.df
        #self.df_db2_mixrecamb = self._model.db2_ltr.mix_rec_amb_df.df
        self.df_db3_mixrecamb = self._model.db3_gtr4.mixrecamb_df.df
        self.df_db4_mixrecamb = self._model.db4_gtr8.mixrecamb_df.df
        #self.df_db5_mixrecamb = self._model.db5_ftr.mixrecamb_df.df
        #self.df_db6_mixrecamb = self._model.db6_csird.mixrecamb_df.df


    def on_aircraftHOV_comboBox_changed(self, value):
        if self._view.STRradioButton.isChecked() == True:
            print("aircraft comboBox changed to: ", value)
            # Populate Flow Tables (LAO-LH, CAO-LH, CAO-RH, LAO-RH) according to selectedHoV
            #selectedHoV = self.on_aircraftHOV_comboBox_changed(self)
            #df_flow = self._model.db1_str.flow_df.df
            self.populateFlowTables(value, self.df_db1_flow.copy())
            self.populateAmbMixCabTables(value, 'str', self.df_db1_mixrecamb.copy())
        elif self._view.LTRradioButton.isChecked() == True:
            print("aircraft comboBox changed to: ", value)
            # Populate Flow Tables (LAO-LH, CAO-LH, CAO-RH, LAO-RH) according to selectedHoV
            #selectedHoV = self.on_aircraftHOV_comboBox_changed(self)
            #df_flow = self._model.db1_str.flow_df.df
            self.populateFlowTables(value, self.df_db2_flow.copy())
            #self.populateAmbMixCabTables(value, 'ltr', self.df_db2_mixrecamb.copy())
        elif self._view.GTR4radioButton.isChecked() == True:
            print("aircraft comboBox changed to: ", value)
            # Populate Flow Tables (LAO-LH, CAO-LH, CAO-RH, LAO-RH) according to selectedHoV
            #selectedHoV = self.on_aircraftHOV_comboBox_changed(self)
            #df_flow = self._model.db1_str.flow_df.df
            self.populateFlowTables(value, self.df_db3_flow.copy())
            self.populateAmbMixCabTables(value, 'gtr4', self.df_db3_mixrecamb.copy())
        elif self._view.GTR8radioButton.isChecked() == True:
            print("aircraft comboBox changed to: ", value)
            # Populate Flow Tables (LAO-LH, CAO-LH, CAO-RH, LAO-RH) according to selectedHoV
            #selectedHoV = self.on_aircraftHOV_comboBox_changed(self)
            #df_flow = self._model.db1_str.flow_df.df
            self.populateFlowTables(value, self.df_db4_flow.copy())
            self.populateAmbMixCabTables(value, 'gtr8', self.df_db4_mixrecamb.copy())
        return value


    def populateFlowTables(self, selectedHoV, df):
        if (selectedHoV != ''):
            df_flow_selected = df[df.index.get_level_values('HoV') == selectedHoV].head(1)
            print("Selected HoV is: ", selectedHoV)
            lao_lh_data_dict = df_flow_selected.loc[(selectedHoV), ('LAO', 'LH')].to_dict('list')
            cao_lh_data_dict = df_flow_selected.loc[(selectedHoV), ('CAO', 'LH')].to_dict('list')
            cao_rh_data_dict = df_flow_selected.loc[(selectedHoV), ('CAO', 'RH')].to_dict('list')
            lao_rh_data_dict = df_flow_selected.loc[(selectedHoV), ('LAO', 'RH')].to_dict('list')

            lao_lh_data = pd.DataFrame([[k, *v] for k, v in lao_lh_data_dict.items()], columns=['Section', 'Value'])
            cao_lh_data = pd.DataFrame([[k, *v] for k, v in cao_lh_data_dict.items()], columns=['Section', 'Value'])
            cao_rh_data = pd.DataFrame([[k, *v] for k, v in cao_rh_data_dict.items()], columns=['Section', 'Value'])
            lao_rh_data = pd.DataFrame([[k, *v] for k, v in lao_rh_data_dict.items()], columns=['Section', 'Value'])

            lao_lh_data.insert(0, 'AVG', '0%')
            lao_lh_data.insert(1, 'REF', '0')
            lao_lh_data.insert(2, 'STR', lao_lh_data['Value'])
            lao_lh_data.insert(3, 'LAO', '0%')
            lao_lh_data.insert(4, '', lao_lh_data['Section'])
            lao_lh_data.drop('Section', axis=1, inplace=True)
            lao_lh_data.drop('Value', axis=1, inplace=True)
            lao_lh_data.loc[0] = ''

            cao_lh_data.insert(0, 'AVG', '0%')
            cao_lh_data.insert(1, 'REF', '0')
            cao_lh_data.insert(2, 'STR', cao_lh_data['Value'])
            cao_lh_data.insert(3, 'LAO', '0%')
            cao_lh_data.insert(4, '', cao_lh_data['Section'])
            cao_lh_data.drop('Section', axis=1, inplace=True)
            cao_lh_data.drop('Value', axis=1, inplace=True)
            cao_lh_data.loc[0] = ''

            cao_rh_data.insert(0, '', cao_rh_data['Section'])
            cao_rh_data.insert(1, 'LAO', '0%')
            cao_rh_data.insert(2, 'STR', cao_rh_data['Value'])
            cao_rh_data.insert(3, 'REF', '0')
            cao_rh_data.insert(4, 'AVG', '0%')
            cao_rh_data.drop('Section', axis=1, inplace=True)
            cao_rh_data.drop('Value', axis=1, inplace=True)
            cao_rh_data.loc[0] = ''

            lao_rh_data.insert(0, '', lao_rh_data['Section'])
            lao_rh_data.insert(1, 'LAO', '0%')
            lao_rh_data.insert(2, 'STR', lao_rh_data['Value'])
            lao_rh_data.insert(3, 'REF', '0')
            lao_rh_data.insert(4, 'AVG', '0%')
            lao_rh_data.drop('Section', axis=1, inplace=True)
            lao_rh_data.drop('Value', axis=1, inplace=True)
            lao_rh_data.loc[0] = ''

            # Define colorlimlts
            colorlimlts = [(-0.4, -0.2), (-0.2, -0.1), (-0.1, 0.1), (0.1, 0.2), (0.2, 0.4)]

            comment_df1 = pd.DataFrame(['Comment for LAO-LH Table'], columns=['Comment'])
            self._view.resetTable_LH_first(self._view.flowValueLAOLH_tableWidget)
            self._view.adjustColWidthOf_LH_firstTable(self._view.flowValueLAOLH_tableWidget)
            self._view.adjustRowHeightOf_LH_firstTable(self._view.flowValueLAOLH_tableWidget)
            self._view.populateTable_LH_first(self._view.flowValueLAOLH_tableWidget, lao_lh_data, comment_df1)
            self._view.resizeTableWidget_LH_first(self._view.flowValueLAOLH_tableWidget)
            self._view.backgroundColorForLH(self._view.flowValueLAOLH_tableWidget, colorlimlts)
            self._view.tableHeadBold(self._view.flowValueLAOLH_tableWidget)
            self._view.setSpanLH(self._view.flowValueLAOLH_tableWidget)
            self._view.setCellColor(self._view.flowValueLAOLH_tableWidget)
            self._view.alignHeadingLH(self._view.flowValueLAOLH_tableWidget)

            comment_df2 = pd.DataFrame(['Comment for CAO-LH Table'], columns=['Comment'])
            self._view.resetTable(self._view.flowValueCAOLH_tableWidget)
            self._view.adjustColWidth(self._view.flowValueCAOLH_tableWidget)
            self._view.adjustRowHeight(self._view.flowValueCAOLH_tableWidget)
            self._view.populateTable(self._view.flowValueCAOLH_tableWidget, cao_lh_data, comment_df2)
            self._view.resizeTableWidget(self._view.flowValueCAOLH_tableWidget)
            self._view.backgroundColorForLH(self._view.flowValueCAOLH_tableWidget, colorlimlts)
            self._view.tableHeadBold(self._view.flowValueCAOLH_tableWidget)
            self._view.setSpanLH(self._view.flowValueCAOLH_tableWidget)
            self._view.setCellColor(self._view.flowValueCAOLH_tableWidget)
            self._view.alignHeadingLH(self._view.flowValueCAOLH_tableWidget)

            comment_df3 = pd.DataFrame(['Comment for CAO-RH Table'], columns=['Comment'])
            self._view.resetTable_RH_first(self._view.flowValueCAORH_tableWidget)
            self._view.adjustColWidthOf_RH_firstTable(self._view.flowValueCAORH_tableWidget)
            self._view.adjustRowHeightOf_RH_firstTable(self._view.flowValueCAORH_tableWidget)
            self._view.populateTable_RH_first(self._view.flowValueCAORH_tableWidget, cao_rh_data, comment_df3)
            self._view.resizeTableWidget_RH_first(self._view.flowValueCAORH_tableWidget)
            self._view.backgroundColorForRH(self._view.flowValueCAORH_tableWidget, colorlimlts)
            self._view.tableHeadBold(self._view.flowValueCAORH_tableWidget)
            self._view.setSpanRH(self._view.flowValueCAORH_tableWidget)
            self._view.setCellColor(self._view.flowValueCAORH_tableWidget)
            self._view.alignHeadingRH(self._view.flowValueCAORH_tableWidget)

            comment_df4 = pd.DataFrame(['Comment for LAO-RH Table'], columns=['Comment'])
            self._view.resetTable_RH_second(self._view.flowValueLAORH_tableWidget)
            self._view.adjustColWidthOf_RH_secondTable(self._view.flowValueLAORH_tableWidget)
            self._view.adjustRowWidthOf_RH_secondTable(self._view.flowValueLAORH_tableWidget)
            self._view.populateTable_RH_second(self._view.flowValueLAORH_tableWidget, lao_rh_data, comment_df4)
            self._view.resizeTableWidget_RH_second(self._view.flowValueLAORH_tableWidget)
            self._view.backgroundColorForRH(self._view.flowValueLAORH_tableWidget, colorlimlts)
            self._view.tableHeadBold(self._view.flowValueLAORH_tableWidget)
            self._view.setSpanRH(self._view.flowValueLAORH_tableWidget)
            self._view.setCellColor(self._view.flowValueLAORH_tableWidget)
            self._view.alignHeadingRH(self._view.flowValueLAORH_tableWidget)

            # load image
            self._view.loadImage()
            self._view.loadImage_ADAMANT_Logo()
            self._view.aircraftImage_label.setGeometry(5 + self._view.TZ_LH_tableWidget.width() + self._view.flowValueLAOLH_tableWidget.width() + self._view.flowValueCAOLH_tableWidget.width(), 14, 600, self._view.flowValueLAOLH_tableWidget.height())

            #      TZ LH flow table
            self._view.setRowSpanOfTZ_table(self._view.TZ_LH_tableWidget)
            self._view.adjustRowHeightOf_LH_firstTable(self._view.TZ_LH_tableWidget)
            self._view.resizeTableWidget_LH_TZ_first(self._view.TZ_LH_tableWidget)
            self._view.tableHeadBold(self._view.TZ_LH_tableWidget)

            #      TZ RH Flow table
            self._view.setRowSpanOfTZ_table(self._view.TZ_RH_tableWidget)
            self._view.adjustRowHeightOf_LH_firstTable(self._view.TZ_RH_tableWidget)
            self._view.resizeTableWidget_LH_TZ_first(self._view.TZ_RH_tableWidget)
            self._view.tableHeadBold(self._view.TZ_RH_tableWidget)

            #       Set up Layout of Flow Tables properly with borders, etc.
            self._view.setGeometryOFflowTZ1(self._view.TZ_LH_tableWidget)
            self._view.setGeometryOFflowLH1(self._view.flowValueLAOLH_tableWidget, self._view.TZ_LH_tableWidget)
            self._view.setGeometryOFflowLH2(self._view.flowValueCAOLH_tableWidget, self._view.TZ_LH_tableWidget, self._view.flowValueLAOLH_tableWidget)
            self._view.setGeometryOFflowTZ2(self._view.TZ_RH_tableWidget)
            self._view.setGeometryOFflowRH2(self._view.flowValueLAORH_tableWidget)
            self._view.setGeometryOFflowRH1(self._view.flowValueCAORH_tableWidget, self._view.flowValueLAORH_tableWidget)
            self._view.flowValues_groupBox.setGeometry(10, 260, self._view.flowValueLAORH_tableWidget.width() * 5 + 180, self._view.flowValueLAORH_tableWidget.height() + 20)
            self._view.flow_value.setGeometry(10, 10, self._view.flowValueLAORH_tableWidget.width() * 5 + 250, self._view.flowValueLAORH_tableWidget.height() + 3010)


    def populateAmbMixCabTables(self, selectedHoV, db, df):
        AmbP, AmbT, Mx1, Mx2, Mx3, Mx4, Mx5, Mx6, Mx7, Mx8, MxAG, Cb1, Cb2, Cb3, Cb4, Cb5, Cb6, Cb7, Cb8, CbAG = '0','0', ['0','0'], ['0','0'], ['0','0'], \
                                                                                                                 ['0','0'], ['0','0'], ['0','0'], ['0','0'], \
                                                                                                                 ['0','0'], ['0','0'], ['0','0'], ['0','0'], \
                                                                                                                 ['0','0'], ['0','0'], ['0','0'], ['0','0'], \
                                                                                                                 ['0','0'], ['0','0'], ['0']                        # Initialize to 0

        if (selectedHoV != ''):
            df_mixrecamb_selected = df[df.index.get_level_values('HoV') == selectedHoV].head(1)
            print("Selected HoV is: ", selectedHoV)
            if db=='str':
                AmbP = str(df_mixrecamb_selected['AMBP'].values[0])
                AmbT = str(df_mixrecamb_selected['AMBT'].values[0])
            #elif db=='ltr':
            #    AmbP = str(df_mixrecamb_selected['AMBP'].values[0])
            #    AmbT = str(df_mixrecamb_selected['AMBT'].values[0])
            elif db=='gtr4' and selectedHoV!='GTR Definition':
                AmbP = str(df_mixrecamb_selected['AMBP'].values[0])
                AmbT = str(df_mixrecamb_selected['AMBT'].values[0])
                Mx1 = [str(df_mixrecamb_selected['MIXP1'].values[0]), str(df_mixrecamb_selected['MIXT1'].values[0])]
                Mx2 = [str(df_mixrecamb_selected['MIXP2'].values[0]), str(df_mixrecamb_selected['MIXT2'].values[0])]
                Mx3 = [str(df_mixrecamb_selected['MIXP3'].values[0]), str(df_mixrecamb_selected['MIXT3'].values[0])]
                Mx4 = [str(df_mixrecamb_selected['MIXP4'].values[0]), str(df_mixrecamb_selected['MIXT4'].values[0])]
                Mx5 = [str(df_mixrecamb_selected['MIXP5'].values[0]), str(df_mixrecamb_selected['MIXT5'].values[0])]
                Mx6 = [str(df_mixrecamb_selected['MIXP6'].values[0]), str(df_mixrecamb_selected['MIXT6'].values[0])]
                Mx7 = [str(df_mixrecamb_selected['MIXP7'].values[0]), str(df_mixrecamb_selected['MIXT7'].values[0])]
                Mx8 = [str(df_mixrecamb_selected['MIXP8'].values[0]), str(df_mixrecamb_selected['MIXT8'].values[0])]
            elif db=='gtr8' and selectedHoV!='GTR Definition':
                AmbP = str(df_mixrecamb_selected['AMBP'].values[0])
                AmbT = str(df_mixrecamb_selected['AMBT'].values[0])
                Mx1 = [str(df_mixrecamb_selected['MIXP1'].values[0]), str(df_mixrecamb_selected['MIXT1'].values[0])]
                Mx2 = [str(df_mixrecamb_selected['MIXP2'].values[0]), str(df_mixrecamb_selected['MIXT2'].values[0])]
                Mx3 = [str(df_mixrecamb_selected['MIXP3'].values[0]), str(df_mixrecamb_selected['MIXT3'].values[0])]
                Mx4 = [str(df_mixrecamb_selected['MIXP4'].values[0]), str(df_mixrecamb_selected['MIXT4'].values[0])]
                Mx5 = [str(df_mixrecamb_selected['MIXP5'].values[0]), str(df_mixrecamb_selected['MIXT5'].values[0])]
                Mx6 = [str(df_mixrecamb_selected['MIXP6'].values[0]), str(df_mixrecamb_selected['MIXT6'].values[0])]
                Mx7 = [str(df_mixrecamb_selected['MIXP7'].values[0]), str(df_mixrecamb_selected['MIXT7'].values[0])]
                Mx8 = [str(df_mixrecamb_selected['MIXP8'].values[0]), str(df_mixrecamb_selected['MIXT8'].values[0])]

            self._view.populateTable_AMBIENT_PRESSURE_TEMP_table(self._view.Ambient_P_T_tableWidget,AmbP,AmbT)         #Amb P,T
            self._view.populateTable_Mx1_table(self._view.MxP1_tableWidget,Mx1)         # Mx1
            self._view.populateTable_Mx2_table(self._view.MxP2_tableWidget,Mx2)        # Mx2
            self._view.populateTable_Mx3_table(self._view.MxP3_tableWidget,Mx3)        # Mx3
            self._view.populateTable_Mx4_table(self._view.MxP4_tableWidget,Mx4)        # Mx4
            self._view.populateTable_Mx5_table(self._view.MxP5_tableWidget,Mx5)        # Mx5
            self._view.populateTable_Mx6_table(self._view.MxP6_tableWidget,Mx6)        # Mx6
            self._view.populateTable_Mx7_table(self._view.MxP7_tableWidget,Mx7)        # Mx7
            self._view.populateTable_Mx8_table(self._view.MxP3_tableWidget,Mx8)        # Mx8
            self._view.populateTable_MxAG_table(self._view.MxPAG_tableWidget,MxAG)    # MxAG
            self._view.populateTable_Cb1_table(self._view.CbP1_tableWidget,Cb1)        # Cb1
            self._view.populateTable_Cb2_table(self._view.CbP2_tableWidget,Cb2)        # Cb2
            self._view.populateTable_Cb3_table(self._view.CbP3_tableWidget,Cb3)        # Cb3
            self._view.populateTable_Cb4_table(self._view.CbP4_tableWidget,Cb4)        # Cb4
            self._view.populateTable_Cb5_table(self._view.CbP5_tableWidget,Cb5)        # Cb5
            self._view.populateTable_Cb6_table(self._view.CbP6_tableWidget,Cb6)        # Cb6
            self._view.populateTable_Cb7_table(self._view.CbP7_tableWidget,Cb7)        # Cb7
            self._view.populateTable_Cb8_table(self._view.CbP8_tableWidget,Cb8)        # Cb8
            self._view.populateTable_CbAG_table(self._view.CbPAG_tableWidget,CbAG)    # CbAG


    def onModeChangedtoSTR(self):
        if self._view.STRradioButton.isChecked() == True:
            print("STRradioButton was clicked")
            #Populate HoVComboBox
            #df_flow=self._model.db1_str.flow_df.df
            Hovnames = set(self.df_db1_flow.index.get_level_values('HoV'))
            #print(Hovnames)
            self._view.populate_HOV(Hovnames)

            #Populate Flow Tables (LAO-LH, CAO-LH, CAO-RH, LAO-RH) according to selectedHoV
            #selectedHoV = str(self._view.aircraftHOV_comboBox.currentText())
            #selectedHoV = self.on_aircraftHOV_comboBox_changed(self)
            #self.populateFlowTables(selectedHoV, df_flow.copy())
            return True
        else:
            return False

    def onModeChangedtoLTR(self):
        if self._view.LTRradioButton.isChecked() == True:
            print("LTRradioButton was clicked")
            #Populate HoVComboBox
            #df_flow=self._model.db2_ltr.flow_df.df
            print(self.df_db2_flow)
            Hovnames = set(self.df_db2_flow.index.get_level_values('HoV'))
            self._view.populate_HOV(Hovnames)

            #Populate Flow Tables (LAO-LH, CAO-LH, CAO-RH, LAO-RH) according to selectedHoV
            #selectedHoV = str(self._view.aircraftHOV_comboBox.currentText())
            #self.populateFlowTables(selectedHoV, df_flow.copy())
            return True
        else:
            return False

    def onModeChangedtoGTR4(self):
        if self._view.GTR4radioButton.isChecked() == True:
            print("GTR4radioButton was clicked")

            #Populate HoVComboBox
            #df_flow=self._model.db3_gtr4.flow_df.df
            #Hovnames=set(df_flow.index.tolist())
            Hovnames = set(self.df_db3_flow.index.get_level_values('HoV'))
            self._view.populate_HOV(Hovnames)

            #Populate Flow Tables (LAO-LH, CAO-LH, CAO-RH, LAO-RH) according to selectedHoV
            #selectedHoV = str(self._view.aircraftHOV_comboBox.currentText())
            #self.populateFlowTables(selectedHoV, df_flow.copy())
            return True
        else:
            return False

    def onModeChangedtoGTR8(self):
        if self._view.GTR8radioButton.isChecked() == True:
            print("GTR8radioButton was clicked")

            #Populate HoVComboBox
            #df_flow=self._model.db4_gtr8.flow_df.df
            #Hovnames=set(df_flow.index.tolist())
            Hovnames = set(self.df_db4_flow.index.get_level_values('HoV'))
            self._view.populate_HOV(Hovnames)

            # Populate Flow Tables (LAO-LH, CAO-LH, CAO-RH, LAO-RH) according to selectedHoV
            #selectedHoV = str(self._view.aircraftHOV_comboBox.currentText())
            #self.populateFlowTables(selectedHoV, self.df_flow.copy())
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
