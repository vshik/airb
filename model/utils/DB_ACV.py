import pandas as pd
from datetime import datetime
import sqlalchemy as db
import os

class DB_ACV:
    def __init__(self,folderpath= None):
        self.db_acv = pd.DataFrame()
        self.conn= self._getlatestsql(folderpath)
        self.load_dataset(self.conn)        

    def load_dataset(self, connection):
        try:
            #df_table= pd.read_sql_table(table_name= "DB_ACV",con= connection)
            df_table= pd.read_sql_table(table_name="DB_ACV",con= connection, index_col= ('type','side','Frame'))
            df_table= df_table.set_index(["type","side","Frame"])        
            df_table= df_table.T
            print("\n Printing RAW LOADED df from SQL:\n")
            print(df_table.head())
            self.db_acv= df_table
        except Exception as e:
            print("Error:",e)

    def export_dataset(self, connection):
        raw_df= self.db_acv
        raw_df.T.to_sql("DB_ACV",con=connection,if_exists="replace")

    
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

    @property
    def df(self):
        return self.db_acv

if __name__=="__main__":
    db_acv= DB_ACV()
    from model.utils.global_info import ACv_frame_df
    db_acv.db_acv= ACv_frame_df
    db_acv.export_dataset(db_acv.conn)
    db_acv.load_dataset(db_acv.conn)
    print(db_acv.db_acv.head())
