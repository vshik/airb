
from datetime import datetime
import logging
from model.utils.global_info import HoV_acv_df
import re
import pandas as pd
import os
import collections
import numpy as np
import sqlite3
import sqlalchemy as db
#==================================================================================================
# Interfaces for Data import
#==================================================================================================
# FLOWTYPE= ["LTRFlowDEF", "STR", "GTR4", "LTR", "GTR8", "FTR"]
# RESTRICTORTYPE= [ "STR", "GTR4", "LTR", "GTR8", "FTR", "CSIRDRestrictorDEF"]

class IDataset():
    
    """ Interface to describe an Adamant Dataset. Examples of datasets are DB0_DEF,
    DB1_STR, DB2_LTR, DB3_GTR8 etc """
    
    def __init__(self):
        
        #Object of the Respective Flowdef Class
        self.flow_df= None
        
        #Object of the Respective Restrictordef Class
        self.restrictor_df= None
        
        #Object of the Respective Pressure Port  Class
        self.pp_df= None

        #Object of the Respective Ambient Class
        self.mix_rec_amb_df = None
        
        #Object of repective TZ Class
        self.tz_df = None

        # Object of Respective info Class
        self.info_df= None
    
    def load_dataset(self,connection):
         pass
    #
    def export_dataset(self,connection):
        pass

    def addNewRecord(self):
        pass    
    def _get_multi_index_labels(self,dataframetype):
    
        """ Get a list of all multiple index labels / levels for a particular type of dataframe
        
        :type self: Derived IDataset Class
        :param self: Calling object of the Derived IDataset Class
    
        :type dataframetype: string
        :param dataframetype: type of dataframe valid types include: "FLOW","Restrictor","PP"
    
        :raises: None
    
        :rtype: Python list
        :returns: List of Multiindex labels.
        """    
        label_list= []
        
        if(dataframetype=="FLOW"):
            label_list=["type","side","Frame"]
        elif(dataframetype=="Restrictor"):
            label_list= ["TZ","Restrictor"]
        elif(dataframetype=="PP"):
            label_list=["TZ","PP"]
        else: 
            label_list = None
        
        return label_list 
        

    
    def _exporttosql_multi_index(self,raw_df,connection,table_name,type_of_df= None):
    
        """ Function to export an input MUlti Index dataframe of a given type to an SQL TABLE.
        
        :type self: Derived IDataset Class
        :param self: Calling object of the Derived IDataset Class
    
    
        :type raw_df: Pandas Dataframe
        :param raw_df: Input raw dataframe (Multi index on columns) to be exported to SQL.
    
        :type connection: SQLAlchemy connection
        :param connection: Sql alchemy connection to the latest SQLITE3 DB file on the network location.
    
        :type table_name: string
        :param table_name: Input table name to which the dataframe will be exported 
    
        :type type_of_df: string
        :param type_of_df: Type of dataframe valid types include: "FLOW","Restrictor","PP"
        
        :raises: SqlOperationError
    
        :rtype: None
        :returns: None
        """    
        print(raw_df.head())
        #raw_df.to_excel("op.xlsx")
        
        # engine= db.create_engine("sqlite:///\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup\\mysqidb.db")
        # connection= engine.connect()
        raw_df.T.to_sql(table_name,con=connection,if_exists="replace") 
    
    def _fromsql_multi_index(self,connection,table_name,type_of_df=None):
    
        """ Function to import a dataframe Multiindex on columns from an SQL table.

        :type self: Derived IDataset Class
        :param self: Calling object of the Derived IDataset Class
    
        :type connection: SQLAlchemy connection
        :param connection: Sql alchemy connection to the latest sqlite Db file on the network location.
    
        :type table_name: string
        :param table_name: Input SQL table name from which data will be imported.
        
        :type type_of_df: string
        :param type_of_df: Type of dataframe valid types include: "FLOW","Restrictor","PP"
        
        :raises:SqlOperationError
    
        :rtype: Pandas Dataframe
        :return: pandas dataframe multiindex on columns and imported from SQL.
        """
        # engine= db.create_engine("sqlite:///\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup\\mysqidb.db")
        # connection= engine.connect()
        #list of columns to make multi index
        label_list= self._get_multi_index_labels(type_of_df)
        # Read from sql
        df_table= pd.read_sql_table(table_name=table_name,con= connection, index_col= tuple(label_list))
        df_table= df_table.set_index(label_list)
        df_table= df_table.T
        print(df_table.head())
        return df_table
        

    def _exporttosql_flat_index(self,raw_df,connection,table_name,type_of_df=None):
    
        """  Funtion to export a dataframe (flat indexed on columns) to an Sql table
        
        :type self: Derived IDataset Class
        :param self: Calling object of the Derived IDataset Class
    
    
        :type raw_df: Pandas Dataframe
        :param raw_df: Input raw dataframe (FLAT index on columns) to be exported to SQL.
    
        :type connection: SQLAlchemy connection
        :param connection: Sql alchemy connection to the latest sqlite Db file on the network location.
        
        :type table_name: string
        :param table_name: Input SQL table name to which data will be exported.
    
        :type type_of_df: string
        :param type_of_df: Type of dataframe valid types include: "FLOW","Restrictor","PP"
    
        :raises: None
    
        :rtype: None
        """    
        #raw_df= raw_df.reset_index()
        print(raw_df.head())
        #raw_df.to_excel("op.xlsx")        
        # engine= db.create_engine("sqlite:///\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup\\mysqidb.db")
        # connection= engine.connect()
        raw_df.T.to_sql(table_name,con=connection,if_exists="replace")
    
    def _fromsql_flat_index(self,connection,table_name,type_of_df= None):

        """ 
            Function to import a dataframe (FLAT INDEX on columns) from an SQL Table
            
            :type self: Derived IDataset Class
            :param self: Calling object of the Derived IDataset Class
    
            :type connection: SQLAlchemy connection
            :param connection: Sql alchemy connection to the latest sqlite Db file on the network location.

            :type table_name: string
            :param table_name: Input SQL table name from which data will be imported.

            :type type_of_df: string
            :param type_of_df: Type of dataframe valid types include: "FLOW","Restrictor","PP"
            
            :raises: KeyError

            :rtype: Pandas Dataframe

            :return: Pandas dataframe Flat indexed on columns imported from SQL.
        """
        


        # engine= db.create_engine("sqlite:///\\\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\NETWORKDRIVE\\adamantBackup\\mysqidb.db")
        # connection= engine.connect()
        df_table= pd.read_sql_table(table_name=table_name,con= connection)
        # df_table= pd.read_sql_table(table_name="Flowdef",con= connection, index_col= ('type','side','Frame'))
        # df_table= df_table.set_index(["type","side","Frame"])        
        df_table= df_table.T
        print(df_table.head())
        columns_list= df_table.iloc[0].values.tolist()
        df_table= df_table.iloc[1:,:]
        df_table.columns= columns_list       
        
        print(df_table.head())
        return df_table
    #
    # def applyflowfilters(self,*params):
    #     raise NotImplementedError
    #
    # def applyrestrictorfilters(self,*params):
    #     raise NotImplementedError
    


class IData():
    
    """
    Interface for Input Data.
    
    """

    def __init__(self):
        """
        Constructor for IData interface
        
        """
        self._dataframe= pd.DataFrame()
        # self.__loadpath=""
        # self.__importpath=""
        #

    

    def importAllFiles(self, folderpath):

        """ Function to import data from all files from a single folder and append them to the dataset
        To be over ridden by the derived classes.
        
        :type self: Derived IData Class
        :param self: Calling object of the derived IData class.

        :type folderpath: string
        :param folderpath: Complete path to the folder with all input files

        :raises:None

        :rtype: None
        """
        self._dataframe = pd.DataFrame()
        
        if (os.path.exists(folderpath)):
            files = os.listdir(folderpath)
            files = list(filter(lambda filename: False if filename.startswith("~") else True, files))
            filepaths= map (lambda file: os.path.join(folderpath, file), files)
            for filepath in filepaths:

                try:
                    self.addNewRecord(filepath)

                except Exception as e:
                    print("Exception occurred for file: %s. Error:  %s "%(filepath,e))
                    continue

            print("\n\n\n\n\n IMPORT DATA SUCCESSFULLY\n\n\n\n")

        else:
            raise FileNotFoundError("Entered path to the import repository does not exist")
         

    def importAllFilesinFolders(self, folderpath):

        """ Function to import data from all files in folders and append them to the dataset
        To be over ridden by the derived classes.
        
        :type self: Derived IData Class
        :param self: Calling object of the derived IData class.

        :type folderpath: string
        :param folderpath: Absolute path to the repsoitory which consists of folders for each HoV and each subsequent folder has input files for each test reference.

        :raises: None

        :rtype: None
        """
        self._dataframe = pd.DataFrame()

        if (os.path.exists(folderpath)):
            HoV_folder_list = os.listdir(folderpath)
            rows_in_final_df = []
            exceptionlist=[]
            for i in HoV_folder_list:
                # Create path to a particular HoV
                path_to_HoV = os.path.join(folderpath,i)
                file_list = os.listdir(path_to_HoV)
                path_list = [os.path.join(path_to_HoV,x) for x in file_list if not x.startswith("~")]
    
                for fil_path in path_list:

            
                    self.addNewRecord(fil_path,HoV= i)


            print(" IMPORT DATA SUCCESSFULLY: ", folderpath)

        else:
            raise FileNotFoundError("Entered path to the import repository does not exist")

    def addNewRecord(self, filepath, HoV=None, ACversion=None):

        """ Funtion to add the data of a new input file to th existing dataframe.
        To be overridden by the derived class.

        :type self: Derived IData Class
        :param self: Calling object of the derived IData class.

        :type filepath: string
        :param filepath: Full path to the new input file complete with file extension.

        :type HoV: string
        :param HoV: HoV of the aircraft

        :type ACversion:string
        :param ACversion: Version of the aircraft. For example "A350-900 Step 7"

        :raises: FileNotFoundError

        :rtype: None
        :return : None
        """        

        try:
            oneline_df = self._parse(filepath)
            self._dataframe = pd.concat([self._dataframe, oneline_df], axis=0)
            print("Imported: ", filepath)
        except Exception as e:
            print("Exception occurred for file: %s. Error:  %s "%(filepath,e))

        



        # append to the self.__dataframe



    # def load_data(self, path):
    #    raise NotImplementedError
    #
    # def get_load_path(self):
    #     """
    #     Function to RETRIEVE the path from which the cleaned data from an excel file probably,
    #     will be loaded directly into a pandas dataframe.
    #     Developer please ensure that the constructors of the overriding class have a load path variable
    #     which hold the path to the excel file or sql file of the clean data from where the data is to be loaded.
    #     """
    #
    #     return self.__loadpath
    #
    # def set_load_path(self,path):
    #     """
    #     Function to SET the path from which the cleaned data from an excel file probably,
    #     will be loaded directly into a pandas dataframe.
    #     Developer please ensure that the constructors of the overriding class have a load path variable
    #     which hold the path to the excel file or sql file of the clean data from where the data is to be loaded.
    #     Set the path to the load file
    #
    #     :type self: Calling class
    #     :param self: Calling object of the Calling class
    #
    #     :type path: string
    #     :param path: Full path to the new import repository.
    #
    #     :raises: None
    #
    #     :rtype: None
    #     """
    #     if(os.path.exists(path)):
    #         self.__loadpath= path
    #     else:
    #         print("New Load path does not exists")
    

    def _parse(self, **kargs):
        """
        To parse(interpret data) an XLSX file: Abstract Function
                -- To be overridden by the respective Flow class
        :return:
        """
        raise NotImplementedError

    def export2Excel(self, filename, export_path):

        """  Creates a backup of the calling objects self._dataframe object into an excel file of the specified filename.

        :type self: Derived IData Class
        :param self: Calling object of the derived IData class.

        :type filename: string
        :param filename: Name of the file to which the data will be written

        :type export_path: string
        :param export_path: path to the repository in which the written excel file will be stored.

        :raises: None

        :rtype: string
        :return: Full path to the excel file just written by this function.
        """
        filename = filename + ".xlsx" if not filename.endswith(".xlsx") else filename
        filepath = os.path.join(export_path, filename)
        print("Writing File:", filepath, "\t SHAPE ", self._dataframe.shape)
    
        self._dataframe.to_excel(filepath)
        return filepath

    def expandedDiff(self, testFile, refFile):
        """define the expanded diff"""
        pass

    def expandedDiffRestrictors(self, testFile, refFile):
        """ Funtion to compare test and reference file and generate the result.


        :type self:Derived IData Class
        :param self: Calling object of the derived IData class

        :type testFile: string
        :param testFile: the test file
        :type refFile: string
        :param refFile: the reference file


        :raises:

        :rtype:dataframe
        """
        new_restrictor = pd.read_excel(testFile)
        old_restrictor = pd.read_excel(refFile)
        oldColumnName = new_restrictor.columns[0]
        new_restrictor.rename(columns={oldColumnName: 'HoV'}, inplace=True)
        # new_restrictor.HoV = new_restrictor.HoV.apply(self._removeFileExtension)
        # Replace nan values i.e. values which are not in old data with 0;0;0;0
        new_restrictor.fillna('0;0;0;0', inplace=True)
        new_restrictor.set_index('HoV', inplace=True)
        new_restrictor = new_restrictor.applymap(self._validate)

        old_restrictor.fillna('0;0;0;0', inplace=True)
        old_restrictor.set_index('HoV', inplace=True)
        old_restrictor = old_restrictor.applymap(self._validate)

        # old_restrictor.to_excel("old_data_before_expansion.xlsx")
        # new_restrictor.to_excel('new_data_before_expansion.xlsx')

        hov_onlynew = set(new_restrictor.index) - set(old_restrictor.index)
        # print("HOV_ONLYNEW: ", hov_onlynew, " Len: ", len(hov_onlynew))
        hov_onlyold = set(old_restrictor.index) - set(new_restrictor.index)
        # print("HOV_ONLYOLD: ", hov_onlyold, " Len: ", len(hov_onlyold))


        duplicatelist = collections.Counter(new_restrictor.index)
        new_restrictor_uniq = new_restrictor[~new_restrictor.index.duplicated(keep='last')]
        # hov_new = new_restrictor_uniq.index
        hov_old = old_restrictor.index
        new_restrictor_uniq_hov = new_restrictor_uniq[new_restrictor_uniq.index.isin(hov_old)]
        # print('new_restrictor_uniq_hov:',new_restrictor_uniq_hov.index,'len:',len(new_restrictor_uniq_hov))

        old_restrictor_hov = old_restrictor[old_restrictor.index.isin(new_restrictor_uniq_hov.index)]

        # print('New Hov:',hov_new,'len:',len(hov_new))
        # print('old hov:',old_restrictor_hov.index, 'len:',len(old_restrictor_hov))

        # col_only_old_data = set(old_restrictor_hov.columns) - set(new_restrictor_uniq.columns)
        # col_only_new_data = set(new_restrictor_uniq.columns) - set(old_restrictor_hov.columns)
        # new_expand = new_restrictor_uniq.copy(deep=True)

        col_only_old_data = set(old_restrictor_hov.columns) - set(new_restrictor_uniq_hov.columns)
        col_only_new_data = set(new_restrictor_uniq_hov.columns) - set(old_restrictor_hov.columns)
        new_expand = new_restrictor_uniq_hov.copy(deep=True)
        old_expand = old_restrictor_hov.copy(deep=True)
        for col in col_only_old_data:
            new_expand[col] = "0;0;0;0"

        for col in col_only_new_data:
            old_expand[col] = "0;0;0;0"

        # old_expand.to_excel("OLD_Expand_restrictor.xlsx")
        # new_expand.to_excel("NEW_Expand_restrictor.xlsx")

        old_expand_full = pd.DataFrame()
        new_expand_full = pd.DataFrame()
        compactdiff = pd.DataFrame()

        dia = lambda x: int(x.split(";")[0])
        fwd = lambda x: int(x.split(";")[1])
        mid = lambda x: int(x.split(";")[2])
        aft = lambda x: int(x.split(";")[3])

        for col in sorted(old_expand.columns):
            old_expand_full[col + "_dia"] = old_expand[col].apply(dia)
            old_expand_full[col + "_fwd"] = old_expand[col].apply(fwd)
            old_expand_full[col + "_mid"] = old_expand[col].apply(mid)
            old_expand_full[col + "_aft"] = old_expand[col].apply(aft)

            new_expand_full[col + "_dia"] = new_expand[col].apply(dia)
            new_expand_full[col + "_fwd"] = new_expand[col].apply(fwd)
            new_expand_full[col + "_mid"] = new_expand[col].apply(mid)
            new_expand_full[col + "_aft"] = new_expand[col].apply(aft)

        # old_expand_full.to_excel("old_expand_full.xlsx")
        # new_expand_full.to_excel("new_expand_full.xlsx")

        rest_diff = new_expand_full - old_expand_full
        # rest_diff.to_excel("full_diff_rest.xlsx")

        compactdiff = pd.DataFrame()
        old_expand_sorted = old_expand.copy().sort_index()
        for col in sorted(old_expand_sorted.columns):
            diaNew = old_expand[col].apply(dia)
            fwdNew = old_expand[col].apply(fwd)
            midNew = old_expand[col].apply(mid)
            aftNew = old_expand[col].apply(aft)

            diaOld = new_expand[col].apply(dia)
            fwdOld = new_expand[col].apply(fwd)
            midOld = new_expand[col].apply(mid)
            aftOld = new_expand[col].apply(aft)

            diadiff = list(map(str, diaNew - diaOld))
            fwddiff = list(map(str, fwdNew - fwdOld))
            middiff = list(map(str, midNew - midOld))
            aftdiff = list(map(str, aftNew - aftOld))

            combinefunc = lambda a, b, c, d: a + ";" + b + ";" + c + ";" + d

            compactdiff[col] = np.vectorize(combinefunc)(diadiff, fwddiff, middiff, aftdiff)

        compactdiff.index = old_expand_sorted.index
        # compactdiff.to_excel("compact_rest_diff.xlsx")

        return compactdiff

    def _getIndexes(self,dfObj, value):
    
        """ Get index positions of value in dataframe i.e. dfObj

        :type self: Derived IData Class
        :param self: Calling object of the derived IData class.
    
        :type dfObj: Pandas Dataframe
        :param dfObj: Input dataframe which needs to be processed
    
        :type value: object
        :param value: any value in the dataframe
    
        :raises: KeyError
    
        :rtype: List
        :return: List of Positions where vallue in input "dfObj" is equal to "value".
        """   
        listOfPos = list()
        # Get bool dataframe with True at positions where the given value exists
        result = dfObj.isin([value])
        # Get list of columns that contains the value
        seriesObj = result.any()
        columnNames = list(seriesObj[seriesObj == True].index)
        # Iterate over list of columns and fetch the rows indexes where value exists
        for col in columnNames:
            rows = list(result[col][result[col] == True].index)
            for row in rows:
                listOfPos.append((row, col))
        # Return a list of tuples indicating the positions of value in the dataframe
        return listOfPos
            
    def printDiffReport(self, df,filepath=None,tolerance= 0.001):
    
        """ Function to print the positions (Row and column) in the input dataframe where values are grater than tolerance value.
        Input dataframe is an expanded diff.
        
        :type self: Derived IData Class
        :param self: Calling object of the derived IData class.
    
        :type df: Pandas Dataframe
        :param df: Input dataframe as a result of Expanded Diff which needs to be processed.
    
        :type filepath: string
        :param filepath: Full path to the .log file to which the results are written.
    
        :type tolerance: float
        :param tolerance: tolerance value for the difference 
    
        :raises: None
    
        :rtype: None
        """    
        def difffunc(value):
            tolerance= 0.01
            if(abs(value) < tolerance):
                return 0
            else:
                return 1
       
        #filepath= os.path.join(work_dir,"/tests/RESULTS/DB0_DEF",filename)
        df=df.applymap(difffunc)
        listOfPositions = self._getIndexes(df,1)

        with open(filepath,"w") as file:
            file.write('Displaying HoV names AND Columns WITH DIFFERENCES : \n')
            file.write("\n No.of Entries with differences:{0}\n".format(len(listOfPositions)))
        
            for i in range(len(listOfPositions)):
                # Define the log string
                log_string= "\nPosition:,{0}, (Row, Column) : {1}\n".format(i,listOfPositions[i])
                file.write(log_string)
    
    # def getimportpath(self):
    #
    #     """ Get the path to the repository in network drive from where the data will be imported
    #
    #     :type self: Calling class
    #     :param self: Calling object
    #
    #     :raises:
    #     :return: Current import path
    #     :rtype: string
    #     """
    #     return self.__importpath
    #
    # def setimportpath(self,path):
    #
    #     """  Set the path to the import Repository
    #
    #
    #     :type self: Calling class
    #     :param self: Calling object of the Calling class
    #
    #     :type path: string
    #     :param path: Full path to the new import repository.
    #
    #     :raises: None
    #
    #     :rtype: None
    #     """
    #     if(os.path.exists(path)):
    #         self.__importpath= path
    #     else:
    #         print("New Import path does not exists")
    #
    #
    #
    # def process(self):
    #
    #     """ Process one file and return the Intermediate df
    #     :type self:
    #     :param self:
    #
    #     :raises:
    #
    #     :rtype:
    #     """
    #     pass
    #
    # def get_record(self, HoV):
    #     raise NotImplementedError
    #
    # def headdf(self):
    #     """ Prints the head of dataframe of the calling object of DB0_DEF_FLOW class.
    #
    #     :type self:Calling class
    #     :param self: Calling Object of LTR0 DATASET
    #
    #     :raises: None
    #
    #     :rtype: None
    #     """
    #     #self.__dataframe.reset_index(inplace=True)
    #     print(self.__dataframe.head())
    #     #print(self.__dataframe["HUM"]["UAL01"])

    def clean(self):
        raise NotImplementedError
    
    @property
    def df(self):
        return self._dataframe
    
    @df.setter
    def df(self,value_df):
        self._dataframe= value_df
    
    
    # def get_df(self):
    
    #     """ Property which returns self. dataframe
           
    #     :raises: None
    
    #     :rtype: Pandas Dataframe
    #     """    
    #     return self._dataframe
    
    # def set_df(self,data_frame):
    #     self._dataframe= data_frame
    
    # df=property(get_df,set_df)
    



        
