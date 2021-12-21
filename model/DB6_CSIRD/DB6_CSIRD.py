from model.interfaces import IDataset
from model.DB6_CSIRD.rest import DB6_CSIRD_REST
from  model.DB6_CSIRD.rest_exist import DB6_CSIRD_REST_EXIST
from  model.DB6_CSIRD.DB_Variant import DB6_CSIRD_VARIENT
from model.DB6_CSIRD.info import DB6_CSIRD_INFO
import pandas as pd


class DB6_CSIRD(IDataset):
    def __init__(self):
        self.restrictor_df= DB6_CSIRD_REST()
        self.restrictor_exist_df=DB6_CSIRD_REST_EXIST()
        self.DB_Variant = DB6_CSIRD_VARIENT()
        self.restrictor_info=DB6_CSIRD_INFO()

    def addNewRecord(self, filepath,HoV= None,AC_version= None,Notes= None):
        
        # Add a new record to DB6_CSIRD_REST:
        self.restrictor_df.addNewRecord(filepath=filepath,HoV=HoV)

        #Add a new record to DB6_CSIRD_REST_EXIST:
        self.restrictor_exist_df.addNewRecord(filepath=filepath,HoV=HoV,ACversion=AC_version)

        #Add a new record to DB6_CSIRD_VARIENT
        self.DB_Variant.addNewRecord(filepath=filepath)

        #Add a new record to DB6_CSIRD_INFO
        #self.restrictor_info.addNewRecord()

         
    
    def export_dataset(self, connection):
        #EXPORT DB6_CSIRD_REST_EXIST
        self._exporttosql_multi_index(self.restrictor_exist_df.df,connection = connection,table_name="DB6_CSIRD_REST_EXIST")
    
        #EXPORT DB6_CSIRD_REST
        self._exporttosql_multi_index(self.restrictor_df.df,connection = connection,table_name="DB6_CSIRD_REST")

        #EXPORT DB6_CSIRD_VARIENT
        self.DB_Variant.df.to_sql("DB6_CSIRD_VARIANT",con=connection,if_exists="replace",index = False)

        #eXPORT DB6_CSIRD_INFO
        self.restrictor_info.df.to_sql("DB6_CSIRD_INFO",con=connection,if_exists="replace",index = False)

    

    def load_dataset(self, connection):
        #Load  DB6_CSIRD_REST_EXIST
        rest_exist_df_raw= self._fromsql_multi_index(connection=connection,table_name="DB6_CSIRD_REST_EXIST",type_of_df="FLOW")
        self.restrictor_exist_df.df=rest_exist_df_raw

        #Load  DB6_CSIRD_REST
        rest_df_raw= self._fromsql_multi_index(connection=connection,table_name="DB6_CSIRD_REST",type_of_df="Restrictor")
        self.restrictor_df.df=rest_df_raw

        #Load DB6_CSIRD_VARIENT
        df3= pd.read_sql_table(table_name="DB6_CSIRD_VARIANT",con= connection)
        self.DB_Variant.df = df3

        ##Load DB6_CSIRD_INFO
        df3= pd.read_sql_table(table_name="DB6_CSIRD_INFO",con= connection)
        self.restrictor_info.df = df3
        
    
