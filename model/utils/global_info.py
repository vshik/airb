from model.utils.DB_HoV import DB_HoV
import pandas as pd 
import numpy as np


"""

SPECIFY THE FILE PATH WHICH CONTAINS GLOBAL INFORMATION

"""
global_file_path= r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\Adamant_Data\\global_info.xlsx"


"""
HoV_acv_df : Dataframe Containing information about HoV Versions, Is Batch2 , Is PREMAU, FCRC, CCRC
and other information like Airline Name , CSIRD and Colour)

"""
HoV_acv_df= pd.read_excel(global_file_path,"HoV_acv")


"""
ACv_frame_df: Dataframe with particular frame section definations, Restrictor Definitions and Pressure Port Definations for each Aircraft Version
(ACv).This dataframe does not have column indices. Column indices are numeric (from  0 to number _of_columns -1).
"""
ACv_frame_df= pd.read_excel(global_file_path,"acv_frame",header=[0,1,2])


"""
gtr8_msn_df : Dataframe which has Information like  MSN , HoV, Test date , Test Reference, loop etc for DB4_GTR8.

"""
gtr8_msn_df= pd.read_excel(global_file_path,"gtr8_msn")


"""
ltr2_dates_df: Dataframe Containing COULMNS: HoV, Test Reference, Notes ,Test date, Import date, and Imported By
from DB2 LTR. 

"""
ltr2_dates_df=  pd.read_excel(global_file_path,"ltr2_dates")



"""
str_dates_df: Dataframe  containing columns : HoV, Test Name, Notes, Test Date , Import Date , and Imported By from 
DB1 STR. 

"""
str_dates_df=  pd.read_excel(global_file_path,"str_dates")



"""
ltr0_dates_df: Dataframe containing columns: HoV , Test date , Import Date and Imported By from DBO DEF dataset.

"""
ltr0_dates_df= pd.read_excel(global_file_path,"ltr0_dates")



"""
gtr4_dates_df: Dataframe containing Columns MSN, HoV, Import Date, Imported by, Gtr Loop , Test date Columns from DB3_GTR4.

"""
gtr4_dates_df=  pd.read_excel(global_file_path,"gtr4_dates")

"""
historical_users_df: Dataframe holding the Userid, Username , UserGroup(henceforth called Access Level), Date of User Add,
"""
historical_users_df= pd.read_excel(global_file_path,"history_users")

"""
db_ac_df : Data Frame holding MSN AND delivery status values
"""
db_ac_df = pd.read_excel(global_file_path,"DB_AC")
if __name__=="__main__":
    print(HoV_acv_df.head())
    print(historical_users_df.head())
    print(ltr2_dates_df.head())
    print(ACv_frame_df.head())
