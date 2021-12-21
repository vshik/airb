# from model import Model
# from model.DB0_DEF.LTRFlowDef import DB0_DEF
# from model.DB4_GTR8.GTR8 import DB4_GTR8
import pandas as pd
import numpy as np
from model.interfaces import IData
import os


class DB6_CSIRD_REST_EXIST(IData):
    """
        class to instantiate the DB6_CSIRD DATASET.

    """
    # def __init__(self):
        # self.__loadpath = "X:"
        # self.export_path = r"X:/Export"
    def _processDB0_Def(self,file):
        """
        Function to process DB0_DEF file

        :type self:DB6_CSIRD_REST_EXIST
        :param self: Calling object of the DB6_CSIRD_REST_EXIST class

        :param file: Full path of DB_DEF file
        :type file: str

        :return:db0_def dataframe
        """
        df = pd.read_excel(file,'DB0 DEF')
        df = df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)
        col = df.columns
        c = []
        for i in col:
            i = i[0:3]
            c.append(i)
        df.columns = c
        for i in range(211):
            df.iloc[0, i] = c[i] + str(df.iloc[0, i]) + str(df.iloc[1, i])
        df.iloc[0, 0] = df.iloc[0, 0].replace('nanHoV', 'HoV')
        df = df.drop([df.index[1]], axis=0)
        df.columns = df.iloc[0, :]
        df = df.drop([df.index[0]], axis=0)
        oldColumnName = df.columns[0]
        df.rename(columns={oldColumnName: 'HoV'}, inplace=True)
        df = df.set_index(df.iloc[:, 0])
        df = df.drop(['HoV'], axis=1)
        # df.to_excel('df.xlsx')
        return  df




    def _processGTR8(self,file):
        """
        Function to process DB4_GTR8 file

        :type self:DB6_CSIRD_REST_EXIST
        :param self: Calling object of the DB6_CSIRD_REST_EXIST class

        :param file: Full path of DB4_GTR8 file
        :type file: str

        :return:gtr8_def dataframe
        """
        df = pd.read_excel(file, 'DB4 GTR8')
        df1 = pd.DataFrame()
        df1 = df.head(4)
        df1 = df1.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7',
                      'Unnamed: 8'], axis=1)
        for i in range(len(df1.columns)):
            df1.iloc[1, i] = str(df1.iloc[1, i]) + str(df1.iloc[2, i]) + str(df1.iloc[3, i])

        df1.iloc[2, :] = df1.columns
        df1.columns = df1.iloc[1, :]
        df1 = df1.drop([df1.index[1], df1.index[3]], axis=0)
        # df1 = df1.drop('123', axis=1)
        df1 = df1.set_index(df1.iloc[:, 0])
        df1.drop(df1.iloc[:, 211:], inplace=True, axis=1)
        df1 = df1.drop('nannanMSN', axis=1)
        c = []
        for i in df1.iloc[1, :]:
            i = str(i)
            i = i.split('.')
            d = i[0] + '.' + i[1]
            c.append(d)
        df1.iloc[1, :] = c
        # df1.to_excel('df1.xlsx')
        return df1

    def _retriveACversionName(self,val):
        """
        Function to retrive ACversion from column of dataframe.

        :type self:DB6_CSIRD_REST_EXIST
        :param self: Calling object of the DB6_CSIRD_REST_EXIST class

        :param val: String containing ACversion
        :type file: str

        :return:str
        """
        val = str(val)
        return val[15:]

    def processFiles(self, db0File, gtr8File,acVersion):
        """
        Function to get REST_EXIST value by process DB0_DEF and DB4_GTR8 file.

        :type self:DB6_CSIRD_REST_EXIST
        :param self: Calling object of the DB6_CSIRD_REST_EXIST class

        :param db0File: DB_DEF File
        :param gtr8File:DB4_GTR8 File
        :param acVersion:List containing ACversion
        :return: rest_exist dataframe
        """
        df0_def = self._processDB0_Def(db0File)
        gtr8 = self._processGTR8(gtr8File)
        gtr8.index = map(self._retriveACversionName,gtr8.index)

        # df0_def.to_excel('db0_def_processsed.xlsx')
        # gtr8.to_excel('gtr8_processed.xlsx')

        # self._dataframe.index = df0_def.index

        df_exist = pd.DataFrame(index=df0_def.index)
        df_exist['ACversion'] = acVersion
        # self._dataframe['ACversion'] = acVersion
        for hov in df0_def.index:
            for sectioname in df0_def.columns:
                if df0_def.at[hov, sectioname] > 0:
                    for acv in acVersion:
                        if (int(float(gtr8.at[acv, sectioname])) / df0_def.at[hov, sectioname]) < 1:
                            df_exist.at[hov, sectioname] = 1
                        else:
                            df_exist.at[hov, sectioname] = 0.5
                else:
                    df_exist.at[hov, sectioname] = 0
        # df_exist.to_excel('df_exist.xlsx')
        self._dataframe = df_exist

        # return df_exist

    def expandedDiff(self, testFile, refFile):
        """
        Function to generate dataframe by subtraction two dataframes.

        :type self:DB6_CSIRD_REST_EXIST
        :param self: Calling object of the DB6_CSIRD_REST_EXIST class

        :param testFile: REST_EXIST File
        :param refFile: REST_EXIST REF File
        :return: expanded_df dataframe
        """
        test = pd.read_excel(testFile)
        ref = pd.read_excel(refFile)
        ref = ref.drop(
            ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8'], axis=1)
        c = []
        for i in ref.columns:
            i = i[0:3]
            c.append(i)
        ref.columns = c
        for i in range(212):
            ref.iloc[0, i] = c[i] + str(ref.iloc[0, i]) + str(ref.iloc[1, i])

        ref.iloc[0, 0] = ref.iloc[0, 0].replace('UnnnanHoV', 'HoV')
        ref.iloc[0, 1] = ref.iloc[0, 1].replace('UnnnanAC Version', 'ACversion')

        ref = ref.drop([ref.index[1]], axis=0)
        ref.columns = ref.iloc[0, :]
        ref = ref.drop([ref.index[0]], axis=0)
        ref.iloc[:, 1] = [s.replace('Step7', '') for s in ref.iloc[:, 1]]

        ref.index = ref.iloc[:, 0] + " " + ref.iloc[:, 1]
        test.index = test.iloc[:, 0] + " " + test.iloc[:, 1]

        test = test.drop(['HoV', 'ACversion'], axis=1)
        ref = ref.drop(['HoV', 'ACversion'], axis=1)

        ref.index = [s.replace(' ', '') for s in ref.index]
        test.index = [s.replace(' ', '') for s in test.index]

        HoV_only_in_test = set(test.iloc[:, 0]) - set(ref.iloc[:, 0])
        HoV_only_in_ref = set(ref.iloc[:, 0]) - set(test.iloc[:, 0])

        test_hov = test[test.index.isin(ref.index)]
        ref_hov = ref[ref.index.isin(test_hov.index)]

        test_drop = set(test.index) - set(test_hov.index)
        print(test_drop, 'Len:', len(test_drop))

        ref_out = set(ref.index) - set(ref_hov.index)
        print(ref_out, 'Len:', len(ref_out))

        expanded_df = pd.DataFrame(columns=test_hov.columns, index=test_hov.index)

        # for i in test_hov.index:
        #     for j in test_hov.columns:
        #         expanded_df.at[i, j] = int(test_hov.at[i, j]) - int(ref_hov.at[i, j])

        expanded_df = test_hov.subtract(ref_hov)

        return  expanded_df

    def printDiffReport(self,exp_diff_df, filepath):
        '''
               import logging
               pd.set_option('display.max_rows', None)
               pd.set_option('display.max_columns', None)
               pd.set_option('display.width', None)
               pd.set_option('display.max_colwidth', -1)
               print("Writing Flow DiffFile Logger:", filepath, "\t SHAPE ", exp_diff_df.shape)
               logging.basicConfig(filename=filepath, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
               logging.info('Diff dataframe head - {}'.format(exp_diff_df))
               return logging
               '''
        print("Writing Restrictor Diff File:", filepath)
        exp_diff_df.to_excel(filepath)
        return filepath

if __name__ == "__main__":
        import os
        from pathlib import Path
        curdir = os.getcwd()
        print(curdir)
        p = Path(curdir).parent
        rootdir = p.parent
        print(rootdir)
        export_folderpath = os.path.join(rootdir, "tests\OUT\DB6_CSIRD")
        print(export_folderpath)

        # folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\Aditi\\Repository\\6-cSIRD_restrictorDef"

        db0_def_file='X:\Aditi\Work_Done\RestrictorData\Rest_Exist\db0_def.xlsx'
        gtr8_file = 'X:\Aditi\Work_Done\RestrictorData\Rest_Exist\GTR8.xlsx'
        acVersion = ['A350-900','A350-1000','A350-1000','A350-900'
                                  ,'A350-900','A350-900','A350-900','A350-900',
                                 'A350-900','A350-900','A350-900','A350-900',
                                 'A350-900','A350-900','A350-900','A350-900',
                                 'A350-900','A350-900','A350-900','A350-900',
                                 'A350-900','A350-900','A350-900','A350-900',
                                 'A350-1000','A350-1000','A350-1000','A350-900',
                                 'A350-900','A350-900','A350-1000','A350-900',
                                 'A350-900','A350-900','A350-900','A350-900','A350-1000',
                                 'A350-900','A350-900','A350-900','A350-1000','A350-900',
                                 'A350-900','A350-1000','A350-900','A350-900','A350-900',
                                 'A350-900','A350-900','A350-900','A350-1000','A350-900',
                                 'A350-900','A350-1000','A350-1000','A350-900','A350-900',
                                 'A350-900','A350-900','A350-1000','A350-900','A350-900',
                                 'A350-1000','A350-900','A350-900','A350-900','A350-1000',
                                 'A350-900','A350-900','A350-900','A350-1000','A350-1000',
                                 'A350-900','A350-1000','A350-900','A350-900']


        referenceFileName1 = "X:\Aditi\Work_Done\RestrictorData\Rest_Exist\Book_REstrictor.xlsx"
        reffile1 = os.path.join(rootdir, "tests\REF\DB6_CSIRD", referenceFileName1)

        DB6_Rest_Exist = DB6_CSIRD_REST_EXIST()

        # test1
        DB6_Rest_Exist.processFiles(db0File=db0_def_file ,gtr8File=gtr8_file,acVersion=acVersion)
        testfile1 = DB6_Rest_Exist.export2Excel('Rest_Exist_test1.xlsx',export_path=export_folderpath)

        referenceFileName1 = "DB6_CSIRD_Rest_Exist_REF.xlsx"
        reffile1 = os.path.join(rootdir, "tests\REF\DB6_CSIRD", referenceFileName1)

        exp_diff = DB6_Rest_Exist.expandedDiff(testfile1, reffile1)

        diff_filename = "DB6_CSIRD_REST_Exist_DIFF_test1.xlsx"
        diff_report_path = os.path.join(rootdir, "tests\RESULTS\DB6_CSIRD", diff_filename)
        DB6_Rest_Exist.printDiffReport(exp_diff, diff_report_path)

#         test2

        # referenceFileName2 = "DB6_CSIRD_Rest_Exist_REF.xlsx"
        # reffile2 = os.path.join(rootdir, "tests\REF\DB6_CSIRD", referenceFileName2)


