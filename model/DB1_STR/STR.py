from model.interfaces import IDataset
from model.DB1_STR.flow import DB1_STR_FLOW
from model.DB1_STR.rest import DB1_STR_REST
from model.DB1_STR.info1 import DB1_STR_INFO
from model.DB1_STR.mix_rec_amb import DB1_STR_MIXRECAMB
from model.DB1_STR.pp import DB1_STR_PP

class DB1_STR(IDataset):
    def __init__(self):
        self.flow_df= DB1_STR_FLOW()
        self.restrictor_df= DB1_STR_REST()
        self.info_df = DB1_STR_INFO()
        self.mix_rec_amb_df = DB1_STR_MIXRECAMB()
        self.pp_df= DB1_STR_PP()
