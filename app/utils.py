from passlib.context import CryptContext # to encrypt the password which user enters

# passlib's default algorithm
pwd_context = CryptContext(schemes=['bcrypt'], deprecated ='auto')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)