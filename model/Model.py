from model.DB0_DEF.flow import DB0_DEF_FLOW
from pathlib import Path
from model.DB0_DEF.DB0_DEF import DB0_DEF
from model.DB2_LTR.LTR import DB2_LTR
from model.DB1_STR.STR import DB1_STR
from model.DB3_GTR4.GTR4 import DB3_GTR4
from model.DB4_GTR8.GTR8 import DB4_GTR8
# from model.DB5_FTR.FTR import FTR
from model.DB6_CSIRD.DB6_CSIRD import DB6_CSIRD
#from model.utils.DB_User import DB_User
from model.utils import global_objects
import pandas as pd
import os
import sqlite3
import sqlalchemy as db
from datetime import datetime
# from

class Model():
    def __init__(self):
        self.db0_def= DB0_DEF()
        self.db1_str= DB1_STR()
        self.db2_ltr= DB2_LTR()
        self.db3_gtr4= DB3_GTR4()
        self.db4_gtr8= DB4_GTR8()
        # self.excel_path= ""
        # self.sql_path= "\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup"
        """
        None Values Signify that the respective classes need to be defined for these datasets.

        """
        self.db6_restCsird= DB6_CSIRD()
        # self.visioJpeg = None
        self.db_user= global_objects.db_user
        self.db_ac= global_objects.db_ac
        self.db_acv= global_objects.db_acv
        self.db_hov = global_objects.db_hov
        # self.db_restrictor= None
        # self.db_ftr= FTR()
        # self.df_tr = pd.DataFrame()
        # self.df_restrictorChain= pd.DataFrame()
        # self.df_restVariants= pd.DataFrame()

        #self.fromSQL(self.sql_path)
    
    """
    Below Are all Correction functions

    """
    def correct_sigma(self):
        pass
    
    def correct_preMAU(self):
        pass
    
    def correct_normFlow(self):
        pass 

    def correct_norm_Pres(self):
        pass
    
    def calc_avg(self,df):
        pass
    
    def calc_max(self,df):
        pass

    def calc_min(self,df):
        pass

    def calc_PercentDiff(self,df1,df2):
        pass

    def calc_AbsoluteDiff(self,df1,df2):
        pass
    
    def calc_tr(self,*params):
        pass
    
    def calc_restrictorChain(self):
        pass

    def calc_restVariants(self):
        pass

    def get_data(self):
        pass
    
    def fromSQL(self,folderpath=None):
    
        """ Load the entire model from sql

        :type self: Model
        :param self: Calling object of Model class
    
        :type folderpath: string
        :param folderpath: full path to the folder in which all adamant sql files are stored.
    
        :raises: None
    
        :rtype: None
        """    
        connection= self.getLatestSQL(folderpath)
        self.db0_def.load_dataset(connection)
        self.db1_str.load_dataset(connection)
        self.db2_ltr.load_dataset(connection)
        self.db3_gtr4.load_dataset(connection)
        self.db4_gtr8.load_dataset(connection)
        
        #Below function calls are to classes which are not derived from IDataset interface 
        # Therefore load dataset and export dataset has to be defined for these classes 
        self.db6_restCsird.load_dataset(connection)
        self.db_user.load_dataset(connection)
        #self.db_ftr.load_dataset(connection)

    def toSQl(self, folderpath = None):
        if(folderpath == None):
            folderpath = "\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup"
        
        user_date= datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        db_name= "ADAMANT_"+ user_date +".db"
             
        db_string = "sqlite:///"+folderpath + "\\"+ db_name
        #engine= db.create_engine("sqlite:///\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup\\mysqidb.db")
        engine= db.create_engine(db_string)
        connection= engine.connect()

        
        self.db0_def.export_dataset(connection)
        self.db1_str.export_dataset(connection)
        self.db2_ltr.export_dataset(connection)
        self.db3_gtr4.export_dataset(connection)
        self.db4_gtr8.export_dataset(connection)
        self.db_ac.export_dataset(connection)
        self.db_acv.export_dataset(connection)
        self.db_hov.export_dataset(connection)
        #Below function calls are to classes which are not derived from IDataset interface 
        # Therefore load dataset and export dataset has to be defined for these classes 
        self.db6_restCsird.export_dataset(connection)
        self.db_user.export_dataset(connection)
        self.db_ftr.export_dataset(connection)


    def getLatestSQL(self, folderpath = None):
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
    # print(min(timestamps))


    def set_user_access(self,user_id,level):
    
        """ Set the Access level (UserGroup) of the User
        
        :type self: Model
        :param self: Calling object of Model class
    
        :type user_id: string
        :param user_id: Unique Airbus user ID (FOR example SP008976)
    
        :type level:int
        :param level: Integer value corresponding to the new access level
    
        :raises: KeyError
    
        :rtype: None
        :return: None
        """    
        self.db_user.set_user_access(user_id,access_level=level)
    
    def get_user_access(self,user_id):
    
        """ Get Current Access level(UserGroup) of the given UserId
        
        :type self: Model
        :param self: Calling object of Model class
    
        :type user_id: string
        :param user_id: Unique Airbus user ID (FOR example SP008976)
    
        :raises: KeyError
    
        :rtype: int
        :return: Integer value corresponding to the current access level
        """  
         
        return self.db_user.get_user_access(user_id)
       

    def add_new_user(self,user_id,name,access_level,siglum="AIOESSA"):
    
        """ Add a new user

        :type self: Model
        :param self: Calling object of Model class
    
        :type user_id: string
        :param user_id: Unique Airbus user ID (FOR example SP008976)
    
        :type name: string
        :param name: Name of the user
    
        :type access_level: int
        :param access_level:Integer value corresponding to the user access level
    
        :type siglum: string
        :param siglum: Airbus team Acronym (for example AIOESSA)
    
        :raises:None
    
        :rtype:None
        """    
        self.db_user.add_new_user(user_id,access_level,name=name,siglum=siglum)

    def remove_user(self,userid):
    
        """ Remove the user with the given userID
        
        :type self: Model
        :param self: Calling object of Model class
    
        :type user_id: string
        :param user_id: Unique Airbus user ID (FOR example SP008976)
    
        :raises: KeyError
    
        :rtype: None
        """    
        
        self.db_user.remove_user(userid)

    def load_model_from_excel(self,repo_path):
        import model.utils.load_functions as lf
               
        
        """
        LOAD DB0_DEF
        """

        #Loading DB0_DEF
        db0_path=os.path.join(repo_path,"DB0_DEF")       


        #Loading Db0_def_flow
        db0_flow_path= os.path.join(db0_path,"DB0_DEF_FLOW.xlsx")
        db0_flow_raw= pd.read_excel(db0_flow_path,"Flow",engine= "xlrd",header=[0,1,2])    
        # print(db0_flow_raw.head())
        # print(db0_flow_raw.index.values)

        self.db0_def.flow_df.df = db0_flow_raw
        print(self.db0_def.flow_df.df.head())
        
        #Loading Db0_def_info       
        db0_info_path= os.path.join(db0_path,"DB0_DEF_INFO.xlsx")
        db0_info_raw= pd.read_excel(db0_info_path,sheetname="Info",engine= "xlrd")    
        #print(db0_info_raw.head())

        self.db0_def.info_df.df = db0_info_raw
        print(self.db0_def.info_df.df.head())

        #Loading Db0_def_tz
        db0_tz_path= os.path.join(db0_path,"DB0_DEF_TZ.xlsx")
        db0_tz_raw= pd.read_excel(db0_tz_path,sheetname="TZ",engine= "xlrd",index_col=0)
        #print(db0_tz_raw.head())  

        self.db0_def.tz_df.df = db0_tz_raw
        print(self.db0_def.tz_df.df.head()) 
        

        #Loading DB2_LTR
        db2_path=os.path.join(repo_path,"DB2_LTR")


        #Loading Db2_ltr_flow 
        db2_flow_path= os.path.join(db2_path,"DB2_LTR_FLOW.xlsx")
        db2_flow_raw= lf.load_frame_df(db2_flow_path)
            
        #print(db2_flow_raw.head())      
            

        self.db2_ltr.flow_df.df = db2_flow_raw
        print(self.db2_ltr.flow_df.df.head())

        #Loading Db2_ltr_restrictor
        db2_rest_path= os.path.join(db2_path,"DB2_LTR_REST.xlsx")
        db2_rest_raw= lf.load_rest_df(db2_rest_path)
        #print(db2_rest_raw.head())
        
        self.db2_ltr.restrictor_df.df = db2_rest_raw
        print(self.db2_ltr.restrictor_df.df.head())
        
        #Loading Db2_ltr_pp
        db2_pp_path= os.path.join(db2_path,"DB2_LTR_PP.xlsx")
        db2_pp_raw= lf.load_pp_df(db2_pp_path)
        #print(db2_pp_raw.head())
        self.db2_ltr.pp_df.df=db2_pp_raw
        print(self.db2_ltr.pp_df.df.head())
        
        #Loading Db2_ltr_info
        db2_info_path= os.path.join(db2_path,"DB2_LTR_INFO.xlsx")
        db2_info_raw= pd.read_excel(db2_info_path,"Info",engine= "xlrd")
        #print(db2_info_raw.head())
        self.db2_ltr.info_df.df_info=db2_info_raw
        print(self.db2_ltr.info_df.df_info.head())

        #Loading Db2_ltr_tz
        db2_tz_path= os.path.join(db2_path,"DB2_LTR_TZ.xlsx")
        db2_tz_raw= lf.load_tz(db2_tz_path)
        #print(db2_tz_raw.head())
        self.db2_ltr.tz_df.df= db2_tz_raw
        print(self.db2_ltr.tz_df.df.head())    
        
        #Loading Db2_ltr_mix_rec_amb
        db2_mixrec_path= os.path.join(db2_path,"DB2_LTR_MIX_REC_AMB.xlsx")
        db2_mixrec_raw= lf.load_mix_rec(db2_mixrec_path)
        #print(db2_mixrec_raw.head())
        self.db2_ltr.mix_rec_amb_df.df= db2_mixrec_raw
        print(self.db2_ltr.mix_rec_amb_df.df.head())
        
        """
        LOAD DB1_STR
        """


        #Loading DB1_STR
        db1_path=os.path.join(repo_path,"DB1_STR")

        #Loading Db1_str_flow 
        db1_flow_path= os.path.join(db1_path,"DB1_STR_FLOW.xlsx")
        db1_flow_raw= lf.load_frame_df(db1_flow_path,["HoV","Test Name"])
            
        print(db1_flow_raw.head())

        #self.db1_str.flow_df.df= db1_flow_raw
        #print(self.db1_str.flow_df.df.head())

        #Loading Db1_STr_restrictor
        db1_rest_path= os.path.join(db1_path,"DB1_STR_REST.xlsx")
        db1_rest_raw= lf.load_rest_df(db1_rest_path,["HoV","Test Name"])
        print(db1_rest_raw.head())
        
        #self.db1_str.restrictor_df.df = db1_rest_raw
        #print(self.db1_str.restrictor_df.df.head())

        #Loading Db1_STr_info
        db1_info_path= os.path.join(db1_path,"DB1_STR_INFO.xlsx")
        db1_info_raw= pd.read_excel(db1_info_path,"Info",engine= "xlrd")
        #print(db1_info_raw.head())
        
        
        self.db1_str.info_df.df_info= db1_info_raw
        print(self.db1_str.info_df.df_info.head())
        
        #Loading Db1_STR_pp
        db1_pp_path= os.path.join(db1_path,"DB1_STR_PP.xlsx")
        db1_pp_raw= lf.load_pp_df(db1_pp_path,["HoV","Test Name"])
        print(db1_pp_raw.head())
        
        #self.db1_str.pp_df.df=db1_pp_raw
        #print(self.db1_str.pp_df.df.head())

        #Loading Db1_Str_mix_rec_amb
        db1_mixrec_path= os.path.join(db1_path,"DB1_STR_MIX_REC_AMB.xlsx")
        db1_mixrec_raw= lf.load_mix_rec(db1_mixrec_path,["HoV","Test Name"])
        print(db1_mixrec_raw.head())
        
        #self.db1_str.mix_rec_amb_df.df= db1_mixrec_raw
        #print(self.db1_str.mix_rec_amb_df.df.head())

        """
        LOAD DB3_GTR4
        """
        #Loading DB3_GTR4
        db3_path=os.path.join(repo_path,"DB3_GTR4")

        #Loading  DB3_GTR4_flow 
        db3_flow_path= os.path.join(db3_path,"DB3_GTR4_FLOW.xlsx")
        db3_flow_raw= lf.load_frame_df(db3_flow_path)
            
        print(db3_flow_raw.head())
        
        #self.db3_gtr4.flow_df.df=db3_flow_raw
        #print(self.db3_gtr4.flow_df.df.head())

        #Loading Db3_gtr4_pp
        db3_pp_path= os.path.join(db3_path,"DB3_GTR4_PP.xlsx")
        db3_pp_raw= lf.load_pp_df(db3_pp_path)
        print(db3_pp_raw.head())
        
        #self.db3_gtr4.pp_df.df=db3_pp_raw
        #print(self.db3_gtr4.pp_df.df.head())

        #Loading Db3_gtr4_info
        db3_info_path= os.path.join(db3_path,"DB3_GTR4_INFO.xlsx")
        db3_info_raw= pd.read_excel(db3_info_path,"Info",engine= "xlrd")
        print(db3_info_raw.head())
        
        #self.db3_gtr4.info_df.df_info=db3_info_raw
        #print(self.db3_gtr4.info_df.df_info.head())

        #Loading Db3_gtr4_mix_rec_amb
        db3_mixrec_path= os.path.join(db3_path,"DB3_GTR4_MIX_REC_AMB.xlsx")
        db3_mixrec_raw= lf.load_mix_rec(db3_mixrec_path)
        print(db3_mixrec_raw.head())
        
        #self.db3_gtr4.mix_rec_amb_df.df= db3_mixrec_raw
        #print(self.db3_gtr4.mix_rec_amb_df.df.head())

        #loading gtr4 definition
        db3_def_path= os.path.join(db3_path,"DB3_GTR4_DEF.xlsx")
        db3_def_raw= pd.read_excel(db3_def_path,"Flow",engine= "xlrd",header=[0,1,2])
        print(db3_def_raw.head())

        #self.db3_gtr4.gtr4_def= db3_def_raw
        #print(self.db3_gtr4.gtr4_def.head())


        """
        LOAD DB4_GTR8
        """

        #Loading DB4_GTR8
        db4_path=os.path.join(repo_path,"DB4_GTR8")

        #Loading Db4_gtr8_INFO
        db4_info_path= os.path.join(db4_path,"DB4_GTR8_INFO.xlsx")
        db4_info_raw= pd.read_excel(db4_info_path,engine= "xlrd")
        print(db4_info_raw.head())
        
        #self.db4_gtr8.info_df.df_info=db4_info_raw
        #print(self.db4_gtr8.info_df.df_info.head())
        
        #Loading Db4_gtr8_mix_rec_amb
        db4_mixrec_path= os.path.join(db4_path,"DB4_GTR8_MIX_REC_AMB.xlsx")
        db4_mixrec_raw=  pd.read_excel(db4_mixrec_path,engine= "xlrd")
        print(db4_mixrec_raw.head())
        
        #self.db4_gtr8.mix_rec_amb_df.df= db4_mixrec_raw
        #print(self.db4_gtr8.mix_rec_amb_df.df.head())
        
        #Loading  DB4_GTR8_flow 
        db4_flow_path= os.path.join(db4_path,"DB4_GTR8_FLOW.xlsx")
        db4_flow_raw= pd.read_excel(db4_flow_path,engine= "xlrd",header=[0,1,2])
        db4_flow_raw=db4_flow_raw.reset_index(drop= True)    
        print(db4_flow_raw.head())
        
        #self.db4_gtr8.flow_df.df=db4_flow_raw
        #print(self.db4_gtr8.flow_df.df.head())
        
        #Loading Db4_gtr8_pp
        db4_pp_path= os.path.join(db4_path,"DB4_GTR8_PP.xlsx")
        db4_pp_raw= pd.read_excel(db4_pp_path,engine= "xlrd",header=[0,1])
        db4_pp_raw=db4_pp_raw.reset_index(drop= True)
        print(db4_pp_raw.head())
        #self.db4_gtr8.pp_df.df= db4_pp_raw
        #print(self.db4_gtr8.pp_df.df.head())

       #Loading GTR8 DEF
        db4_def_path= os.path.join(db4_path,"DB4_GTR8_DEF.xlsx")
        db4_def_raw= pd.read_excel(db4_def_path,"Flow",engine= "xlrd",header=[0,1,2])
        print(db4_def_raw.head())
        

        #self.db4_gtr8.gtr8_def= db4_def_raw
        #print(self.db4_gtr8.gtr8_def.head())

        #Loading gtr8 restrictor
        db4_rest_path= os.path.join(db4_path,"DB4_GTR8_DEF.xlsx")


        """
        LOAD DB6_CSIRD
        """
        db6_path=os.path.join(repo_path,"DB6_CSIRD")

        # Load DB6_CSIRD_REST_EXIST
        db6_rest_exist_path= os.path.join(db6_path,"DB6_CSIRD_REST_EXIST.xlsx")
        db6_rest_exist_raw= pd.read_excel(db6_rest_exist_path,"Frame",engine= "xlrd",header=[0,1,2])    
        print(db6_rest_exist_raw.head())

        #self.db6_restCsird.restrictor_exist_df.df= db6_rest_exist_raw
        #print(self.db6_restCsird.restrictor_exist_df.df.head())

        # Load DB6_CSIRD_REST
        db6_rest_path= os.path.join(db6_path,"DB6_CSIRD_REST.xlsx")
        db6_rest_raw= pd.read_excel(db6_rest_path,"Restrictor",engine= "xlrd",header=[0,1])    
        print(db6_rest_raw.head())

        #self.db6_restCsird.restrictor_df.df= db6_rest_raw 
        #print(self.db6_restCsird.restrictor_df.df.head())

        #Load DB6_CSIRD_VARIANT
        db6_rest_variant_path= os.path.join(db6_path,"DB6_CSIRD_VARIANT.xlsx")
        db6_rest_variant_raw= pd.read_excel(db6_rest_variant_path,"Variant",engine= "xlrd")
        db6_rest_variant_raw["Variant"] =  db6_rest_variant_raw["Variant"].fillna(0).astype(int) 
        print(db6_rest_variant_raw.head())

        #self.db6_restCsird.DB_Variant.df = db6_rest_variant_raw
        #print(self.db6_restCsird.DB_Variant.df.head())

        #Load DB6_CSIRD_INFO
        db6_info_raw= global_objects.db_hov.db_hov
        print(db6_info_raw.head())

        #self.db6_restCsird.restrictor_info.df= db6_info_raw
        #print(self.db6_restCsird.restrictor_info.df.head())

        #db5_ftr_path = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\Aditi\\Repository\\5-FTR"
        #self.db_ftr.addDataframeToDictionary(db5_ftr_path)
       
         
        
        

       



if __name__=="__main__":
    #instatiate Model and test
    model= Model()
    path=r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\Adamant_Data"
    model.load_model_from_excel(path)
