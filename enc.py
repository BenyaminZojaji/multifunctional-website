import bcrypt
class Encryption:
    def __init__(self):
        ...
        
    def hash_password(self, password):
        password = password.encode("utf-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed
        
    def check(self, password, hashed_password):
        password = password.encode("utf-8")
        if bcrypt.checkpw(password, hashed_password):
            return True
        else:
            return False
        