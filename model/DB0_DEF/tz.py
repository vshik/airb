import os
import pandas as pd
import re
from model.interfaces import IData
from model.utils.global_info import HoV_acv_df
from model.utils.global_objects import db_hov

class DB0_DEF_TZ(IData):
    def __init__(self):
        self._dataframe= pd.DataFrame()
        # self.__loadpath = "X:"
        self.__flowdefpath=r"X:/DEV/Repository/0-LTRinput_flowDef"
    

    def _readDF(self,path,file):
    
        """ Description
        
        :type self: DB0_DEF_TZ 
        :param self: Calling object of the LTR 0 Dataset
    
        :type path: string
        :param path: Path to the repository of the file in Network Drive
    
        :type file: string
        :param file: Exact filename with extension
    
        :raises:
    
        :return: Pandas Datframe corresponding to one file Of the same shape as input HOV files.
        :rtype: Pandas Dataframe
        """    #print ("Reading %s"%file)
        df=pd.read_excel(os.path.join(path, file),convert_float=True)

        print(file)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        df.drop(df.columns[df.columns.str.contains('num',case = False)],axis = 1, inplace = True)
        
        columnName=["Frame", "Length", "LAOR", "Flag", "Vdef", "CAOR", "Flag.1", "Vdef.1","CAOR.1", "Flag.2", "Vdef.2","LAOR.1", "Flag.3", "Vdef.3","V_Zone"]
        df=df.iloc[:,0:15]
        df.set_axis(labels=columnName, axis=1)
        #df= df[df["Frame"].notnull()]
        
        # drop the first row with garbage values
        df.drop(0,inplace=True)
        print(df.head(10))
        # df["LAOR"]= df["LAOR"].fillna(0).astype(int)
        # df["LAOR"]= df["LAOR"].fillna(0).astype(int)
        print(df.head(10))
        return df
    
    def _process(self,raw_df,HoV):
    
        """ Process the input raw dataframe perform some cleaning based on Aircraft version and return
        a one row dataset .

        :type self: DB0_DEF_TZ 
        :param self: Calling object of the LTR 0 Dataset
    
        :type raw_df: Pandas Dataframe
        :param raw_df: Input Dataframe returned by self._readDF. 
    
        :type HoV: string
        :param HoV: HoV of the aircraft.
    
        :raises: None
    
        :rtype: Pandas Dataframe
        :return: Pandas Dataframe (preprocessed) with one row corresponding to the HoV file.
        """    
        acv_df= db_hov.df.set_index("HoV")
        #acv_df= HoV_acv_df.set_index("HoV")
        ac_version= acv_df.at[HoV,"AC Version"]
        no_of_tzs= 8
        columnslist=["TZ"+ str(i+1) for i in range(no_of_tzs-1)]
        
        if(ac_version=="A350-900"or ac_version=="A350-900 Step7"):
            columnslist.append("AFT-GAL")

        
        if(ac_version=="A350-1000"or ac_version=="A350-1000 Step7"):
            no_of_tzs= 9            
            columnslist.append("TZ8")
            columnslist.append("AFT-GAL")

        #columnslist.extend(["Bulk_cc","Total"])
        
        tz_flow_values= raw_df[["V_Zone"]].dropna()
        #tz_flow_values= tz_flow_values.reset_index()

        print(tz_flow_values.head())
        # tz_flow_values= tz_fl
        # list(map(lambda x: round(x,3),tz_flow_values))
        
        process_df= tz_flow_values.T

        # Take the Bulk cc and total values also
        process_df=process_df.iloc[:,:no_of_tzs+2]
        
        #Filter only the tz values
        tz_df= process_df.iloc[:,:no_of_tzs]
        tz_df.columns= columnslist
        
        total_flow=process_df.iat[0,no_of_tzs+1] 
        tz_df["Total"]= total_flow
        print(tz_df.head())
        return tz_df.copy()
    
    def _parse(self, filename, path,HoV= None):
    
        """ Parse the data from one file and return a dataframe with a single row corresponding to that particular
        HoV after applying all preprocessing , cleaning and postprocessing of data. The returned dataframe will be concatenated directly 
        to the self.__dataframe.  
        
        
        :type filename: string
        :param filename: Full filename with extension. for example("AAR01.xlsx")
    
        :type path: string
        :param path: Path to the repository of the file in Network Drive
        
        :raises:
    
        :rtype:Pandas Dataframe
        :return: Dataframe with one row corresponding to the file, cleaned and indexed by HoV.
        """
        if(HoV==None):   
            HoV= re.sub(r'\.x[a-z]*$','',filename)
        raw_df= self._readDF(path,filename)
        processed_df= self._process(raw_df=raw_df,HoV=HoV)
        processed_df= processed_df.fillna(0.0)
        processed_df.index=[HoV]
        processed_df.index.name= "HoV"
        # print(processed_df.index)
        return processed_df

    def __postprocess_df(self):
        """
         Removes NaN values from self.__dataframe. Add code here to do postprocessing on whole dataframe.

        :type self: DB0_DEF_TZ 
        :param self: Calling object of the LTR 0 Dataset
    
        :raises: None

        :rtype: None
        """   
        df= self._dataframe.fillna(0.0)
        self._dataframe= df
        
    
    def addNewRecord(self, filepath,HoV=None):

        """ Append a new record to the LTR 0 TZ dataframe. The arguements are set from the GUI browse utitlity.
        Only appending of new records is supported modification of existing records is not supported.
        
        :type self: DB0_DEF_TZ 
        :param self: Calling object of the LTR 0 Dataset
       
        :type filepath:string
        :param filepath: Full path to the file which needs to be ingested and appended to dataframe.

        :raises: FileNotFoundError
    
        :rtype: None
        :return: None
        """    

        if(os.path.exists(filepath)):
            #self.load_data()
            path_elements= os.path.split(filepath)
            parent_repo =path_elements[0]
            filename= path_elements[1]
            file_df = self._parse(filename, parent_repo,HoV)
            try:
                    self._dataframe=pd.concat([self._dataframe,file_df],axis=0)
                
            except:
                    print ("Exception occurred for: ",filename)
            #self.export()  

                                     
        else:
            raise FileNotFoundError("Entered path to the File does not exist")

    
        
    def get_record(self,HoV):
    
        """ Description
        
        :type self:DB0_DEF_TZ
        :param self: Calling Object of LTR0 DATASET
    
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
            return self._dataframe.loc[HoV,:].values.tolist()
        except KeyError:
            print("No such HoV exists in DB0-DEF")
       
             
        

if __name__=="__main__":

    curdir= os.getcwd()
    print(curdir)
    export_folderpath = os.path.join(curdir,"tests\OUT\DB0_DEF")
    print(export_folderpath)
    # Please change the below path to your respective network location
    folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\0-LTRinput_flowDef"
    
    usecase= DB0_DEF_TZ()
    # df = usecase._parse("BAW01.xlsx","X:/DEV/Repository/0-LTRinput_flowDef")
    # print(df.head())
    usecase.importAllFiles(folderpath=folderpath)
    print(usecase.df.head())
    print(usecase.get_record("BAW01"))
    print(usecase.get_record("BAv01"))
    # usecase.process(df,"BAW01") 
    # curdir= os.getcwd()
    
    
    LTR0TZ = DB0_DEF_TZ()

    #Test 1
    LTR0TZ.importAllFiles(folderpath)
    print(LTR0TZ.df.head())
    testfile1= LTR0TZ.export2Excel("test1DB0_TZ.xlsx", export_folderpath)
    # exp_diff1=LTR0TZ.expandedDiff(testfile1,reffile1)
    # print("Expanded diff successfull")
    # log_filename="DB0_DEF_FLOW.log"
    # diff_report_path= os.path.join(curdir, "tests\RESULTS\DB0_DEF",log_filename)
    # LTR0TZ.printDiffReport(exp_diff1,filepath=diff_report_path)

    #test 2:
    LTR0TZ.addNewRecord(filepath="X:\DEV\Repository\VIR02.xlsx")
    testfile2= LTR0TZ.export2Excel("test2DB0_TZ.xlsx", export_folderpath)
    # exp_diff2=LTR0TZ.expandedDiff(testfile2,reffile2)
    # print("Expanded diff successfull")
    # LTR0TZ.printDiffReport(exp_diff2,filepath=diff_report_path)     
