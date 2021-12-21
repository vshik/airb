from model.interfaces import IDataset
from model.DB3_GTR4.flow import DB3_GTR4_FLOW
from model.DB3_GTR4.rest import DB3_GTR4_REST
from model.DB3_GTR4.info import DB3_GTR4_INFO
from model.DB3_GTR4.mix_rec_amb import DB3_GTR4_MIXRECAMB
from model.DB3_GTR4.pp import DB3_GTR4_PP

class DB3_GTR4(IDataset):
    def __init__(self):
        self.flow_df= DB3_GTR4_FLOW()
        self.restrictor_df= DB3_GTR4_REST()
        self.info_df = DB3_GTR4_INFO()
        self.mixrecamb_df = DB3_GTR4_MIXRECAMB()
        self.pp_df= DB3_GTR4_PP()
