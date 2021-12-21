from model.utils.DB_HoV import DB_HoV
from model.utils.DB_User import DB_User
from model.utils.DB_AC import DB_AC
from model.utils.DB_ACV import DB_ACV

db_hov= DB_HoV()
db_user= DB_User()
db_ac= DB_AC()
db_acv= DB_ACV()

if __name__=="__main__":
    dbhov= DB_HoV()
    print(db_hov.df.head())
    df= db_hov.df.set_index("HoV")
    print(df.head())
