from model.interfaces import IData
from model.utils.global_info import ltr2_dates_df
import getpass
from datetime import datetime
from datetime import date
import pandas as pd
import re

class DB2_LTR_INFO(IData):
    def __init__(self):
        self.df_info= pd.read_excel(r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\Adamant_Data\\DB2_LTR\\DB2_LTR_INFO.xlsx")
        #self.df_info= self.df_info.fillna("00:00:00")
    
    def _read_df(self, path):
    
        """ Read the dataframe from an input file as is and return a raw input dataframe.
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
        
        :type path: string
        :param path: Path to the input file corresponding to a Test Reference

    
        :raises: FileNotFoundError
        
        :return: Raw Dataframe of the same shape as the input data read as it is from the file.
        :rtype: Pandas Dataframe
        """    
        raw_df = pd.read_excel(path,sheetname="Flow",header= None,skiprows=3)
        return raw_df
    
    def _getHPAvalue(self,raw_df):
    
        """ Get the HPA value from the raw file dataframe
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
    
        :type raw_df: Pandas dataframe
        :param raw_df: Raw Dataframe which results from reading the file as it is.
    
        :raises:
    
        :return: HPA value
        :rtype: float
        """    
        hpa_value =0
        try:
            first_column = raw_df.iloc[:,0]
            hpa_index= first_column[first_column=="HPA"].index[0]
            hpa_value = raw_df.iloc[hpa_index,1]
        except:
            pass
        finally:
            return hpa_value

    def _getMixP(self,test_reference):
        experiment_type_string= test_reference

        # When type reference is FINAL
        if(experiment_type_string.upper() == str("FINAL").upper()):
            mixp= 26
        
        #When type reference is simval
        elif(experiment_type_string.upper() == str("SIMVAL").upper()):
            mixp= 26
        
        # When type reference is NOT Final
        elif(experiment_type_string.upper() != str("FINAL").upper()):
            temp= re.findall(r'\d+',experiment_type_string)
            list_of_mixes= list(map(int,temp))
            print(list_of_mixes)
            mixp= list_of_mixes[0]
                 
        
        # for all other cases
        else:
            mixp= 26
        
        return mixp
        
    def addNewRecord(self, filepath, HoV=None, ACversion=None,test_reference= None,test_date= None,Notes= None):
        """Function to add a New Record to DB2_LTR_INFO 

        :type self: DB2_LTR_INFO
        :param self: Calling object of the DB2_LTR_INFO Class
    
        :type HoV: string
        :param HoV: HoV of the Aircraft
    
        :type test_reference: string
        :param test_reference: Test Reference for the new record in DB2_LTR_INFO
    
        :type test_date: Python Date
        :param test_date: Test Date
    
        :type Notes: string
        :param Notes: Test Notes
    
        :raises: None
    
        :rtype: None
        """

    
        if (test_date== None):
            d= datetime(2001,1,1)
            #test_date= d.strftime("%d/%m/%Y %H:%M:%S")
            test_date= d            
        else:
            test_date_string= test_date + " 00:00:00"
            d= datetime.strptime(test_date_string,"%d/%m/%Y %H:%M:%S")
            #test_date= d.strftime("%Y-%m-%d %H:%M:%S")
            test_date= d        
        # else:
        #     test_date= datetime.strptime(test_date,"%d/%m/%Y")
        #     test_date= test_date.strftime("%d/%m/%Y")

        if(test_reference== None):
            test_reference= "FINAL"

        raw_df= self._read_df(filepath)
        hpa_value= self._getHPAvalue(raw_df)
        
        mixp= self._getMixP(test_reference)
        
        imported_by= getpass.getuser()
        import_date= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_dict= {"HoV":HoV,"Test Reference":test_reference,"Notes":"","Test Date":test_date,"Import Date":import_date,"Imported By":imported_by,"mixP":mixp,"HPA":hpa_value}
        self.df_info= self.df_info.append(other=row_dict,ignore_index=True)

    def edit_record(self,HoV,test_reference,test_date,import_date,imported_by,mixp=None,hpa_value= None):
    
        """  Function to edit Record in DB2_LTR_INFO Dataset

        :type self: DB2_LTR_INFO
        :param self: Calling object of the DB2_LTR_INFO Class
    
        :type HoV: string
        :param HoV: HoV of the Aircraft
    
        :type test_reference: string
        :param test_reference: Test Reference for the new record in DB2_LTR_INFO
    
        :type test_date: Python Date
        :param test_date: Test Date
    
        :type import_date: string
        :param import_date: Date of Import of input file.
    
        :type imported_by: string
        :param imported_by: AIRBUS userID OR NG ID of the new importing user.  
    
        :raises: None
    
        :rtype: None
        """
        self.df_info= self.df_info.loc[self.df_info["HoV"]!= HoV,:]
        row_dict= {"HoV":HoV,"Test Reference":test_reference,"Notes":"","Test Date":test_date,"Import Date":import_date,"Imported By":imported_by,"mixP":mixp,"HPA":hpa_value}
        self.df_info= self.df_info.append(other=row_dict,ignore_index=True)

    def get_record(self,HoV, test_reference= None):
        """ 
        Get a Record corresponding to One HoV from the DB2_LTR_INFO class.
        
        :type self: DB2_LTR_INFO
        :param self: Calling object of the DB2_LTR_INFO Class

        :type HoV: string
        :param HoV: HoV of the Aircraft

    
        :type test_reference: string
        :param test_reference: Test Reference for the record in DB2_LTR_INFO / LTR 2 Test Reference
    
    
        :raises: KeyError
    
        :rtype: None
           
        
        """    
        if(self.if_exists(HoV,test_reference)):
            
            return self.df_info.loc[(self.df_info["HoV"]== HoV) & (self.df_info["Test Reference"]== test_reference) ,:]

        else:
            raise KeyError("No such Record Exists")     

    def if_exists(self,HoV, test_reference):
    
        """CHeck if a particular HoV exists in the DB0_DEF_INFO class.
        
        :type self: DB2_LTR_INFO
        :param self: Calling object of the DB2_LTR_INFO Class

    
        :type HoV: string
        :param HoV: HoV of the Aircraft

        :type test_reference: string
        :param test_reference: Test Reference for the record in DB2_LTR_INFO / LTR 2 Test Reference
    
        :raises: None
    
        :rtype: Boolean 
        :return: Boolean value representing whether HoV exists.
        """
        HoV_list= self.df_info["HoV"].values.tolist()
        test_reference_list= self.df_info["Test Reference"].values.tolist()
        if(HoV  in HoV_list and test_reference in test_reference_list):
            return True
        else:
            return False

if __name__=="__main__":
    usecas = DB2_LTR_INFO()
    print(usecas.df_info.head(10))
    print(usecas.df_info.info())
    print(usecas.get_record(HoV="AFR02",test_reference="FINAL"))
    import os
    curdir= os.getcwd()
    new_record_path= os.path.join(curdir,"tests\\NEW\DB2_LTR\D0008-MIX22.xlsm")
    usecas.addNewRecord(filepath=new_record_path,HoV= "D0008",test_reference="MIX29",test_date="12/09/2001")
    print(usecas.df_info.tail())
    print(usecas.df_info.info())
