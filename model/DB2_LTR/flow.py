from pandas.core import frame
from model.interfaces import IData
import os
import pandas as pd
import re
import numpy as np


class DB2_LTR_FLOW(IData):
    """
    class to instantiate the LTR 2 DATASET.

    """
    def __init__(self):
        self._dataframe= pd.DataFrame()
        self.__loadpath = "X:"
        self.export_path=r"X:/Export"
        self.__flowdefpath="X:\DEV\Repository\\2-LTR"

        folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\DEV\\Repository\\2-LTR"
        self.importAllFilesinFolders(folderpath)
    
    def _parse(self, path, HoV,db2_ltr_test_reference=None):
    
        """ 
        PARSE ONE FILE FROM A NETWORK LOCATION RETURN A DATAFRAME WITh one row correponding to one test reference.
        
        :type self: DB2_LTR_FLOW 
        :param self: Calling object of the LTR 2 Dataset
    
        :type path: string
        :param path: Full path to the file on the specified network location 
    
        :raises:

    
        :return: Dataframe with one line indexed by HoV
        :rtype: Pandas dataframe
        

        """
        raw_df= self._read_df(path)
        hpa_value= self._getHPAvalue(raw_df)
        frame_actual_df = self._process(raw_df)
        alt1_df= self._reformat_frame_old_new(frame_actual_df)
        alt_df= self._reformatframes(alt1_df)
        frame_actual_df= alt_df

        """
        frame_actual_df is a two column dataframe which consists of Frame and Actual columns.
        It is the dataframe which needs to be transposed to create the single row dataframe .
        Frame is the uniquely identifiable section name for example,"CAO-LH-C32-C36"
        Actual is the actual measured flow value. example, 30.2
 
        """ 

        "Below are the steps to create multiindexing"

        #Creating three columns for type, side ,frame using apply  

        frame_actual_df["type"]= frame_actual_df["Frame"].apply(lambda x: x.split("-")[0])
        frame_actual_df["side"]= frame_actual_df["Frame"].apply(lambda x: x.split("-")[1])
        frame_actual_df["Frame"]= frame_actual_df["Frame"].apply(lambda x: x.split("-")[2] +"-"+ x.split("-")[3] if len(x.split("-"))==4 else x.split("-")[2])

        # create the multiindex using set index . Note that the dataframe is still a vertical one which needs to be transposed to obtain the row dataframe.
        frame_actual_df= frame_actual_df.set_index(["type","side","Frame"])
        
        """Create the Transpose dataframe.
        The below function also takes care of creating the multindex for the rows.
        The function self._createTranspose first transposes the input df, adds columns for HoV and test reference and creates a multiindex.
        Finally the function returns the single row dataframe. Please look at the comments in self._createTranspose for better understanding.
        """
        tran_df=self._createTranspose(frame_actual_df,path,HoV,hpa_value,db2_ltr_test_ref=db2_ltr_test_reference) 
        #tran_df_columns= tran_df.columns.astype("str")
        # tran_df.columns = tran_df_columns  
        # try:
        #     for i in tran_df.columns.values.tolist():            
        #         if i in ["-1001","-1001.0","-1001.00","-1001.000"]:
        #             tran_df= tran_df.drop(labels=i,axis= 1)
        # except:
        #     pass  
        # # Rearrange the Columns in Ascending Order
        # tran_df= tran_df.sort_index(axis=1)
        # # tran_df["ID"]= tran_df["HoV"] + tran_df["Test Reference"]
        # # tran_df= tran_df.set_index("ID")    
        # #
          
                 
        return tran_df

    
    def importAllFilesinFolders(self, folderpath):

        """ Function to import data from all files in folders and append them to the dataset
        To be over ridden by the derived classes.
        
        :type self: DB2_LTR_FLOW 
        :param self: Calling object of the LTR 2 Dataset
    
        :type folderpath: string
        :param folderpath: Absolute path to the repository which consists of folders for each HoV and each subsequent folder has input files for each test reference.

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

            
                    self.addNewRecord(filepath= fil_path,HoV=i)


            print(" IMPORT DATA SUCCESSFULLY: ", folderpath)

        else:
            raise FileNotFoundError("Entered path to the import repository does not exist")
        
    def addNewRecord(self, filepath, HoV= None, ACversion= None,db2_ltr_test_reference= None):

        """ Adds a new record (a new Test reference ) to the existing dataframe by reading one file. 

        :type self: DB2_LTR_FLOW 
        :param self: Calling object of the LTR 2 Dataset

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
        
        #self.load_data()
        if(os.path.exists(filepath)):
            path_elements= os.path.split(filepath)
            file_df = self._parse(filepath, HoV,db2_ltr_test_reference= db2_ltr_test_reference)
            filename= path_elements[1]
            try:
                    self._dataframe=pd.concat([self._dataframe,file_df],axis=0)
                
            except:
                    print ("Exception occurred for: ",filename)
                                            
        else:
            raise FileNotFoundError("Entered path to the File does not exist")
        #self.export()
       
    
        

    def export(self):
        """
        Creates a backup of the calling LTR2 Datset using export path  
        
        Writes the new load path to a config file on network drive.
        """
        pass
    
    def _getHPAvalue(self,raw_df):
    
        """ Get the HPA value from the raw file dataframe
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
    
        :type raw_df: Pandas dataframe
        :param raw_df: Raw Dataframe which results from reading the file as it is.
    
        :raises:
    
        :return: HPA value
        :rtype: float
        """    
        hpa_value =0
        try:
            first_column = raw_df.iloc[:,0]
            hpa_index= first_column[first_column=="HPA"].index[0]
            hpa_value = raw_df.iloc[hpa_index,1]
        except:
            pass
        finally:
            return hpa_value

    def _read_df(self, path):
    
        """ Read the dataframe from an input file as is and return a raw input dataframe.
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
        
        :type path: string
        :param path: Path to the input file corresponding to a Test Reference

    
        :raises: FileNotFoundError
        
        :return: Raw Dataframe of the same shape as the input data read as it is from the file.
        :rtype: Pandas Dataframe
        """    
        raw_df = pd.read_excel(path,sheetname="Flow",header= None,skiprows=3)
        return raw_df
    
    def __postprocess_df(self,df):
    
        """ Does some postprocessing to remove nan values and -1001 values on the final output dataset.
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
    
        :type df: Pandas Dataframe
        :param df: Output datframe obtained after concatenating multiple single row dataframes.
    
        :raises:
        
        :return: Cleaned output dataframe without nan "n/a" or -1001 values indexed by HoV
        :rtype: Pandas dataframe
        """   
        output_df= df
        output_df=output_df.fillna(0)
        output_df = output_df.replace(["nan","n/a","#N/A","-1001.0","-1001.00","-1001.000"],0)
        output_df = output_df.replace([-1001.0],0)

        #output_df = output_df.set_index("HoV")
        return output_df

            
    def _process(self,raw_df):
    
        """ Function to preprocess the raw dataframe and reshape into a one column intermediate dataframe on 
        which transformations(mostly section renamings) can be applied.
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
    
        :type raw_df:Pandas Dataframe
        :param raw_df:  Raw Dataframe of the same shape as the input data read as it is from the file.
    
        :raises:None

        :return: Intermediate Dataframe with only two columns one for Frame and other for flow value.
        :rtype:Pandas Dataframe
        """        
        
        # find the row with index all nan values
        rows_with_nan = [index for index,row in raw_df.iterrows() if row.isnull().all()]
        #print(rows_with_nan)
        # Subset the data on flow value rows only which are denoted by the 
        # first and the second value in the row_with nan list.
        
        
        """
        LOGIC TO DETERMINE WHERE THE FLOW TABLE ENDS
        """
        table_end_index= 0
        if(rows_with_nan[0]<30):
            table_end_index = rows_with_nan[1]
        elif(rows_with_nan[0]>40):
            table_end_index = rows_with_nan[0]
        else:
            table_end_index= rows_with_nan[1]


        """
        alter the below line to change the logic 
        If the above logic doesnt work then fallback to using 
        flow_data= raw_df.iloc[:rows_with_nan[1],:]
        """
        #flow_data= raw_df.iloc[:rows_with_nan[1],:]
        flow_data= raw_df.iloc[:table_end_index,:]

        # get the top row as a list and process it
        top_row_list= flow_data.iloc[0].values.tolist()
        #print(top_row_list)
        
        try:
            first_cut_index= top_row_list.index("Total TZ")
            second_cut_index= top_row_list.index("CAO RH")
            last_index= top_row_list.index("Remark")
        except:
            print("input file is misformatted")
        # DECIDE WHAT TO RETURN IF INPUT FILE IS MISFORMATTED.
            return
        
        #left_df= flow_data.iloc[:,:first_cut_index]
        #right_df= flow_data.iloc[:,second_cut_index:last_index]

        """
        Defining the split indices
        and 
        Splitting the Data into 
        left LAO,
        left CAO.,
        RIGHT CAO,
        RIGHT LAO,
        dataframes

        """
        left_cao_lao_split_index= top_row_list.index("TZ")
        right_cao_lao_split_index= top_row_list.index("TZ",first_cut_index)
        
        left_lao_df = flow_data.iloc[:,1:left_cao_lao_split_index]
        left_cao_df=  flow_data.iloc[:,left_cao_lao_split_index+1:first_cut_index]
        right_cao_df= flow_data.iloc[:,second_cut_index:right_cao_lao_split_index]
        right_lao_df= flow_data.iloc[:,right_cao_lao_split_index+1:last_index]

        temp_df_list =[left_lao_df,left_cao_df,right_cao_df,right_lao_df]
        frame_series= flow_data.iloc[:,0]
        
        # #for i in temp_df_list:
        #     print(i.head())
    
        # function to add frames and reindex
        def addreindex(df):
            #print(df.head())
            df.insert(loc=0,column= "Frame",value=frame_series)
            df= df.reindex()
            #print(df.head())
            return df
        
        #Function to reformat frame names into uniquely identifiable frames 
        def reformat_rows(df):
            head_row_list = df.iloc[0].values.tolist()
            #print(head_row_list)
            value= ""
            
            #Get the type and side of the df store in value
            for i in head_row_list:
                if(isinstance(i,str)):
                    value= i
                    break

            # Format the frame name to add type and side    
            def format_string(x):
                if(isinstance(x,str)):
                    str_1= value + " " + x
                    str_1= str_1.replace(" ","-")
                    str_1= str_1.replace(",",".")
                    return str_1
                else:
                    return np.nan  
            df["Frame"]= df.loc[:,"Frame"].apply(format_string)

            # get the value of type and side of frame
            #print(df.iloc[10:15,:])
            #print(value)

            #Reset and rename columns
            proc_df= df.iloc[2:,:]
            proc_df.columns=  ["Frame","Actual (l/s)","Target (l/s)","Deviation (%)"]
            #print(proc_df.iloc[10:15,:])
            return proc_df

        def format_df(df):
            """ function to add above transformations in order."""
            df1= addreindex(df)
            df1= reformat_rows(df1)
            # Fill na values
            df1= df1.fillna(-1001)
            #Round to 2 decimal places
            df1= df1.round(3)
            # Fill na values
            #print(df1.head())
            return df1


        # Generate a list of dataframes to be concatenated
        new_df_list = list(map(format_df,temp_df_list)) 
        
        # verify the type of the elements of new df list
        #print(type(new_df_list[0]))
        
        # Concatenate the dataframe.
        concat_df= pd.concat(new_df_list,axis=0)
        
        # Verify Concat_df tail and shape
        #print(concat_df.tail())
        #print(concat_df.shape)

        """
        BELOW COMES THE LOGIC TO TRANSPOSE THE CONCATENATED  DATAFRAME

        """
        

        # aDD A cOLUMN TO CONCAT DATAFRAME WHICH CONTAINS ALL THE DATA AS A STRING
        
        """
        APPARENTLY WE NEED ONLY THE ACTUAL VALUES NOT TARGET OR DEVIATION VALUES 
        THEREFORE WE WILL SUBSET THE DATAFRAME INTO fRAME AND ACTUAL NUMBERS

        """



        frame_actual_df = concat_df.loc[:,["Frame","Actual (l/s)"]] 
        frame_actual_df= frame_actual_df.replace(["n/a","N/A","#N/A"],0) 
        #print("\n\n\n\n\n\n\n PRINTING FRAME ACTUAL DF\n\n\n\n")
        #print(frame_actual_df.head())
        return frame_actual_df  
        
        
    

    def _reformat_frame_old_new(self,df):
    
        """ Apply frame renamings according to the shop floor conventions.
            This is a function corresponing to oldAOframeAdapt function in vba code of the previous tool.
            This function is applied to old format ltr0.
            Similar(basic row wise functionality is same function is also applied to old format ltr2. 
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
    
        :type df: Pandas Dataframe
        :param df: Intermediate datframe returned by self.process() of the calling object.
    
        :raises:

        :return: Cleaned dataset with 2 columns one for Frame and other for Actual flow definition values.
        :rtype: Pandas Dataframe 
        """    
        def row_format(row):
            frame_desc = row["Frame"]
            # Split the comlpete frame description
            element_list = frame_desc.split("-")
            restrictor_type= element_list[0]
            restrictor_side = element_list[1]
            start_frame= element_list[2]
            end_frame= element_list[3]

            frame_final= start_frame + "-" + end_frame   

                  
            if(len(frame_final)!= 7 or not frame_final[1:3].isnumeric()):
                return frame_desc            
            elif(len(frame_final)==7 and frame_final[1:3].isnumeric()):
                left= int(frame_final[1:3])
                right= int(frame_final[5:7])
                if(right in [18,19,79]):
                    left= right-1
                elif(right==20):
                    if(restrictor_type == "CAO"):
                        left= 18
                        right= 19
                    else:
                        left= right-1
                elif(left==78 and right==80):
                    if(restrictor_type =="CAO"):
                        left=78
                        right=79
                    else:
                        left= right-2
                elif(right==22):
                    if(restrictor_type =="CAO"):
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
                    
                frame= "-".join([restrictor_type,restrictor_side,("C" + str(left)+"-C" + str(right))])  
                return frame  
            else:
                return frame_desc
        
        #Dropping all frame rows with numeric values
        df=df.loc[df["Frame"].apply(lambda x: not str(x)[1:].isdigit()),:]

        df["Frame"] = df.apply(row_format,axis=1)    
        
        return df
    
    def _reformatframes(self,frame_df):
    
        """ Funtion to perform additional correction on the frame names based on version. 
        Maps the correct column names and removes duplicate frame section names.
        Function for new format ltr2 only.
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
    
        :type frame_df: Pandas Dataframe
        :param frame_df: Dataframe resulting after calling self._reformatframesoldnew(). 
    
        :raises:
    
        :return: Final Cleaned dataset with unique frame section names and 2 column namely Frame ,Actual (flow definition values).
        :rtype: Pandas Dataframe 
        """    
        new_frame_df= pd.DataFrame(columns=["Frame_section","Frame","Actual (l/s)"])
        
    
        
        for index,row in frame_df.iterrows():
            new_row_dict= {}
            #Look at the frames already existing
            # We will have a frame section column in each new df.

            #print("Printing row",row,sep="\n")

            flow_value = float(row["Actual (l/s)"])
            frame_list= new_frame_df["Frame"].values.tolist()
            # Find frame
            frame_desc = row["Frame"]
            if(not(isinstance(frame_desc,str))): 
                continue

            # Split the comlpete frame description
            element_list = frame_desc.split("-")
            restrictor_type= element_list[0]
            restrictor_side = element_list[1]
            start_frame= element_list[2]
            end_frame= element_list[3]
            frame_final= start_frame + "-" + end_frame

             
            if(frame_final in ["C20-C21","C21-C22"]):
                new_frame="-".join([restrictor_type,restrictor_side ,"C20-C22"])                
                new_row_dict={"Frame_section":"C20-C22", "Frame":new_frame, "Actual (l/s)": flow_value}
                new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)

            elif(frame_final=="C41-C42"):
                    new_frame="-".join([restrictor_type,restrictor_side ,"C40-C42"])
                     
                    new_row_dict={"Frame_section":"C40-C42", "Frame":new_frame, "Actual (l/s)": flow_value}
                    new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)
            
            

            elif(frame_final=="C78-C80" and restrictor_type =="CAO"):
                    new_frame="-".join([restrictor_type,restrictor_side ,"C78-C79"])
                    new_row_dict={"Frame_section":"C78-C79", "Frame":new_frame, "Actual (l/s)": flow_value}
                    new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)
            
                        

            elif(frame_final in ["C90-C91","C91-C92","C86-C88","C88-C90"]):
                if(frame_final=="C90-C91"):
                    if(restrictor_type =="LAO"):
                        new_frame="-".join(["CAO",restrictor_side ,"CAS"])
                         
                        new_row_dict={"Frame_section":"CAS", "Frame":new_frame, "Actual (l/s)": flow_value}
                        new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)


                elif(frame_final=="C91-C92"):
                    if(restrictor_type =="LAO"):
                        new_frame="-".join(["LAO",restrictor_side ,"CORNER"])
                         
                        new_row_dict={"Frame_section":"CORNER", "Frame":new_frame, "Actual (l/s)": flow_value}
                        new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)
                    else:
                        new_frame="-".join(["CAO",restrictor_side ,"C92-C93"])                        
                        new_row_dict={"Frame_section":"C92-C93", "Frame":new_frame, "Actual (l/s)": flow_value}
                        new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)

                

                elif(frame_final== "C88-C90"):
                    new_frame="-".join(["CAO",restrictor_side ,"C88-C89"])
                    
                    new_row_dict={"Frame_section":"C88-C89", "Frame":new_frame, "Actual (l/s)": flow_value}
                    new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)
                
                elif(frame_final== "C86-C88"):
                    new_frame="-".join(["CAO",restrictor_side ,"C86-C88"])
                    
                    new_row_dict={"Frame_section":"C86-C88", "Frame":new_frame, "Actual (l/s)": flow_value}
                    new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)
                
            elif(frame_final=="C30-C30.2" or frame_final == "C30-C30,2"):
                new_frame="-".join([restrictor_type,restrictor_side ,"C30-C32"])                    
                new_row_dict={"Frame_section":"C30-C32", "Frame":new_frame, "Actual (l/s)": flow_value}
                new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)
            
            elif(frame_final=="C72-C72.2" or frame_final == "C72-C72,2"):
                new_frame="-".join([restrictor_type,restrictor_side ,"C72-C74"])                    
                new_row_dict={"Frame_section":"C72-C74", "Frame":new_frame, "Actual (l/s)": flow_value}
                new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)


            else:
                new_row_dict={"Frame_section":frame_final, "Frame":frame_desc, "Actual (l/s)": flow_value}
                new_frame_df= new_frame_df.append(new_row_dict, ignore_index =True)        
        
            
                

                

        # new_frame_df=new_frame_df.replace(-1001,np.nan)
        # new_frame_df= new_frame_df.replace(-1001.000,np.nan)
        # new_frame_df= new_frame_df.dropna(axis=0, how="all")             
        #new_frame_df=new_frame_df.drop_duplicates()
        new_frame_df=new_frame_df.drop(labels="Frame_section",axis= 1)
        # Group duplicate values and aggregate them
        new_frame_df= new_frame_df.groupby(["Frame"]).max()
       
       #GROUPING LEADS TO AN INDEXED DATAFRAME WHICH NEEDS TO BE RESET BEFORE DOWNSTREAM PROCESSING.
        new_frame_df= new_frame_df.reset_index()
        return new_frame_df 
        # new_frame_df= new_frame_df.astype({"Frame":"str","Actual (l/s)":"float"})
        
        # return new_frame_df 

    def _createTranspose(self,df,fil_path,HoV,hpa_value,db2_ltr_test_ref= None):
    
        """  Function transposes the cleaned 2 column dataset obtained from self._reformatframes 
        and adds other values as columns namely, HPA flow rate, MixP and Test Reference
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
    
        :type df:Pandas Dataframe
        :param df: Dataframe resulting from self._reformatframes() and having only 1 columns and multiindex. 
    
        :type fil_path: string
        :param fil_path: Path to the input file corresponding to a Test Reference
    
        :type HoV: string
        :param HoV: HoV of the aircraft.
    
        :type hpa_value: float
        :param hpa_value: Hpa value for the particular aircraft.
    
        :raises:
    
        :return: Transposed Datframe containing only one row with flow values for a particular Test Reference.   
        :rtype: Pandas Dataframe
        """   
       
        #Create the raw transpose of the input dataframe .
        raw_transpose= df.T
        filename= str(os.path.split(fil_path)[1])
        #raw_transpose.columns= raw_transpose.iloc[0]
        # raw_transpose= raw_transpose.drop("Frame",axis= 0 )
        #raw_transpose= raw_transpose.drop("Frame",axis= 1 )
        #print(raw_transpose.head())

        #remove file extension from file name
        filename= re.sub(r'\.x[a-z]*$','',filename)

        # Code to add the Test reference column to the single row dataframe.
        if(db2_ltr_test_ref == None):
                filename= str(os.path.split(fil_path)[1])
                #remove file extension from file name
                filename= re.sub(r'\.x[a-z]*$','',filename)
                #experiment_type_string=""
            
                # CHeck if filename contains HoV
                if(filename.find(HoV) != -1):
                    file_index= filename[::-1].find("-")
                    index_of_split= len(filename)- file_index -1
                    experiment_type_string= filename[index_of_split+1:]
                    raw_transpose["Test Reference"]= experiment_type_string
                else:
                    experiment_type_string= filename.replace("-","")
                    raw_transpose["Test Reference"]= experiment_type_string
        else:
            raw_transpose["Test Reference"] = db2_ltr_test_ref
        
                  
        #Insert the HoV column to the Single row Dataframe
        raw_transpose.insert(0,"HoV",HoV)
        

        
        #print(raw_transpose.head())
        #print(raw_transpose.index.values.tolist())
        
        #Create a multiindex using df.set_index
        raw_transpose= raw_transpose.set_index(["HoV","Test Reference"])
        
        #Return the single row dataframe.
        return raw_transpose



    def getimportpath(self):
    
        """ Get the path to the repository in network drive from where the data will be imported
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
        
        :raises:
        :return: Current import path   
        :rtype: string
        """   
        return self.__flowdefpath 
    
    def setimportpath(self,path):

        """  Set the path to the import Repository
        
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET

        :type file: string
        :param file: Exact filename with extension

        :raises:

        :rtype: None
        """
        if(os.path.exists(path)):
            self.__flowdefpath= path
        else:
            print("New Import path does not exists")

    def expandedDiff(self,testFile, refFile):
        """ Generates expanded difference between read and original data from test and ref files
        
        :type self: DB2_LTR_FLOW 
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
        print(df1.head())

        type_list= df1.iloc[0,:].fillna("None").values.tolist()
        #Side of Air Outlet
        side_list= df1.iloc[1,:].fillna("None").values.tolist()
        
        frame_list= df1.iloc[2,:].fillna("None").values.tolist()

        

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

        type_list = fill_none(type_list)[1:]
        side_list = fill_none(side_list)[1:]
        frame_list = fill_none(frame_list)[1:]

        
        
        def NewColumnNames(type_list,side_list,frame_list):
            try:
                a= len(frame_list)
                # Initialising the name list with the name of the first column
                name_list=["HoV","Test Reference"]
                for i in range(1,a):
                    name= str(type_list[i]) +"-"+ str(side_list[i]) + "-"+ str(frame_list[i]) 
                    name_list.append(name)
            except Exception as e:
                print(e)
                print("List Lengths are not equal")
            finally:
                return name_list

        name_list = NewColumnNames(type_list, side_list, frame_list)
        print(name_list)

        # Slicing the Core Data (Getting the data except the column names)
        df1=df1.iloc[4:,0:]
        
        #Assigning new Column Names
        df1.columns=name_list
        df1= df1.fillna(method= "ffill",limit= 6)


        # #df1= correctcolumns(df1,frame_list,type_list,side_list)
        # #type_indexes=
        print(df1.head())

        df2= pd.read_excel(io= refFile, sheet_name=1,engine="xlrd",header=None,index_col= None)
        print(df2.head())

        # Listing the Type, Side and Frame Section
        type_list= df2.iloc[0,:].fillna("None").values.tolist()
        side_list= df2.iloc[1,:].fillna("None").values.tolist()
        frame_list=df2.iloc[2,:].fillna("None").values.tolist()


        #Filling None and Selecting everything but the first column
        type_list = fill_none(type_list)[1:]
        side_list = fill_none(side_list)[1:]
        frame_list= fill_none(frame_list)[1:]


        # Generating New Name list for the target dataframe
        name_list = NewColumnNames(type_list,side_list,frame_list)

        #Slicing the core Data
        df2=df2.iloc[3:,0:]
        df2.columns=name_list
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
        df1_common_hov = df1.set_index("ID").loc[Common_Hov_list,:].fillna(0)
        df2_common_hov = df2.set_index("ID").loc[Common_Hov_list,:].fillna(0)
        
        # drop duplicated indices:
        df1_common_hov= df1_common_hov[~df1_common_hov.index.duplicated(keep="first")]
        df2_common_hov= df2_common_hov[~df2_common_hov.index.duplicated(keep="first")]

        droplist= [i for i in df1_common_hov.columns if("mixP" in i) ]
        df1_common_hov= df1_common_hov.drop(droplist,axis=1)
        print(df1_common_hov.head())
        print(df2_common_hov.head())

        # Drop the Temperature and Pressure Related Columns.
        droplist=[i for i in df2_common_hov.columns if ("TEMPERATURE" in i or "PRESSURE" in i or "TZ" in i or "MIXER" in i or "Import" in i or "HPA" in i or "Test" in i or "Restrictors" in i or "Notes" in i or "mixP" in i)]
        df2_common_hov_trimmed= df2_common_hov.drop(droplist,axis=1)
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
        df2_cm_specific_hovs= df2_cm_specific_hovs.drop(["HoV"], axis = 1)

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
    
    
    
    
    def getexportpath(self):
    
        """ Get the export repository path
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
    
        :raises:

        :return: Current export path    
        :rtype:string 
        """  
        return self.export_path 
    
    def setexportpath(self,path):
    
        """ Set the export repository path
        :type self:DB2_LTR_FLOW
        :param self: Calling Object of LTR2 DATASET
    
        :type file: string
        :param file: Exact filename with extension
    
        :raises:
    
        :rtype: None
        """ 
        if(os.path.exists(path)):
            self.export_path= path
        else:
            print("New EXPORT path does not exists")   
    
    
    

if __name__=="__main__":
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
    
       
    LTR2_flow = DB2_LTR_FLOW()

    #Test 1
    LTR2_flow.importAllFilesinFolders(folderpath)
    print(LTR2_flow.df.head())
    testfile1= LTR2_flow.export2Excel("test1DB2_FLOW.xlsx", export_folderpath)
    reffile1= os.path.join(curdir,"tests\REF\DB2_LTR","DB2_LTR_ADAMANT.xlsx")
    exp_diff1=LTR2_flow.expandedDiff(testfile1,reffile1)
    print("Expanded diff successfull")
    log_filename="DB2_LTR_FLOW.log"
    diff_report_path= os.path.join(curdir, "tests\RESULTS\DB2_LTR",log_filename)
    LTR2_flow.printDiffReport(exp_diff1,filepath=diff_report_path)

    #test 2:
    #
    # LTR2_flow.addNewRecord(filepath="X:\DEV\Repository\D0008-MIX22.xlsm",HoV= "D0008")
    new_record_path= os.path.join(curdir,"tests\\NEW\DB2_LTR\D0008-MIX22.xlsm")
    LTR2_flow.addNewRecord(filepath=new_record_path,HoV= "D0008",ACversion=None,db2_ltr_test_reference="MIX18")
    testfile2= LTR2_flow.export2Excel("test2DB2_FLOW.xlsx", export_folderpath)
    exp_diff2=LTR2_flow.expandedDiff(testfile2,reffile1)
    print("Expanded diff successfull")
    LTR2_flow.printDiffReport(exp_diff2,filepath=diff_report_path)
