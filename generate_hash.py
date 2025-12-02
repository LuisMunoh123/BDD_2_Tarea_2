# generate_hash.py
from app.repositories.user import password_hasher

# Elige la contraseña que quieras usar para el login, por ejemplo "admin123"
plain_password = "admin123"

hashed = password_hasher.hash(plain_password)
print("Plain :", plain_password)
print("Hash  :", hashed)