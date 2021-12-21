from model.interfaces import IData
import os
import pandas as pd
import re
import numpy as np
import logging


class DB1_STR_REST(IData):
    """
    class to instantiate the STR DATASET.
    """

    def __init__(self):
        self._dataframe = pd.DataFrame()
        self._restpath = ''

    def _parse(self, path, HoV):
        """
        PARSE ONE FILE FROM A NETWORK LOCATION RETURN A DATAFRAME WITh one row correponding to one test reference.

        :type self: DB1_STR_REST
        :param self: Calling object of the STR Dataset

        :type path: string
        :param path: Full path to the file on the specified network location

        :raises:


        :return: Dataframe with one line indexed by HoV
        :rtype: Pandas dataframe
        """
        raw_df = self._read_df(path)
        # hpa_value = self._getHPAvalue(raw_df)
        frame_actual_df = self.process(raw_df)

        frame_actual_df = frame_actual_df.set_index(["TZ", "Restrictor"])
        frame_actual_df = frame_actual_df.T

        # frame_actual_df.rename(columns=lambda x: x.rsplit('_', 1)[0], inplace=True)
        test = path[path.rindex('-')+1:].split('.', 1)[0]
        frame_actual_df.insert(0, column='HoV', value=HoV)
        frame_actual_df.insert(1, column='Test', value=test)
        frame_actual_df = frame_actual_df.fillna('0;0;0;0')           # Fill NaNs with zero

        frame_actual_df = frame_actual_df.set_index(["HoV", "Test"])

        logging.info('Parse: {}, {}'.format(path, HoV))

        '''
        frame_actual_df.replace('', np.NaN, inplace=True)                 # replace ''s with NaNs
        frame_actual_df.dropna(axis=1, how='all', inplace=True)           # drop all columns with all NaNs
        frame_actual_df.replace(np.NaN, '0;0;0;0', inplace=True)          # replace NaNs with 0s
        #frame_actual_df = frame_actual_df.set_index("HoV")               # Set index to 'HoV'

        test = path[path.rindex('-')+1:].split('.', 1)[0]
        frame_actual_df.insert(0, column='HoV', value=HoV)
        frame_actual_df.insert(1, column='Test', value=test)

        logging.info('Parse: {}, {}'.format(path, HoV))
        '''

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

        :type self: DB1_STR_REST
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

        :type self: DB1_STR_REST
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
        """ Prints the head of dataframe of the calling object of DB1_STR_REST class.

        :type self: DB1_STR_REST
        :param self: Calling Object of STR DATASET

        :raises:

        :rtype:
        """
        print(self._dataframe.head())

    def process(self, raw_df):
        """ Function to preprocess the raw dataframe and reshape into a one column intermediate dataframe on
        which transformations(mostly section renamings) can be applied.

        :type self: DB1_STR_REST
        :param self: Calling Object of STR DATASET

        :type raw_df: Pandas Dataframe
        :param raw_df:  Raw Dataframe of the same shape as the input data read as it is from the file.

        :raises:None

        :return: Intermediate Dataframe with only two columns one for Frame and other for flow value.
        :rtype:Pandas Dataframe
        """
        '''
        # Parse out Restrictor data (R100-R4400)
        restrictor_dfr = raw_df[raw_df['Parameter'].str.startswith('R')]
        restrictor_dfr = restrictor_dfr[~restrictor_dfr['Parameter'].str.startswith('Ref')]
        del restrictor_dfr['Temp Zone']
        data_dict_rest = restrictor_dfr.set_index('Parameter').T.to_dict('list')
        restrictor_cols_list = ['R' + format(x, '02d') for x in range(100, 4401)]
        for key in restrictor_cols_list:
           if key not in data_dict_rest:
              data_dict_rest[key]=''
        data_df_rest = pd.DataFrame(data_dict_rest)

        frame_actual_df = pd.DataFrame()
        frame_actual_df = pd.concat([frame_actual_df, data_df_rest], axis=1)

        return frame_actual_df
        '''
        # Parse out Pressure data (PP2100-PP14040)
        restrictor_dfr = raw_df[raw_df['Parameter'].str.startswith('R')]
        data_dict_restrictor = restrictor_dfr.T.to_dict('list')
        data_df_rest = pd.DataFrame(data_dict_restrictor)
        data_df_rest = data_df_rest.T
        data_df_rest.columns = ['TZ', 'Restrictor', 'Value']
        data_df_rest['TZ'].fillna(method='ffill', inplace=True)

        frame_actual_df = pd.DataFrame()
        frame_actual_df = pd.concat([frame_actual_df, data_df_rest], axis=1)

        return frame_actual_df

    def getimportpath(self):
        """ Get the path to the repository in network drive from where the data will be imported

        :type self: DB1_STR_REST
        :param self: Calling Object of STR DATASET

        :raises:
        :return: Current import path
        :rtype: string
        """
        return self._restpath

    def setimportpath(self, path):
        """  Set the path to the import Repository

        :type self: DB1_STR_REST
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises:

        :rtype: None
        """
        if (os.path.exists(path)):
            self._restpath = path
        else:
            print("New Import path does not exists")

    @property
    def df(self):
        return self._dataframe

    def getexportpath(self):

        """ Get the export repository path
        :type self: DB1_STR_REST
        :param self: Calling Object of STR DATASET

        :raises:

        :return: Current export path
        :rtype: string
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


    def export2Excel(self, filename, export_path):
        """ Creates a backup of the calling LTR2 Datset using export path. Writes the new load path to a config file on network drive.

        :type self: DB1_STR_REST
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        filename = filename + ".xlsx" if not filename.endswith(".xlsx") else filename
        filepath = os.path.join(export_path, filename)
        print("Writing Restrictor Dataframe File:", filepath, "\t SHAPE ", self._dataframe.shape)
        self._dataframe.to_excel(filepath)

        logging.info('Export2Excel: {}, {}'.format(filename, export_path))

        return filepath

    def flattened_df(self, df):
        """ Creates a flattened dataframe by dropping existing indexes from multi-indexed dataframe

        :type self: DB1_STR_REST
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        flattened_df = df
        #level_one = flattened_df.columns.get_level_values(0)
        level_two = flattened_df.columns.get_level_values(1)
        flattened_df.columns = level_two
        flattened_df = flattened_df.reset_index()
        #print(flattened_df)

        return flattened_df

    def expandedDiff(self, testFile, refFile):
        """ Creates an expanded Difference File for Restrictor data by comparing cleaned data from Input files with Reference STR Dataset

        :type self: DB1_STR_REST
        :param self: Calling Object of STR DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        # define the expanded diff
        #df_actual_out_restrictor = pd.read_excel(testFile, sheetname='Sheet1', header=None)
        df_copy = self.df.copy()
        df_actual_out_restrictor = self.flattened_df(df_copy)

        df_expt_out_restrictor = pd.read_excel(refFile, sheetname='DB1 STR', parse_cols='A,B,NY:VW', header=None)       # using 'parse_cols' instead of 'usecols' because of older pandas version
        df_expt_out_restrictor = df_expt_out_restrictor.iloc[2:]
        df_expt_out_restrictor_new_header = df_expt_out_restrictor.iloc[0]
        df_expt_out_restrictor = df_expt_out_restrictor[1:]
        df_expt_out_restrictor.columns = df_expt_out_restrictor_new_header
        df_expt_out_restrictor.rename(columns={df_expt_out_restrictor.columns[1]: 'Test'}, inplace=True)

        '''
        df_expt_out_restrictor = pd.read_excel(refFile, sheetname='DB1 STR', parse_cols='A,B,NY:VW', header=None)      # using 'parse_cols' instead of 'usecols' because of older pandas version
        df_expt_out_restrictor = df_expt_out_restrictor.iloc[2:]
        df_actual_out_restrictor.columns = df_actual_out_restrictor.iloc[0]
        df_actual_out_restrictor = df_actual_out_restrictor.iloc[1:, :]
        df_expt_out_restrictor.columns = df_expt_out_restrictor.iloc[0]
        df_expt_out_restrictor = df_expt_out_restrictor.iloc[1:, :]
        df_expt_out_restrictor.rename(columns={df_expt_out_restrictor.columns[1]: 'Test'}, inplace=True)
        df_actual_out_restrictor = df_actual_out_restrictor.dropna(axis=1, how='all')
        df_expt_out_restrictor = df_expt_out_restrictor.dropna(axis=1, how='all')
        '''

        common_rows_restrictor_df = pd.merge(df_expt_out_restrictor, df_actual_out_restrictor, how='inner', on=['HoV', 'Test'])
        selected_col_x = [col for col in common_rows_restrictor_df.columns if col.endswith('_x')]
        common_rows_restrictor_df_actual_out = common_rows_restrictor_df[selected_col_x]
        selected_col_y = [col for col in common_rows_restrictor_df.columns if col.endswith('_y')]
        common_rows_restrictor_df_expt_out = common_rows_restrictor_df[selected_col_y]

        common_rows_restrictor_df_actual_out.columns = common_rows_restrictor_df_actual_out.columns.str.rstrip('_x')
        common_rows_restrictor_df_expt_out.columns = common_rows_restrictor_df_expt_out.columns.str.rstrip('_y')
        common_rows_restrictor_df_actual_out.replace('', '0;0;0;0', inplace=True)
        common_rows_restrictor_df_expt_out.replace('', '0;0;0;0', inplace=True)
        common_rows_restrictor_df_actual_out.replace(np.NaN, '0;0;0;0', inplace=True)
        common_rows_restrictor_df_expt_out.replace(np.NaN, '0;0;0;0', inplace=True)

        for col in (common_rows_restrictor_df_actual_out.columns):
            '''
            dia = common_rows_restrictor_df_actual_out[col].apply(str).str.split(';', expand=True)[0]
            fwd = common_rows_restrictor_df_actual_out[col].apply(str).str.split(';', expand=True)[1]
            mid = common_rows_restrictor_df_actual_out[col].apply(str).str.split(';', expand=True)[2]
            aft = common_rows_restrictor_df_actual_out[col].apply(str).str.split(';', expand=True)[3]
            '''
            dia_fwd_mid_aft = common_rows_restrictor_df_actual_out[col].apply(str).str.split(';', expand=True)
            common_rows_restrictor_df_actual_out[col + '_dia'] = dia_fwd_mid_aft[0]
            common_rows_restrictor_df_actual_out[col + '_fwd'] = dia_fwd_mid_aft[1]
            common_rows_restrictor_df_actual_out[col + '_mid'] = dia_fwd_mid_aft[2]
            common_rows_restrictor_df_actual_out[col + '_aft'] = dia_fwd_mid_aft[3]

        for col in (common_rows_restrictor_df_expt_out.columns):
            '''
            dia = common_rows_restrictor_df_expt_out[col].astype('str').split(';', expand=True)[0]
            fwd = common_rows_restrictor_df_expt_out[col].astype('str').split(';', expand=True)[1]
            mid = common_rows_restrictor_df_expt_out[col].astype('str').split(';', expand=True)[2]
            aft = common_rows_restrictor_df_expt_out[col].astype('str').split(';', expand=True)[3]
            '''
            dia_fwd_mid_aft = common_rows_restrictor_df_actual_out[col].apply(str).str.split(';', expand=True)
            common_rows_restrictor_df_expt_out[col + '_dia'] = dia_fwd_mid_aft[0]
            common_rows_restrictor_df_expt_out[col + '_fwd'] = dia_fwd_mid_aft[1]
            common_rows_restrictor_df_expt_out[col + '_mid'] = dia_fwd_mid_aft[2]
            common_rows_restrictor_df_expt_out[col + '_aft'] = dia_fwd_mid_aft[3]

        common_rows_restrictor_df_actual_out_expanded = common_rows_restrictor_df_actual_out.loc[:,common_rows_restrictor_df_actual_out.columns.str.contains('_dia|_fwd|_mid|_aft', na=False)]
        common_rows_restrictor_df_expt_out_expanded = common_rows_restrictor_df_expt_out.loc[:,common_rows_restrictor_df_expt_out.columns.str.contains('_dia|_fwd|_mid|_aft', na=False)]

        common_rows_restrictor_df_actual_out_expanded = common_rows_restrictor_df_actual_out_expanded.fillna(0)
        common_rows_restrictor_df_expt_out_expanded = common_rows_restrictor_df_expt_out_expanded.fillna(0)

        result_diff_restrictor_df_expanded = common_rows_restrictor_df_actual_out_expanded.astype(int) - common_rows_restrictor_df_expt_out_expanded.astype(int)

        appended_data = []
        for i in range(0, result_diff_restrictor_df_expanded.shape[1] - 1, 4):
            df_slice = result_diff_restrictor_df_expanded.iloc[:, i:i + 4]
            col_name = df_slice.columns[0].split('_')[0]
            df = df_slice.iloc[:, 0].astype(str) + ';' + df_slice.iloc[:, 1].astype(str) + ';' + df_slice.iloc[:, 2].astype(str) + ';' + df_slice.iloc[:, 3].astype(str)
            df = df.to_frame(col_name)
            appended_data.append(df)
        appended_data = pd.concat(appended_data, axis=1)
        result_diff_restrictor_df = appended_data

        add_HoV_col = common_rows_restrictor_df.iloc[:, 0].tolist()
        add_Test_col = common_rows_restrictor_df.iloc[:, 1].tolist()
        result_diff_restrictor_df.insert(0, column='HoV', value=add_HoV_col)
        result_diff_restrictor_df.insert(1, column='Test', value=add_Test_col)

        return result_diff_restrictor_df


    def printDiffReport(self, exp_diff_df, filepath):
        """ Creates a Report for expanded Difference File for Restrictor data

        :type self: DB1_STR_REST
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
        print("Writing Restrictor Diff File:", filepath, "\t SHAPE ", self._dataframe.shape)
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
    referenceFileName= "DB1_STR_REST.xlsm"
    reffile= os.path.join(rootdir, "tests\REF\DB1_STR",referenceFileName)

    logfilename="DB1_STR_REST.log"
    logfilepath= os.path.join(rootdir, "tests\RESULTS\DB1_STR",logfilename)
    logging.basicConfig(filename=logfilepath, format='Date-Time: %(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    STR1Rest = DB1_STR_REST()

    #Test 1
    STR1Rest.importAllFilesinFolders(folderpath)
    STR1Rest.headdf()
    testfile1=STR1Rest.export2Excel("test1DB1_REST.xlsx", export_folderpath)
    exp_diff1=STR1Rest.expandedDiff(testfile1,reffile)
    print("Expanded diff successfull")
    diff_filename1="DB1_STR_REST_DIFF_1.xlsx"
    diff_report_path= os.path.join(rootdir, "tests\RESULTS\DB1_STR",diff_filename1)
    STR1Rest.printDiffReport(exp_diff1, diff_report_path)

    #test 2:
    new_record_path = os.path.join(rootdir, "tests\\NEW\\DB1_STR\\CNK12-EXAMPLE.xlsm")
    STR1Rest.addNewRecord(new_record_path, "CNK12", "A350-900")
    STR1Rest.headdf()
    testfile2 = STR1Rest.export2Excel("test2DB1_REST.xlsx", export_folderpath)
    exp_diff2 = STR1Rest.expandedDiff(testfile2, reffile)
    print("Expanded diff successfull")
    diff_filename2="DB1_STR_REST_DIFF_2.xlsx"
    diff_report_path= os.path.join(rootdir, "tests\RESULTS\DB1_STR",diff_filename2)
    STR1Rest.printDiffReport(exp_diff2, diff_report_path)
