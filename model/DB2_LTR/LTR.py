from model.interfaces import IDataset
from model.DB2_LTR.flow import DB2_LTR_FLOW
from model.DB2_LTR.rest import DB2_LTR_REST
from model.DB2_LTR.tz import DB2_LTR_TZ
from model.DB2_LTR.pp import DB2_LTR_PP
from model.DB2_LTR.info import DB2_LTR_INFO
from model.DB2_LTR.mix_rec_amb import DB2_LTR_MIX_REC_AMB
from datetime import datetime

class DB2_LTR(IDataset):
    def __init__(self):
        self.flow_df= DB2_LTR_FLOW()
        self.restrictor_df= DB2_LTR_REST()
        self.pp_df= DB2_LTR_PP()
        self.tz_df= DB2_LTR_TZ()
        self.info_df= DB2_LTR_INFO()
        self.mix_rec_amb_df= DB2_LTR_MIX_REC_AMB()

    def addNewRecord(self, filepath, test_date,HoV= None ,test_reference= None,AC_version= None,Notes= None):
        
        #Add a new record to DB2_LTR_FLOW 
        self.flow_df.addNewRecord(filepath=filepath, HoV= HoV,ACversion=AC_version,db2_ltr_test_reference=test_reference)
        
        # Add A NEW RECORD to DB2_LTR_REST
        self.restrictor_df.addNewRecord(filepath=filepath,HoV=HoV,ACversion=AC_version,db2_ltr_test_reference=test_reference)

        #Add a new record to DB2_LTR_PP
        self.pp_df.addNewRecord(filepath=filepath,HoV=HoV,ACversion=AC_version,db2_ltr_test_reference=test_reference)

        #Add a new record to DB2_LTR_TZ
        self.tz_df.addNewRecord(filepath=filepath,HoV=HoV,db2_ltr_test_reference=test_reference,ACversion=AC_version)

        #Add a new record to DB2_LTR_INFO
        self.info_df.addNewRecord(filepath=filepath,HoV=HoV,test_reference=test_reference,test_date=test_date,Notes=Notes) 

        #Add a new DB2_LTR_MIX_REC_AMB
        #self.mix_rec_amb_df.addNewRecord(filepath=filepath,HoV=HoV,ACversion=AC_version)


    def export_dataset(self, connection):
        # Export TZ DF
        df2= self.tz_df.df
        df2= df2.reset_index()
        self._exporttosql_flat_index(df2,connection=connection,table_name="DB2_LTR_TZ")

        #Export MIX_REC_AMB
        df2= self.mix_rec_amb_df.df
        df2= df2.reset_index()
        self._exporttosql_flat_index(df2,connection=connection,table_name="DB2_LTR_MIX_REC_AMB")

        #Export flow df
        df2= self.flow_df.df
        df2= df2.reset_index()
        self._exporttosql_multi_index(df2,connection=connection,table_name="DB2_LTR_FLOW")

        #Export Restrictor df
        df2= self.restrictor_df.df
        df2= df2.reset_index()
        self._exporttosql_multi_index(df2,connection=connection,table_name="DB2_LTR_REST")

        #Export PP df
        df2= self.pp_df.df
        df2= df2.reset_index()
        self._exporttosql_multi_index(df2,connection=connection,table_name="DB2_LTR_PP")

        #Export DB2_LTR_INFO
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

        self._exporttosql_flat_index(df2,connection=connection,table_name="DB2_LTR_INFO")


    def load_dataset(self, connection):
        #LOAD TZ df
        df3= self._fromsql_flat_index(connection=connection,table_name="DB2_LTR_TZ")
        df3=df3.set_index(["HoV","Test Reference"])

        self.tz_df.df= df3
        
        #lOAD MIXRECAMB DF
        df3= self._fromsql_flat_index(connection=connection,table_name="DB2_LTR_MIX_REC_AMB")
        df3=df3.set_index(["HoV","Test Reference"])

        self.mix_rec_amb_df.df= df3
       
        #Load flow_Df
        df3= self._fromsql_multi_index(connection=connection,table_name="DB2_LTR_FLOW",type_of_df="FLOW")
        df3=df3.set_index(["HoV","Test Reference"])

        self.flow_df.df= df3

        #lOAD Restrictor df
        df3= self._fromsql_multi_index(connection=connection,table_name="DB2_LTR_REST",type_of_df="Restrictor")
        df3=df3.set_index(["HoV","Test Reference"])

        self.restrictor_df.df= df3

        #lOAD  PP df
        df3= self._fromsql_multi_index(connection=connection,table_name="DB2_LTR_PP",type_of_df="PP")
        df3=df3.set_index(["HoV","Test Reference"])

        self.pp_df.df= df3

        #Load db0_def_info
        df3= self._fromsql_flat_index(connection= connection,table_name="DB2_LTR_INFO")
        df3["Test Date"]= df3["Test Date"].apply(lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
        df3["Import Date"]= df3["Import Date"].apply(lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
        print(df3.head())
        print(df3.info()) 

        self.info_df.df_info= df3



