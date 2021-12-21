from model.interfaces import IData
from model.utils.global_info import gtr4_dates_df
import getpass
from datetime import datetime
from datetime import date
import pandas as pd
import re


class DB3_GTR4_INFO(IData):
    def __init__(self):
        self.df_info = pd.read_excel(r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\Adamant_Data\\DB3_GTR4\\DB3_GTR4_INFO.xlsx")
        # self.df_info= self.df_info.fillna("00:00:00")

    def add_record(self, MSN=None, HoV=None, test_reference="N/A", notes="N/A", test_date=None, hpa_value=None, gtr_ref=0):
        """ Adds a new HoV record as per specified information.

        :type self: DB3_GTR4_INFO
        :param self: Calling Object of GTR4 DATASET

        :raises:

        :rtype:
        """
        if (test_date == None):
            test_date = "2021-01-01 00:00:00"
        imported_by = getpass.getuser()
        import_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_dict = {"MSN": MSN, "HoV": HoV, "Test Reference": test_reference, "Notes": notes, "Test Date": test_date, "Import Date": import_date, "Imported By": imported_by, "hPa": hpa_value, "GTR Reference": gtr_ref}
        self.df_info = self.df_info.append(other=row_dict, ignore_index=True)


    def edit_record(self, MSN, HoV, test_reference, test_date, import_date, imported_by, hpa_value=None):
        """  Function to edit Record in DB3_GTR4_INFO Dataset

        :type self: DB3_GTR4_INFO
        :param self: Calling object of the DB3_GTR4_INFO Class

        :type HoV: string
        :param HoV: HoV of the Aircraft

        :type test_reference: string
        :param test_reference: Test Reference for the new record in DB3_GTR4_INFO

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
        row_dict = {"MSN": MSN, "HoV": HoV, "Test Reference": test_reference, "Notes": "", "Test Date": test_date,
                    "Import Date": import_date, "Imported By": imported_by, "HPA": hpa_value}
        self.df_info = self.df_info.append(other=row_dict, ignore_index=True)

    def get_record(self, HoV, test_reference=None):
        """
        Get a Record corresponding to One HoV from the DB3_GTR4_INFO class.

        :type self: DB3_GTR4_INFO
        :param self: Calling object of the DB3_GTR4_INFO Class

        :type HoV: string
        :param HoV: HoV of the Aircraft


        :type test_reference: string
        :param test_reference: Test Reference for the record in DB3_GTR4_INFO / GTR4 Test Reference


        :raises: KeyError

        :rtype: None
        """
        if (self.if_exists(HoV, test_reference)):

            return self.df_info.loc[(self.df_info["HoV"] == HoV) & (self.df_info["Test Reference"] == test_reference), :]
        else:
            raise KeyError("No such Record Exists")


    def if_exists(self, HoV, test_reference):
        """CHeck if a particular HoV exists in the DB0_DEF_INFO class.

        :type self: DB3_GTR4_INFO
        :param self: Calling object of the DB3_GTR4_INFO Class


        :type HoV: string
        :param HoV: HoV of the Aircraft

        :type test_reference: string
        :param test_reference: Test Reference for the record in DB3_GTR4_INFO / GTR4 Test Reference

        :raises: None

        :rtype: Boolean
        :return: Boolean value representing whether HoV exists.
        """
        HoV_list = self.df_info["HoV"].values.tolist()
        test_reference_list = self.df_info["Test Reference"].values.tolist()
        if (HoV in HoV_list and test_reference in test_reference_list):
            return True
        else:
            return False


if __name__ == "__main__":
    usecas = DB3_GTR4_INFO()
    print(usecas.df_info.head(10))
    print(usecas.df_info.info())
    print(usecas.get_record(HoV="D0008", test_reference="MSN65_26hPa_conf_1.0_v001_Complete_wPPs"))
    usecas.add_record(MSN="65", HoV="CRK01", test_reference="SAMPLE", notes="00:00:00", test_date="2021-05-31 10:00:00")
    print(usecas.df_info.tail())
    usecas.edit_record(MSN="60", HoV="CRK01", test_reference="Trial", test_date="2021-06-31 11:11:11", import_date="2021-05-31 10:59:59", imported_by="SP00260C")
    print(usecas.df_info)
