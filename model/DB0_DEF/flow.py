

from numpy.lib.function_base import percentile
from model.interfaces import IData
import os
import pandas as pd
import numpy as np
import re


class DB0_DEF_FLOW(IData):
    """
    class to instantiate the DB0 DEF FLOW DATASET.

    """
    def __init__(self):
        self._dataframe= pd.DataFrame()
        
    
    def _process(self,filename, path= None):
    
        """ Read one file , process the dataframe and returns the dataframe"
        
        :type self:DB0_DEF_FLOW
        :param self: Calling Object of LTR0 DATASET
    
        :type file: string
        :param file: Exact filename with extension
    
        :type path: string
        :param path: Path to the repository of the file in Network Drive, if not specified current import repository will be used.
    
        :raises:
    
        :return: The processed pandas dataframe corresponding to one HOV files.
        :rtype: Pandas Dataframe
        """    


        if(path== None):
            path= self.__flowdefpath
        
        if(os.path.exists(path)):
            df= self._readDF(path,filename)
            df= self._processDF(filename,df)
            return df
        else:
            print("Entered new file path does not exist")
            return        
    
    def _parse(self,filepath= None):
    
        """ 
        PARSE ONE FILE FROM A NETWORK LOCATION RETURN A DATAFRAME WITh one row
        
        :type self: DB0_DEF_FLOW 
        :param self: Calling object of the LTR 0 Dataset
    
        :type importpath: string
        :param importpath: Full path of the import repository.

        :type filename: string
        :param filename: Full filename with extension.
    
        :raises:

    
        :return: Dataframe with one line indexed by HoV
        :rtype: Pandas Dataframe

        """
        path_elements= os.path.split(filepath)
        parent_repo =path_elements[0]
        filename= path_elements[1]
        
        # get the intermediate Dataframe which is read from files and reshaped into a single column df for all frame sections 
        df= self._process(filename,parent_repo)
        
        if "C" not in str(df.loc[0,"Frame"]):
            df=self._framerange_1(df)
            df= self._reformat_Frames(df)
        
        #Replace commas with periods. The data frame df alrady consists of four columns "type", "side", "Frame", and Vdef"
        df["Frame"]=df["Frame"].apply(lambda section:section.replace(",",".") if isinstance(section,str) else section)
        df= df.loc[:,["type","side","Frame","Vdef"]]

        #Apply Generic Transformations
        multi = self._lateralFramesformat(df)
        # The above function has a groupby statement which creates the multi-index with type side and Frame columns.

        #Apply some hard coded cleaning on the dataframe.
        multi= self.clean(multi) 

        #multi= multi[~multi.index.duplicated(keep="first")]
        hov= filename
        multi=multi[["Vdef"]]
        multi.rename(columns={"Vdef": hov.replace(".xlsx","")} ,inplace=True)
        multi_transpose= multi.T

        
        # multi_transpose["HUM"]= self.__humidityflag

        dummy_df= multi_transpose.copy()       
        #Change type labels from CAOR ,LAOR to CAO and LAO
        columnmi= dummy_df.columns.set_levels(["CAO","LAO"],level = 0)
        dummy_df.columns= columnmi
        
        # dummy_df.insert(0,column="HUM",value=humidity_series)
        
        return dummy_df

    def clean(self,multi_df):
    
        """ Function to add hard codings. This function is used to add dataframe level transformations to the input pandas dataframe.
        
        :type self:DB0_DEF_FLOW
        :param self: Calling Object of LTR0 DATASET
    
        :type multi_df: Pandas Dataframe
        :param multi_df: Input Dataframe to apply transformations on
    
        :raises: KeyError
    
        :rtype: Pandas Dataframe
        
        :returns: Transformed pandas dataframe
        """    """
        
        """
        df= multi_df.drop(labels=[("LAOR","RH","C34-C36"),("LAOR","RH","C36-C38")],axis= 0)
        return df

    """
    This function is optional but is kept for performing expanded diffs. However, filtering will need multiindexing.
    We will have to reset the dataframe to multiindex once we achiove the final column mappings for the dataset.
    
    """
    def __flattenIndexdf(self):
    
        """ Does Final Column Transformations, Converts LAOR/ CAOR to LAO/CAO respectively 
        and flattens the multiindex to form a dataframe with uniquely identifiable columns
        

        :type self: DB0_DEF_FLOW 
        :param self: Calling object of the LTR 0 Dataset
    
        :raises:
    
        :rtype:
        """   
        df1= self._dataframe
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
                # Initialising the name list with the name of the first column
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

    
    def _lateralFramesformat(self,df):
    
        """ Apply some General column transformations according to shop floor conventions. 
        These transformations are to be applied to all dataframes.
        
        :type self: DB0_DEF_FLOW 
        :param self: Calling object of the LTR 0 Dataset
    
        :type df: Pandas Dataframe
        :param df: Input dataframe to apply transformations on
        
        :return: Dataframe with section renaming transformations applied.
    
        :raises:

        :return: datframe with applied  section renamings. 
        :rtype: Pandas dataframe
        """    
        new_frame_df= pd.DataFrame(columns=["type","side","Frame","Vdef"])

        for index,row in df.iterrows():
            frame = row.loc["Frame"]
            type_ao= row.loc["type"]
            side= row.loc["side"]
            flow_value= float(row.loc["Vdef"])
            new_type= ""
            new_frame=""
            
            if(frame== "C86-C88"):
                new_type= "CAOR"
                row_dict={"type":new_type,"side":side,"Frame":frame,"Vdef":flow_value}
                new_frame_df= new_frame_df.append(row_dict, ignore_index =True)

            elif(frame=="C17-C19"):
                if(type_ao == "CAOR"):
                    new_frame="C19-C21"
                    row_dict={"type":type_ao,"side":side,"Frame":new_frame,"Vdef":flow_value}
                    new_frame_df= new_frame_df.append(row_dict, ignore_index =True)
                
            
            elif(frame== "C30-C30,2" or frame == "C30-C30.2"):
                new_frame="C30-C32"
                row_dict={"type":type_ao,"side":side,"Frame":new_frame,"Vdef":flow_value}
                new_frame_df= new_frame_df.append(row_dict, ignore_index =True) 
                
            elif(frame== "C72-C72,2" or frame == "C72-C72.2"):
                new_frame="C72-C74"
                row_dict={"type":type_ao,"side":side,"Frame":new_frame,"Vdef":flow_value}
                new_frame_df= new_frame_df.append(row_dict, ignore_index =True)
            
            
            elif(frame=="C88-C90"):
                new_frame ="C88-C89"
                new_type= "CAOR"
                row_dict={"type":new_type,"side":side,"Frame":new_frame,"Vdef":flow_value}
                new_frame_df= new_frame_df.append(row_dict, ignore_index =True)
            
            elif(frame=="C90-C91"):
                new_frame ="CAS"
                new_type= "CAOR"
                row_dict={"type":new_type,"side":side,"Frame":new_frame,"Vdef":flow_value}
                new_frame_df= new_frame_df.append(row_dict, ignore_index =True)
            
            elif(frame== "C17-C18" and type_ao=="LAOR"):
                new_flow= 0
                row_dict={"type":type_ao,"side":side,"Frame":frame,"Vdef":new_flow}
                new_frame_df= new_frame_df.append(row_dict, ignore_index =True)
            
            # elif(frame in ["C34-C36","C36-C38"] and type_ao=="LAOR" and side =="RH"):
            #     new_flow= 0
            #     row_dict={"type":type_ao,"side":side,"Frame":frame,"Vdef":new_flow}
            #     new_frame_df= new_frame_df.append(row_dict, ignore_index =True)

            elif(frame=="C91-C92"):
                if(type_ao != "CAOR"):
                    new_frame= "CORNER"
                    new_type="LAOR"
                    row_dict={"type":new_type,"side":side,"Frame":new_frame,"Vdef":flow_value}
                    new_frame_df= new_frame_df.append(row_dict, ignore_index =True)
                else:
                    new_frame="C92-C93"
                    row_dict={"type":type_ao,"side":side,"Frame":new_frame,"Vdef":flow_value}
                    new_frame_df= new_frame_df.append(row_dict, ignore_index =True)
            else:
                row_dict={"type":type_ao,"side":side,"Frame":frame,"Vdef":flow_value}
                new_frame_df= new_frame_df.append(row_dict, ignore_index =True)
        
        # Group duplicate values and aggregate them
        new_frame_df= new_frame_df.groupby(["type","side","Frame"]).max()
        print(new_frame_df.tail(100))
        return new_frame_df    
    
    
    
    def expandedDiff(self, testFile, refFile):
    
        """ Generates expanded difference between read and original data from test and ref files
        
        :type self: DB0_DEF_FLOW 
        :param self: Calling object of the LTR 0 Dataset
    
        :type testFile: string
        :param testFile: Full path to the Test file written as a result of ExportToExcel funtion.

        :type refFile: string
        :param refFile: Full path to the Reference file from which the data will be compared to generate expanded diffrence.
    
        :raises:
    
        :rtype: Pandas Dataframe
        :return: Expanded Difference Dataframe showing differences in test and ref File data.
        """    
        #df_test= self.__flattenIndexdf()
        df1= pd.read_excel(io= testFile, sheet_name=1,engine="xlrd",header=None)
        #df1=df1.loc[:,df1.loc[0]!="HUM"]
        #df1= df1.replace(to_replace=["CAOR","LAOR"], value=["CAO","LAO"])



        print(df1.head())

        


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
        # Function Generating new Column names:
        def NewColumnNames(frame_list):
            try:
                a= len(frame_list)
                # Initialising the name list with the name of the first column
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
        df1= df1.fillna(0)


        #df1= correctcolumns(df1,frame_list,type_list,side_list)
        #type_indexes=
        print(df1.head())

        # #drop humidity values
        # droplist= [i for i in df1.columns if ("HUM" in i)]
        # df1= df1.drop(labels= droplist,axis= 1)

        df2= pd.read_excel(io= refFile, sheet_name=1,engine="xlrd",header=None,index_col= None)
        # Listing the Type, Side and Frame Section
        
        type_list= df2.iloc[0,:].fillna("None").values.tolist()
        side_list= df2.iloc[1,:].fillna("None").values.tolist()
        frame_list=df2.iloc[2,:].fillna("None").values.tolist()


        #Filling None and Selecting everything but the first column
        type_list = fill_none(type_list)[1:]
        side_list = fill_none(side_list)[1:]
        frame_list= fill_none(frame_list)[1:]


        # Generating New Name list for the target dataframe
        name_list = NewColumnNames(frame_list)


        #Slicing the core Data
        df2=df2.iloc[3:,0:]
        df2.columns=name_list
        
        df2= df2.fillna(0)

        #Verify
        print(df2.head())


        # Generating the HoV list for both dataframes
        Test_Hov_List= df1["HoV"].values.tolist()
        Target_Hov_List= df2["HoV"].values.tolist()
        # Generating the common Hov List
        Common_Hov_list= [value for value in Target_Hov_List if value in Test_Hov_List]


        # Subset the datasets based on Common Hovs
        df1_common_hov = df1.set_index("HoV").loc[Common_Hov_list,:].fillna(0)
        df2_common_hov = df2.set_index("HoV").loc[Common_Hov_list,:].fillna(0)

        print(df1_common_hov.head())
        print(df2_common_hov.head())

        """
        NOTE: Dataframes
        DF1_COMMON_HOV
        DF2_COMMON_HOV

        AND ALL DEPENDENT DATAFRAMES  
        below this line are INDEXED ON HOV.

        """
        # Drop the Temperature and Pressure Related Columns.
        droplist=[i for i in df2_common_hov.columns if ("TEMPERATURE" in i or "PRESSURE" in i or "TZ" in i or "MIXER" in i or "Import" in i or "HUM" in i or "Test" in i )]
        df2_common_hov_trimmed= df2_common_hov.drop(droplist,axis=1)
        print(df2_common_hov_trimmed.head(2))

        # Verify if there are any all zero column in df1_common_hov
        #df1_common_hov.to_excel("op.xlsx")

        # # Generate individual dataframe subset on common hovs with  columns specific to hovs removed 
        # df1_cm_specific_hovs= df1_common_hov.loc[:,(df1_common_hov!=0).any(axis=0)] 
        # df2_cm_specific_hovs= df2_common_hov_trimmed.loc[:,(df2_common_hov_trimmed!=0).any(axis=0)]
        """
        TRIAL NEW LOGIC
        """
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
        df1_cm_specific_hovs= df1_common_hov.loc[:,(df1_common_hov!=0).any(axis=0) + df1_inclusion_series] 
        df2_cm_specific_hovs= df2_common_hov_trimmed.loc[:,(df2_common_hov_trimmed!=0).any(axis=0) + df2_inclusion_series]


        # # Generate individual dataframe subset on common hovs with  columns specific to hovs removed 
        # df1_cm_specific_hovs= df1_common_hov.copy()
        # df2_cm_specific_hovs= df2_common_hov_trimmed.copy()


        print(df1_cm_specific_hovs.shape)
        print(df2_cm_specific_hovs.shape)

        # Create list of common columns:
        common_columns= df2_cm_specific_hovs.columns.intersection(df1_cm_specific_hovs.columns)
        common_columns=common_columns.values

        print(common_columns)
        """

        EXPANDING THE DATAFRAMES WITH ALL POSSIBLE COLUMN NAMES OVER COMMON HOVS

            Generate residual dataframes
            
            Verify an print their shapes

            Generate one ALL ZERO DATAFRAMES OF THE SHAPE OF EACH RESIDUAL

            Join them to the df1_cm_specific and df2_cm_specific to get expanded dataframes



        """
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

        df1_cm_specific_hovs_expanded = df1_cm_specific_hovs_expanded.fillna(0)
        df2_cm_specific_hovs_expanded = df2_cm_specific_hovs_expanded.fillna(0)

        print(df1_cm_specific_hovs_expanded.head(2))
        print(df2_cm_specific_hovs_expanded.head(2))

        """
        CREATING THE EXPANDED DIFFERENCE DATAFRAME

        """
        df_expanded_diff = df2_cm_specific_hovs_expanded - df1_cm_specific_hovs_expanded

        print(df_expanded_diff.head(2))

        #df_expanded_diff.to_excel("op.xlsx")

        return df_expanded_diff
    
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
            tolerance= 0.001
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
    
   
    
    def _reformat_Frames(self,df):
    
        """ Apply frame renamings specific to generated frame section( from single frame value) according to the shop floor conventions.
            This is a function corresponing to oldAOframeAdapt function in vba code of the previous tool.
            This function is applied to old format ltr0.
            Similar(basic row wise functionality is same function is also applied to old format ltr2.
        
        :type self: DB0_DEF_FLOW 
        :param self: Calling object of the LTR 0 Dataset
    
        :type df: Pandas Dataframe
        :param df: Input df with generated frame ranges from Frame Range 1 function
    
        :raises:

        :return: Datframe with modified section/ frame ranges. 
        :rtype:Pandas Dataframe
        """    
        def row_format(row):    
            frame = row.loc["Frame"]
            type_ao= row.loc["type"]
            side= row.loc["side"]
            
            if(len(frame)!= 7 or not frame[1:3].isnumeric()):
                return frame            
            elif(len(frame)==7 and frame[1:3].isnumeric()):
                left= int(frame[1:3])
                right= int(frame[5:7])
                
                if(right in [18,19,79]):
                    left= right-1
                elif(right==20):
                    if(type_ao == "CAOR"):
                        left= 18
                        right= 19
                    else:
                        left= right-1
                elif(right==21):
                    if(type_ao =="LAOR"):
                        left= 22
                        right= 24
                elif(right==80):
                    if(type_ao =="CAOR"):
                        left=78
                        right=79
                    else:
                        left= right-2
                elif(right==22):
                    if(type_ao =="CAOR"):
                        left=19
                        right=21
                    else:
                        left= right-2
                elif(right==92):
                    left=90
                    right=91
                elif(right==94):
                    left= 91
                    right= 92
                else:
                    left= right-2
                    
                frame= "C" + str(left)+"-C" + str(right)  
                return frame  
            else:
                return frame
        
        df["Frame"]= df.apply(row_format,axis=1)    
        
        return df

    def _framerange_1(self,ab):
    
        """ Generate frame ranges from single frame Value
        
        :type self: DB0_DEF_FLOW 
        :param self: Calling object of the LTR 0 Dataset
    
        :type ab: Pandas Dataframe
        :param ab: Dataframe with single numeric Frame values.
    
        :raises:
    
        :rtype: Pandas Dataframe
        :return: Dataframe with Frame Ranges in the column Frame.
        """
         # Create a numpy array of frame values
        frames= ab.Frame.values
        
        def frameSection(val1, val2):
            return "C"+str(val1)+"-C"+str(val2)
        
        # Iterate over rows in ab
        for i in range(len(ab)):
            
            frame= frames[i]
            
            # Define Previous Values
            if(i==0):
                prev_frame= 17
            else:
                prev_frame= frames[i-1]
            
            #Handling integer frame values
            if(frame %1 <= 0.001):
                frame= int(frame)
                if((prev_frame % 1) >= 0.1):
                    if(abs(frame - 32) <= 0.001):
                        ab.loc[i,"Frame"]= "C30.6-C32"
                    if(abs(frame- 74) <= 0.001):
                        ab.loc[i,"Frame"]= "C72.5-C74"
                else:
                    ab.loc[i,"Frame"]= frameSection(frame-2,frame)
                    
                    
            
            # Decimal frame values
            elif(frame%1 >= 0.1):
                if(frame == 30.2):
                    ab.loc[i,"Frame"]= "C30-C32"
                elif(frame == 30.4):
                    ab.loc[i,"Frame"]= "C30.2-C30.4"
                elif(frame == 30.6):
                    ab.loc[i,"Frame"]= "C30.4-C30.6"
                elif(frame == 72.2):
                    ab.loc[i,"Frame"]= "C72-C74"
                elif(frame == 72.3):
                    ab.loc[i,"Frame"]= "C72.2-C72.3"
                elif(frame == 72.5):
                    ab.loc[i,"Frame"]= "C72.3-C72.5"
                else:
                    ab.loc[i,"Frame"]= frameSection(prev_frame,frame)            
        
        return ab
    
    

    def _readDF(self,path,file):
    
        """ Description
        
        :type self: DB0_DEF_FLOW 
        :param self: Calling object of the LTR 0 Dataset
    
        :type path: string
        :param path: Path to the repository of the file in Network Drive
    
        :type file: string
        :param file: Exact filename with extension
    
        :raises:
    
        :return: Pandas Datframe corresponding to one file Of the same shape as input HOV files.
        :rtype: Pandas Dataframe
        """    #print ("Reading %s"%file)
        df=pd.read_excel(os.path.join(path, file))
        print(file)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        df.drop(df.columns[df.columns.str.contains('num',case = False)],axis = 1, inplace = True)
        columnName=["Frame", "Length", "LAOR", "Flag", "Vdef", "CAOR", "Flag.1", "Vdef.1","CAOR.1", "Flag.2", "Vdef.2","LAOR.1", "Flag.3", "Vdef.3","V_Zone"]
        df=df.iloc[:,0:15]
        df.set_axis(labels=columnName, axis=1)
        df= df[df["Frame"].notnull()]
        humidity= df.loc[df["LAOR.1"]=="HPA",'Vdef.3'].values[0]
        self.__humidityflag = humidity 
        print(df.tail())
        return df
    
    def _processDF(self,filename, df):
    
        """ Function which reads vdef values from different columns and reshapes them into a single column dataframe
        
        :type self: DB0_DEF_FLOW 
        :param self: Calling object of the LTR 0 Dataset
    
        :type filename:string
        :param filename: Full filename with extension
    
        :type df:Pandas Dataframe
        :param df: Input data frame  of the same shape as input file and having multiple columns each for CAO,LAO, LH RH, combination.
    
        :raises:

        :return: Dataframe with one column with UNIQUE IDENTIFIABLE frame sections names 
        :rtype:  Pandas Dataframe
        """
        print ("Processing %s" % filename)
        try:
            #df=df.drop(df.index[0])
            df=df[df['Length'].notnull()]
            df0=df.iloc[:,0:2]
            df2= df.iloc[:, 5:8 ]
            df3= df.iloc[:,8:11 ]
            df4= df.iloc[:,11:14 ]
            df01= df.iloc[:,0:5 ]

            renamecol= {'Flag.1':'Flag','Flag.2':'Flag', 'Flag.3':'Flag','Vdef.1':'Vdef',
                        'Vdef.2':'Vdef','Vdef.3':'Vdef', 'CAOR.1':'CAOR', 'LAOR.1':'LAOR'  }

            renamecol2= { 'CAOR':'ID', 'LAOR':'ID'  }
            ordercol=['type','side','Frame','Length','ID',  'Flag',  'Vdef']
            df02= pd.concat([df0, df2], axis=1) 
            df03= pd.concat([df0, df3], axis=1)
            df04= pd.concat([df0, df4], axis=1)

            df02.rename(columns = renamecol, inplace = True)
            df03.rename(columns = renamecol, inplace = True)
            df04.rename(columns = renamecol, inplace = True)

            df01.rename(columns = renamecol2, inplace = True)
            df02.rename(columns = renamecol2, inplace = True)
            df03.rename(columns = renamecol2, inplace = True)
            df04.rename(columns = renamecol2, inplace = True)

            df01["type"]="LAOR"
            df01["side"]="LH"
            df02["type"]="CAOR"
            df02["side"]="LH"
            df03["type"]="CAOR"
            df03["side"]="RH"
            df04["type"]="LAOR"
            df04["side"]="RH"

            # df001=df01[ordercol]
            # df002=df02[ordercol]
            # df003=df03[ordercol]
            # df004=df04[ordercol]

            
            dff00=df01.append(df02, ignore_index = True) 
            dff00=dff00.append(df03, ignore_index = True) 
            dff=dff00.append(df04, ignore_index = True) 
            dff= dff[ordercol]
            dff = dff.replace(np.nan, 0, regex=True)
            #export(filename,dff)
        except Exception as e:
            print(e)
            print(dff.head())
        
        
                
        return dff

    
        

if __name__=="__main__":
    import os
    curdir= os.getcwd()
    print(curdir)
    export_folderpath = os.path.join(curdir,"tests\OUT\DB0_DEF")
    print(export_folderpath)
    # Please change the below path to your respective network location
    folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\0-LTRinput_flowDef"
    referenceFileName1= "DB0_DEF_FLOW.xlsx"
    reffile1= os.path.join(curdir, "tests\REF\DB0_DEF",referenceFileName1 )
    referenceFileName2= "DB0_DEF_FLOW.xlsx"
    reffile2= os.path.join(curdir, "tests\REF\DB0_DEF",referenceFileName2)

    LTR0Flow = DB0_DEF_FLOW()

    #Test 1
    LTR0Flow.importAllFiles(folderpath)
    print(LTR0Flow.df.head())
    # print(LTR0Flow.df.loc["AAL01",:])
    # print(LTR0Flow.df.loc[:,"HUM"])

    # print("\n"*6)
    # print("Printing hum rh corner")
    # print(LTR0Flow.df.loc[:,(("HUM","RH","CORNER"))])
    testfile1=LTR0Flow.export2Excel("test1_DB0_DEF_FLOW.xlsx", export_folderpath)
    exp_diff1=LTR0Flow.expandedDiff(testfile1,reffile1)
    print("Expanded diff successfull")
    exp_filename= "DB0_DEF_FLOW_EXP_DIFF_1.xlsx"
    exp_diff1.to_excel(os.path.join(curdir, "tests\RESULTS\DB0_DEF",exp_filename))
    log_filename="DB0_DEF_FLOW.log"
    diff_report_path= os.path.join(curdir, "tests\RESULTS\DB0_DEF",log_filename)
    LTR0Flow.printDiffReport(exp_diff1,filepath=diff_report_path)

    #test 2:
    new_record_path= os.path.join(curdir,"tests\\NEW\DB0_DEF\VIR02.xlsx")
    LTR0Flow.addNewRecord(filepath=new_record_path)
    testfile2= LTR0Flow.export2Excel("test2_DB0_DEF_FLOW.xlsx", export_folderpath)
    exp_diff2=LTR0Flow.expandedDiff(testfile2,reffile2)
    print("Expanded diff successfull")
    exp_filename= "DB0_DEF_FLOW_EXP_DIFF_2.xlsx"
    exp_diff1.to_excel(os.path.join(curdir, "tests\RESULTS\DB0_DEF",exp_filename))
    LTR0Flow.printDiffReport(exp_diff2,filepath=diff_report_path)
