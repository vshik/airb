
from model.interfaces import IData
import numpy as np
import pandas as pd
import os 
import re 

class DB2_LTR_PP(IData):
    def __init__(self):
        self._dataframe= pd.DataFrame()

    def _postprocessdf(self):
        self._dataframe= self._dataframe.fillna(0)       

    def _parse(self,filepath,HoV,db2_ltr_test_ref =None):
        
        try:
            raw_df = pd.read_excel(filepath,sheetname="Pressure",header= None,skiprows=3)
            print(raw_df.shape)
            format =1
            print(format)
        except Exception as e:
            try:
                raw_df=pd.read_excel(filepath,sheetname="Pressue +Temperature",header= None,skiprows=3)
                format = 2
                print(format)
            except Exception as e:
                print("Error:",e,"or file is misformatted")

                return
        

        #The below function generates a dataframe with Three columns namely TZ ,PP and value.
        concat_df= self._process(raw_df,format= format)
        
        # generate the multiindex concat dataframe. Note that the dataframe is still a vertical one which needs to be transposed to obtain the row dataframe. 
        concat_multi_df= concat_df.set_index(["TZ","PP"])
        
        
        print(concat_multi_df.head())
        
        # GENERATE THE transpose df:
        raw_transpose_df = concat_multi_df.T    
        print(raw_transpose_df.head())

        #Below is the Code to insert HoV and Test Reference as Columns into the single row Dataframe
        #obtained after transposing concat multi_df.

        if(db2_ltr_test_ref == None):
            filename= str(os.path.split(filepath)[1])
            #remove file extension from file name
            filename= re.sub(r'\.x[a-z]*$','',filename)
            #experiment_type_string=""
        
            # CHeck if filename contains HoV
            if(filename.find(HoV) != -1):
                file_index= filename[::-1].find("-")
                index_of_split= len(filename)- file_index -1
                experiment_type_string= filename[index_of_split+1:]
                raw_transpose_df["Test Reference"]= experiment_type_string
            else:
                experiment_type_string= filename.replace("-","")
                raw_transpose_df["Test Reference"]= experiment_type_string
        else:
            raw_transpose_df["Test Reference"] = db2_ltr_test_ref
        

        raw_transpose_df["HoV"]= HoV
        
        #Create a multindex for rows using df.set_index. Multi indexing on HoV and Test reference.
        transpose_df=raw_transpose_df.set_index(["HoV","Test Reference"])

        return transpose_df

        # find the hov 
    
    def _process(self,raw_df,format= 1):
            def extract_pressureport_id(pp_string): 
                try:    
                    pp_id= int(pp_string[3:])
                except:
                    pp_id= np.nan
                finally:
                    return str(pp_id)

            def extract_tz(row):
                #Pressureport ID number
                pp= row.iloc[0]
                if(pd.isnull(pp)):
                    return np.nan
                else:
                    pp_number= int(row.iloc[0])     
                
            
                if(pp_number< 9000):
                    tz_numeric= int((pp_number%1000)/100)
                    row_TZ= "TZ" + str(tz_numeric)
                    return row_TZ
                else:
                    other_tz_id= str(pp_number)[0:3]
                    if(other_tz_id=="134"):
                        row_TZ= "CVS"
                    elif(other_tz_id=="137"):
                        row_TZ= "AVS"
                    elif(other_tz_id=="140"):
                        row_TZ= "FWD CC"
                    elif(other_tz_id=="130"):
                        row_TZ= "FCRC"
                    elif(other_tz_id=="131"):
                        row_TZ= "CCRC"
                    else:
                        row_TZ= "Other"
                    return row_TZ
            
            def extract_tz_row2(raw_df,end_row_index=200,start_row_index= 0,format= 0):
                """
                Extract one row of tz tables
                """      
                df_list=[]      
                i=0
                end_col_index= raw_df.shape[1] 
                offset= 0
                #Convert first column into a list
                first_col= raw_df.iloc[:,0].values.tolist()

                if(format== 2.1):
                    offset=2
                    if(start_row_index > 5):
                        end_row_index= first_col.index("Temperature")
                        end_col_index = 12
                    print("Format 2.1")
                                   
                    
                
                if(format==1):
                    print("Format 1")
                    offset= 3

                if(format==1.1):
                    print("Format 1.1")
                    offset= 2
                
                if(format== 2):
                    print("Format 2")
                    offset= 2


                while(i< end_col_index and pd.notnull(raw_df.iat[start_row_index,i])):
                    # Extract the temperature zone of the pressure port
                    tz= raw_df.iat[start_row_index,i]
                    if(tz!="AFT CC"):                
                        tz_df= raw_df.iloc[(start_row_index + 1):end_row_index,i:i+2]
                        tz_df= tz_df.dropna(axis= 0,how="all")
                        tz_df.columns= ["PP","value"]
                        if(format in  [2,2.1]):
                            tz_df["PP"]= tz_df["PP"].apply(extract_pressureport_id)
                        else:
                            tz_df["PP"]= tz_df["PP"].astype(str)
                        tz_df["TZ"] = tz_df.apply(extract_tz,axis=1)
                        tz_df= tz_df.dropna(axis=0,how="any")
                        df_list.append(tz_df)
                        i= i + offset
                    else: i= i + offset
                
                df= pd.concat(df_list,axis=0,ignore_index=True)
                return df
            
            #Convert first column into a list
            first_col= raw_df.iloc[:,0].values.tolist()
            
            if("Temperature" in first_col):
                "Temperature information for AGU in first column"
                format= 2.1
            
            if("CVS" not in first_col and format==1):
                "Only one row of TZ tables exists"
                format= 1.1

            if(format==1):
                print("Format 1: Pressure Only","Tz tables seperated by blank columns")               

                
                row1_index= 0
                #Convert first column into a list
                first_col= raw_df.iloc[:,0].values.tolist()
                
                #find the index of the second row
                end_row_index= first_col.index("CVS")        
                
                #Parse the first row of a data tables
                row1_df= extract_tz_row2(raw_df,end_row_index,row1_index,format=format)

                #Parse the second row of tables.
                row2_df= extract_tz_row2(raw_df,start_row_index=end_row_index,format= format)

                # Create concatenated vertical dataframe    
                concat_df= pd.concat([row1_df,row2_df],axis=0)   

            if(format==2 or format== 2.1):
                print("Pressure and ambient temperature Only")                        
                
                row1_index= 0
                #Convert first column into a list
                first_col= raw_df.iloc[:,0].values.tolist()
                
                #find the index of the second row
                end_row_index= first_col.index("CVS")        
                
                #Parse the first row of a data tables
                row1_df= extract_tz_row2(raw_df,end_row_index,row1_index,format=format)

                #Parse the second row of tables.
                row2_df= extract_tz_row2(raw_df,start_row_index=end_row_index,format= format)

                # Create concatenated vertical dataframe    
                concat_df= pd.concat([row1_df,row2_df],axis=0)

            if(format== 1.1):
                row1_index= 0
                #Convert first column into a list
                first_col= raw_df.iloc[:,0].values.tolist()
                
                    
                
                #Parse the first row of a data tables
                row1_df= extract_tz_row2(raw_df,end_row_index=200,start_row_index=row1_index,format=format)
                
                concat_df= row1_df 

            return concat_df        
            
    def addNewRecord(self, filepath, HoV=None, ACversion=None, db2_ltr_test_reference= None):
    
        """ Funtion to add the data of a new input file to th existing dataframe.
        To be overridden by the derived class.

        :type self:DB2_LTR_PP
        :param self: Calling Object of LTR2 PP 
    
        :type filepath:string
        :param filepath: full path to the file which needs to be parsed with extension
    
        :type HoV: string
        :param HoV: HoV of the aircraft
    
        :type ACversion: string
        :param ACversion: Aircraft Version of the particular HoV example "A350-900" 
    
        :type db2_ltr_test_reference: string
        :param db2_ltr_test_reference: Test Reference for new record in DB2_LTR_FLOW
    
        :raises: FileNotFoundError
    
        :rtype: None
        
        """
        try:
            oneline_df = self._parse(filepath,HoV=HoV,db2_ltr_test_ref= db2_ltr_test_reference)
            self._dataframe = pd.concat([self._dataframe, oneline_df], axis=0)
            print("Imported: ", filepath)
        except Exception as e:
            print("Exception occurred for file: %s. Error:  %s "%(filepath,e))
    
    def expandedDiff(self,testFile, refFile):

            """ Generates expanded difference between read and original data from test and ref files
            
            :type self: DB2_LTR_PP 
            :param self: Calling object of the LTR 2 Dataset
        
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
            pp_list= df1.iloc[1,:].fillna("None").values.tolist()

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
            pp_list = fill_none(pp_list)[1:]
            
            
            def NewColumnNames(frame_list):
                try:
                    a= len(frame_list)
                    # Initialising the name list with the name of the first column
                    name_list=["HoV","Test Reference"]
                    for i in range(1,a):
                        name= str(tz_list[i]) +"-"+str(int(pp_list[i])) 
                        name_list.append(name)
                except Exception as e:
                    print(e)
                    print("List Lengths are not equal")
                finally:
                    return name_list

            name_list = NewColumnNames(tz_list)
            print(name_list)

            # Slicing the Core Data (Getting the data except the column names)
            df1=df1.iloc[3:,0:]
            
            #Assigning new Column Names
            df1.columns=name_list
            df1= df1.fillna(method= "ffill",limit= 6)


            #df1= correctcolumns(df1,frame_list,type_list,side_list)
            #type_indexes=
            print(df1.head())

            df2= pd.read_excel(io= refFile, sheet_name=1,engine="xlrd",header=None,index_col= None)
            print(df2.head())

            tz_list=df2.iloc[1,:].fillna("None").values.tolist()
            pp_list= df2.iloc[2,:].fillna("None").values.tolist()

            tz_list = fill_none(tz_list)[1:]
            pp_list = fill_none(pp_list)[1:]

            name_list = NewColumnNames(tz_list)
            
            print(name_list)
            #Slicing the core Data
            df2=df2.iloc[3:,0:]
            df2.columns=name_list
            
            df2= df2.fillna(0)

            #Verify
            print(df2.head())

            df1["ID"]= df1["HoV"] +":"+ df1["Test Reference"]
            df2["ID"]= df2["HoV"] +":" + df2["Test Reference"]

            # Generating the id list for both dataframes
            Test_Hov_List= df1["ID"].values.tolist()
            Target_Hov_List= df2["ID"].values.tolist()
            # Generating the common Hov List
            Common_Hov_list= [value for value in Target_Hov_List if value in Test_Hov_List]
            
            # Subset the datasets based on Common Hovs
            df1_common_hov = df1.set_index("ID").loc[Common_Hov_list,:].fillna(0)
            df2_common_hov = df2.set_index("ID").loc[Common_Hov_list,:].fillna(0)
            
            # drop duplicated indices:
            df1_common_hov= df1_common_hov[~df1_common_hov.index.duplicated(keep="first")]
            df2_common_hov= df2_common_hov[~df2_common_hov.index.duplicated(keep="first")]

            print(df1_common_hov.head())
            print(df2_common_hov.head())

            df2_common_hov_trimmed= df2_common_hov.drop([],axis=1)
            print(df2_common_hov_trimmed.head(2))

            # Create list of common columns:
            common_columns= df2_common_hov_trimmed.columns.intersection(df1_common_hov.columns)
            common_columns=common_columns.values

            #Create  Series of equal length as columns in each df and index equal to column names of each df

            df1_inclusion_list= [(x in common_columns) for x in df1_common_hov.columns.values.tolist()] 
            df2_inclusion_list= [(x in common_columns) for x in df2_common_hov_trimmed.columns.values.tolist()]

            df1_inclusion_series= pd.Series(data= df1_inclusion_list,index=df1_common_hov.columns)
            df2_inclusion_series= pd.Series(data= df2_inclusion_list,index=df2_common_hov_trimmed.columns)

            print(df1_inclusion_series)
            print(df2_inclusion_series)

            # Generate individual dataframe subset on common hovs with  columns specific to hovs removed 
            df1_cm_specific_hovs= df1_common_hov.loc[:,(df1_common_hov!=0).any(axis=0) | df1_inclusion_series] 
            df2_cm_specific_hovs= df2_common_hov_trimmed.loc[:,(df2_common_hov_trimmed!=0).any(axis=0) | df2_inclusion_series]

            print(df1_cm_specific_hovs.shape)
            print(df2_cm_specific_hovs.shape)

            #DRop Hovs and other strin g values
            df1_cm_specific_hovs=df1_cm_specific_hovs.drop(["Test Reference","HoV"], axis= 1)
            df2_cm_specific_hovs= df2_cm_specific_hovs.drop(["Test Reference","HoV"], axis = 1)

            df1_cm_specific_hovs= df1_cm_specific_hovs.astype(dtype= "float")
            df2_cm_specific_hovs= df2_cm_specific_hovs.astype(dtype= "float")

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

            df1_cm_specific_hovs_expanded = df1_cm_specific_hovs_expanded.fillna(0.0)
            df2_cm_specific_hovs_expanded = df2_cm_specific_hovs_expanded.fillna(0.0)

            print(df1_cm_specific_hovs_expanded.head(2))
            print(df2_cm_specific_hovs_expanded.head(2))

            """
            CREATING THE EXPANDED DIFFERENCE DATAFRAME

            """
            df_expanded_diff = df2_cm_specific_hovs_expanded - df1_cm_specific_hovs_expanded

            print(df_expanded_diff.head(2))

            # Force typecast expanded diff df to float
            df_expanded_diff= df_expanded_diff.astype(dtype= "float")

            return df_expanded_diff

    def printDiffReport(self, df,filepath=None,tolerance= 0.001):
        """ Function to print the positions (Row and column) in the input dataframe where values are grater than tolerance value.
        Input dataframe is an expanded diff.
        
        :type self:DB2_LTR_PP
        :param self: Calling Object of LTR2 PP 
    
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
            file.write('Displaying HoV names AND FRAME WITH DIFFERENCES : \n')
            file.write("\n No.of frames with differences:{0}\n".format(len(listOfPositions)))
        
            for i in range(len(listOfPositions)):
                # Define the log string
                log_string= "\nPosition:,{0}, (HoV, frame) : {1}\n".format(i,listOfPositions[i])
                file.write(log_string)
            
            
        # print('Displaying HoV names AND FRAME WITH DIFFERENCES : ')

        # print("No.of frames with differences:",len(listOfPositions))
        # for i in range(len(listOfPositions)):
        #     print('Position ', i, ' (HoV , frame) : ', listOfPositions[i])
    
    
    
if __name__=="__main__":
    ltr2_pp = DB2_LTR_PP()
    path="X:\DEV\Repository\\2-LTR\HVN01\HVN01-MIX18.xlsx"
    ltr2_pp.addNewRecord(path,"HVN01")
    # GTR8Flow.headdf()
    # print(GTR8Flow.df.loc["AAR01",:])

    curdir= os.getcwd()
    print(curdir)
    export_folderpath = os.path.join(curdir,"tests\OUT\DB2_LTR")
    print(export_folderpath)
    # Please change the below path to your respective network location
    folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\2-LTR"
    
       
    LTR2PP = DB2_LTR_PP()

    #Test 1
    LTR2PP.importAllFilesinFolders(folderpath)
    print(LTR2PP.df.head())
    testfile1= LTR2PP.export2Excel("test1DB2_PP.xlsx", export_folderpath)
    reffile1= os.path.join(curdir,"tests\REF\DB2_LTR","DB2_LTR_PP.xlsx")
    exp_diff1=LTR2PP.expandedDiff(testfile1,reffile1)
    print("Expanded diff successfull")
    log_filename="DB2_LTR_PP.log"
    diff_report_path= os.path.join(curdir, "tests\RESULTS\DB2_LTR",log_filename)
    LTR2PP.printDiffReport(exp_diff1,filepath=diff_report_path)

    #test 2:
    new_record_path= os.path.join(curdir,"tests\\NEW\DB2_LTR\D0008-MIX22.xlsm")
    LTR2PP.addNewRecord(filepath=new_record_path,HoV= "D0008")
    testfile2= LTR2PP.export2Excel("test2DB2.xlsx", export_folderpath)
    exp_diff2=LTR2PP.expandedDiff(testfile2,reffile1)
    print("Expanded diff successfull")
    LTR2PP.printDiffReport(exp_diff2,filepath=diff_report_path)     
