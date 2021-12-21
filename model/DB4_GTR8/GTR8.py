from model.interfaces import IDataset
from model.DB4_GTR8.flow import DB4_GTR8_FLOW
from model.DB4_GTR8.rest import DB4_GTR8_REST
from model.DB4_GTR8.info import DB4_GTR8_INFO
from model.DB4_GTR8.mix_rec_amb import DB4_GTR8_MIXRECAMB
from model.DB4_GTR8.pp import DB4_GTR8_PP

class DB4_GTR8(IDataset):
    def __init__(self):
        self.flow_df= DB4_GTR8_FLOW()
        self.restrictor_df= DB4_GTR8_REST()
        self.info_df = DB4_GTR8_INFO()
        self.mixrecamb_df = DB4_GTR8_MIXRECAMB()
        self.pp_df= DB4_GTR8_PP()
