from hashlib import sha256
import random
import string

def generate_secret_key(length=32):
    characters = string.ascii_letters + string.digits + '(,._-*~"<>/|!@#$%^&)+='
    return ''.join(random.choice(characters) for _ in range(length))

def make_password(plaintext, app_name, secret_key):
    salt = get_hexdigest(secret_key, app_name)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return ''.join((salt, hsh))
        
def get_hexdigest(salt, plaintext):
    return sha256((salt + plaintext).encode('utf-8')).hexdigest()

def generate_password(plaintext, app_name, length, secret_key):
    raw_hex = make_password(plaintext, app_name, secret_key)
    ALPHABET = ('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '0123456789', '(,._-*~"<>/|!@#$%^&)+=')

    num = int(raw_hex, 16)

    chars = []

    while len(chars) < length:
        n = random.randint(0, len(ALPHABET)-1)
        alpha = ALPHABET[n]
        n = random.randint(0, len(alpha)-1)
        chars.append(alpha[n])

    return ''.join(chars)

# Example usage:
plaintext = "MyPassword123"
app_name = "ExampleApp"
secret_key = generate_secret_key()

generated_password = generate_password(plaintext, app_name, 12, secret_key)
print("Generated Password:", generated_password)
