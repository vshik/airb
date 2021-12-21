from model.interfaces import IData
import os
import pandas as pd
import re
import numpy as np


class DB3_GTR4_PP(IData):
    """
    class to instantiate the GTR4 DATASET.
    """

    def __init__(self):
        self._dataframe = pd.DataFrame()
        self._pppath = ''

    def _parse(self, path):
        """
        PARSE REF FILE FROM A NETWORK LOCATION RETURN A DATAFRAME WITh one row correponding to one test reference.

        :type self: DB3_GTR4_PP
        :param self: Calling object of the GTR4 Dataset

        :type path: string
        :param path: Full path to the file on the specified network location

        :raises:

        :return: Dataframe with one line indexed by HoV
        :rtype: Pandas dataframe
        """
        # header (HoV, Test) columns
        header_df = pd.read_excel(path, sheetname="DB3 GTR4", parse_cols='B,G', header=None, skiprows=3)        # using 'parse_cols' instead of 'usecols' because of older pandas version
        header_df.columns = header_df.iloc[0]
        header_df = header_df[1:]

        # gtr data columns
        raw_df = pd.read_excel(path, sheetname="DB3 GTR4", parse_cols='JC:PA', header=None, skiprows=2)     # using 'parse_cols' instead of 'usecols' because of older pandas version)
        raw_df = raw_df.T
        raw_df.rename(columns={raw_df.columns[0]:'TZ', raw_df.columns[1]:'PP'}, inplace=True)
        raw_df['PP'] = 'PP' + raw_df['PP'].astype(str)

        # below are the steps for multi-indexing
        raw_df = raw_df.set_index(["TZ", "PP"])
        raw_df = raw_df.T

        # Add HoV and Test Reference cols to gtr data
        add_HoV_col = header_df.iloc[:, 0].tolist()
        add_Test_col = header_df.iloc[:, 1].tolist()
        raw_df.insert(0, column='HoV', value=add_HoV_col)
        raw_df.insert(1, column='Test Reference', value=add_Test_col)

        raw_df = self.__postprocess_df(raw_df)

        self._dataframe = raw_df
        print("\n\n\n\n\n IMPORT DATA SUCCESSFULLY\n\n\n\n")

    def __postprocess_df(self, df):

        """ Does some postprocessing to remove nan values and -1001 values on the final output dataset.

        :type self: DB3_GTR4_PP
        :param self: Calling Object of GTR4 DATASET

        :type df: Pandas Dataframe
        :param df: Output datframe obtained after concatenating multiple single row dataframes.

        :raises:

        :return: Cleaned output dataframe without nan "n/a" or -1001 values indexed by HoV
        :rtype: Pandas dataframe
        """
        output_df = df
        output_df = output_df.fillna(0)
        output_df = output_df.replace(["nan", "n/a", "#N/A", "-1001.0", "-1001.00", "-1001.000"], 0)
        output_df = output_df.replace([-1001.0], 0)
        output_df = output_df.dropna(axis=1, how='all')
        output_df = output_df.fillna(0)
        #output_df = output_df.set_index("HoV")
        return output_df

    def headdf(self):
        """ Prints the head of dataframe of the calling object of DB3_GTR4_PP class.

        :type self: DB3_GTR4_PP
        :param self: Calling Object of GTR4 DATASET

        :raises:

        :rtype:
        """
        print(self._dataframe.head())

    def getexportpath(self):
        """ Get the export repository path
        :type self: DB3_GTR4_PP
        :param self: Calling Object of GTR4 DATASET

        :raises:

        :return: Current export path
        :rtype: string
        """
        return self.export_path

    def setexportpath(self, path):
        """ Set the export repository path
        :type self: DB3_GTR4_PP
        :param self: Calling Object of GTR4 DATASET

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
        """ Creates a backup of the calling GTR8 Datset using export path. Writes the new load path to a config file on network drive.

        :type self: DB3_GTR4_PP
        :param self: Calling Object of GTR4 DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        filename = filename + ".xlsx" if not filename.endswith(".xlsx") else filename
        filepath = os.path.join(export_path, filename)
        print("Writing Pressure Dataframe File:", filepath, "\t SHAPE ", self._dataframe.shape)
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
    export_folderpath = os.path.join(rootdir, "tests\OUT\DB3_GTR4")
    print(export_folderpath)
    referenceFileName = "DB3_GTR4.xlsm"
    reffilepath = os.path.join(rootdir, "data", referenceFileName)

    GTR4PP = DB3_GTR4_PP()

    # Test 1
    GTR4PP._parse(reffilepath)
    GTR4PP.headdf()
    testfile = GTR4PP.export2Excel("test1DB3_PP.xlsx", export_folderpath)
