from model.interfaces import IData
import os
from pathlib import Path
import pandas as pd
import re
import numpy as np


class DB4_GTR8_FLOW(IData):
    """
    class to instantiate the GTR8 DATASET.
    """

    def __init__(self):
        self._dataframe = pd.DataFrame()
        self._flowpath = ''

        curdir = os.getcwd()
        print(curdir)
        rootdir = Path(curdir).parent
        #rootdir = p.parent
        referenceFileName = "DB4_GTR8.xlsm"
        reffilepath = os.path.join(rootdir, "data", referenceFileName)
        self._parse(reffilepath)


    def _parse(self, path):
        """
        PARSE REF FILE FROM A NETWORK LOCATION RETURN A DATAFRAME WITh one row correponding to one test reference.

        :type self: DB4_GTR8_FLOW
        :param self: Calling object of the GTR8 Dataset

        :type path: string
        :param path: Full path to the file on the specified network location

        :raises:

        :return: Dataframe with one line indexed by HoV
        :rtype: Pandas dataframe
        """
        # header (HoV, Test) columns
        header_df = pd.read_excel(path, sheetname="DB4 GTR8", parse_cols='B,G', header=None, skiprows=4)        # using 'parse_cols' instead of 'usecols' because of older pandas version
        header_df.columns = header_df.iloc[0]
        header_df = header_df[1:]

        # gtr data
        flow_df = pd.read_excel(path, sheetname="DB4 GTR8", parse_cols='I:HK', skiprows=2, header=[0,1,2])        # using 'parse_cols' instead of 'usecols' because of older pandas version     #Starting from column 'I', otherwise C17-18 will get dropped
        flow_df.columns = flow_df.columns.map('_'.join)

        # gtrdef data
        flow_gtrdef_df = pd.read_excel(path, sheetname="DB4 GTR8", parse_cols='J:HK', header=None)        # using 'parse_cols' instead of 'usecols' because of older pandas version
        flow_gtrdef_df = flow_gtrdef_df[:1]
        flow_gtrdef_df.columns = flow_df.columns

        # Below, we create multi-indexed dataframe for gtr data
        flow_df = flow_df.reset_index()
        flow_df.drop(flow_df.columns[[0]], axis=1, inplace=True)
        flow_df = flow_df.T.reset_index()
        flow_df.rename(columns={'index':'Frame'}, inplace=True)
        # Creating three columns for type, side ,frame using apply
        flow_df["type"] = flow_df["Frame"].apply(lambda x: x.split("_")[0])
        flow_df["side"] = flow_df["Frame"].apply(lambda x: x.split("_")[1])
        flow_df["Frame"] = flow_df["Frame"].apply(lambda x: x.split("_")[2] + "-" + x.split("_")[3] if len(x.split("_")) == 4 else x.split("_")[2])
        flow_df = flow_df.set_index(["type", "side", "Frame"])
        flow_df = flow_df.T

        # Below, we create multi-indexed dataframe for gtrdef data
        flow_gtrdef_df = flow_gtrdef_df.reset_index()
        flow_gtrdef_df.drop(flow_gtrdef_df.columns[[0]], axis=1, inplace=True)
        flow_gtrdef_df = flow_gtrdef_df.T.reset_index()
        flow_gtrdef_df.rename(columns={'index':'Frame'}, inplace=True)
        # Creating three columns for type, side ,frame using apply
        flow_gtrdef_df["type"] = flow_gtrdef_df["Frame"].apply(lambda x: x.split("_")[0])
        flow_gtrdef_df["side"] = flow_gtrdef_df["Frame"].apply(lambda x: x.split("_")[1])
        flow_gtrdef_df["Frame"] = flow_gtrdef_df["Frame"].apply(lambda x: x.split("_")[2] + "-" + x.split("_")[3] if len(x.split("_")) == 4 else x.split("_")[2])
        flow_gtrdef_df = flow_gtrdef_df.set_index(["type", "side", "Frame"])
        flow_gtrdef_df = flow_gtrdef_df.T

        # Add HoV and Test Reference cols to gtrdef data
        flow_gtrdef_df.insert(0, column='HoV', value='GTR Definition')
        flow_gtrdef_df.insert(1, column='Test Reference', value='Definition')

        # Add HoV and Test Reference cols to gtr data
        add_HoV_col = header_df.iloc[:, 0].tolist()
        add_Test_col = header_df.iloc[:, 1].tolist()
        flow_df.insert(0, column='HoV', value=add_HoV_col)
        flow_df.insert(1, column='Test Reference', value=add_Test_col)

        flow_df = pd.concat([flow_df, flow_gtrdef_df], axis=0)

        flow_df = self.__postprocess_df(flow_df)
        flow_df = flow_df.set_index(["HoV", "Test Reference"])

        self._dataframe = flow_df

        print("\n\n\n\n\n IMPORT DATA SUCCESSFULLY\n\n\n\n")


    def __postprocess_df(self, df):
        """ Does some postprocessing to remove nan values and -1001 values on the final output dataset.

        :type self: DB4_GTR8_FLOW
        :param self: Calling Object of GTR8 DATASET

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
        """ Prints the head of dataframe of the calling object of DB4_GTR8_FLOW class.

        :type self: DB4_GTR8_FLOW
        :param self: Calling Object of GTR8 DATASET

        :raises:

        :rtype:
        """
        print(self._dataframe.head())

    def getimportpath(self):
        """ Get the path to the repository in network drive from where the data will be imported

        :type self: DB4_GTR8_FLOW
        :param self: Calling Object of GTR8 DATASET

        :raises:
        :return: Current import path
        :rtype: string
        """
        return self._flowpath

    def setimportpath(self, path):
        """  Set the path to the import Repository

        :type self: DB4_GTR8_FLOW
        :param self: Calling Object of GTR8 DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises:

        :rtype: None
        """
        if (os.path.exists(path)):
            self._flowpath = path
        else:
            print("New Import path does not exists")

    @property
    def df(self):
        return self._dataframe

    def export2Excel(self, filename, export_path):
        """ Creates a backup of the calling GTR8 Datset using export path. Writes the new load path to a config file on network drive.

        :type self: DB4_GTR8_FLOW
        :param self: Calling Object of GTR8 DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises: None

        :rtype: None
        """
        filename = filename + ".xlsx" if not filename.endswith(".xlsx") else filename
        filepath = os.path.join(export_path, filename)
        print("Writing Flow Dataframe File:", filepath, "\t SHAPE ", self._dataframe.shape)
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

    GTR8FLOW = DB4_GTR8_FLOW()

    # Test 1
    GTR8FLOW._parse(reffilepath)
    GTR8FLOW.headdf()
    testfile = GTR8FLOW.export2Excel("test1DB4_FLOW.xlsx", export_folderpath)
