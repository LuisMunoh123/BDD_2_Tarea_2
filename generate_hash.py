
from app.repositories.user import password_hasher

plain_password = "admin123"

hashed = password_hasher.hash(plain_password)
print("Plain :", plain_password)
print("Hash  :", hashed)