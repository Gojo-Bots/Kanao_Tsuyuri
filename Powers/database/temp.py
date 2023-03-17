from threading import RLock

from Powers.database import MongoDB

INSERTION_LOCK = RLock()

class TEMP(MongoDB):
    db_name = "temp"

    def __init__(self):
        super().__init__(self.db_name)
    
    def save_temp(self, user:int, money:int):
        with INSERTION_LOCK:
            curr = self.find_one({"user_id": user})
            if not curr:
                self.insert_one(
                    {
                        "user_id": user,
                        "coin": money
                    }
                )
                return
            else:
                return False

    def compensate(self):
        with INSERTION_LOCK:
            curr = self.find_all()
            return curr

    def get_temp_info(self, user):
        with INSERTION_LOCK:
            curr = self.find_one({"user_id": user})
            if curr:
                return True
            else:
                return False

    def drop_collection(self,user):
        with INSERTION_LOCK:
            self.delete_one({"user_id": user})