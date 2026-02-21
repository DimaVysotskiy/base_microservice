from argon2 import PasswordHasher




class Security:
    """Добавить ф-ции для JWT после создания класса JWTData"""
    def __init__(self):
        self.ph = PasswordHasher()

    def hash_password(self, password: str) -> str:
        return self.ph.hash(password)

    def verify_password(self, hashed_password: str, password: str) -> bool:
        try:
            return self.ph.verify(hashed_password, password)
        except Exception:
            return False
        
        
security = Security()