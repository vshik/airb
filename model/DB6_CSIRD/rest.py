from model.interfaces import IData
import os
import pandas as pd
import numpy as np
import collections
from pathlib import Path


class DB6_CSIRD_REST(IData):
    """
        class to instantiate the DB6_CSIRD DATASET.

    """
    # def __init__(self):
    #     self.__dataframe = pd.DataFrame()

    def _floatToIntConversion(self, val):
        """ Function to convert float value to int value of the dataframe column.


        :type self: DB6_CSIRD_REST
        :param self: Calling object of the DB6_CSIRD_REST class

        :type val:int or float
        :param val:
        :raises:None

        :return: int value
        :rtype: int
        """

        if type(val) == float:
            return int(val)
        else:
            return val

    def _readDF(self,filepath):
        """ Function to read excel file from input folder and convert it to dataframe.



        :type self: DB6_CSIRD_REST_REST
        :param self: Calling object of the DB6_CSIRD_REST class

        :type path:string
        :param path: the folder in which all the files for this data resides
        :raises:None

        :return: dataframe
        :rtype: pandas dataframe
        """
        try:

            if 'D0006.xlsx' in filepath:
                df = pd.read_excel(filepath, "D0006")
            if 'QTR01.xlsx' in filepath:
                df = pd.read_excel(filepath, "MSN021_QTR01NC")
            return df
        except:
            df = pd.read_excel(filepath)
        return df

    # Added a default arguement for HoV in case the file name is not formatted well.
    def addNewRecord(self, filepath,HoV= None):

        """ Function to add the data of a new input file to the existing dataframe.


        :type self:DB6_CSIRD_REST
        :param self: Calling object of the DB6_CSIRD_REST class

        :type filepath: string
        :param filepath: the folder in which all the files for this data resides

        :raises:Exception

        :rtype:None
        """

        try:
            oneline_df = self._parse(filepath)
            self._dataframe = pd.concat([self._dataframe, oneline_df], axis=0,ignore_index=False)
            # self.__dataframe = self.__dataframe.set_index(self.__dataframe['HoV'])
            self._dataframe = self._dataframe.drop('HoV',axis=1)

            print("Imported: ", filepath)
        except Exception as e:
            print("Exception occurred for file: %s. Error:  %s " % (filepath, e))

    def _ignoreSmallName(self,name):
        """ Function to return nan if string length is more than 10 .


        :type self:DB6_CSIRD_REST
        :param self: Calling object of the DB6_CSIRD_REST class

        :type name: string
        :param name:column value

        :raises:None

        :rtype:string
        """
        if not isinstance(name, str):
            return name
        if len(name) <= 10:
            return np.NaN
        else:
            return name

    def _identifyZone(self,num):
        """ Function to identify the temperature zone of the restrictor.


        :type self:DB6_CSIRD_REST
        :param self: Calling object of the DB6_CSIRD_REST class

        :type num: int
        :param num: restrictor number

        :raises:None

        :rtype: string
        """
        if not isinstance(num, int):
            return "No TZ"
        if num < 100:
            return "No TZ"
        else:
            return "TZ" + str(num // 100)

    def _processHoleDiameter(self, val):
        """
        Funtion to process the hole diameter .

        :type self: DB6_CSIRD_REST
        :param self: Calling object of the Db6_CSIRD_REST class

        :type val:string
        :param val:column value

        :return: return integer value
        """
        try:
            val = int(val)
            return val
        except:
            return -1

    def _replaceDash(self,val):
        """
        Function to replace '-' with ';'

        :type self: DB6_CSIRD_REST
        :param self: Calling object of the BD6_CSIRD_REST class

        :type val: string
        :param val: column value

        :return: return modified string

        """
        return val.replace('-', ';')

    def _processNoOfOpenHoles(self,val):
        """ Function to add zero if any value is missing among FWD, MID, AFT in the number of open holes.
            Basically it tries to arrange value in this 'FWD-MID-AFT' format any if any value is missing replace it with 0.


        :type self:DB6_CSIRD_REST
        :param self: Calling object of the DB6_CSIRD_REST class

        :type val: string
        :param val:

        :raises:None

        :rtype: string
        """
        val = str(val)
        if len(val) > 11:
            val = '0-0-0'
            return val
        if val.count('-') == 1:
            return (val + '-0')
        if val.count('-') == 0:
            return val + '-0-0'
        if val.count('-') == 2:
            return val

    def _appendRestrictorWithR(self,val):
        """
        Function to add 'R' before restrictor.

        :type self: DB6_CSIRD_REST
        :param self: Calling

        :type val: integer
        :param val: restrictor value

        :return: restrictor value appended by R

        """
        val = 'R' + str(val)
        return val

    def _parse(self, filepath):
        """ Function to parse input excel file and return parsed dataframe.


        :type self:DB6_CSIRD_REST
        :param self: Calling object of the DB6_CSIRD_REST class

        :type filepath: string
        :param filepath: full file path

        :raises:None

        :rtype:pandas dataframe
        """

        df = self._readDF(filepath)
        df["Restrictor Long Type"] = df.iloc[:, 0]
        df["Restrictor Long Type"] = df["Restrictor Long Type"].apply(self._ignoreSmallName)
        df["Restrictor Long Type"] = df["Restrictor Long Type"].ffill()
        df = df[df['Restrictor-number'].notnull()]
        df['Restrictor-number'] = df['Restrictor-number'].apply(self._floatToIntConversion)
        df['Restrictor-number'] = df['Restrictor-number'].apply(self._appendRestrictorWithR)

        df['Restrictor Type and Position'] = df['Restrictor Type and Position'].ffill()

        df['Restrictor-Zone'] = df['Restrictor-number'].apply(self._identifyZone)

        df['Hole diameter [mm]'] = df['Hole diameter [mm]'].apply(self._processHoleDiameter)

        df.iloc[:, 6] = df.iloc[:, 6].replace(np.nan, '0')

        df.iloc[:, 6] = df.iloc[:, 6].apply(self._processNoOfOpenHoles)

        df.iloc[:, 6] = df.iloc[:, 6].apply(self._replaceDash)
        for i in range(len(df)):
            df.iloc[i, 6] = str(df.iloc[i, 5]) + ';' + df.iloc[i, 6]

        df1 = pd.DataFrame(columns=['HoV', 'File'])

        df1 = df[['Restrictor-number', 'Number of open holes']]

        df1 = df1.T
        df1.columns = df1.iloc[0]
        df1 = df1.drop(['Restrictor-number'])

        df1['HoV'] = filepath
        # df1 = df1.set_index(df1['HoV'])
        df1 = df1.loc[:, ~df1.columns.duplicated()]
        df1 = df1.replace(np.nan, '0;0;0;0')
        df1['HoV'] = df1['HoV'].apply(self._retriveHoVname)
        df1.HoV = df1.HoV.apply(self._removeFileExtension)
        df1 = df1.set_index(df1.HoV)
        # if 'HoV' in df1.columns:
        #     df1 = df1.drop(['HoV'], axis=1)
        if  "R--"  in df1.columns:
            df1 = df1.drop(["R--"], axis=1)
        if "R-" in df1.columns:
            df1 = df1.drop(["R-"], axis=1)

        return df1


    def _retriveHoVname(self,val):
        """

        Function to retrivev HoV name from string

        :type self: DB6_CSIRD_REST
        :param self: Calling object of the DB6_CSIRD REST class

        :type val:str
        :param val: full file path

        :return: HoV name
        """
        return val[-10:-1]

    def export2Excel(self, filename, export_path):

        """ Function to convert pandas dataframe to excel file.

        :type self:DB0_DEF_FLOW
        :param self: Calling Object of LTR0 DATASET

        :type filename: string
        :param filename: Exact filename with extension


        :raises: None

        :rtype: filepath
        """
        filename = filename + ".xlsx" if not filename.endswith(".xlsx") else filename
        filepath = os.path.join(export_path, filename)
        # self.__dataframe = self.__dataframe.replace(np.nan, '0;0;0;0')
        # self.__dataframe['HoV'] = self.__dataframe['HoV'].apply(self._retriveHoVname)
        # self.__dataframe = self.__dataframe.set_index(self.__dataframe['HoV'])
        # self.__dataframe = self.__dataframe.drop(['HoV', "R--", "R-"], axis=1)

        print("Writing File:", filepath, "\t SHAPE ", self._dataframe.shape)
        self._dataframe.to_excel(filepath)
        return filepath


    def _removeFileExtension(self,val):
        """
        Function to remove file extension

        :type self:DB0_DEF_FLOW
        :param self: Calling Object of LTR0 DATASET

        :type val: str
        :param val: string of file name with extension
        :return: string
        """
        a = val.index('.')
        return val[0:a]

    def _validate(self,val):
        """
            Function to validate the value.

        :type self:DB0_DEF_FLOW
        :param self: Calling Object of LTR0 DATASET

        :param val:column value
        :return:
        """
        restrictor_def = str(val).split(';')
        if len(restrictor_def) != 4:
            return '0;0;0;0'
        for i, integer_value in enumerate(restrictor_def):
            try:
                int(integer_value)
            except ValueError:
                restrictor_def[i] = '0'

        return ';'.join(restrictor_def)

    def printDiffReport(self,exp_diff_df, filepath):
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
    curdir= os.getcwd()
    print(curdir)
    p = Path(curdir).parent
    rootdir = p.parent
    print(rootdir)
    export_folderpath = os.path.join(rootdir, "tests\OUT\DB6_CSIRD")
    print(export_folderpath)


    folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\Aditi\\Repository\\6-cSIRD_restrictorDef"
    referenceFileName1= "DB6_CSIRD_REF.xlsx"
    reffile1= os.path.join(rootdir, "tests\REF\DB6_CSIRD",referenceFileName1)
    referenceFileName2 = "DB6_CSIRD_REF.xlsx"
    reffile2 = os.path.join(rootdir, "tests\REF\DB6_CSIRD", referenceFileName2)


    DB6_Rest = DB6_CSIRD_REST()

     # test1

    DB6_Rest.importAllFiles(folderpath)


    testfile1=DB6_Rest.export2Excel("test1_DB6_CSIRD_REST_OUT.xlsx", export_folderpath)

    exp_diff1=DB6_Rest.expandedDiffRestrictors(testfile1,reffile1)

    diff_filename="test1_DB6_CSIRD_REST_DIFF.xlsx"
    diff_report_path= os.path.join(rootdir, "tests\RESULTS\DB6_CSIRD",diff_filename)
    DB6_Rest.printDiffReport(exp_diff1, diff_report_path)

    # test2

    # new_record_path = r"X:\Aditi\Work_Done\ADAMANT_GitHub\tests\NEW\DB6_CSIRD\ABC01.xlsx"
    new_record_path = r"X:\Aditi\Work_Done\ADAMANT_GitHub\tests\NEW\DB6_CSIRD\CPA01.xlsx"
    DB6_Rest.addNewRecord(filepath=new_record_path)
    testfile2 = DB6_Rest.export2Excel("test2_DB6_CSIRD_REST_OUT.xlsx", export_folderpath)
    exp_diff2 = DB6_Rest.expandedDiffRestrictors(testfile2, reffile2)
    diff_filename2="test2_DB6_CSIRD_REST_DIFF.xlsx"
    diff_report_path= os.path.join(rootdir, "tests\RESULTS\DB6_CSIRD",diff_filename2)
    DB6_Rest.printDiffReport(exp_diff2, filepath=diff_report_path)


