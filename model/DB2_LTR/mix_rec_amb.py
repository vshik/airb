from model.interfaces import IData
import pandas as pd

class DB2_LTR_MIX_REC_AMB(IData):
    def __init__(self):
        self._dataframe= pd.DataFrame()
