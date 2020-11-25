from Crypto.Cipher import AES as CCAES
import random
import string
import base64

def getRandomString(length):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

def padding(text, length = 16):
    while len(text.encode('utf-8')) % length != 0:
        text += '\0'
    return text.encode('utf-8')

class AES():
    def __init__(self, key = None):
        if key:
            self.key = padding(key)
        else:
            self.key = getRandomString(16).encode('utf-8')

    def getKey(self):
        return self.key.decode('utf-8')

    def encrypt(self, text):
        aes = CCAES.new(self.key, CCAES.MODE_ECB)
        encrypt_aes = aes.encrypt(padding(text))
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')[:-1]
        return encrypted_text

    def decrypt(self, text):
        aes = CCAES.new(self.key, CCAES.MODE_ECB)
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
        return decrypted_text
