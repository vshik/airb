from model.interfaces import IData
from model.utils.global_info import str_dates_df
import getpass
from datetime import datetime
from datetime import date
import pandas as pd
import re


class DB1_STR_INFO(IData):
    def __init__(self):
        self.df_info = pd.read_excel(r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\Adamant_Data\\DB1_STR\\DB1_STR_INFO.xlsx")
        # self.df_info= self.df_info.fillna("00:00:00")

    def _read_df(self, path):
        """ Read the dataframe from an input file as is and return a raw input dataframe.

        :type self:DB1_STR_FLOW
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

    def _getHPAvalue(self, raw_df):
        """ Get the HPA value from the raw file dataframe

        :type self:DB1_STR_FLOW
        :param self: Calling Object of STR DATASET

        :type raw_df: Pandas dataframe
        :param raw_df: Raw Dataframe which results from reading the file as it is.

        :raises:

        :return: HPA value
        :rtype: float
        """
        hpa_value = 0
        try:
            hpa_row = raw_df.loc[raw_df['Parameter'].str.startswith('Reference hPa')]
            hpa_value = hpa_row['Input'].iloc[0]
        except:
            pass
        finally:
            return hpa_value


    def addNewRecord(self, filepath, HoV=None, ACversion=None, test_name=None, test_date=None, Notes=None):
        """Function to add a New Record to DB1_STR_INFO

        :type self: DB1_STR_INFO
        :param self: Calling object of the DB1_STR_INFO Class

        :type HoV: string
        :param HoV: HoV of the Aircraft

        :type test_reference: string
        :param test_reference: Test Reference for the new record in DB1_STR_INFO

        :type test_date: Python Date
        :param test_date: Test Date

        :type Notes: string
        :param Notes: Test Notes

        :raises: None

        :rtype: None
        """

        if (test_date == None):
            d = datetime(2001, 1, 1)
            # test_date= d.strftime("%d/%m/%Y %H:%M:%S")
            test_date = d
        else:
            test_date_string = test_date + " 00:00:00"
            d = datetime.strptime(test_date_string, "%d/%m/%Y %H:%M:%S")
            # test_date= d.strftime("%Y-%m-%d %H:%M:%S")
            test_date = d
            # else:
        #     test_date= datetime.strptime(test_date,"%d/%m/%Y")
        #     test_date= test_date.strftime("%d/%m/%Y")

        if (test_name == None):
            test_name = "FINAL"

        raw_df = self._read_df(filepath)
        hpa_value = self._getHPAvalue(raw_df)

        imported_by = getpass.getuser()
        import_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_dict = {"HoV": HoV, "Test Name": test_name, "Notes": "", "Test Date": test_date, "Import Date": import_date, "Imported By": imported_by, "HPA": hpa_value}
        self.df_info = self.df_info.append(other=row_dict, ignore_index=True)


    def edit_record(self, HoV, test_name, test_date, import_date, imported_by, hpa_value=None):
        """  Function to edit Record in DB1_STR_INFO Dataset

        :type self: DB1_STR_INFO
        :param self: Calling object of the DB1_STR_INFO Class

        :type HoV: string
        :param HoV: HoV of the Aircraft

        :type test_reference: string
        :param test_reference: Test Reference for the new record in DB1_STR_INFO

        :type test_date: Python Date
        :param test_date: Test Date

        :type import_date: string
        :param import_date: Date of Import of input file.

        :type imported_by: string
        :param imported_by: AIRBUS userID OR NG ID of the new importing user.

        :raises: None

        :rtype: None
        """
        self.df_info = self.df_info.loc[self.df_info["HoV"] != HoV, :]
        row_dict = {"HoV": HoV, "Test Name": test_name, "Notes": "", "Test Date": test_date,
                    "Import Date": import_date, "Imported By": imported_by, "HPA": hpa_value}
        self.df_info = self.df_info.append(other=row_dict, ignore_index=True)

    def get_record(self, HoV, test_name=None):
        """
        Get a Record corresponding to One HoV from the DB1_STR_INFO class.

        :type self: DB1_STR_INFO
        :param self: Calling object of the DB1_STR_INFO Class

        :type HoV: string
        :param HoV: HoV of the Aircraft

        :type test_reference: string
        :param test_reference: Test Reference for the record in DB1_STR_INFO / STR Test Reference

        :raises: KeyError

        :rtype: None


        """
        if (self.if_exists(HoV, test_name)):

            return self.df_info.loc[(self.df_info["HoV"] == HoV) & (self.df_info["Test Name"] == test_name), :]

        else:
            raise KeyError("No such Record Exists")

    def if_exists(self, HoV, test_name):
        """CHeck if a particular HoV exists in the DB0_DEF_INFO class.

        :type self: DB1_STR_INFO
        :param self: Calling object of the DB1_STR_INFO Class

        :type HoV: string
        :param HoV: HoV of the Aircraft

        :type test_reference: string
        :param test_reference: Test Reference for the record in DB1_STR_INFO / STR Test Reference

        :raises: None

        :rtype: Boolean
        :return: Boolean value representing whether HoV exists.
        """
        HoV_list = self.df_info["HoV"].values.tolist()
        test_name_list = self.df_info["Test Name"].values.tolist()
        if (HoV in HoV_list and test_name in test_name_list):
            return True
        else:
            return False


if __name__ == "__main__":
    usecas = DB1_STR_INFO()
    print(usecas.df_info.head(10))
    print(usecas.df_info.info())
    print(usecas.get_record(HoV="MAS01", test_name="CFD"))

    import os
    from pathlib import Path
    curdir= os.getcwd()
    print(curdir)
    p = Path(curdir).parent
    rootdir = p.parent

    new_record_path = os.path.join(rootdir, "tests\\NEW\DB1_STR\CNK12-EXAMPLE.xlsm")
    usecas.addNewRecord(filepath=new_record_path, HoV="CES01", test_name="EXAMPLE", test_date="12/09/2001")
    print(usecas.df_info.tail())
    print(usecas.df_info.info())
