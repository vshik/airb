"""
THIS FILE IS MEANT TO CONTAIN UTILITY FUNCTIONS WHICH WILL HELP TO LOAD
DATA FROM EXCEL.

THIS FILE IS FOR MODEL INITIALISATION ONLY.

"""
import os
import sqlite3
import pandas as pd
import sqlalchemy as db
from datetime import datetime

def load_frame_df(filepath,row_index_names=["HoV","Test Reference"]):
    df2= pd.read_excel(filepath,"Flow",engine="xlrd",header=[0,1,2],index_col= [0,1])
    #df1= pd.read_csv("a.csv")
    

    df2.columns=df2.columns.set_names(["type","side","Frame"])
   
    df2.index= df2.index.set_names(row_index_names)
    
    return df2

def load_tz(filepath,row_index_names=["HoV","Test Reference"]):
    df2= pd.read_excel(filepath,"TZ",engine="xlrd")
    df2= df2.fillna(method="ffill")
    df2= df2.set_index(row_index_names)
    return df2

def  load_mix_rec(filepath,row_index_names=["HoV","Test Reference"]):
    df2= pd.read_excel(filepath,"mixrec",engine="xlrd")
    df2= df2.set_index(row_index_names)
    return df2

def load_rest_df(filepath,row_index_names=["HoV","Test Reference"]):
    df2= pd.read_excel(filepath,"Restrictor",engine="xlrd",header=[0,1],index_col= [0,1])
    #df1= pd.read_csv("a.csv")
    

    df2.columns=df2.columns.set_names(["TZ","Restrictor"])
    

    df2.index= df2.index.set_names(row_index_names)
        
    return df2

def load_pp_df(filepath,row_index_names=["HoV","Test Reference"]):
    df2= pd.read_excel(filepath,"Pressure",engine="xlrd",header=[0,1],index_col= [0,1])
    #df1= pd.read_csv("a.csv")
    

    df2.columns=df2.columns.set_names(["TZ","PP"])
       
    df2.index= df2.index.set_names(row_index_names)
    
    return df2


def exporttosql_multi_index(raw_df):
        # # path="DB0c_DEF.xlsx"
        # # raw_df= pd.read_excel(path, header=[0,1,2], index_col=0)
        # # #raw_df= raw_df.reset_index()
        # # print(raw_df.head())
        # #raw_df.to_excel("op.xlsx")
        # user_date= datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        # db_name= "ADAMANT_"+ user_date +".db"
        # db_string= "sqlite:///\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup\\" + db_name
        # #engine= db.create_engine("sqlite:///\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup\\mysqidb.db")
        # engine= db.create_engine(db_string)
        engine= db.create_engine("sqlite:///\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\sqltesting\\mysqidb.db")
        connection= engine.connect()
        raw_df.T.to_sql("Flowdef",con=connection,if_exists="replace") 

def db0_flow_framefunc(x):
            if(x.split("-")[2]== "HUM"):
                return ""
            else:
                if(len(x.split("-"))==4):
                    return  x.split("-")[2] +"-"+ x.split("-")[3]
                else:
                    return x.split("-")[2]
def fromsql_multi_index():
    engine= db.create_engine("sqlite:///\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\sqltesting\\mysqidb.db")
    connection= engine.connect()
    df_table= pd.read_sql_table(table_name="Flowdef",con= connection, index_col= ('type','side','Frame'))
    df_table= df_table.set_index(["type","side","Frame"])
    df_table= df_table.T
    print(df_table.head())
    return df_table

def db_to_multi_index(df,type_of_df):
    if(type_of_df=="FLOW"):
        trandf= df.T
        trandf.columns= trandf.columns.rename("HoV")


def flow_flatten_index(df):
    
        """ Does Final Column Transformations, Converts LAOR/ CAOR to LAO/CAO respectively 
        and flattens the multiindex to form a dataframe with uniquely identifiable columns
        

        :type df: Pandas Dataframe
        :param self: Input dataset to be flattened
    
        :raises:
    
        :rtype:
        """   
        df1= df
        # List the type of Air Outlets
        type_list= df1.iloc[0,:].fillna("None").values.tolist()


        #Side of Air Outlet
        side_list= df1.iloc[1,:].fillna("None").values.tolist()


        # List Frame Sections
        frame_list=df1.iloc[2,:].values.tolist()


        # fill None VALUES
        def fill_none(a):
            #temp_list= [x for x in a  
            for i,j in enumerate(a):
                if (j == "None"):
                    if i==0:
                        a[0]= next(item for item in a if item !='None')
                    else:
                        a[i] = a[i-1]
            return a



        #Filling nones And selecting Columns other than the first column
        type_list = fill_none(type_list)[1:]
        side_list = fill_none(side_list)[1:]
        frame_list= fill_none(frame_list)[1:]
        def NewColumnNames(frame_list):
            try:
                a= len(frame_list)
                # Initialising the name list with the name of the first columndb
                name_list=["HoV"]
                for i in range(0,a):
                    name= str(type_list[i]) +"-"+str(side_list[i]) +"-"+ str(frame_list[i])
                    name_list.append(name)
            except Exception as e:
                print(e)
                print("List Lengths are not equal")
            finally:
                return name_list
        name_list = NewColumnNames(frame_list)
        print(type_list)
        print(side_list)



        #name_list=name_list.insert(0,"Frame")

        # Slicing the Core Data (Getting the data except the column names)
        df1=df1.iloc[3:,0:]


        #Assigning new Column Names
        df1.columns=name_list

        return df1
