import rsa
import os

KEY_DIR = 'keys'

def generate_keys():
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)
    
    if not os.path.exists(os.path.join(KEY_DIR, 'public.pem')) or not os.path.exists(os.path.join(KEY_DIR, 'private.pem')):
        (pubkey, privkey) = rsa.newkeys(512)
        with open(os.path.join(KEY_DIR, 'public.pem'), 'wb') as f:
            f.write(pubkey.save_pkcs1())
        with open(os.path.join(KEY_DIR, 'private.pem'), 'wb') as f:
            f.write(privkey.save_pkcs1())

def get_public_key():
    with open(os.path.join(KEY_DIR, 'public.pem'), 'rb') as f:
        return rsa.PublicKey.load_pkcs1(f.read())

def get_private_key():
    with open(os.path.join(KEY_DIR, 'private.pem'), 'rb') as f:
        return rsa.PrivateKey.load_pkcs1(f.read())

def encrypt_password(password):
    # Ensure keys exist
    generate_keys()
    pubkey = get_public_key()
    return rsa.encrypt(password.encode('utf-8'), pubkey)

def decrypt_password(encrypted_password):
    # Ensure keys exist
    generate_keys()
    privkey = get_private_key()
    try:
        return rsa.decrypt(encrypted_password, privkey).decode('utf-8')
    except rsa.Pkcs1Error:
        return None
