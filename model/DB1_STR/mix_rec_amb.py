from model.interfaces import IData
import os
import pandas as pd
import re
import numpy as np
import logging


class DB1_STR_MIXRECAMB(IData):
    """
    class to instantiate the STR DATASET.
    """

    def __init__(self):
        self._dataframe = pd.DataFrame()
        self._mixrecambpath = ''

        folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\1-STR"
        self.importAllFilesinFolders(folderpath)

    def _parse(self, path, HoV):
        """
        PARSE ONE FILE FROM A NETWORK LOCATION RETURN A DATAFRAME WITh one row correponding to one test reference.

        :type self: DB1_STR_MIXRECAMB
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

        test = path[path.rindex('-')+1:].split('.', 1)[0]
        frame_actual_df.insert(0, column='HoV', value=HoV)
        frame_actual_df.insert(1, column='Test', value=test)

        frame_actual_df = frame_actual_df.fillna(0)  # Fill NaNs with zero

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

        :type self: DB1_STR_MIXRECAMB
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

        :type self: DB1_STR_MIXRECAMB
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
        """ Prints the head of dataframe of the calling object of DB1_STR_MIXRECAMB class.

        :type self: DB1_STR_MIXRECAMB
        :param self: Calling Object of STR DATASET

        :raises:

        :rtype:
        """
        print(self._dataframe.head())


    def process(self, raw_df):
        """ Function to preprocess the raw dataframe and reshape into a one column intermediate dataframe on
        which transformations(mostly section renamings) can be applied.

        :type self: DB1_STR_MIXRECAMB
        :param self: Calling Object of STR DATASET

        :type raw_df: Pandas Dataframe
        :param raw_df:  Raw Dataframe of the same shape as the input data read as it is from the file.

        :raises: None

        :return: Intermediate Dataframe with only two columns one for Frame and other for flow value.
        :rtype: Pandas Dataframe
        """

        # Parse out MixRecAmb data
        data_df_mixp = pd.DataFrame({'MIXP':[0]})
        data_df_mixt = pd.DataFrame({'MIXT':[0]})
        data_df_lhsfwd = pd.DataFrame({'LHSFWD': [0]})
        data_df_rhsfwd = pd.DataFrame({'RHSFWD': [0]})
        data_df_lhsaft = pd.DataFrame({'LHSAFT': [0]})
        data_df_rhsaft = pd.DataFrame({'RHSAFT': [0]})

        ambp_column = raw_df[raw_df['Parameter'].str.startswith('Ambient Pressure')]
        ambt_column = raw_df[raw_df['Parameter'].str.startswith('Ambient Temperature')]
        del ambp_column['Temp Zone']
        del ambt_column['Temp Zone']
        data_dict_ambp = ambp_column.set_index('Parameter').T.to_dict('list')
        data_dict_ambt = ambt_column.set_index('Parameter').T.to_dict('list')
        data_df_ambp = pd.DataFrame(data_dict_ambp)
        data_df_ambt = pd.DataFrame(data_dict_ambt)
        data_df_ambp.rename(columns={data_df_ambp.columns[0]: 'AMBP'}, inplace=True)
        data_df_ambt.rename(columns={data_df_ambt.columns[0]: 'AMBT'}, inplace=True)

        frame_actual_df = pd.DataFrame()
        frame_actual_df = pd.concat([frame_actual_df, data_df_mixp], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_mixt], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_ambp], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_ambt], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_lhsfwd], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_rhsfwd], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_lhsaft], axis=1)
        frame_actual_df = pd.concat([frame_actual_df, data_df_rhsaft], axis=1)

        frame_actual_df = frame_actual_df.fillna(0)

        return frame_actual_df


    def getimportpath(self):
        """ Get the path to the repository in network drive from where the data will be imported

        :type self: DB1_STR_MIXRECAMB
        :param self: Calling Object of STR DATASET

        :raises:
        :return: Current import path
        :rtype: string
        """
        return self._mixrecambpath

    def setimportpath(self, path):
        """  Set the path to the import Repository

        :type self: DB1_STR_MIXRECAMB
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises:

        :rtype: None
        """
        if (os.path.exists(path)):
            self._mixrecambpath = path
        else:
            print("New Import path does not exists")

    @property
    def df(self):
        return self._dataframe

    def getexportpath(self):

        """ Get the export repository path
        :type self: DB1_STR_MIXRECAMB
        :param self: Calling Object of LTR2 DATASET

        :raises:

        :return: Current export path
        :rtype: string
        """
        return self.export_path

    def setexportpath(self, path):
        """ Set the export repository path
        :type self: DB1_STR_MIXRECAMB
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

    def export2Excel(self, filename, export_path):
        """ Creates a backup of the calling STR Datset using export path. Writes the new load path to a config file on network drive.

        :type self: DB1_STR_MIXRECAMB
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        filename = filename + ".xlsx" if not filename.endswith(".xlsx") else filename
        filepath = os.path.join(export_path, filename)
        print("Writing MixRecAmb Dataframe File:", filepath, "\t SHAPE ", self._dataframe.shape)
        self._dataframe.to_excel(filepath)

        logging.info('Export2Excel: {}, {}'.format(filename, export_path))

        return filepath

    def flattened_df(self, df):
        """ Creates a flattened dataframe by dropping existing indexes from multi-indexed dataframe

        :type self: DB1_STR_MIXRECAMB
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        flattened_df = df
        flattened_df = flattened_df.reset_index(level=[0,1])
        #print(flattened_df)

        return flattened_df

    def expandedDiff(self, testFile, refFile):
        """ Creates an expanded Difference File for MixRecAmb data by comparing cleaned data from Input files with Reference STR Dataset

        :type self: DB1_STR_MIXRECAMB
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        # define the expanded diff
        #df_actual_out_mixrecamb = pd.read_excel(testFile, sheetname='Sheet1', header=None)
        df_copy = self.df.copy()
        df_actual_out_mixrecamb = self.flattened_df(df_copy)
        df_actual_out_mixrecamb = df_actual_out_mixrecamb.dropna(axis=1, how='all')

        df_expt_out_mixrecamb = pd.read_excel(refFile, sheetname='DB1 STR', parse_cols='A,B,HJ:HQ', header=None)       # using 'parse_cols' instead of 'usecols' because of older pandas version
        df_expt_out_mixrecamb = df_expt_out_mixrecamb.iloc[2:]
        df_expt_out_mixrecamb.columns = df_expt_out_mixrecamb.iloc[0]
        df_expt_out_mixrecamb = df_expt_out_mixrecamb.iloc[1:, :]
        df_expt_out_mixrecamb.rename(columns={df_expt_out_mixrecamb.columns[0]: 'HoV'}, inplace=True)
        df_expt_out_mixrecamb.rename(columns={df_expt_out_mixrecamb.columns[1]: 'Test'}, inplace=True)
        df_expt_out_mixrecamb = df_expt_out_mixrecamb.dropna(axis=1, how='all')

        common_rows_mixrecamb_df = pd.merge(df_expt_out_mixrecamb, df_actual_out_mixrecamb, how='inner', on=['HoV', 'Test'])
        selected_col_x = [col for col in common_rows_mixrecamb_df.columns if col.endswith('_x')]
        common_rows_mixrecamb_df_actual_out = common_rows_mixrecamb_df[selected_col_x]
        selected_col_y = [col for col in common_rows_mixrecamb_df.columns if col.endswith('_y')]
        common_rows_mixrecamb_df_expt_out = common_rows_mixrecamb_df[selected_col_y]

        common_rows_mixrecamb_df_actual_out.columns = common_rows_mixrecamb_df_actual_out.columns.str.rstrip('_x')
        common_rows_mixrecamb_df_expt_out.columns = common_rows_mixrecamb_df_expt_out.columns.str.rstrip('_y')
        common_rows_mixrecamb_df_actual_out = common_rows_mixrecamb_df_actual_out.fillna(0)
        common_rows_mixrecamb_df_expt_out = common_rows_mixrecamb_df_expt_out.fillna(0)

        result_diff_mixrecamb_df = common_rows_mixrecamb_df_actual_out.astype(float) - common_rows_mixrecamb_df_expt_out.astype(float)

        add_HoV_col = common_rows_mixrecamb_df.iloc[:, 0].tolist()
        add_Test_col = common_rows_mixrecamb_df.iloc[:, 1].tolist()
        result_diff_mixrecamb_df.insert(0, column='HoV', value=add_HoV_col)
        result_diff_mixrecamb_df.insert(1, column='Test', value=add_Test_col)

        return result_diff_mixrecamb_df


    def printDiffReport(self, exp_diff_df, filepath):
        """ Creates a Report for expanded Difference File for MixRecAmb data

        :type self: DB1_STR_MIXRECAMB
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
        print("Writing MixRecAmb Diff File:", filepath, "\t SHAPE ", self._dataframe.shape)
        exp_diff_df.to_excel(filepath)
        return filepath


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
    referenceFileName= "DB1_STR_MIXRECAMB.xlsm"
    reffile= os.path.join(rootdir, "tests\REF\DB1_STR",referenceFileName)

    logfilename="DB1_STR_MIXRECAMB.log"
    logfilepath= os.path.join(rootdir, "tests\RESULTS\DB1_STR",logfilename)
    logging.basicConfig(filename=logfilepath, format='Date-Time: %(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    STR1MixRecAmb = DB1_STR_MIXRECAMB()

    #Test 1
    STR1MixRecAmb.importAllFilesinFolders(folderpath)
    STR1MixRecAmb.headdf()
    testfile1=STR1MixRecAmb.export2Excel("test1DB1_MixRecAmb.xlsx", export_folderpath)
    exp_diff1=STR1MixRecAmb.expandedDiff(testfile1,reffile)
    print("Expanded diff successfull")
    diff_filename1="DB1_STR_MIXRECAMB_DIFF_1.xlsx"
    diff_report_path= os.path.join(rootdir, "tests\RESULTS\DB1_STR",diff_filename1)
    STR1MixRecAmb.printDiffReport(exp_diff1, diff_report_path)

    #test 2:
    new_record_path = os.path.join(rootdir, "tests\\NEW\\DB1_STR\\CNK12-EXAMPLE.xlsm")
    STR1MixRecAmb.addNewRecord(new_record_path, "CNK12", "A350-900")
    STR1MixRecAmb.headdf()
    testfile2 = STR1MixRecAmb.export2Excel("test2DB1_MixRecAmb.xlsx", export_folderpath)
    exp_diff2 = STR1MixRecAmb.expandedDiff(testfile2, reffile)
    print("Expanded diff successfull")
    diff_filename2="DB1_STR_MIXRECAMB_DIFF_2.xlsx"
    diff_report_path= os.path.join(rootdir, "tests\RESULTS\DB1_STR",diff_filename2)
    STR1MixRecAmb.printDiffReport(exp_diff2, diff_report_path)
