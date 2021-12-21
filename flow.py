from model.interfaces import IData
import os
import pandas as pd
import re
import numpy as np
import logging


class DB1_STR_FLOW(IData):
    """
    class to instantiate the STR DATASET.
    """

    def __init__(self):
        self._dataframe = pd.DataFrame()
        self._flowdefpath = ''

        folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\1-STR"
        self.importAllFilesinFolders(folderpath)


    def _parse(self, path, HoV, db1_str_test_reference=None):
        """
        PARSE ONE FILE FROM A NETWORK LOCATION RETURN A DATAFRAME WITh one row correponding to one test reference.

        :type self: DB1_STR_FLOW
        :param self: Calling object of the STR Dataset

        :type path: string
        :param path: Full path to the file on the specified network location

        :raises:

        :return: Dataframe with one line indexed by HoV
        :rtype: Pandas dataframe
        """
        raw_df = self._read_df(path)
        #hpa_value = self._getHPAvalue(raw_df)
        frame_actual_df = self.process(raw_df)

        # Below, we create multi-indexed dataframe
        frame_actual_df = frame_actual_df.T.reset_index()
        frame_actual_df.columns = ['Frame', 'Actual']
        frame_actual_df['Frame'] = frame_actual_df['Frame'].apply(lambda x: x.rsplit("_", 1)[0])

        # Creating three columns for type, side ,frame using apply
        frame_actual_df["type"] = frame_actual_df["Frame"].apply(lambda x: x.split("_")[0])
        frame_actual_df["side"] = frame_actual_df["Frame"].apply(lambda x: x.split("_")[1])
        frame_actual_df["Frame"] = frame_actual_df["Frame"].apply(lambda x: x.split("_")[2] + "-" + x.split("_")[3] if len(x.split("_")) == 4 else x.split("_")[2])

        frame_actual_df = frame_actual_df.set_index(["type", "side", "Frame"])
        frame_actual_df = frame_actual_df.T

        # frame_actual_df.rename(columns=lambda x: x.rsplit('_', 1)[0], inplace=True)
        test = path[path.rindex('-')+1:].split('.', 1)[0]
        frame_actual_df.insert(0, column='HoV', value=HoV)
        frame_actual_df.insert(1, column='Test', value=test)
        frame_actual_df = frame_actual_df.fillna(0)           # Fill NaNs with zero

        frame_actual_df = frame_actual_df.set_index(["HoV", "Test"])

        logging.info('Parse: {}, {}'.format(path, HoV))

        return frame_actual_df

    def importAllFilesinFolders(self, folderpath):
        """ Function to import data from all  files and append them to the dataset.
        To be over ridden by the derived classes.
        :type self:
        :param self:

        :type folderpath:
        :param folderpath: the folder in which all the files for this data resides

        :raises:

        :rtype:
        """
        if (os.path.exists(folderpath)):
            HoV_folder_list = os.listdir(folderpath)
            for i in HoV_folder_list:
                # Create path to a particular HoV
                path_to_HoV = os.path.join(folderpath, i)
                file_list = os.listdir(path_to_HoV)
                path_list = [os.path.join(path_to_HoV, x) for x in file_list if not x.startswith("~")]

                for fil_path in path_list:
                    self.addNewRecord(fil_path, HoV=i)

            print("\n\n\n\n\n IMPORT DATA SUCCESSFULLY\n\n\n\n")

        else:
            raise FileNotFoundError("Entered path to the import repository does not exist")

    def addNewRecord(self, filepath, HoV=None, ACversion=None):
        """ Function to add the data of a new input file to the existing dataframe.
        To be overridden by the derived class.

        Please follow the above order of the arguements wherever possible.

        :type self:
        :param self:

        :type filepath:
        :param filepath:

        :raises:

        :rtype:
        """
        path_elements = os.path.split(filepath)
        filename = path_elements[1]
        oneline_df = self._parse(filepath, HoV)
        try:
            self._dataframe = pd.concat([self._dataframe, oneline_df], axis=0)
        except:
            print("Exception occurred for: ", filename)

    '''
    def _getHPAvalue(self, raw_df):
        """ Get the HPA value from the raw file dataframe

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type raw_df: Pandas dataframe
        :param raw_df: Raw Dataframe which results from reading the file as it is.

        :raises:

        :return: HPA value
        :rtype: float
        """
        hpa_value = 0
        try:
            first_column = raw_df.iloc[:, 0]
            hpa_index = first_column[first_column == "HPA"].index[0]
            hpa_value = raw_df.iloc[hpa_index, 1]
        except:
            pass
        finally:
            return hpa_value
    '''

    def _read_df(self, path):
        """ Read the dataframe from an input file as is and return a raw input dataframe.

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type path: string
        :param path: Path to the input file corresponding to a Test Reference

        :raises: FileNotFoundError

        :return: Raw Dataframe of the same shape as the input data read as it is from the file.
        :rtype: Pandas Dataframe
        """
        raw_df = pd.read_excel(path, sheetname="Template", header=None, skiprows=3)
        raw_df = raw_df.drop(raw_df.columns[[3,4,5]], axis=1)
        raw_df.columns = ['Temp Zone', 'Parameter', 'Input']
        return raw_df

    def headdf(self):
        """ Prints the head of dataframe of the calling object of DB1_STR_FLOW class.

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :raises:

        :rtype:
        """
        print(self._dataframe.head())


    def process(self, raw_df):
        """ Function to preprocess the raw dataframe and reshape into a one column intermediate dataframe on
        which transformations(mostly section renamings) can be applied.

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type raw_df:Pandas Dataframe
        :param raw_df:  Raw Dataframe of the same shape as the input data read as it is from the file.

        :raises:None

        :return: Intermediate Dataframe with only two columns one for Frame and other for flow value.
        :rtype:Pandas Dataframe
        """

        # Define mapping functions 'cao_lh_map', cao_rh_map', 'lao_lh_map', 'lao_rh_map' for mapping 'AO Flow' rows in I/P files to 'CAO', 'LAO' columns of O/P Template format file. The mapping function is derived based on "A350-900" Standard defined in 'DB ACV' Sheet
        # Below mapping functions can be replaced or eliminated once the exact logic for mapping I/P files to O/P Template is well-defined & understood.
        cao_lh_map = {'CAO_LH_C17-C18_R1': 'AO Flow Z1 LH C1', 'CAO_LH_C18-C20_R1': '0', 'CAO_LH_C20-C21_R1': '0', 'CAO_LH_C21-C22_R1': '0', 'CAO_LH_C18-C19_R1': 'AO Flow Z1 LH C2', 'CAO_LH_C19-C21_R1': 'AO Flow Z1 LH C3', 'CAO_LH_C22-C24_R1': 'AO Flow Z1 LH C4', 'CAO_LH_C24-C26_R1': 'AO Flow Z1 LH C5', 'CAO_LH_C26-C28_R1': 'AO Flow Z1 LH C6', \
                      'CAO_LH_C28-C30_R2': 'AO Flow Z2 LH C1', 'CAO_LH_C30-C32_R2': 'AO Flow Z2 LH C2', 'CAO_LH_C30.2-C30.4_R2': '0', 'CAO_LH_C30.4-C30.6_R2': '0', 'CAO_LH_C30.6-C32_R2': '0', 'CAO_LH_C32-C34_R2': 'AO Flow Z2 LH C3', 'CAO_LH_C34-C36_R2': 'AO Flow Z2 LH C4', 'CAO_LH_C36-C38_R2': 'AO Flow Z2 LH C5', 'CAO_LH_C38-C40_R3': 'AO Flow Z3 LH C1', \
                      'CAO_LH_C40-C42_R3': 'AO Flow Z3 LH C2', 'CAO_LH_C40.2-C40.4_R3': '0', 'CAO_LH_C40.4-C40.6_R3': '0', 'CAO_LH_C40.6-C40.7_R3': '0', 'CAO_LH_C40.7-C40.9_R3': '0', 'CAO_LH_C40.9-C42_R3': '0', 'CAO_LH_C42-C44_R3': 'AO Flow Z2 LH C3', 'CAO_LH_C44-C46_R3': 'AO Flow Z2 LH C4', 'CAO_LH_C46-C48_R4': 'AO Flow Z4 LH C1', 'CAO_LH_C48-C50_R4': 'AO Flow Z4 LH C2', \
                      'CAO_LH_C50-C52_R4': 'AO Flow Z4 LH C3', 'CAO_LH_C52-C54_R4': 'AO Flow Z4 LH C4', 'CAO_LH_C54-C56_R5': 'AO Flow Z5 LH C1', 'CAO_LH_C56-C58_R5': 'AO Flow Z5 LH C2', 'CAO_LH_C58-C60_R5': 'AO Flow Z5 LH C3', 'CAO_LH_C60-C62_R5': 'AO Flow Z5 LH C4', 'CAO_LH_C62-C64_R5': 'AO Flow Z5 LH C5', 'CAO_LH_C64-C66_R5': 'AO Flow Z5 LH C6', 'CAO_LH_C66-C68_R6': 'AO Flow Z6 LH C1', \
                      'CAO_LH_C68-C70_R6': 'AO Flow Z6 LH C2', 'CAO_LH_C70-C72_R6': 'AO Flow Z6 LH C3', 'CAO_LH_C70.2-C70.3_R6': '0', 'CAO_LH_C70.3-C70.5_R6': '0', 'CAO_LH_C70.5-C70.7_R6': '0', 'CAO_LH_C70.5-C72_R6': '0', 'CAO_LH_C72-C74_R6': 'AO Flow Z6 LH C4', 'CAO_LH_C72.2-C72.3_R6': '0', 'CAO_LH_C72.3-C72.5_R6': '0', 'CAO_LH_C72.5-C74_R6': '0', 'CAO_LH_C74-C76_R6': 'AO Flow Z6 LH C5', \
                      'CAO_LH_C76-C78_R6': 'AO Flow Z6 LH C6', 'CAO_LH_C78-C79_R7': 'AO Flow Z7 LH C1', 'CAO_LH_C79-C80_R7': 'AO Flow Z7 LH C2', 'CAO_LH_C80-C82_R7': 'AO Flow Z7 LH C3', 'CAO_LH_C82-C84_R7': 'AO Flow Z7 LH C4', 'CAO_LH_C84-C86_R7': 'AO Flow Z7 LH C5', 'CAO_LH_C86-C88_R7': '0', 'CAO_LH_C88-C89_R7': '0', 'CAO_LH_C92-C93_R7': '0', 'CAO_LH_CAS_R7': '0'}

        cao_rh_map = {'CAO_RH_C17-C18_R1': 'AO Flow Z1 RH C1', 'CAO_RH_C18-C20_R1': '0', 'CAO_RH_C20-C21_R1': '0', 'CAO_RH_C21-C22_R1': '0', 'CAO_RH_C18-C19_R1': 'AO Flow Z1 RH C2', 'CAO_RH_C19-C21_R1': 'AO Flow Z1 RH C3', 'CAO_RH_C22-C24_R1': 'AO Flow Z1 RH C4', 'CAO_RH_C24-C26_R1': 'AO Flow Z1 RH C5', 'CAO_RH_C26-C28_R1': 'AO Flow Z1 RH C6', \
                      'CAO_RH_C28-C30_R2': 'AO Flow Z2 RH C1', 'CAO_RH_C30-C32_R2': 'AO Flow Z2 RH C2', 'CAO_RH_C30.2-C30.4_R2': '0', 'CAO_RH_C30.4-C30.6_R2': '0', 'CAO_RH_C30.6-C32_R2': '0', 'CAO_RH_C32-C34_R2': 'AO Flow Z2 RH C3', 'CAO_RH_C34-C36_R2': 'AO Flow Z2 RH C4', 'CAO_RH_C36-C38_R2': 'AO Flow Z2 RH C5', 'CAO_RH_C38-C40_R3': 'AO Flow Z3 RH C1', 'CAO_RH_C40-C42_R3': 'AO Flow Z3 RH C2', \
                      'CAO_RH_C40.2-C40.4_R3': '0', 'CAO_RH_C40.4-C40.6_R3': '0', 'CAO_RH_C40.6-C40.7_R3': '0', 'CAO_RH_C40.7-C40.9_R3': '0', 'CAO_RH_C40.9-C42_R3': '0', 'CAO_RH_C42-C44_R3': 'AO Flow Z3 RH C3', 'CAO_RH_C44-C46_R3': 'AO Flow Z3 RH C4', 'CAO_RH_C46-C48_R4': 'AO Flow Z4 RH C1', 'CAO_RH_C48-C50_R4': 'AO Flow Z4 RH C2', 'CAO_RH_C50-C52_R4': 'AO Flow Z4 RH C3', 'CAO_RH_C52-C54_R4': 'AO Flow Z4 RH C4', \
                      'CAO_RH_C54-C56_R5': 'AO Flow Z5 RH C1', 'CAO_RH_C56-C58_R5': 'AO Flow Z5 RH C2', 'CAO_RH_C58-C60_R5': 'AO Flow Z5 RH C3', 'CAO_RH_C60-C62_R5': 'AO Flow Z5 RH C4', 'CAO_RH_C62-C64_R5': 'AO Flow Z5 RH C5', 'CAO_RH_C64-C66_R5': 'AO Flow Z5 RH C6', 'CAO_RH_C66-C68_R6': 'AO Flow Z6 RH C1', 'CAO_RH_C68-C70_R6': 'AO Flow Z6 RH C2', 'CAO_RH_C70-C72_R6': 'AO Flow Z6 RH C3', \
                      'CAO_RH_C70.2-C70.3_R6': '0', 'CAO_RH_C70.3-C70.5_R6': '0', 'CAO_RH_C70.5-C70.7_R6': '0', 'CAO_RH_C70.5-C72_R6': '0', 'CAO_RH_C72-C74_R6': 'AO Flow Z6 RH C4', 'CAO_RH_C72.2-C72.3_R6': '0', 'CAO_RH_C72.3-C72.5_R6': '0', 'CAO_RH_C72.5-C74_R6': '0', 'CAO_RH_C74-C76_R6': 'AO Flow Z6 RH C5', 'CAO_RH_C76-C78_R6': 'AO Flow Z6 RH C6', 'CAO_RH_C78-C79_R7': 'AO Flow Z7 RH C1', \
                      'CAO_RH_C79-C80_R7': '0', 'CAO_RH_C80-C82_R7': 'AO Flow Z7 RH C2', 'CAO_RH_C82-C84_R7': 'AO Flow Z7 RH C3', 'CAO_RH_C84-C86_R7': 'AO Flow Z7 RH C4', 'CAO_RH_C86-C88_R7': '0', 'CAO_RH_C88-C89_R7': '0', 'CAO_RH_C92-C93_R7': '0', 'CAO_RH_CAS_R7': '0'}

        lao_lh_map = {'LAO_LH_C19-C20_R1': 'AO Flow Z1 LH L1', 'LAO_LH_C20-C22_R1': 'AO Flow Z1 LH L2', 'LAO_LH_C22-C24_R1': 'AO Flow Z1 LH L3', 'LAO_LH_C24-C26_R1': 'AO Flow Z1 LH L4', 'LAO_LH_C26-C28_R1': 'AO Flow Z1 LH L5', 'LAO_LH_C28-C30_R2': 'AO Flow Z2 LH L1', 'LAO_LH_C30-C32_R2': 'AO Flow Z2 LH L2', 'LAO_LH_C30.2-C30.4_R2': '0', 'LAO_LH_C30.4-C30.6_R2': '0', 'LAO_LH_C30.6-C32_R2': '0', 'LAO_LH_C32-C34_R2': 'AO Flow Z2 LH L3', \
                      'LAO_LH_C34-C36_R2': 'AO Flow Z2 LH L4', 'LAO_LH_C36-C38_R2': '0', 'LAO_LH_C38-C40_R3': 'AO Flow Z3 LH L1', 'LAO_LH_C40-C42_R3': 'AO Flow Z3 LH L2', 'LAO_LH_C40.2-C40.4_R3': '0', 'LAO_LH_C40.8-C40.9_R3': '0', 'LAO_LH_C40.9-C42_R3': '0', 'LAO_LH_C42-C44_R3': 'AO Flow Z3 LH L3', 'LAO_LH_C44-C46_R3': 'AO Flow Z3 LH L4', 'LAO_LH_C46-C48_R4': 'AO Flow Z4 LH L1', 'LAO_LH_C48-C50_R4': 'AO Flow Z4 LH L2', 'LAO_LH_C50-C52_R4': 'AO Flow Z4 LH L3', \
                      'LAO_LH_C52-C54_R4': 'AO Flow Z4 LH L4', 'LAO_LH_C54-C56_R5': 'AO Flow Z5 LH L1', 'LAO_LH_C56-C58_R5': 'AO Flow Z5 LH L2', 'LAO_LH_C58-C60_R5': 'AO Flow Z5 LH L3', 'LAO_LH_C60-C62_R5': 'AO Flow Z5 LH L4', 'LAO_LH_C62-C64_0': 'AO Flow Z5 LH L5', 'LAO_LH_C66-C68_R6': 'AO Flow Z6 LH L1', 'LAO_LH_C68-C70_R6': 'AO Flow Z6 LH L2', 'LAO_LH_C70-C72_R6': 'AO Flow Z6 LH L3', 'LAO_LH_C70.2-C70.3_R6': '0', \
                      'LAO_LH_C70.3-C70.5_R6': '0', 'LAO_LH_C70.5-C70.7_R6': '0', 'LAO_LH_C70.7-C72_R6': '0', 'LAO_LH_C72-C74_R6': 'AO Flow Z6 LH L4', 'LAO_LH_C72.2-C72.3_R6': '0', 'LAO_LH_C72.3-C72.5_R6': '0', 'LAO_LH_C72.5-C74_R6': '0', 'LAO_LH_C74-C76_R6': 'AO Flow Z6 LH L5', 'LAO_LH_C76-C78_R6': 'AO Flow Z6 LH L6', 'LAO_LH_C78-C80_R7': 'AO Flow Z7 LH L1', 'LAO_LH_C80-C82_R7': 'AO Flow Z7 LH L2', \
                      'LAO_LH_C82-C84_R7': 'AO Flow Z7 LH L3', 'LAO_LH_C84-C86_R7': 'AO Flow Z7 LH L4', 'LAO_LH_CORNER_R7': 'AO Flow Z7 LH L5'}

        lao_rh_map = {'LAO_RH_C19-C20_R1': '0', 'LAO_RH_C20-C22_R1': 'AO Flow Z1 RH L1', 'LAO_RH_C22-C24_R1': 'AO Flow Z1 RH L2', 'LAO_RH_C24-C26_R1': 'AO Flow Z1 RH L3', 'LAO_RH_C26-C28_R1': 'AO Flow Z1 RH L4', 'LAO_RH_C28-C30_R2': 'AO Flow Z2 RH L1', 'LAO_RH_C30-C32_R2': 'AO Flow Z2 RH L2', 'LAO_RH_C30.2-C30.4_R2': '0', 'LAO_RH_C30.4-C30.6_R2': '0', 'LAO_RH_C30.6-C32_R2': '0', 'LAO_RH_C32-C34_R2': 'AO Flow Z2 RH L3', \
                      'LAO_RH_C34-C36_R2': '0', 'LAO_RH_C36-C38_R2': '0', 'LAO_RH_C38-C40_R3': 'AO Flow Z3 RH L1', 'LAO_RH_C40-C42_R3': 'AO Flow Z3 RH L2', 'LAO_RH_C40.2-C40.4_R3': '0', 'LAO_RH_C40.8-C40.9_R3': '0', 'LAO_RH_C40.9-C42_R3': '0', 'LAO_RH_C42-C44_R3': 'AO Flow Z3 RH L3', 'LAO_RH_C44-C46_R3': 'AO Flow Z3 RH L4', 'LAO_RH_C46-C48_R4': 'AO Flow Z4 RH L1', 'LAO_RH_C48-C50_R4': 'AO Flow Z4 RH L2', 'LAO_RH_C50-C52_R4': 'AO Flow Z4 RH L3', \
                      'LAO_RH_C52-C54_R4': 'AO Flow Z4 RH L4', 'LAO_RH_C54-C56_R5': 'AO Flow Z5 RH L1', 'LAO_RH_C56-C58_R5': 'AO Flow Z5 RH L2', 'LAO_RH_C58-C60_R5': 'AO Flow Z5 RH L3', 'LAO_RH_C60-C62_R5': 'AO Flow Z5 RH L4', 'LAO_RH_C62-C64_R5': 'AO Flow Z5 RH L5', 'LAO_RH_C66-C68_R6': 'AO Flow Z6 RH L1', 'LAO_RH_C68-C70_R6': 'AO Flow Z6 RH L2', 'LAO_RH_C70-C72_R6': 'AO Flow Z6 RH L3', 'LAO_RH_C70.2-C70.3_R6': '0', 'LAO_RH_C70.3-C70.5_R6': '0', \
                      'LAO_RH_C70.5-C70.7_R6': '0', 'LAO_RH_C70.7-C72_R6': '0', 'LAO_RH_C72-C74_R6': 'AO Flow Z6 RH L4', 'LAO_RH_C72.2-C72.3_R6': '0', 'LAO_RH_C72.3-C72.5_R6': '0', 'LAO_RH_C72.5-C74_R6': '0', 'LAO_RH_C74-C76_R6': 'AO Flow Z6 RH L5', 'LAO_RH_C76-C78_R6': 'AO Flow Z6 RH L6', 'LAO_RH_C78-C80_R7': 'AO Flow Z7 RH L1', 'LAO_RH_C80-C82_R7': 'AO Flow Z7 RH L2', 'LAO_RH_C82-C84_R7': 'AO Flow Z7 RH L3', 'LAO_RH_C84-C86_R7': 'AO Flow Z7 RH L4', \
                      'LAO_RH_CORNER_R7': '0'}

        # temp_zones = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'AG']
        cao_lao_dfr = raw_df[raw_df['Parameter'].str.startswith('AO Flow')]
        cao_lh_dfr = cao_lao_dfr[cao_lao_dfr['Parameter'].str.contains('LH C')]
        del cao_lh_dfr['Temp Zone']
        cao_rh_dfr = cao_lao_dfr[cao_lao_dfr['Parameter'].str.contains('RH C')]
        del cao_rh_dfr['Temp Zone']
        lao_lh_dfr = cao_lao_dfr[cao_lao_dfr['Parameter'].str.contains('LH L')]
        del lao_lh_dfr['Temp Zone']
        lao_rh_dfr = cao_lao_dfr[cao_lao_dfr['Parameter'].str.contains('RH L')]
        del lao_rh_dfr['Temp Zone']

        data_dict_cao_lh = cao_lh_dfr.set_index('Parameter').T.to_dict('list')
        data_dict_cao_rh = cao_rh_dfr.set_index('Parameter').T.to_dict('list')
        data_dict_lao_lh = lao_lh_dfr.set_index('Parameter').T.to_dict('list')
        data_dict_lao_rh = lao_rh_dfr.set_index('Parameter').T.to_dict('list')

        data_dict_cao_lh_new = cao_lh_map
        for km, vm in data_dict_cao_lh_new.items():
            for k, v in data_dict_cao_lh.items():
                if vm == k:
                    data_dict_cao_lh_new[km] = v[0]
        for km, vm in data_dict_cao_lh_new.items():
            if str(vm).startswith('AO'):
                data_dict_cao_lh_new[km] = None
        data_df_cao_lh_new = pd.DataFrame(data_dict_cao_lh_new, index=[0])

        data_dict_cao_rh_new = cao_rh_map
        for km, vm in data_dict_cao_rh_new.items():
            for k, v in data_dict_cao_rh.items():
                if vm == k:
                    data_dict_cao_rh_new[km] = v[0]
        for km, vm in data_dict_cao_rh_new.items():
            if str(vm).startswith('AO'):
                data_dict_cao_rh_new[km] = None
        data_df_cao_rh_new = pd.DataFrame(data_dict_cao_rh_new, index=[0])

        data_dict_lao_lh_new = lao_lh_map
        for km, vm in data_dict_lao_lh_new.items():
            for k, v in data_dict_lao_lh.items():
                if vm == k:
                    data_dict_lao_lh_new[km] = v[0]
        for km, vm in data_dict_lao_lh_new.items():
            if str(vm).startswith('AO'):
                data_dict_lao_lh_new[km] = None
        data_df_lao_lh_new = pd.DataFrame(data_dict_lao_lh_new, index=[0])

        data_dict_lao_rh_new = lao_rh_map
        for km, vm in data_dict_lao_rh_new.items():
            for k, v in data_dict_lao_rh.items():
                if vm == k:
                    data_dict_lao_rh_new[km] = v[0]
        for km, vm in data_dict_lao_rh_new.items():
            if str(vm).startswith('AO'):
                data_dict_lao_rh_new[km] = None
        data_df_lao_rh_new = pd.DataFrame(data_dict_lao_rh_new, index=[0])

        frame_actual_df = pd.DataFrame()
        frame_actual_df = pd.concat([frame_actual_df, data_df_cao_lh_new], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_cao_rh_new], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_lao_lh_new], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_lao_rh_new], axis=1)

        return frame_actual_df

    def getimportpath(self):
        """ Get the path to the repository in network drive from where the data will be imported

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :raises:
        :return: Current import path
        :rtype: string
        """
        return self._flowdefpath

    def setimportpath(self, path):
        """  Set the path to the import Repository

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises:

        :rtype: None
        """
        if (os.path.exists(path)):
            self._flowdefpath = path
        else:
            print("New Import path does not exists")

    @property
    def df(self):
        return self._dataframe

    def getexportpath(self):
        """ Get the export repository path
        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :raises:

        :return: Current export path
        :rtype:string
        """
        return self.export_path

    def setexportpath(self, path):
        """ Set the export repository path
        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises:

        :rtype: None
        """
        if (os.path.exists(path)):
            self.export_path = path
        else:
            print("New EXPORT path does not exists")

    def clean(self):
        """
        To clean an HOV data from one file: Abstract Function
                -- To be overridden by the respective Flow class
        :return:
        """
        raise NotImplementedError

    def export2Excel(self, filename, export_path):
        """ Creates a backup of the calling LTR2 Datset using export path. Writes the new load path to a config file on network drive.

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        filename = filename + ".xlsx" if not filename.endswith(".xlsx") else filename
        filepath = os.path.join(export_path, filename)
        print("Writing Flow Dataframe File:", filepath, "\t SHAPE ", self._dataframe.shape)
        self._dataframe.to_excel(filepath)

        logging.info('export2Excel: {}, {}'.format(filename, export_path))

        return filepath

    def flattened_df(self, df):
        """ Creates a flattened dataframe by dropping existing indexes from multi-indexed dataframe

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        flattened_df = df
        flattened_df = flattened_df.reset_index(level=[0,1])
        flattened_df.columns = ['_'.join(col) for col in flattened_df.columns.values]
        flattened_df.rename(columns={'HoV__': 'HoV', 'Test__': 'Test'}, inplace=True)

        return flattened_df

    def expandedDiff(self, testFile, refFile):
        """ Creates an expanded Difference File for Flow data by comparing cleaned data from Input files with Reference STR Dataset

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        # define the expanded diff
        #df_actual_out_aoflow = pd.read_excel(testFile, sheetname='Sheet1', header=None)
        df_copy = self.df.copy()
        df_actual_out_aoflow = self.flattened_df(df_copy)

        df_expt_out_aoflow = pd.read_excel(refFile, sheetname='DB1 STR', parse_cols='A,B,H:HI', header=None)      # using 'parse_cols' instead of 'usecols' because of older pandas version
        df_expt_out_aoflow = df_expt_out_aoflow.iloc[3:]
        '''
        df_expt_out_aoflow.columns = list(df_actual_out_aoflow.columns.values)
        df_expt_out_aoflow = df_expt_out_aoflow.iloc[1:]
        df_actual_out_aoflow.columns = df_actual_out_aoflow.iloc[0]
        df_actual_out_aoflow = df_actual_out_aoflow.iloc[1:, :]
        df_expt_out_aoflow.columns = df_actual_out_aoflow.columns
        '''
        df_expt_out_aoflow.columns = list(df_actual_out_aoflow.columns.values)

        common_rows_df = pd.merge(df_expt_out_aoflow, df_actual_out_aoflow, how='inner', on=['HoV', 'Test'])
        selected_col_x = [col for col in common_rows_df.columns if col.endswith('_x')]
        common_rows_df_actual_out_aoflow = common_rows_df[selected_col_x]
        selected_col_y = [col for col in common_rows_df.columns if col.endswith('_y')]
        common_rows_df_expt_out_aoflow = common_rows_df[selected_col_y]

        common_rows_df_actual_out_aoflow.columns = common_rows_df_actual_out_aoflow.columns.str.rstrip('_x')
        common_rows_df_expt_out_aoflow.columns = common_rows_df_expt_out_aoflow.columns.str.rstrip('_y')
        common_rows_df_actual_out_aoflow = common_rows_df_actual_out_aoflow.fillna(0)
        common_rows_df_expt_out_aoflow = common_rows_df_expt_out_aoflow.fillna(0)

        result_diff_df = common_rows_df_actual_out_aoflow.astype(float) - common_rows_df_expt_out_aoflow.astype(float)
        add_HoV_col = common_rows_df.iloc[:, 0].tolist()
        add_Test_col = common_rows_df.iloc[:, 1].tolist()
        result_diff_df.insert(0, column='HoV', value=add_HoV_col)
        result_diff_df.insert(1, column='Test', value=add_Test_col)

        return result_diff_df

    def printDiffReport(self, exp_diff_df, filepath):
        """ Creates a Report for expanded Difference File for Flow data

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        '''
        import logging
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
        print("Writing Flow DiffFile Logger:", filepath, "\t SHAPE ", exp_diff_df.shape)
        logging.basicConfig(filename=filepath, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.info('Diff dataframe head - {}'.format(exp_diff_df))
        return logging
        '''
        print("Writing Flow Diff File:", filepath, "\t SHAPE ", self._dataframe.shape)
        exp_diff_df.to_excel(filepath)
        return filepath

    def multiInd(self):
        """ Creates a Report for expanded Difference File for Flow data

        :type self: DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        df_copy = self._dataframe
        df_copy_cao_lh = df_copy[[col for col in df_copy if col.startswith('CAO_LH')]]
        df_copy_cao_rh = df_copy[[col for col in df_copy if col.startswith('CAO_RH')]]
        df_copy_lao_lh = df_copy[[col for col in df_copy if col.startswith('LAO_LH')]]
        df_copy_lao_rh = df_copy[[col for col in df_copy if col.startswith('LAO_RH')]]
        df_copy_cao_lh.columns = df_copy_cao_lh.columns.str[7:]
        df_copy_cao_rh.columns = df_copy_cao_rh.columns.str[7:]
        df_copy_lao_lh.columns = df_copy_lao_lh.columns.str[7:]
        df_copy_lao_rh.columns = df_copy_lao_rh.columns.str[7:]
        df_copy_cao_lh.columns = pd.MultiIndex.from_product([['LH'], df_copy_cao_lh.columns])
        df_copy_cao_lh.columns = pd.MultiIndex.from_product([['CAO']] + df_copy_cao_lh.columns.levels)
        df_copy_cao_rh.columns = pd.MultiIndex.from_product([['RH'], df_copy_cao_rh.columns])
        df_copy_cao_rh.columns = pd.MultiIndex.from_product([['CAO']] + df_copy_cao_rh.columns.levels)
        df_copy_lao_lh.columns = pd.MultiIndex.from_product([['LH'], df_copy_lao_lh.columns])
        df_copy_lao_lh.columns = pd.MultiIndex.from_product([['LAO']] + df_copy_lao_lh.columns.levels)
        df_copy_lao_rh.columns = pd.MultiIndex.from_product([['RH'], df_copy_lao_rh.columns])
        df_copy_lao_rh.columns = pd.MultiIndex.from_product([['LAO']] + df_copy_lao_rh.columns.levels)
        multi_df = pd.concat([df_copy_cao_lh, df_copy_cao_rh, df_copy_lao_lh, df_copy_lao_rh], axis=1)
        add_HoV_col = df_copy.iloc[:, 0].tolist()
        add_Test_col = df_copy.iloc[:, 1].tolist()
        multi_df.insert(0, column='HoV', value=add_HoV_col)
        multi_df.insert(1, column='Test', value=add_Test_col)
        multi_df = multi_df.set_index(['HoV', 'Test'])
        return multi_df


if __name__=="__main__":
    import os
    from pathlib import Path
    curdir= os.getcwd()
    print(curdir)
    p = Path(curdir).parent
    rootdir = p.parent
    print(rootdir)
    export_folderpath = os.path.join(rootdir, "tests\OUT\DB1_STR")
    print(export_folderpath)
    # Please change the below path to your respective network location
    folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\1-STR"
    referenceFileName= "DB1_STR_FLOW.xlsm"
    reffile= os.path.join(rootdir, "tests\REF\DB1_STR",referenceFileName)

    logfilename="DB1_STR_FLOW.log"
    logfilepath= os.path.join(rootdir, "tests\RESULTS\DB1_STR",logfilename)
    logging.basicConfig(filename=logfilepath, format='Date-Time: %(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    STR1Flow = DB1_STR_FLOW()

    #Test 1
    STR1Flow.importAllFilesinFolders(folderpath)
    STR1Flow.headdf()
    '''
    testfile1=STR1Flow.export2Excel("test1DB1_FLOW.xlsx", export_folderpath)
    exp_diff1=STR1Flow.expandedDiff(testfile1,reffile)
    print("Expanded diff successfull")
    diff_filename="DB1_STR_FLOW_DIFF_1.xlsx"
    diff_report_path= os.path.join(rootdir, "tests\RESULTS\DB1_STR",diff_filename)
    STR1Flow.printDiffReport(exp_diff1, diff_report_path)
    '''

    #Test 11
    #multi = STR1Flow.df
    ##lao_lh_cols = multi.index.get_level_values('HoV').tolist()
    #hov = 'CES01'
    #test = 'CFD'
    #type = 'CAO'
    #side = 'LH'
    #flow_dict = multi.loc[(hov, test), ('CAO', 'LH')].to_dict()

    #test 2:
    new_record_path = os.path.join(rootdir, "tests\\NEW\\DB1_STR\\CNK12-EXAMPLE.xlsm")
    STR1Flow.addNewRecord(new_record_path, "CNK12", "A350-900")
    STR1Flow.headdf()
    testfile2= STR1Flow.export2Excel("test2DB1_FLOW.xlsx", export_folderpath)
    exp_diff2=STR1Flow.expandedDiff(testfile2, reffile)
    print("Expanded diff successfull")
    diff_filename="DB1_STR_FLOW_DIFF_2.xlsx"
    diff_report_path= os.path.join(rootdir, "tests\RESULTS\DB1_STR",diff_filename)
    STR1Flow.printDiffReport(exp_diff2, diff_report_path)
