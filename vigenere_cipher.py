import base64
import string
import sys

def vigenere_matrix(chars=string.printable, debug=False):
    l = []
    for i in range(len(chars)):
         left = chars[i:]
         right = chars[:i]
         if debug:
             print('{}{}'.format(left, right))
         l.append([i for i in ''.join((left, right))])
    return l

class VigenereCipher(object):
    def __init__(self, chars=string.printable, debug=False):
        """charset is a string containing all the allowed chars"""
        self.chars = chars
        self.matrix = vigenere_matrix(chars)
        self.debug = debug
    
    def get_mapped_char(self, x, y):
        return self.matrix[y][x]
    
    def get_keystream(self, key, lenght):
        res = ''
        while len(res) < lenght:
            for char in key:
                 if len(res) == lenght: break
                 res += char
        return res
    
    def get_mapped_position(self, char1, char2):
        col = self.chars.index(char1)
        row = self.chars.index(char2)
        return self.matrix[col][row]
    
    def get_reverse_position(self, char1, char2):
        row = self.chars.index(char1)
        col = self.matrix[row].index(char2)
        return self.chars[col]
    
    def crypt(self, text, key):
        res = ''
        keystream = self.get_keystream(key, len(text))
        for pos in range(len(text)):
            m = self.get_mapped_position(text[pos], 
                                         keystream[pos])
            res += m
            if self.debug: 
                print(text[pos], keystream[pos], m)
        return res
    
    def decrypt(self, text, key):
        res = ''
        keystream = self.get_keystream(key, len(text))
        for pos in range(len(keystream)):
            m = self.get_reverse_position(keystream[pos], 
                                          text[pos])
            res += m
            if self.debug: 
                print(text[pos], keystream[pos], m)
        return res

if __name__ == '__main__':
    cipher = VigenereCipher()
    text = "ATTACK AT DAWN WITH SPACES"
    key = "avi mo ca si fforte".upper()

    crypted = cipher.crypt(text, key)
    decrypted = cipher.decrypt(crypted, key)
    
    if sys.version_info.major > 2:
        crypted_b64 = base64.b64encode(crypted.encode('utf-8'))
    else:
        crypted_b64 = base64.b64encode(crypted)
    print('Crypted text: ', crypted)
    print('Crypted text encoded in base64: ', crypted_b64.decode('ascii'))
    print('Decrypted text: ', decrypted)
