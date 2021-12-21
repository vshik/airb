

from model.interfaces import IData
import os
import pandas as pd
import re
import numpy as np


class DB2_LTR_REST(IData):
    def __init__(self):
        self._dataframe= pd.DataFrame()
        self.__loadpath = "X:"
        self.export_path=r"X:/Export"
        self.__restictordefpath="X:\DEV\Repository\\2-LTR"


    
    def _clean_concatenated_rest_df(self,restrictor_concat_df):
    
        """ Clean the concatenated restrictor Datset. This function cleans invalid values 
         in the vertical (2 column) dataset which is obtained after parsing a single file 
         and concatenating the datframes for all temperature zones. It return a cleaned dataset after 
         replacing bad values like n/a, "Na" and other invalid string patterns. 
        
        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type restrictor_concat_df: Pandas Dataframe
        :param restrictor_concat_df: Concatenated vertical dataframe with 2 columns resulting from self.process()
    
        :raises: None
    
        :return: Cleaned vertical dataframe with invalid values like nan ,"n/a" and other invalid strings removed
        :rtype: Pandas Dataframe
        """    
        # Drop all Empty Columns
        restrictor_concat_df= restrictor_concat_df.dropna(how= "all",axis= 1)   
        
        # SUbset only 2 columns
        restrictor_concat_df= restrictor_concat_df.iloc[:,:2]   
        
        #Drop all Empty rows 
        restrictor_concat_df= restrictor_concat_df.dropna(how= "all",axis=0) 
        print(restrictor_concat_df.iloc[:,:2])
    
        # Reset Index
        restrictor_concat_df= restrictor_concat_df.reset_index()
        # Drop the extra index column
        restrictor_concat_df= restrictor_concat_df.drop("index",axis=1)        
    

        """
        CLean the dataset
        """
        restrictor_concat_df= restrictor_concat_df.replace(['^\D*\\n\D*','^[nan;]+','^[-;]+','\w*(nan)$','n/a',';-'],[np.nan,np.nan,np.nan,np.nan,"0",";0"],regex=True)
        
        restrictor_concat_df= restrictor_concat_df.dropna(how= "all",axis=0) 
        restrictor_concat_df= restrictor_concat_df.fillna("0;0;0;0")      


        # SEt index tor Restrictors
        #restrictor_concat_df = restrictor_concat_df.set_index("Restrictor")
        print(restrictor_concat_df)

        return restrictor_concat_df

    def _create_test_ref(self,df,HoV,fil_path):
    
        """ Add Test Reference column to the final horizontal dataframe which constitutes one row in 
        self.__dataframe(LTR2 Restrictor Definition data). This row corresponds to one HoV and Test Reference combination.
        
        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type df: Pandas Dataframe
        :param df: Horizontal dataframe corresponding to one row in the LTR2 Restrictor Definition Data
    
        :type HoV: string
        :param HoV: HoV of the aircraft
    
        :type fil_path: string
        :param fil_path: Full path to the file in the input repository which is being parsed,complete with file extension. 
    
        :raises: None

        :return: A Horizontal Dataframe corresponding to one row of the LTR 2 Restrictor definition dataset with an added Test Reference Column.  
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

    def _reformat_tz_df(self,df):
    
        """ Function to perform basic cleaning operations on restrictor definition values in each temperature zone. 
        The function reformats an input dataframe of restrictor definition for one temperature zone, cleans, adds a datastring 
        and returns the cleaned dataframe for that temperature zone. The returned dataframe consists of two columns namely, Restrictor
        and Datastring. Datastring is a single string representation which combines multiple numeric values of a restrictor
        defination or configuration. 
        
        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type df: Pandas Dataframe
        :param df: Dataframe with restriuctor defination values for one particular Temperature Zone
    
        :raises: None
    
        :return: A cleaned Dataframe, corresponding to a particular temperature zone, and having only two columns.  
        :rtype:Pandas Dataframe
        """       
        """
        Function to do basic cleaning on restrictor definition in each tz
        df: Restrictor definition for a particular tz
        
        """
        def addDataStringToTz(df,list_of_columns):
            """ aDD A cOLUMN TO CONCAT DATAFRAME WHICH CONTAINS ALL THE DATA AS A STRING
                df: Data frame to which a Datastring column has to be added
                list of columns to be concatenated into the datA STRING
                CAUTION:
                only the first four will be added
            """
            column_list= ["Restrictor","Hole","FWD","MID","AFT"]
            df.columns = column_list
            
            list_of_columns= column_list[1:]
            column_dict= {}
            for i in column_list:
                column_dict[i]= "str"
            df= df.astype(column_dict)
            
            # concat_df["Target (l/s)"]= concat_df["Target (l/s)"].astype(str)
            # concat_df["Deviation (%)"]= concat_df["Deviation (%)"].astype(str)                    
            df["DataString"]= df[list_of_columns[0]] +";"+ df[list_of_columns[1]] +";"+ df[list_of_columns[2]]+";"+df[list_of_columns[3]]
            #df["DataString"]= df["DataString"].replace('\D+;\D+;\D+;\D+',0,regex= True)
            print(df.columns)
            print(column_list)
            return df
        
        #Extract the temperature zone
        temp_zone= df.iloc[0,0]
        
        # check for empty datatframe
        if(df.isnull().values.all()):
            return df

        # Remove all empty rows
        df= df.dropna(axis=0,how="all")               
        

        """
        SET THE NEW COLUMN NAMES
        """
        new_column_names = df.iloc[1,:].values.tolist()
        df= df.iloc[2:,:]
        df.columns= new_column_names
        listcol=df.columns.values.tolist()[1:]
        
        """
        ADD DATASTRING TO COMBINE ALL THE DATA ENTRIES

        """                
        df= addDataStringToTz(df,listcol)
        
        #generate Comparable column names

        if(str(temp_zone).upper() not in ["TZ1","TZ2","TZ3","TZ4","TZ5","TZ6","TZ7","TZ8"]):
            temp_zone= "Other"
        
        df["Restrictor"]= "Restrictors"+"-"+ temp_zone + "-"+ df["Restrictor"]            


        # SUBSET THE DATAFRAME ON RESTRICTORS AND DATASTRING

        df= df.loc[:,["Restrictor","DataString"]]

        return df   

    def _read_df(self,path):
    
        """ Read the data from the file as it is and return a raw dataframe of the same shape as the input data.

        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type path: string 
        :param path: Full path to the file which needs to be imported, complete with file extension. 
    
        :raises:FileNotFoundError
    
        :return: Pandas dataframe of the same shape as the input data, read from the file as it is. 
        :rtype: Pandas Dataframe
        """    
        #Read the raw restrictor files
        raw_restrictor_df = pd.read_excel(path,sheetname="Restrictor",skiprows=1,header= None)
        print(raw_restrictor_df.shape)
        return raw_restrictor_df

    def _process(self,raw_restrictor_df):
    
        """ Process the raw file dataframe and return an intermediate dataframe. 
         This function handles two type of input data formats .
         One in which data for all temperature zones are aligned side by side, and
         other in which  temperature zone tables are presented in groups of 4 TZs.
         The returned dataframe is vertical and has two columns namely Restrictor and Datastring.
         It contains the combined data for all the temperature zones . The returned dataframe is passed to 
         self._clean_concatenated_rest_df() for further cleaning.

        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type raw_restrictor_df: Pandas Dataframe
        :param raw_restrictor_df: Dataframe of the same shape as the input data; resulting after reading the excel file as it is.
    
        :raises: None

        :return: Intermediate pandas dataframe with 2 columns with combined data from all temperature zones. 
        :rtype: Pandas Dataframe
        """    
        # Remove the restrictor rows with whitespaces.
        restrictor_df_trim= raw_restrictor_df.dropna(axis=0,how="all")
        #restrictor_df_trim= restrictor_df_trim.dropna(axis=1,how="all")
        # Get the first row to determine the pattern of the file
        restrictor_first_row = restrictor_df_trim.iloc[0].values.tolist()
        length_of_first_row= len(restrictor_first_row)
        print(length_of_first_row)

        if(length_of_first_row> 34):
            print("FORMAT 1 aLL TZ TOGETHER")
            first_column_list=restrictor_df_trim.iloc[:,0].values.tolist()
            print(first_column_list.index("FCRC"))        
            tz1_8_row_limit= first_column_list.index("FCRC")
            print(first_column_list)
            try:
                last_limit = first_column_list.index("Legende")
            except:
                last_limit= len(first_column_list)-1
            format_1_df_list=[]

            #Loop for first row of tzs
            #
            column_iter=0
            while(column_iter < length_of_first_row):

                tz_df = restrictor_df_trim.iloc[:tz1_8_row_limit,column_iter:column_iter+5]
                format_1_df_list.append(tz_df)
                column_iter= column_iter +5 
            
            ##LOOP FOR second row of tz:

            column_iter=0
            while(column_iter < (length_of_first_row-4)):

                tz_df = restrictor_df_trim.iloc[tz1_8_row_limit:last_limit,column_iter:column_iter+5]
                format_1_df_list.append(tz_df)
                column_iter= column_iter +5 
            
            # Reformat each datafframe for Tz and store it in a list
            reformatted_df_list = list(map(self._reformat_tz_df,format_1_df_list))
            
            # Concatenate the dataframes into a vertical dataframe
            restrictor_concat_df= pd.concat(reformatted_df_list,axis=0)
            return restrictor_concat_df

        elif(len(restrictor_first_row) < 35): 
            print("FORMAT 2 TZ ARE WRAPPED AROUND")
            
            """
            Since tz1 to tz4 are in the first row we will find column indexes first
            
            """
            zero_index= 0
            tz1_index= zero_index +5
            tz2_index= tz1_index + 6
            tz3_index= tz2_index + 6
            tz4_index= tz3_index + 6

            print(restrictor_df_trim.head())

            first_column_list=restrictor_df_trim.iloc[:,0].values.tolist()
            tz1_4_row_limit= first_column_list.index("TZ5")
            tz5_8_row_limit= first_column_list.index("FCRC")
            fcrc_row_limit= first_column_list.index("CVS")
            
            try:
                cvs_row_limit = first_column_list.index("Legende")
            except:
                cvs_row_limit= len(first_column_list)-1

            second_tz_group=set(restrictor_df_trim.iloc[tz1_4_row_limit,:].dropna().values.tolist())
            print("SECOND TZ GOUP:",second_tz_group)
            #Get the number of tzs in the second row of tables
            no_of_tzs_second = len(second_tz_group)

            print("NO OF TZS SECOND ROW:",no_of_tzs_second)

            """
            EXTRACT DATFRAMES FOR THE FIRST ROW OF TZS

            """
            tz1_df= restrictor_df_trim.iloc[:tz1_4_row_limit,zero_index:tz1_index]
            tz2_df= restrictor_df_trim.iloc[:tz1_4_row_limit,tz1_index+1:tz2_index]
            tz3_df= restrictor_df_trim.iloc[:tz1_4_row_limit,tz2_index+1:tz3_index]
            tz4_df= restrictor_df_trim.iloc[:tz1_4_row_limit,tz3_index+1:tz4_index]

            fcrc_df= restrictor_df_trim.iloc[tz5_8_row_limit:fcrc_row_limit,zero_index:tz1_index]
            ccrc_df= restrictor_df_trim.iloc[tz5_8_row_limit:fcrc_row_limit,tz1_index+1:tz2_index]

            cvs_df= restrictor_df_trim.iloc[fcrc_row_limit:cvs_row_limit,zero_index:tz1_index]
            avs_b_df= restrictor_df_trim.iloc[fcrc_row_limit:cvs_row_limit,tz1_index+1:tz2_index]
            fwd_cc_df= restrictor_df_trim.iloc[fcrc_row_limit:cvs_row_limit,tz2_index+1:tz3_index]
            bulk_cc_df= restrictor_df_trim.iloc[fcrc_row_limit:cvs_row_limit,tz3_index+1:tz4_index]

            df_list=[]

            if(no_of_tzs_second==4):

                #thus there are 4 tables of tzs
                tz5_index= zero_index +5
                tz6_index= tz5_index + 6
                tz7_index= tz6_index + 6
                tz8_index= tz7_index + 6

                """
                SUBSETTING THE DATAFRAMES WITH 4 TZS IN SECOND ROW

                CHECK FILE AAR01FINAL XLSX TO VERIFY THE INDEXING AND SUBSETTING

                """
                tz5_df= restrictor_df_trim.iloc[tz1_4_row_limit:tz5_8_row_limit,zero_index:tz5_index]
                tz6_df= restrictor_df_trim.iloc[tz1_4_row_limit:tz5_8_row_limit,tz5_index+1:tz6_index]
                tz7_df= restrictor_df_trim.iloc[tz1_4_row_limit:tz5_8_row_limit,tz6_index+1:tz7_index]
                tz8_df= restrictor_df_trim.iloc[tz1_4_row_limit:tz5_8_row_limit,tz7_index+1:tz8_index]

                df_list= [tz1_df,tz2_df,tz3_df,tz4_df,tz5_df,tz6_df,tz7_df,tz8_df,fcrc_df,ccrc_df,cvs_df,avs_b_df,fwd_cc_df,bulk_cc_df]
            
            elif(no_of_tzs_second<4):

                # thus there are 3 tables of tzs in the second row of tables
                tz5_index= zero_index +5
                tz6_index= tz5_index + 6
                tz7_index= tz6_index + 6  

                """
                SUBSETTING THE DATAFRAMES WITH 3 TZS IN SECOND ROW

                CHECK FILE AAR01 FINAL XLSX TO VERIFY THE INDEXING AND SUBSETTING

                """
                tz5_df= restrictor_df_trim.iloc[tz1_4_row_limit:tz5_8_row_limit,zero_index:tz5_index]
                tz6_df= restrictor_df_trim.iloc[tz1_4_row_limit:tz5_8_row_limit,tz5_index+1:tz6_index]
                tz7_df= restrictor_df_trim.iloc[tz1_4_row_limit:tz5_8_row_limit,tz6_index+1:tz7_index]

                df_list= [tz1_df,tz2_df,tz3_df,tz4_df,tz5_df,tz6_df,tz7_df,fcrc_df,ccrc_df,cvs_df,avs_b_df,fwd_cc_df,bulk_cc_df]
            
            reformatted_df_list = list(map(self._reformat_tz_df,df_list))
        
            #Vertical dataframe for all restrictors

            restrictor_concat_df= pd.concat(reformatted_df_list,axis=0)
            return restrictor_concat_df
        
        else:
            print("INVALID INPUT")
            return 

    def __postprocess_df(self,df):
    
        """  Apply some postprocessing on the conmbined dataframe for multiple HoV and Test Reference combinations.
        The input Dataframe would look like a subset of the LTR2 Restrictor Defination Dataset. The input dataframe
        is a result of concatenating multiple "single row" dataframes. Each single row dataframe has one row correponding to the 
        parsed input file and results from self.parse().

        This function performs some data cleanimg operations on the combined dataframe level.

        
        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type df: Pandas Dataframe
        :param df: Output datframe obtained after concatenating multiple single row dataframes.
    
        :raises:

        :return: The Cleaned output dataframe after replacing nan values and other invalid string patterns.
        :rtype: Pandas Dataframe
        """    
        # Replace all Nan values with the valid O string
        df = df.fillna("0;0;0;0")
        
        #Replace "Frame" at the beginning of a string with "0" 
        df= df.replace('^Frame',"0",regex=True)
        return df
        
        

    def _parse(self, path, HoV, db2_ltr_test_reference= None):
    
        """ Parse a single file from a path and generate a single row dataframe corresponding to one HoV and Test Reference combination.
        This function handles reading, processing and cleaning (end to end parsing) of files and results in a single row dataframe.
        These dataframes can then be comnbined to form an Output dataframe or a dataset which looks like a subset of the LTR2 Restrictor 
        Definition dataset.

        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type path: string
        :param path: Full path to the file which needs to be parsed, complete with file extension.
    
        :type HoV: string
        :param HoV: HoV of the aircraft.

        :type db2_ltr_test_reference: string
        :param db2_ltr_test_reference: Test reference corresponding to the input file in the LTR 2 Dataset.
    
        :raises: FileNotFoundError
    
        :return: Single Row Pandas dataframe corresponding to one parsed file.  
        :rtype: Pandas Dataframe
        """    
        # Read the raw data 
        raw_restrictor_df= self._read_df(path)

        """Below function self._process generates the intermediate 2 column datset for further processing
        The Below function generates a two column dataframe namely "Restrictor" and "Datastring".
        The Restrictor column values are of the type "TZ1-R101"
        The Datastring columns are of the type "0;0;0;0"
        """
        restrictor_concat_df = self._process(raw_restrictor_df)
        
        """Perform some cleaning on the final 2 column dataframe """
        restrictor_concat_df= self._clean_concatenated_rest_df(restrictor_concat_df) 
        
        #Creates columns  TZ and Restrictor using df.apply for multiindexing.
        # Note that the dataframe is still a vertical one which needs to be transposed to obtain the row dataframe. 
        restrictor_concat_df["TZ"]= restrictor_concat_df["Restrictor"].apply(lambda x: x.split("-")[1])
        restrictor_concat_df["Restrictor"]= restrictor_concat_df["Restrictor"].apply(lambda x: x.split("-")[2])
        
        #Generates multindex on TZ and Restrictor using df.set _index
        restrictor_concat_df= restrictor_concat_df.set_index(["TZ","Restrictor"])
        
        
        """
        CREATE TRANSPOSE FOR RESTRICTOR DTAFRAME
        """
        restrictor_transpose_df = restrictor_concat_df.T
        print(restrictor_transpose_df)

        # Generate the single row dataframe by transposing the single column multiindexed datframe.
        tran_df= restrictor_transpose_df

        #Below code inserts HoV and Test Reference columns into the single row dataframe (tran_df)  
        tran_df["HoV"]= HoV
        if(db2_ltr_test_reference==None):
            tran_df= self._create_test_ref(tran_df,HoV,path)
        else:
            tran_df["Test Reference"] = db2_ltr_test_reference
        
        # Create multindex on HoV and Test Reference using df.set_index.
        tran_df= tran_df.set_index(["HoV","Test Reference"])


        #Return the final single row datframe multindexed on rows and columns.
        return tran_df  

    def addNewRecord(self, filepath, HoV, ACversion= None, db2_ltr_test_ref= None):

        """ Add a new record into the existing dataframe by parsing a single input file.

        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type filepath: string
        :param filepath: Full path to the file that needs to be parsed, complete with file extension.
    
        :type HoV: string
        :param HoV: HoV of the aircraft
    
        :type ACversion: string 
        :param ACversion: One of the allowed aircraft versions namely: A350-900, A350-1000, A350-900 Step7,A350-1000 Step 7
    
        :type db2_ltr_test_reference: string
        :param db2_ltr_test_reference: Test reference corresponding to the input file in the LTR 2 Dataset.

        :raises: FileNotFoundError
    
        :rtype: None
        """    
        #self.load_data()
        if(os.path.exists(filepath)):
            path_elements= os.path.split(filepath)
            file_df = self._parse(filepath, HoV,db2_ltr_test_reference=db2_ltr_test_ref)
            filename= path_elements[1]
            try:
                    self._dataframe=pd.concat([self._dataframe,file_df],axis=0)
                
            except:
                    print ("Exception occurred for: ",filename)
                                            
        else:
            raise FileNotFoundError("Entered path to the File does not exist")
        #self.export()
        self._dataframe=self.__postprocess_df(self._dataframe)

    def importAllFilesinFolders(self, path=None):
    
        """ Import data from multiple input excel files and add it to the existing Pandas Dataframe.
        This functionality is optional but might have useful applications in future.This function is to import files from a
        input repository containing folders corresponding to each HoV.Each such HoV folder in turn contains the input files.

        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type path:string
        :param path: Full path to the import repository holding folders for each HoV 
         where each folder has an input file for each Test Reference. 
    
        :raises:None
    
        
        :return: None
        :rtype: None 
        """    
        if(path==None):
            path = self.__restictordefpath
        
        if(os.path.exists(path)):
            #generate hov list
            #this is also hov list
            HoV_folder_list= os.listdir(path)
            output_df= pd.DataFrame()
            rows_in_final_df = []
            for i in HoV_folder_list:
                # Create path to a particular HoV
                path_to_HoV = os.path.join(path,i)
                file_list = os.listdir(path_to_HoV)
                path_list = [os.path.join(path_to_HoV,x) for x in file_list if not x.startswith("~")]
                
                for fil_path in path_list:
                #   if(str(fil_path)
                    try:                                
                        file_ingested_df = self._parse(fil_path, i)
                        rows_in_final_df.append(file_ingested_df)
                    except:
                        continue
                    
                        
            output_df= pd.concat(rows_in_final_df,axis=0)
            output_df= self.__postprocess_df(output_df)
            
            self._dataframe= pd.concat([self._dataframe,output_df],axis= 0)
            
            print("\n\n\n\n\n IMPORT DATA SUCCESSFULLY\n\n\n\n")


        else:
            
            raise FileNotFoundError("Entered path to the import repository does not exist")
    
    def expandedDiffRestrictors(self, testFile, refFile):
    
        """  Generates expanded difference between read and original data from test and ref files for Restrictor definiation values.
        The data in the input test and Reference files have entries of the form "0;0;0;0" which defines a Restrictor configuration.
        
        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
    
        :type testFile: string
        :param testFile: Full path to the Test file written as a result of ExportToExcel funtion.
    
        :type refFile: string
        :param refFile: Full path to the Reference file from which the data will be compared to generate expanded diffrence.
    
        :raises: None
    
        :rtype: Pandas Dataframe
        :return: Expanded Difference Dataframe showing differences in test and ref File data.
        """   
        #df_test= self.__flattenIndexdf()
        df1= pd.read_excel(io= testFile, sheet_name=1,engine="xlrd",header=None)
        #df1=df1.loc[:,df1.loc[0]!="HUM"]
        #df1= df1.replace(to_replace=["CAOR","LAOR"], value=["CAO","LAO"])

        tz_list= df1.iloc[0,:].fillna("None").values.tolist()
        #Side of Air Outlet
        restrictor_list= df1.iloc[1,:].fillna("None").values.tolist()

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
        print(df1.head())

        tz_list = fill_none(tz_list)[1:]
        restrictor_list = fill_none(restrictor_list)[1:]
        
        def NewColumnNames(tz_list,restrictor_list):
            try:
                a= len(restrictor_list)
                # Initialising the name list with the name of the first column
                name_list=["HoV","Test Reference"]
                for i in range(1,a):
                    name= str(tz_list[i]) +"-"+str(restrictor_list[i]) 
                    name_list.append(name)
            except Exception as e:
                print(e)
                print("List Lengths are not equal")
            finally:
                return name_list

        name_list = NewColumnNames(tz_list,restrictor_list)
        print(name_list)

        # Slicing the Core Data (Getting the data except the column names)
        df1=df1.iloc[3:,0:]
        
        #Assigning new Column Names
        df1.columns=name_list
        df1= df1.fillna(method= "ffill",limit= 6)


        # #df1= correctcolumns(df1,frame_list,type_list,side_list)
        # #type_indexes=
        print(df1.head())

        df2= pd.read_excel(io= refFile, sheet_name=1,engine="xlrd",header=None,index_col= None)
        print(df2.head())
        
        tz_list=df2.iloc[1,:].fillna("None").values.tolist()
        restrictor_list= df2.iloc[2,:].fillna("None").values.tolist()

        tz_list = fill_none(tz_list)[1:]
        restrictor_list = fill_none(restrictor_list)[1:]

        name_list = NewColumnNames(tz_list,restrictor_list)
         
        print(name_list)
        #Slicing the core Data
        df2=df2.iloc[3:,0:]
        df2.columns=name_list
        
        # df2= df2.fillna(0)

        #Verify
        print(df2.head())

        def rename_colums(str1):
            if("HPA" in str1):
                return 'HPA flow Rate'
            elif("mix" in str1):
                return "mixP"
            elif("Test Reference" in str1):
                return "Test Reference"
            else:
                return str1


        df2= df2.rename(columns=rename_colums)
        print(df2.head())


        df1["ID"]= df1["HoV"] +":"+ df1["Test Reference"]
        df2["ID"]= df2["HoV"] +":" + df2["Test Reference"]

        # Generating the id list for both dataframes
        Test_Hov_List= df1["ID"].values.tolist()
        Target_Hov_List= df2["ID"].values.tolist()
        # Generating the common Hov List
        Common_Hov_list= [value for value in Target_Hov_List if value in Test_Hov_List]
        
        # Subset the datasets based on Common Hovs
        df1_common_hov = df1.set_index("ID").loc[Common_Hov_list,:].fillna("0;0;0;0")
        df2_common_hov = df2.set_index("ID").loc[Common_Hov_list,:].fillna("0;0;0;0")
        

        print(df1_common_hov.head())
        print(df2_common_hov.head())
        
        # drop duplicated indices:
        df1_common_hov= df1_common_hov[~df1_common_hov.index.duplicated(keep="first")]
        df2_common_hov= df2_common_hov[~df2_common_hov.index.duplicated(keep="first")]

        # # print(Test_Hov_List)
        # # print("\n"*4)
        # # print(Target_Hov_List)

        print("\n"*4)
        print(df1_common_hov.shape)

        print("\n"*4)
        print(df2_common_hov.shape)


        print(df1_common_hov.head())
        print(df2_common_hov.head())

        # Drop the Temperature and Pressure Related Columns.
        droplist=[i for i in df2_common_hov.columns if ("Date" in i or "Imported" in i or "By" in i or "Import" in i or "HUM" in i or "Test" in i or "CAO" in i or "LAO" in i or "Notes" in i or "HPA"in i or "mix" in i)]
        df2_common_hov_trimmed= df2_common_hov.drop(droplist,axis=1)
        print(df2_common_hov_trimmed.head(2))

        # Generate individual dataframe subset on common hovs with  columns specific to hovs removed 
        df1_cm_specific_hovs= df1_common_hov.loc[:,(df1_common_hov!="0;0;0;0").any(axis=0)] 
        df2_cm_specific_hovs= df2_common_hov_trimmed.loc[:,(df2_common_hov_trimmed!="0;0;0;0").any(axis=0)]

        print(df1_cm_specific_hovs.shape)
        print(df2_cm_specific_hovs.shape)

        # #DRop Hovs and other strin g values
        df1_cm_specific_hovs=df1_cm_specific_hovs.drop(["Test Reference","HoV"], axis= 1)
        df2_cm_specific_hovs= df2_cm_specific_hovs.drop("HoV", axis = 1)

        

        
        # Create list of common columns:
        common_columns= df2_cm_specific_hovs.columns.intersection(df1_cm_specific_hovs.columns)
        common_columns=common_columns.values
    
        # Generate Residual Datasets for each df1(cm SPECIFIC)) and Df2(common SPECIFIC)
        df1_residual= df1_cm_specific_hovs.drop(common_columns,axis=1)
        df2_residual= df2_cm_specific_hovs.drop(common_columns,axis=1)

        #Print and Verify shapes
        print(df1_residual.shape)
        print(df2_residual.shape)

        def generate_zeros_df(df):
            shape= df.shape
            column_names= df.columns.values.tolist()
            zeros_array= np.zeros(shape=shape)
            zeros_df = pd.DataFrame(data= zeros_array,columns=column_names,index= Common_Hov_list)
            zeros_df= zeros_df.replace(0,"0;0;0;0")
            return zeros_df

        #Generate zeroes dAtaframe for each residual dataframe
        df1_residual_zeros = generate_zeros_df(df1_residual)
        df2_residual_zeros = generate_zeros_df(df2_residual)
        
        print(df1_residual_zeros.head())
        print(df1_residual_zeros.shape)

        #Expand df1_cm_specfic 
        # New adamant data is expanded
        df1_cm_specific_hovs_expanded = pd.concat([df1_cm_specific_hovs,df2_residual_zeros],axis=1)

        #Expand df2_cm_specfic 
        # OLD adamant data is expanded
        df2_cm_specific_hovs_expanded = pd.concat([df2_cm_specific_hovs,df1_residual_zeros],axis=1)

        #Print and Verify shapes
        print(df1_cm_specific_hovs_expanded.shape)
        print(df2_cm_specific_hovs_expanded.shape)

        
        # Rearrange the Columns in the ascending order for each expanded dataframe
        df1_cm_specific_hovs_expanded= df1_cm_specific_hovs_expanded.sort_index(axis=1)
        df2_cm_specific_hovs_expanded= df2_cm_specific_hovs_expanded.sort_index(axis=1)

        print(df1_cm_specific_hovs_expanded.head(2))
        print(df2_cm_specific_hovs_expanded.head(2))

        """
            NOTE:  DEPENDING ON WHETHER WE NEED TO TRACK THE MISSING VALUES WE CAN BYPASS THIS STEP 

            NOTE  THAT ALL ABOVE DATAFRAMES HAVE NANS EXCEPT THE ZEROS DATAFRAME 

        """
        #Optional but neccesary 
        # Fill missing values with zero

        df1_cm_specific_hovs_expanded = df1_cm_specific_hovs_expanded.fillna("0;0;0;0")
        df2_cm_specific_hovs_expanded = df2_cm_specific_hovs_expanded.fillna("0;0;0;0")

        def revalidate(string):
            string_list = string.split(";")
            new_string_list= []
            for i in string_list:
                if not i.isnumeric():
                    new_string_list.append("0")    
                else :
                    new_string_list.append(i)
            
            new_string=";".join(new_string_list)
            return new_string

        df1_cm_specific_hovs_expanded= df1_cm_specific_hovs_expanded.applymap(revalidate)
        df2_cm_specific_hovs_expanded= df2_cm_specific_hovs_expanded.applymap(revalidate)

        print(df1_cm_specific_hovs_expanded.tail())
        print(df2_cm_specific_hovs_expanded.tail())
        """
        CREATING THE EXPANDED DIFFERENCE DATAFRAME

        """
        def compareRestrictors(str1,str2):
            """
            takes two Restrictor datastrings and produces the difference
            """
            l1=  str1.split(";")
            l2=  str2.split(";")

            d1= int(l1[0])-int(l2[0])
            d2= int(l1[1])-int(l2[1])
            d3= int(l1[2])-int(l2[2])
            d4= int(l1[3])-int(l2[3])

            d_str= str(d1)+";"+str(d2)+";"+str(d3)+";"+str(d4)
            
            return d_str

        """
        CAUTION:
        AlWAYS DEFINE THIS FUNCTION AS PRIVATE

        """
        def compareRestrictorSeries(Series_1,Series_2):
            if(Series_1.size != Series_2.size):
                print('Series size not equal')
                return 
            else:
                Series_3=[]
                for i in range(Series_2.size):
                    c= compareRestrictors(Series_1.iloc[i],Series_2.iloc[i])
                    Series_3.append(c)
                Series_3= pd.Series(data= Series_3 , index= Common_Hov_list)
                return Series_3

        df_expanded_diff = df2_cm_specific_hovs_expanded.combine(df1_cm_specific_hovs_expanded,compareRestrictorSeries)
        return df_expanded_diff

    
    def printDiffReport(self, df,filepath=None,tolerance= 0.001):

        """ Function to print the positions (Row and column) in the input dataframe where values are NOT EQUAL TO "0;0;0;0"
        
        Input dataframe is an expanded diff dataframe obtained as a result of ExpandedDiffRestrictors Function

        :type self: DB2_LTR_REST
        :param self: Calling object of the DB2_LTR_REST class
        
        :type df: Pandas Dataframe
        :param df: Input dataframe as a result of Expanded Diff Restrictors function in this class  which needs to be processed.
    
        :type filepath: string
        :param filepath: Full path to the .log file to which the results are written.
    
        :type tolerance: float
        :param tolerance: tolerance value for the difference (Not currently implemented but required in future) 
    
        :raises: None
    
        :rtype: None
        """    
        
        
        def difffunc(value):
            
            if(value == "0;0;0;0"):
                return 0
            else:
                return 1
       
        #filepath= os.path.join(work_dir,"/tests/RESULTS/DB0_DEF",filename)
        df=df.applymap(difffunc)
        listOfPositions = self._getIndexes(df,1)

        with open(filepath,"w") as file:
            file.write('Displaying HoV names AND FRAME WITH DIFFERENCES : \n')
            file.write("\n No.of frames with differences:{0}\n".format(len(listOfPositions)))
        
            for i in range(len(listOfPositions)):
                # Define the log string
                log_string= "\nPosition:,{0}, (HoV, frame) : {1}\n".format(i,listOfPositions[i])
                file.write(log_string)
    
              
    
    def clean(self):
        """
        To clean an HOV data from one file: Abstract Function
                -- To be overridden by the respective Flow class
        :return:
        """
        raise NotImplementedError

        
if __name__=="__main__":
    GTR8Flow = DB2_LTR_REST()
    # GTR8Flow = DB2_LTR_FLOW()
    # folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\2-LTR"
    # GTR8Flow.importAllFilesinFolders(folderpath=folderpath)
    # print(GTR8Flow.df.head())
    # print(GTR8Flow.df.loc["AAR01",:])

    curdir= os.getcwd()
    print(curdir)
    export_folderpath = os.path.join(curdir,"tests\OUT\DB2_LTR")
    print(export_folderpath)
    # Please change the below path to your respective network location
    folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\2-LTR"
    
       
    LTR2_REST = DB2_LTR_REST()

    #Test 1
    LTR2_REST.importAllFilesinFolders(folderpath)
    print(LTR2_REST.df.head())
    testfile1= LTR2_REST.export2Excel("test1DB2_REST.xlsx", export_folderpath)
    reffile1= os.path.join(curdir,"tests\REF\DB2_LTR","DB2_LTR_REST.xlsx")
    exp_diff1=LTR2_REST.expandedDiffRestrictors(testfile1,reffile1)
    print("Expanded diff successfull")
    log_filename="DB2_LTR_REST.log"
    diff_report_path= os.path.join(curdir, "tests\RESULTS\DB2_LTR",log_filename)
    LTR2_REST.printDiffReport(exp_diff1,filepath=diff_report_path)

    #Test 2
    new_record_path= os.path.join(curdir,"tests\\NEW\DB2_LTR\D0008-MIX22.xlsm")
    LTR2_REST.addNewRecord(filepath=new_record_path,HoV= "D0008")
    testfile2= LTR2_REST.export2Excel("test2DB2_REST.xlsx", export_folderpath)
    exp_diff2=LTR2_REST.expandedDiffRestrictors(testfile2,reffile1)
    print("Expanded diff successfull")
    LTR2_REST.printDiffReport(exp_diff2,filepath=diff_report_path)
        
        

    

            

                

        



              

