from model.interfaces import IData
import  pandas as pd
import numpy as np
import os

class DB6_CSIRD_VARIENT(IData):

    def __init__(self):
        self.__dataframe = pd.DataFrame()


    def _readExcel(self,filepath):
        """
        Parse specified sheet(s) into a DataFrame.

        :type self:DB6_CSIRD_VARIENT
        :param self: Calling object of the DB6_CSIRD_VARIENT class
        :param filepath: the folder in which all the files for this data resides
        :return: dataframe
        """
        df = pd.ExcelFile(filepath)
        return df

    def _readDF(self,filepath):
        """ Function to read excel file from input folder and convert it to dataframe.



        :type self: DB6_CSIRD_VARIENT
        :param self: Calling object of the DB6_CSIRD_VARIENT class

        :type path:string
        :param path: the folder in which all the files for this data resides
        :raises:None

        :return: dataframe
        :rtype: pandas dataframe
        """
        df = pd.read_excel(filepath,'Type_vs_HTZ', na_Filter=False)
        return df

    def _retriveFileName(self,val):
        """
        Function to retrive file name from string.
        :param val: string containing file name
        :return: file name
        """
        return val[-10:-5]

    def _getSectors(self,val):
        """
        Function to get the sector name from number of open holes.
        :param val: string containing number of open holes values
        :return: sector value
        """
        val = str(val).split('-')
        if len(val) == 1:
            return 1
        if len(val) == 2:
            v = val.count('0')
            return 2 - v
        if len(val) == 3:
            v = val.count('0')
            return 3 - v

    def _removeNan(self,val):
        """
        Function to remove nan values.
        :param val: string
        :return: str without nan
        """
        if ' nan' in val:
            a = val.split()
            return a[0]
        else:
            return val
    def _parse(self,filepath):
        """ Function to parse input excel file and return parsed dataframe.


        :type self:DB6_CSIRD_VARIENT
        :param self: Calling object of the DB6_CSIRD_VARIENT class

        :type filepath: string
        :param filepath: full file path

        :raises:None

        :rtype:pandas dataframe
        """
        df = pd.DataFrame()
        df = self._readExcel(filepath)
        noOfSheet = len(df.sheet_names)
        listOfSheets = df.sheet_names
        # print(noOfSheet,nameOfSheet)
        fileName = self._retriveFileName(filepath)
        # print(fileName)
        for i in listOfSheets:
            if fileName in i:
                sheetName = i

        df_ = pd.DataFrame()

        if 'Type_vs_HTZ' in listOfSheets:
            df_ = self._readDF(filepath)
            df_.columns = df_.iloc[2]
            df_.drop(df_.index[[1, 3]])
            df_ = df_.drop(df_.index[0:3])

            df_ = df_.drop(['Link to drawing', 'Remarks', 'HTZ+Variant'], axis=1)


            df_['Type'] = df_['Type'] + " " + df_['Nominal Duct Diameter'].map(str)
            df_[['FWD', 'MID', 'AFT']] = df_['Number of open holes'].map(str).str.split("-", expand=True)
            df_['Sectors'] = df_['Number of open holes'].apply(self._getSectors)
            self.__dataframe = df_[['Type', 'Sectors', 'hole Diameter', 'FWD', 'MID', 'AFT', 'HTZ', 'Variant']]
            self.__dataframe = self.__dataframe.rename(
                columns={'Type': 'Restrictor Type', 'HTZ': 'Reference(HTZ)', 'hole Diameter': 'Hole diameter [mm]'})
            self.__dataframe = self.__dataframe.drop_duplicates()
            self.__dataframe = self.__dataframe[self.__dataframe['Variant'] != 'not defined*']
            self.__dataframe['Restrictor Type'] = self.__dataframe['Restrictor Type'].apply(self._removeNan)




        else:
            df_ = pd.read_excel(filepath, sheetName, na_Filter=False)
            if 'HTZ' in df_.columns:
                if 'Riveted / Plug in / Small Duct' in df_.columns:
                    df_= df_.drop(['Riveted / Plug in / Small Duct'], axis=1)
                if 'Comment' in df_.columns:

                    df_ = df_.drop(['Restrictor-number', 'Restrictor Type and Position', 'Type', 'Comment', 'Maturity',
                                    'display in Custo documents'], axis=1)
                else:
                    df_ = df_.drop(['Restrictor-number', 'Restrictor Type and Position', 'Type'], axis=1)

                df_ = df_[df_.HTZ.notna()]
                df_ = df_[df_.HTZ != 'not defined*']
                df_ = df_[df_['Restrictor Type'].notna()]
                #                 df_['Duct Diameter [mm]'] = df_['Duct Diameter [mm]'].replace(np.nan , 0)
                if len(df_) != 0:
                    df_[['FWD', 'MID', 'AFT']] = df_['Number of open holes'].map(str).str.split("-", expand=True)
                    df_['Restrictor Type'] = df_['Restrictor Type'] + " " + df_['Duct Diameter [mm]'].map(str)
                    df_['Sectors'] = df_['Number of open holes'].apply(self._getSectors)
                    df_ = df_.drop(['Number of open holes', 'Duct Diameter [mm]', ], axis=1)
                    self.__dataframe = df_[
                    ['Restrictor Type', 'Sectors', 'Hole diameter [mm]', 'FWD', 'MID', 'AFT', 'HTZ', 'Variant']]
                    self.__dataframe = self.__dataframe.rename(columns={'Restrictor Type': 'Restrictor Type', 'HTZ': 'Reference(HTZ)'})
                    self.__dataframe = self.__dataframe.drop_duplicates()
                    self.__dataframe = self.__dataframe[self.__dataframe['Variant'] != 'not defined*']
                    self.__dataframe['Restrictor Type'] = self.__dataframe['Restrictor Type'].apply(self._removeNan)


        return  self.__dataframe





if __name__ == "__main__":
    import os
    from pathlib import Path
    curdir = os.getcwd()
    print(curdir)
    p = Path(curdir).parent
    rootdir = p.parent
    print(rootdir)
    export_folderpath = os.path.join(rootdir, "tests\OUT\DB6_CSIRD")
    print(export_folderpath)

    folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\Aditi\\Repository\\6-cSIRD_restrictorDef"
    # referenceFileName1 = "DB6_CSIRD_REF.xlsx"
    # reffile1 = os.path.join(rootdir, "tests\REF\DB6_CSIRD", referenceFileName1)
    # referenceFileName2 = "DB6_CSIRD_REF.xlsx"
    # reffile2 = os.path.join(rootdir, "tests\REF\DB6_CSIRD", referenceFileName2)

    DB6Varient = DB6_CSIRD_VARIENT()

    # test1

    DB6Varient.importAllFiles(folderpath)

    testfile1 = DB6Varient.export2Excel("DB6_CSIRD_VARIENT_OUT.xlsx", export_folderpath)



