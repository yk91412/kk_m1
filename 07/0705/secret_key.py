import secrets

def secret_key():
    return secrets.token_hex(24)

my_secret_key = secret_key()

print(f"My secret key {my_secret_key}")