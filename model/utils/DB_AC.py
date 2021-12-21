import pandas as pd
from datetime import datetime
import sqlalchemy as db
import os
class DB_AC:
    def __init__(self,folderpath= None):
        self.db_ac = pd.DataFrame()
        self.conn= self._getlatestsql(folderpath)
        self.load_dataset(self.conn)
        

    def load_dataset(self, connection):
        try:
            df_table= pd.read_sql_table(table_name= "DB_AC",con= connection)
            # df_table= pd.read_sql_table(table_name="Flowdef",con= connection, index_col= ('type','side','Frame'))
            # df_table= df_table.set_index(["type","side","Frame"])        
            df_table= df_table.T
            print(df_table.head())
            columns_list= df_table.iloc[0].values.tolist()
            df_table= df_table.iloc[1:,:]
            df_table.columns= columns_list 
            self.db_ac= df_table
        except Exception as e:
            print("Error:",e)

    def export_dataset(self, connection):
        raw_df= self.db_ac
        raw_df.T.to_sql("DB_AC",con=connection,if_exists="replace")

    def set_delivery_status(self,msn, delivery_status):
        self.db_ac.loc[self.db_ac['MSN']==msn , "Delivered"] = delivery_status

    def get_delivery_status(self, msn):
        return self.db_ac.loc[self.db_ac["MSN"] == msn, "Delivered"]

    def add_msn(self,msn,delivery_status):
        new_row_dict= {"MSN":msn, "Delivered":delivery_status}
        self.db_ac.append(new_row_dict,ignore_index=True)

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
        return self.db_ac

if __name__=="__main__":
    db_ac= DB_AC()
    from model.utils.global_info import db_ac_df
    db_ac.db_ac= db_ac_df
    db_ac.export_dataset(db_ac.conn)
    db_ac.load_dataset(db_ac.conn)
    print(db_ac.db_ac.head())
