import pandas as pd
from model.utils.global_info import historical_users_df
from datetime import datetime

class DB_User():
    def __init__(self):
        self.df_user= historical_users_df
        self.df_user= self.df_user.set_index("userID")
        self.df_user= self.df_user.replace("00:00:00","",regex= True)

    def load_dataset(self,connection):
        df_table= pd.read_sql_table(table_name="DB_User",con= connection)
        # df_table= pd.read_sql_table(table_name="Flowdef",con= connection, index_col= ('type','side','Frame'))
        # df_table= df_table.set_index(["type","side","Frame"])        
        df_table= df_table.T
        print(df_table.head())
        columns_list= df_table.iloc[0].values.tolist()
        df_table= df_table.iloc[1:,:]
        df_table.columns= columns_list       
        print(df_table.head())
        return df_table
        
    
    def export_dataset(self,raw_df,connection):
        raw_df.T.to_sql("DB_User",con=connection,if_exists="replace")
                
    def add_new_user(self,userid,access_level,name= None,siglum="AIOESSA"):
        """ Add a new user

        :type self: Model
        :param self: Calling object of Model class
    
        :type user_id: string
        :param user_id: Unique Airbus user ID (FOR example SP008976)
    
        :type name: string
        :param name: Name of the user
    
        :type access_level: int
        :param access_level:Integer value corresponding to the user access level
    
        :type siglum: string
        :param siglum: Airbus team Acronym (for example AIOESSA)
    
        :raises:None
    
        :rtype:None
        """    
        user_date= datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
        new_row_dict={"userName":name,"userSiglum":siglum,"userGroup":access_level, "userDate": user_date}
        row_df= pd.DataFrame(data= new_row_dict, index= [userid])
        self.df_user= pd.concat([self.df_user,row_df],axis=0)
            
    def remove_user(self,userid):
        """ Remove the user with the given userID
        
        :type self: Model
        :param self: Calling object of Model class
    
        :type user_id: string
        :param user_id: Unique Airbus user ID (FOR example SP008976)
    
        :raises: KeyError
    
        :rtype: None
        """    
        self.df_user= self.df_user.drop(labels=userid,axis=0)

    def set_user_access(self,user_id,access_level):
        """ Set the Access level (UserGroup) of the User
        
        :type self: Model
        :param self: Calling object of Model class
    
        :type user_id: string
        :param user_id: Unique Airbus user ID (FOR example SP008976)
    
        :type level:int
        :param level: Integer value corresponding to the new access level
    
        :raises: KeyError
    
        :rtype: None
        :return: None
        """    
        self.df_user.at[user_id,"userGroup"]= access_level
    
    def get_user_access(self,user_id):
        """ Get Current Access level(UserGroup) of the given UserId
        
        :type self: Model
        :param self: Calling object of Model class
    
        :type user_id: string
        :param user_id: Unique Airbus user ID (FOR example SP008976)
    
        :raises: KeyError
    
        :rtype: int
        :return: Integer value corresponding to the current access level
        """    
        return self.df_user.at[user_id,"userGroup"]


if __name__=="__main__":
    users= DB_User()
    users.add_new_user("R01234",5,"bikan","AIOESSA")
    users.add_new_user("W01234",5,"kan","AIOESSA")
    users.add_new_user("X01234",1,"ikan","AIOESSA")
    users.add_new_user("Y01234",5,"sen","AIOESSA")
    print(users.df_user.tail())
    users.remove_user("W01234")
    users.set_user_access("X01234",5)
    print(users.df_user.tail())
    print(users.get_user_access("X01234"))



