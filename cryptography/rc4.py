import base64
import random
        
def isCoPrime(num1, num2):
    smallest = min(num1, num2)
    for i in range(1, smallest + 1):
        if (num1 % i == 0 and num2 % i == 0):
            gcd = i
    return gcd == 1

def keyGen(seed):
    random.seed(seed)
    return random.randint(1, 1000000) 

def vignere_extended_encrypt(plainBytes:bytes, key:str):
    keyLength = len(key)
    plainText = list(plainBytes)
    plainTextLength = len(plainText)
    result = [0 for i in range(plainTextLength)]
    for i in range(plainTextLength):
        result[i] = (((plainText[i]) + ord(key[i % keyLength])) % 256)
    return bytes(result)

def rc4_file(input_file, output_file, key):
    m = keyGen(key)
    b = keyGen(m)

    while not(isCoPrime(m, 26)):
        m += 1

    S = [0 for i in range(256)]
    for i in range(256):
        S[i] = i
        
    j = 0
    for i in range(256):
        p = (j + S[i] + ord(key[i % len(key)])) % 256 
        j = ((m * p) + b ) % 256
        S[i], S[j] = S[j], S[i]

    i = j = count = 0
    fin = open(input_file, "rb") 
    fout = open(output_file, "wb")

    p = fin.read(1)

    while p: 
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = int.from_bytes(vignere_extended_encrypt(S[j].to_bytes(1, 'big'), key)), int.from_bytes(vignere_extended_encrypt(S[i].to_bytes(1, 'big'), key))
        t = (S[i] + S[j]) % 256
        t = int.from_bytes(vignere_extended_encrypt(t.to_bytes(1, 'big'), key))
        u = S[t]  
        u = int.from_bytes(vignere_extended_encrypt(u.to_bytes(1, 'big'), key))
        c = chr(ord(p) ^ u)  
        fout.write(c.encode('latin1'))
        p = fin.read(1)

def rc4_bytes_encrypt(input_bytes, key):
    m = keyGen(key)
    b = keyGen(m)

    while not(isCoPrime(m, 26)):
        m += 1

    S = [0 for i in range(256)]
    for i in range(256):
        S[i] = i
        
    j = 0
    for i in range(256):
        p = (j + S[i] + ord(key[i % len(key)])) % 256 
        j = ((m * p) + b ) % 256
        S[i], S[j] = S[j], S[i]

    i = j = count = 0
    output_bytes = b''

    plainText = list(input_bytes)
    plainTextLength = len(plainText)

    while count < plainTextLength: 
        p = input_bytes[count]
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = int.from_bytes(vignere_extended_encrypt(S[j].to_bytes(1, 'big'), key)), int.from_bytes(vignere_extended_encrypt(S[i].to_bytes(1, 'big'), key))
        t = (S[i] + S[j]) % 256
        t = int.from_bytes(vignere_extended_encrypt(t.to_bytes(1, 'big'), key))
        u = S[t]  
        u = int.from_bytes(vignere_extended_encrypt(u.to_bytes(1, 'big'), key))
        c = chr(p ^ u)  
        output_bytes += (c.encode('latin1'))
        count += 1
    
    return bytes(output_bytes)

def rc4_text_encrypt(input_text, key):
    m = keyGen(key)
    b = keyGen(m)

    while not(isCoPrime(m, 26)):
        m += 1

    S = [0 for i in range(256)]
    for i in range(256):
        S[i] = i
        
    j = 0
    for i in range(256):
        p = (j + S[i] + ord(key[i % len(key)])) % 256 
        j = ((m * p) + b ) % 256
        S[i], S[j] = S[j], S[i]

    i = j =  0

    output_text = b''

    for count in range (len(input_text)):
        p = input_text[count]
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = int.from_bytes(vignere_extended_encrypt(S[j].to_bytes(1, 'big'), key)), int.from_bytes(vignere_extended_encrypt(S[i].to_bytes(1, 'big'), key))
        t = (S[i] + S[j]) % 256
        t = int.from_bytes(vignere_extended_encrypt(t.to_bytes(1, 'big'), key))
        u = S[t]  
        u = int.from_bytes(vignere_extended_encrypt(u.to_bytes(1, 'big'), key))
        c = chr(ord(p) ^ u)  
        output_text += (c.encode('latin1'))

    return output_text.decode('latin1')

def binary_to_base64(binary:bytes):
    return(base64.b64encode(binary))

def string_to_base64(string:str):
    return(base64.b64encode(string.encode("latin1")))

def base64_to_string(base64_string: str):
    return base64.b64decode(base64_string).decode("latin1")

def custom_rc4(encrypt, text, key):
    if encrypt:
        return string_to_base64(rc4_text_encrypt(text, key)).decode("latin1")
    else:
        return (rc4_text_encrypt(base64_to_string(text), key))


if __name__ == "__main__":
    input_file = 'test.txt'
    output_file = 'output.txt'
    output_file_2 = 'output1.txt'
    key = 'ASDASDASDASDASDASD'
    # # rc4_file(input_file, output_file, key)
    # # rc4_file(output_file, output_file_2, key)
    # ciphertext = rc4_bytes_encrypt(b'H', 'ASDFG')
    # print(binary_to_base64(ciphertext))
    # # print(rc4_bytes_encrypt(ciphertext, 'ASDFG'))
    # print(rc4_bytes_encrypt(ciphertext, 'ASDFG'))

    ciphertext = custom_rc4(True, '2539579463978 4598740766512 8509304858189 5218847607527 10188868657 4000356899009 395492846216 8286387848436 5039451896137 3391526815929 8264824530857 2278103020239 3999367175152 6089989049318 96642298260 3052916720904', 'ASDFG')

    print(ciphertext)

    print(custom_rc4(False, ciphertext, 'ASDFG'))