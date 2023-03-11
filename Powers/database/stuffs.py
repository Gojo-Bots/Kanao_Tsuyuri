from threading import RLock

from Powers.database import MongoDB

INSERTION_LOCK = RLock()

class STUFF(MongoDB):
    db_name = "stuff"

    def __init__(self):
        super().__init__(self.db_name)

    def add_file(self, name: str, f_id: str, ncoin: int, dtype: str, file_type: str):
        with INSERTION_LOCK:
            name = name.lower()
            curr = self.find_one({"f_id":f_id})
            if not curr:
                self.insert_one(
                    {
                        "name": name,
                        "f_id": f_id,
                        "ncoin": ncoin,
                        "type": dtype,
                        "file_type": file_type
                    }
                )
                return True
            else:
                return False
    def file_sorted(self):
        with INSERTION_LOCK:
            curr = self.sort_by()
            return set(curr)
    def remove_file(self, f_id: str):
        with INSERTION_LOCK:
            curr = self.find_one({"f_id" : f_id})
            if curr:
                self.delete_one(curr)
                return True
            else:
                return False
    
    def get_files(self, type: str):
        curr = self.find_all({"type" : type})
        if curr:
            file_name = [i["name"] for i in curr]
            return file_name
        else:
            return False

    def get_amount(self, name: str):
        name = name.lower()
        curr = self.find_one({"name" : name})
        if curr:
            amount = curr["ncoin"]
            return amount
        else:
            return False

    def get_file_link(self, name: str):
        name = name.lower()
        curr = self.find_one({"name" : name})
        if curr:
            s_f_id = [curr["f_id"], curr["file_type"]]
            return s_f_id
        else:
            return False
    
    def get_file_info(self, name: str):
        name = name.lower()
        curr = self.find_one({"name" : name})
        if curr:
            return curr
        else:
            return False
