import pandas as pd
import numpy as np
from model.interfaces import IData
class DB6_CSIRD_INFO(IData):
    def __init__(self):
        self._dataframe = pd.DataFrame
        #just wanted the property to work so made this into an Idata class.

    def parse(self,filepath):
        self._dataframe = pd.read_excel(filepath)
        print('hello')


        return self._dataframe


if __name__==" main ":

    DB6Info = DB6_CSIRD_INFO()
    DB6Info.parse(filepath='X:/Aditi/Work_Done/ADAMANT_GitHub/tests/DATA/DB6_CSIRD_INFO.xlsx')



