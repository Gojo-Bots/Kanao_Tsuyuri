from threading import RLock

from Powers.database import MongoDB

INSERTION_LOCK = RLock()

class USERS(MongoDB):
    db_name = "users"

    def __init__(self, user_id: int):
        super().__init__(self.db_name)
        self.user_id = user_id

    @staticmethod
    def is_user(user_id: int):
        with INSERTION_LOCK:
            collection = MongoDB(USERS.db_name)
            curr = collection.find_one({"user_id": user_id})
            if curr:
                return True
            else:
                return False
        

    def save_user(self, link: str, coin: int = 0, joined: int = 0, mess: int = 0):
        with INSERTION_LOCK:
            curr = self.find_one({"user_id": self.user_id})
            if not curr:
                self.insert_one(
                    {
                        "user_id" : self.user_id,
                        "link" : link,
                        "coin" : coin,
                        "joined" : joined,
                        "message" : mess
                    }
                )
            else:
                return False

    def get_link(self):
        with INSERTION_LOCK:
            curr = self.find_one({"user_id": self.user_id})
            if curr:
                link = curr["link"]
                return link
            else:
                return False

    def mess_update(self, is_reset:bool = False):
        with INSERTION_LOCK:
            curr = self.find_one({"user_id": self.user_id})
            if curr:
                if not is_reset:
                    mess = int(curr["message"]) + 1
                else:
                    mess = 0
                self.update(
                    {"user_id" : self.user_id},
                    {"message" : mess}
                )
                return
            else:
                return False

    @staticmethod
    def get_coin_by_link(link: str):
        with INSERTION_LOCK:
            collection = MongoDB(USERS.db_name)
            curr = collection.find_one({"link": link})
            if curr:
                coins = curr["coin"]
                return coins
            else:
                return False
    @staticmethod
    def get_all_users(raw: bool = False):
        with INSERTION_LOCK:
            collection = MongoDB(USERS.db_name)
            curr = collection.find_all()
            if curr:
                if not raw:
                    users = [int(i["user_id"]) for i in curr]
                else:
                    users = curr
                return users
            else:
                return False
    
    def rename_field(self, old, new):
        users = USERS.get_all_users()
        if users:
            updated = self.renamefield(old, new)
            return updated
        else:
            return False
    
    def new_key(self, new, value= 0):
        curr = self.find_one({"user_id": self.user_id})
        if curr:
            self.update({"user_id": self.user_id}, {str(new):value})
            return
        else:
            False

    @staticmethod
    def get_joined_by_link(link: str):
        with INSERTION_LOCK:
            collection = MongoDB(USERS.db_name)
            curr = collection.find_one({"link": link})
            if curr:
                joined = curr["joined"]
                return joined
            else:
                return False
    
    def get_info(self):
        with INSERTION_LOCK:
            curr = self.find_one({"user_id" : self.user_id})
            if curr:
                return curr
            else:
                return False

    def update_link(self, link: str):
        with INSERTION_LOCK:
            self.update(
                {"user_id" : self.user_id},
                {"link" : link}
            )
    def set_users_coin(self, amount:int):
        with INSERTION_LOCK:
            curr = self.find_one(self.user_id)
            if curr:
                self.update(
                    {"user_id":self.user_id},
                    {"coin" : amount}
                )
                return
            return
    @staticmethod
    def update_coin(link: str , amount:int ,deduct: bool = False):
        coin = USERS.get_coin_by_link(link)
        if not deduct:
            coin = int(coin) + int(amount)
        elif deduct:
            coin = int(coin) - int(amount) 
        with INSERTION_LOCK:
            collection = MongoDB(USERS.db_name)
            collection.update(
                {"link" : link},
                {"coin" : int(coin)}
                )
    @staticmethod
    def update_joined(link: str):
        join = USERS.get_joined_by_link(link)
        joined = int(join) + 1
        with INSERTION_LOCK:
            collection = MongoDB(USERS.db_name)
            collection.update(
                {"link" : link},
                {"joined" : int(joined)}
                )
    def delete_user(self):
        with INSERTION_LOCK:
            curr = self.find_one(self.user_id)
            if curr:
                self.delete_one(self.user_id)
                return
            else:
                return