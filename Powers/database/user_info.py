from threading import RLock

from Powers.database import MongoDB

INSERTION_LOCK = RLock()

class USERS(MongoDB):
    db_name = "users"

    def __init__(self, user_id: int):
        super.__init__(self.db_name)
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
        

    def save_user(self, link: str, coin: int = 0, joined: int = 0):
        with INSERTION_LOCK:
            curr = self.find_one({"user_id": self.user_id})
            if not curr:
                self.insert_one(
                    {
                        "user_id" : self.user_id,
                        "link" : link,
                        "coin" : coin,
                        "joined" : joined
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
    
    def get_info(self):
        with INSERTION_LOCK:
            curr = self.find_one({"user_id" : self.user_id})
            if curr:
                return curr
            else:
                return False

    def update_link(self, link: str):
        with INSERTION_LOCK:
            curr = self.update(
                {"user_id" : self.user_id},
                {"link" : link}
            )
    
    @staticmethod
    def update_coin(link: str , deduct: int = 0):
        coin = USERS.get_coin_by_link(link)
        if not deduct:
            coin = int(coin) + 1
        elif deduct:
            coin = int(coin) - int(deduct) 
        with INSERTION_LOCK:
            collection = MongoDB(USERS.db_name)
            collection.update(
                {"link" : link},
                {"coin" : int(coin)}
                )