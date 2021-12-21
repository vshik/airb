import  pandas as pd
import numpy as np
import os

class DB5_FTR:
    def __init__(self):
        self._list_of_dfs = {}
        self._key = []

    def _getKey_and_dfList(self,folderpath):
        """
        Function to get key values and list of files.
        :param folderpath: Complete path to the folder with all input files
        :type folderpath: string
        :return: self._key and filepaths
        :rtype :list
        :raises : FileNotFoundError
        """
        if (os.path.exists(folderpath)):
            files = os.listdir(folderpath)
            files = list(filter(lambda filename: False if filename.startswith("~") else True, files))
            filepaths = map(lambda file: os.path.join(folderpath, file), files)
            filepaths = list(filepaths)
            for f in files:
                filename = os.path.splitext(f)[0]
                self._key.append(filename)
            print("\n\n\n\n\n IMPORT DATA SUCCESSFULLY\n\n\n\n")
            return self._key , filepaths
        else:
            raise FileNotFoundError("Entered path to the import repository does not exist")

    def addDataframeToDictionary(self,folderpath):
        """
        Function to add each file as dataframe to dictioary.
        :param folderpath: Complete path to the folder with all input files
        :type folderpath: string
        :return: self._list_of_dfs
        :rtype: dictionary
        """
        key, filename = self._getKey_and_dfList(folderpath)
        for k, df in zip(key, filename):
            self._list_of_dfs[k] = pd.read_excel(df)
            print(df , ': added to dictionary with key value as: ',k)
        return self._list_of_dfs

    @property
    def list_of_dfs(self):
        return self._list_of_dfs

if __name__=="__main__":

    # test1

    import os
    from pathlib import Path
    curdir= os.getcwd()
    print(curdir)
    p = Path(curdir).parent
    rootdir = p.parent
    print(rootdir)
    folderpath = r"\\in0-india-sfs.as.airbus.corp\\Structure_HPC-2\\Thermal\\Aditi\\Repository\\5-FTR"

    DB5FTR = DB5_FTR()
    df = DB5FTR.addDataframeToDictionary(folderpath)
    print(df['MSN2'])



