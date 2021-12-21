from model.interfaces import IData
import os
import pandas as pd
import re
import numpy as np


class DB4_GTR8_REST(IData):
    """
    class to instantiate the GTR8 DATASET.

    """

    def __init__(self):
        self._dataframe = pd.DataFrame()
        self._restpath = ''

    def _parse(self, path):
        """
        PARSE ONE FILE FROM A NETWORK LOCATION RETURN A DATAFRAME WITh one row correponding to one test reference.

        :type self: DB4_GTR8_REST
        :param self: Calling object of the GTR8 Dataset

        :type path: string
        :param path: Full path to the file on the specified network location

        :raises:

        :return: Dataframe with one line indexed by HoV
        :rtype: Pandas dataframe
        """
        header_df = pd.read_excel(path, sheetname="DB4 GTR8", parse_cols='B,G', header=None, skiprows=4)    # using 'parse_cols' instead of 'usecols' because of older pandas version
        header_df.columns = header_df.iloc[0]
        header_df = header_df[1:]
        rest_data_df = pd.DataFrame()
        restrictor_cols_list = ['R' + format(x, '02d') for x in range(100, 4401)]
        rest_data_df[restrictor_cols_list] = pd.DataFrame([[0] * len(restrictor_cols_list)], index=rest_data_df.index)
        self._dataframe = pd.concat([header_df, rest_data_df], axis=1)
        self._dataframe = self.__postprocess_df(self._dataframe)

        print("\n\n\n\n\n IMPORT DATA SUCCESSFULLY\n\n\n\n")

    def __postprocess_df(self, df):
        """ Does some postprocessing to remove nan values and -1001 values on the final output dataset.

        :type self: DB4_GTR8_REST
        :param self: Calling Object of GTR8 DATASET

        :type df: Pandas Dataframe
        :param df: Output datframe obtained after concatenating multiple single row dataframes.

        :raises:

        :return: Cleaned output dataframe without nan "n/a" or -1001 values indexed by HoV
        :rtype: Pandas dataframe
        """
        output_df = df
        output_df = output_df.fillna('0;0;0;0')
        #output_df = output_df.set_index("HoV")
        return output_df

    def headdf(self):
        """ Prints the head of dataframe of the calling object of DB4_GTR8_REST class.

        :type self: DB4_GTR8_REST
        :param self: Calling Object of GTR8 DATASET

        :raises:

        :rtype:
        """
        print(self._dataframe.head())

    def getexportpath(self):
        """ Get the export repository path
        :type self: DB4_GTR8_REST
        :param self: Calling Object of GTR8 DATASET

        :raises:

        :return: Current export path
        :rtype: string
        """
        return self.export_path

    def setexportpath(self, path):
        """ Set the export repository path
        :type self: DB4_GTR8_REST
        :param self: Calling Object of GTR8 DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises:

        :rtype: None
        """
        if (os.path.exists(path)):
            self.export_path = path
        else:
            print("New EXPORT path does not exists")

    @property
    def df(self):
        return self._dataframe

    def export2Excel(self, filename, export_path):
        """ Creates a backup of the calling LTR2 Datset using export path. Writes the new load path to a config file on network drive.

        :type self: DB4_GTR8_REST
        :param self: Calling Object of GTR8 DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        filename = filename + ".xlsx" if not filename.endswith(".xlsx") else filename
        filepath = os.path.join(export_path, filename)
        print("Writing Restrictor Dataframe File:", filepath, "\t SHAPE ", self._dataframe.shape)
        self._dataframe.to_excel(filepath)
        return filepath



if __name__ == "__main__":
    import os
    from pathlib import Path

    curdir = os.getcwd()
    print(curdir)
    p = Path(curdir).parent
    rootdir = p.parent
    print(rootdir)
    export_folderpath = os.path.join(rootdir, "tests\OUT\DB4_GTR8")
    print(export_folderpath)
    referenceFileName = "DB4_GTR8.xlsm"
    reffilepath = os.path.join(rootdir, "data", referenceFileName)

    GTR8REST = DB4_GTR8_REST()

    # Test 1
    GTR8REST._parse(reffilepath)
    GTR8REST.headdf()
    testfile = GTR8REST.export2Excel("test1DB4_REST.xlsx", export_folderpath)
