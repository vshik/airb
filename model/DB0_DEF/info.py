from model.interfaces import IData
from model.utils.global_info import ltr0_dates_df
import getpass
from datetime import datetime
import pandas as pd
import os
class DB0_DEF_INFO(IData):
    def __init__(self):
        self.df_info= pd.read_excel(r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\Adamant_Data\\DB0_DEF\\DB0_DEF_INFO.xlsx")
        # self.df_info= self.df_info.fillna("00:00:00")

    
    def _find_Hum(self,parent_repo,filename):
    
        """ Description
        
        :type self: DB0_DEF_INFO 
        :param self: Calling object of the LTR 0 Dataset
    
        :type parent_repo: string
        :param path: Path to the repository of the file in Network Drive
    
        :type filename: string
        :param filename: Exact filename with extension
    
        :raises:
    
        :return: Humidity Value
        :rtype: float
        """    #print ("Reading %s"%file)
        df=pd.read_excel(os.path.join(parent_repo, filename))
        print(filename)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        df.drop(df.columns[df.columns.str.contains('num',case = False)],axis = 1, inplace = True)
        columnName=["Frame", "Length", "LAOR", "Flag", "Vdef", "CAOR", "Flag.1", "Vdef.1","CAOR.1", "Flag.2", "Vdef.2","LAOR.1", "Flag.3", "Vdef.3","V_Zone"]
        df=df.iloc[:,0:15]
        df.set_axis(labels=columnName, axis=1)
        df= df[df["Frame"].notnull()]
        humidity= df.loc[df["LAOR.1"]=="HPA",'Vdef.3'].values[0]
        return humidity

    def addNewRecord(self, filepath, HoV=None, ACversion=None,test_date= None):
          
        """Function to add a New Record to DB0_DEF INFO 

        :type self: DB0_DEF_INFO
        :param self: Calling object of the DB0_DEF_INFO Class
    
        :type HoV: string
        :param HoV: HoV of the Aircraft
    
        :type test_date: Python Date
        :param test_date: Test Date
    
        :raises: None
    
        :rtype: None
        :return : None
        """    


        if (test_date== None):
            d= datetime(2001,1,1)
            #test_date= d.strftime("%Y-%m-%d %H:%M:%S")
            test_date= d        
            
        else:
            test_date_string= test_date + " 00:00:00"
            d= datetime.strptime(test_date_string,"%d/%m/%Y %H:%M:%S")
            # test_date= d.strftime("%Y-%m-%d %H:%M:%S")
            test_date= d        
            
        
        path_elements= os.path.split(filepath)
        parent_repo =path_elements[0]
        filename= path_elements[1]

        if(HoV==None):
            HoV= filename.replace(".xlsx","")

        humidity= self._find_Hum(parent_repo,filename)

        imported_by= getpass.getuser()
        import_date= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_dict= {"HoV":HoV,"Test Date":test_date,"Import Date":import_date,"Imported By":imported_by,"HUM":humidity}
        self.df_info= self.df_info.append(other=row_dict,ignore_index=True)

    def edit_record(self,HoV,test_date,import_date,imported_by,humidity= 28.3):
    
        """ Function to edit Record in DB0_DEF_INFO Dataset
        
        :type self: DB0_DEF_INFO
        :param self: Calling object of the DB0_DEF_INFO Class
        
        :type HoV: string
        :param HoV: HoV of the Aircraft

        :type test_date: Python Date
        :param test_date: Test Date
        
        :type import_date: Python Date
        :param import_date: New Import Date
    
        :type imported_by: string
        :param imported_by: User id of the editor
    
        :raises: KeyError
    
        :rtype: None
        """
        self.df_info= self.df_info.loc[self.df_info["HoV"]!= HoV,:]
        # imported_by= getpass.getuser()
        # import_date= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_dict= {"HoV":HoV,"Test Date":test_date,"Import Date":import_date,"Imported By":imported_by,"HUM":humidity}
        self.df_info= self.df_info.append(other=row_dict,ignore_index=True)

    def get_record(self,HoV):
    
        """ Get a Record corresponding to One HoV from the DB0_DEF_INFO class.
        
        :type self: DB0_DEF_INFO
        :param self: Calling object of the DB0_DEF_INFO Class
    
        :type HoV: string
        :param HoV: HoV of the Aircraft

        :raises: KeyError
    
        :rtype: None
        """
        if(self.if_exists(HoV)):
            return self.df_info.loc[self.df_info["HoV"]== HoV,:]
        else:
            raise KeyError("No Such Record Exists")         
        


    def if_exists(self,HoV):
    
        """CHeck if a particular HoV exists in the DB0_DEF_INFO class.
        
        :type self: DB0_DEF_INFO
        :param self: Calling object of the DB0_DEF_INFO Class
    
        :type HoV: string
        :param HoV: HoV of the Aircraft
    
        :raises: None
    
        :rtype: Boolean 
        :return: Boolean value representing whether HoV exists.
        """
        HoV_list= self.df_info["HoV"].values.tolist()
        if(HoV  in HoV_list):
            return True
        else:
            return False

if __name__=="__main__":
    usecas = DB0_DEF_INFO()
    print(usecas.df_info.head(50))
    print(usecas.get_record("SIA06"))
    curdir= os.getcwd()
    new_record_path= os.path.join(curdir,"tests\\NEW\DB0_DEF\VIR02.xlsx")
    usecas.addNewRecord(filepath=new_record_path,HoV="VIR02",test_date="12/09/2021")
    print(usecas.df_info.tail())
    
    
    #addNewRecord(filepath=new_record_path)
    # print(usecas.df_info.tail())


