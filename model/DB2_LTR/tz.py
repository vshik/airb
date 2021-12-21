from datetime import datetime
import os
import pandas as pd
import re
from model.interfaces import IData
from model.utils.global_info import HoV_acv_df
from model.utils.global_objects import db_hov

class DB2_LTR_TZ(IData):
    def __init__(self):
        self._dataframe= pd.DataFrame()

    def _readDF(self,filepath):
    
        """ Reads a dataframe as it is from an excel file and returns only the dataframe containing 
        Total TZ Flow information.
        
        :type self: DB2_LTR_TZ
        :param self: Calling object of the DB2_LTR_TZ class
    
        :type filepath: string
        :param filepath: Full path to the file to be read into a Dataframe complete with file extension.
    
        :raises: FileNotFoundError
    
        :rtype: Pandas Dataframe
        :return: Pandas Datframe which contains information on total TZ flow
        """    
        raw_df = pd.read_excel(filepath,sheetname="Flow",header= None,skiprows=3)
        firstrow= raw_df.iloc[0].values.tolist()
        tz_col_index= firstrow.index("Total TZ")
        tz_col_df= raw_df.iloc[:,tz_col_index:tz_col_index+5]
        return tz_col_df
    
    def _create_test_ref(self,df,HoV,fil_path):
    
        """ Add Test Reference column to the final horizontal dataframe which constitutes one row in 
        self.__dataframe(LTR2 Total TZ Flow data). This row corresponds to one HoV and Test Reference combination.
        
        :type self: DB2_LTR_TZ
        :param self: Calling object of the DB2_LTR_TZ class
    
        :type df: Pandas Dataframe
        :param df: Horizontal dataframe corresponding to one row in the LTR2 Total TZ Flow Data
    
        :type HoV: string
        :param HoV: HoV of the aircraft
    
        :type fil_path: string
        :param fil_path: Full path to the file in the input repository which is being parsed,complete with file extension. 
    
        :raises: None

        :return: A Horizontal Dataframe corresponding to one row of the LTR 2 total TZ flow dataset with an added Test Reference Column.  
        :rtype: Pandas Dataframe
        """    
        filename= str(os.path.split(fil_path)[1])
        #remove file extension from file name
        filename= re.sub(r'\.x[a-z]*$','',filename)
        #experiment_type_string=""      
              
        # CHeck if filename contains HoV
        if(filename.find(HoV) != -1):
            file_index= filename.rfind("-")
            experiment_type_string= filename[file_index+1:]
            df.insert(0,"Test Reference",experiment_type_string)
        else:
            experiment_type_string= filename.replace("-","")
            df.insert(0,"Test Reference",experiment_type_string)
        
        return df



    def _processdf(self, tz_col_df, HoV, ac_version= None):
    
        """ Function to process the input TZ dataframe resulting from readDf operation
        
        :type self: DB2_LTR_TZ
        :param self: Calling object of the DB2_LTR_TZ class
    
        :type tz_col_df: Pandas Dataframe
        :param tz_col_df: Input dataframe containing Total TZ flow Information resulting from _readDF function.
    
        :type HoV: string
        :param HoV: HoV of the aircraft
        
        :type ac_version: string
        :param ac_version: Version of the aircraft (example, "A350-900 Step7")
    
        :raises: None

        :rtype: Pandas Dataframe
        :return: Dataframe with a single row containing information on total flow values of all TZs. 
        """    
        acv_df= db_hov.df.set_index("HoV")
        #acv_df= HoV_acv_df.set_index("HoV")
        
        #Get the Aircraft version from the global object
        if(ac_version == None):
            ac_version= acv_df.at[HoV,"AC Version"]
        
        no_of_tzs= 8

        columnslist=["TZ"+ str(i+1) for i in range(no_of_tzs-1)]
        

        """
        Alter number of TZs according to the A/C version

        """
        if(ac_version=="A350-900"or ac_version=="A350-900 Step7"):
            columnslist.append("AFT-GAL")

        
        if(ac_version=="A350-1000"or ac_version=="A350-1000 Step7"):
            no_of_tzs= 9            
            columnslist.append("TZ8")
            columnslist.append("AFT-GAL")

        def _getdatalist(tz_col_df):
            first_col= tz_col_df.iloc[:,0].values.tolist()
            data_list= []
            for index,element in enumerate(first_col):
                if(element == "Total TZ" ):
                    flow_val= tz_col_df.iloc[index,1]
                    data_list.append(flow_val)
                if(element == "AFT Galley"):
                    flow_val= tz_col_df.iloc[index,2]
                    data_list.append(flow_val)
            return data_list
        
        print(tz_col_df.head(50))
        tz_data_list= _getdatalist(tz_col_df)
        tz_data_list.pop(0)
        while(len(columnslist) >  len(tz_data_list)):
            tz_data_list.append(0)

        #Generate a dataframe out of the TZ data list
        trandf= pd.DataFrame(data= [tz_data_list] , columns= columnslist)


        return trandf   
    
    def _parse(self,filepath,HoV,db2_ltr_test_reference= None,ac_version= None):
    
        """ Function to parse an input file from end to end. All transformations and data cleaning is done within this function. 
        This function returns a dataframe with one row indexed on HoV and Test Reference. The returned dataframe can be directly concatenated to 
        self._dataframe.
        
        :type self: DB2_LTR_TZ
        :param self: Calling object of the DB2_LTR_TZ class
    
        :type filepath: string
        :param filepath: Full path to the file to be parsed (complete with file extension.)
    
        :type HoV: string
        :param HoV: HoV of the aircraft
    
        :type db2_ltr_test_reference: string
        :param db2_ltr_test_reference: Test reference corresponding to the input file in the LTR 2 Dataset.
    
        :type ac_version: string
        :param ac_version: Version of the aircraft (example, "A350-900 Step7")
    
        :raises: FileNotFoundError
    
        :rtype: Pandas Dataframe
        :return: Pandas dataframe with one row multiIndex on HoV and Test Reference 
        """    
        raw_df= self._readDF(filepath)
        processed_df= self._processdf(raw_df,HoV=HoV,ac_version= ac_version)
        processed_df= processed_df.fillna(0.0)
        if(db2_ltr_test_reference== None):
            processed_df= self._create_test_ref(processed_df,HoV,filepath)
        else:
            processed_df["Test Reference"]= db2_ltr_test_reference
        processed_df["HoV"]= HoV
        processed_df= processed_df.set_index(["HoV","Test Reference"])
        # print(processed_df.index)
        return processed_df

    def addNewRecord(self, filepath, HoV=None,db2_ltr_test_reference= None,ACversion=None):
    
        """ Function to parse a New Input file  and add the record to the existing dataframe with Total TZ 
        flow values for DB2_LTR Dataset
        
        :type self: DB2_LTR_TZ
        :param self: Calling object of the DB2_LTR_TZ class
    
        :type filepath: string
        :param filepath: Full path to the file to be read into a Dataframe complete with file extension.
    
        :type HoV: string
        :param HoV: HoV of the aircraft
    
        :type db2_ltr_test_reference: string
        :param db2_ltr_test_reference: Test reference corresponding to the input file in the LTR 2 Dataset.
    
        :type ACversion: string
        :param ACversion: Version of the aircraft (example, "A350-900 Step7")
    
        :raises: FileNotFoundError
    
        :rtype: None
        :return: None
        """    
        try:
            oneline_df = self._parse(filepath,HoV,db2_ltr_test_reference= db2_ltr_test_reference,ac_version=ACversion)
            self._dataframe = pd.concat([self._dataframe, oneline_df], axis=0)
            print("Imported: ", filepath)
        except Exception as e:
            print("Exception occurred for file: %s. Error:  %s "%(filepath,e))
    
    def _get_record(self,HoV):
    
        """ Private function to get a record corresponding to one HoV
        
        :type self:DB2_LTR_TZ
        :param self: Calling Object of LTR2  DATASET
    
        :type HoV: string
        :param HoV: HoV of the Aircraft
    
        :raises: None
    
        :rtype: Pandas Dataframe
        :return: A dataframe with one row corresponding to the given HoV
        """    
        try:
            """
            Returning a list for the time being 
            
            """
            return self._dataframe.loc[HoV,:]
            
        except KeyError:
            print("No such HoV exists in DB2_LTR")
    

if __name__=="__main__":
    # ltr2_tz= DB2_LTR_TZ()
    # path="X:\DEV\Repository\D0008-MIX22.xlsm"
    # df= ltr2_tz._parse(path,"D0008")
    # print(df.head())
  

    curdir= os.getcwd()
    print(curdir)
    export_folderpath = os.path.join(curdir,"tests\OUT\DB2_LTR")
    print(export_folderpath)
    # Please change the below path to your respective network location
    folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\2-LTR"
    
    usecase= DB2_LTR_TZ()
    # df = usecase._parse("BAW01.xlsx","X:/DEV/Repository/0-LTRinput_flowDef")
    # print(df.head())
    usecase.importAllFilesinFolders(folderpath=folderpath)
    print(usecase.df.head())
    print(usecase._get_record("BAW01"))
    print(usecase._get_record("BAv01"))
    # usecase.process(df,"BAW01") 
    # curdir= os.getcwd()
    
    
    LTR2TZ = DB2_LTR_TZ()

    #Test 1
    LTR2TZ.importAllFilesinFolders(folderpath)
    print(LTR2TZ.df.head())
    testfile1= LTR2TZ.export2Excel("test1DB2_TZ.xlsx", export_folderpath)
    # exp_diff1=LTR0TZ.expandedDiff(testfile1,reffile1)
    # print("Expanded diff successfull")
    # log_filename="DB0_DEF_FLOW.log"
    # diff_report_path= os.path.join(curdir, "tests\RESULTS\DB0_DEF",log_filename)
    # LTR0TZ.printDiffReport(exp_diff1,filepath=diff_report_path)

    #test 2:
    new_record_path= os.path.join(curdir,"tests\\NEW\DB2_LTR\D0008-MIX22.xlsm")
    LTR2TZ.addNewRecord(filepath=new_record_path,HoV= "D0008")
    testfile2= LTR2TZ.export2Excel("test2DB2_TZ.xlsx", export_folderpath)
    # exp_diff2=LTR0TZ.expandedDiff(testfile2,reffile2)
    # print("Expanded diff successfull")
    # LTR0TZ.printDiffReport(exp_diff2,filepath=diff_report_path)     



                

            
            
        
