from datetime import datetime
from model.DB0_DEF.flow import DB0_DEF_FLOW
from model.interfaces import IDataset
from model.DB0_DEF.info import DB0_DEF_INFO
from model.DB0_DEF.tz import DB0_DEF_TZ


class DB0_DEF(IDataset):
    def __init__(self):
        self.flow_df= DB0_DEF_FLOW()
        self.info_df = DB0_DEF_INFO()
        self.tz_df = DB0_DEF_TZ()

    def export_dataset(self, connection):
        #Export  db0def-flow
        self._exporttosql_multi_index(self.flow_df.df,connection = connection,table_name="DB0_DEF_FLOW")

        #eXPORT DB0_DEF_TZ
        self._exporttosql_flat_index(self.tz_df.df,connection=connection,table_name="DB0_DEF_TZ")

        #Export DB0_DEF_INFO
        df2= self.info_df.df_info
        d= datetime(2001,1,1)
        test_date= d.strftime("%Y-%m-%d %H:%M:%S")
        df2= df2.replace("00:00:00",d)
        print(df2.info())
        df2["Test Date"]= df2["Test Date"].fillna(d).apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S")).fillna(test_date).astype(str)
        df2["Import Date"]= df2["Import Date"].fillna(d).apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S")).fillna(test_date).astype(str)
        df2= df2.replace("00:00:00","2001-01-01 00:00:00")
        df2= df2.fillna(0)
        print(df2.head())

        self._exporttosql_flat_index(df2,connection=connection,table_name="DB0_DEF_INFO")

    def load_dataset(self, connection):
        #Load  db0def-flow
        flow_df_raw= self._fromsql_multi_index(connection=connection,table_name="DB0_DEF_FLOW",type_of_df="FLOW")
        self.flow_df.df=flow_df_raw
        
        #Load db0_def_tz
        tz_df_raw= self._fromsql_flat_index(connection=connection,table_name="DB0_DEF_TZ")
        tz_df_raw.index= tz_df_raw.index.rename("HoV")
        self.tz_df.df= tz_df_raw
        
        #Load db0_def_info
        df3= self._fromsql_flat_index(connection= connection,table_name="DB0_DEF_INFO")
        df3["Test Date"]= df3["Test Date"].apply(lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
        df3["Import Date"]= df3["Import Date"].apply(lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
        print(df3.head())
        print(df3.info()) 

        self.info_df.df_info= df3
    
    def addNewRecord(self,filepath,HoV=None,AC_version=None,test_date= None):
        
        #Add a new record to DBO_DEF_FLOW 
        self.flow_df.addNewRecord(filepath=filepath, HoV= HoV,ACversion=AC_version)

        #Add a new record to DB0_DEF_INFO
        self.info_df.addNewRecord(filepath=filepath,HoV=HoV,ACversion=AC_version,test_date=test_date)

        #Add a new Record to DB0_DEF_TZ
        self.tz_df.addNewRecord(filepath=filepath,HoV=HoV)

        

    
        
