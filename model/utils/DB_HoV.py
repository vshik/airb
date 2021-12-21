import pandas as pd

import pandas as pd
from datetime import datetime
import sqlalchemy as db
import os

class DB_HoV:
    def __init__(self,folderpath= None):
        self.db_hov = pd.DataFrame()
        self.conn= self._getlatestsql(folderpath)
        self.load_dataset(self.conn)        

    def load_dataset(self, connection):
        try:
            df_table= pd.read_sql_table(table_name= "DB_HoV",con= connection)
            # df_table= pd.read_sql_table(table_name="Flowdef",con= connection, index_col= ('type','side','Frame'))
            # df_table= df_table.set_index(["type","side","Frame"])        
            df_table= df_table.T
            print(df_table.head())
            columns_list= df_table.iloc[0].values.tolist()
            df_table= df_table.iloc[1:,:]
            df_table.columns= columns_list 
            self.db_hov= df_table
        except Exception as e:
            print("Error:",e)

    def export_dataset(self, connection):
        self.db_hov.T.to_sql("DB_HoV",con=connection,if_exists="replace")

    
    def _getlatestsql(self, folderpath = None):
        
        if(folderpath == None):
            folderpath = "\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup"
        def find_timestamp(filename):
            timestring = filename.replace("ADAMANT_","").replace(".db","")
            timestamp= datetime.strptime(timestring,"%Y_%m_%d_%H_%M_%S")
            return timestamp
        
        filelist= os.listdir(folderpath)
        timestamps= list(map(find_timestamp,filelist))
        # print(max(timestamps))
        recent= max(timestamps).strftime("%Y_%m_%d_%H_%M_%S")
        db_filename= "ADAMANT_"+ recent +".db" 
        db_string = "sqlite:///"+folderpath + "\\"+ db_filename

        engine= db.create_engine(db_string)
        connection= engine.connect()  
        return connection  
    
    def get_HoV_info(self,HoV):
        return self.db_hov.loc[self.db_hov["HoV"]== HoV,:]

    def addNewRecord(self,HoV,Ac_version = None,Fcrc= None,Ccrc= None,Csird= None,color= None,Airline= None,isbatch2 = 0.0, isPreMau= 0.0):
            row_dict= {"HoV":HoV, "AC Version":Ac_version,"FCRC":Fcrc,"CCRC":Ccrc,"cSIRD":Csird,"Colour":color,"Airline":Airline,"isBatch2":isbatch2,"isPreMAU":isPreMau}
            self.db_hov= self.db_hov.append(other=row_dict,ignore_index=True)
    @property
    def df(self):
        return self.db_hov

if __name__=="__main__":
    dbhov= DB_HoV()
    from model.utils.global_info import HoV_acv_df
    dbhov.db_hov= HoV_acv_df
    dbhov.export_dataset(dbhov.conn)
    dbhov.load_dataset(dbhov.conn)
    print(dbhov.db_hov.head())
    dbhov.addNewRecord("ASX1","A350-900",1,1,"AUX",1,"airbus")
    print(dbhov.db_hov.tail())
