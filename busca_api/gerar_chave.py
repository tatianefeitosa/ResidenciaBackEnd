import secrets

# Gere um token de 50 bytes e converta para uma string segura para URL
secret_key = secrets.token_urlsafe(50)

print(secret_key)
