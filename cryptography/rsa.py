import json
import sympy
import math
import random

def relatively_prime(a, b):
    return math.gcd(a, b) == 1

def generate_key(lower, upper):
    p = sympy.randprime(lower, upper)
    q = sympy.randprime(lower, upper)

    while p == q:
        q = sympy.randprime(lower, upper)

    n = p * q
    euler_totient = (p-1) * (q-1)

    e = random.randint(lower, upper)

    while not(relatively_prime(euler_totient, e)):
        e += 1
    
    d = sympy.mod_inverse(e, euler_totient)
    
    public_key = json.dumps({'key_type': 'public', 'exponent': e, 'modulus': n})
    private_key = json.dumps({'key_type': 'private', 'exponent': d, 'modulus': n})

    return public_key, private_key


def rsa(input, key):
    return pow(input, key['exponent'], key['modulus'])

def custom_rsa(input, exponent, modulus):
    return pow(input, exponent, modulus)

def add_zero_char(block) -> str:
    zero = ''

    for i in range(3 - len(block)):
        zero += '0'

    return zero + block

def add_zero_block(block, block_length) -> str:
    zero = ''

    for i in range(block_length * 3 - len(block)):
        zero += '0'

    return zero + block

def add_padding(block, block_length) -> str:
    padded_block = block
    
    for i in range(block_length - int(len(block) / 3)):
        padded_block += '000'

    return padded_block


def decode_bytes(input_bytes, encoding):
    return input_bytes.decode(encoding)

def decode_string(input_string, encoding):
    return input_string.encode(encoding)

def custom_generate_signature(input_string, exponent_pri, modulus, block_length):
    counter = 0
    block = ''
    ciphertext = ''

    for char in input_string:
        char_ascii = str(ord(char))

        for i in range(3 - len(char_ascii)):
            block += '0'

        block += char_ascii
    
        counter += 1

        if counter == block_length:
            encrypted_block = str(custom_rsa(int(block), exponent_pri, modulus))

            ciphertext += add_zero_char(encrypted_block) + ' '

            counter = 0
            block = ''
        
    if counter != 0:

        encrypted_block = str(custom_rsa(int(block), exponent_pri, modulus))

        ciphertext += add_zero_char(encrypted_block)

    return ciphertext

def custom_validate_signature(input_string, exponent_pub, modulus, block_length):
    blocks = [int(block) for block in input_string.strip().split()]
    block_counter = 0
    plaintext = ''

    for block in blocks:
        decrypted_block = custom_rsa(block, exponent_pub, modulus)


        if block_counter != len(blocks) - 1:
            block_length_formatting = block_length

        else:
            block_length_formatting = math.ceil(len(str(decrypted_block)) / 3)

        decrypted_block = add_zero_block(str(decrypted_block), block_length_formatting)

        counter = 0

        ascii_char = ''

        for char in decrypted_block:
            ascii_char += char
            counter += 1

            if counter == 3:
                plaintext += chr(int(ascii_char))

                counter = 0
                ascii_char = ''

        block_counter += 1


    return plaintext

def rsa_string_encrypt(input_string, key, block_length):
    counter = 0
    block = ''
    ciphertext = ''
    key_dict = json.loads(key)

    for char in input_string:
        char_ascii = str(ord(char))

        for i in range(3 - len(char_ascii)):
            block += '0'

        block += char_ascii
    
        counter += 1

        if counter == block_length:
            encrypted_block = str(rsa(int(block), key_dict))

            ciphertext += add_zero_char(encrypted_block) + ' '

            counter = 0
            block = ''
        
    if counter != 0:
        # block = add_padding(block, block_length)

        encrypted_block = str(rsa(int(block), key_dict))

        ciphertext += add_zero_char(encrypted_block)

    return ciphertext

def rsa_string_decrypt(input_string, key, block_length):
    blocks = [int(block) for block in input_string.strip().split()]
    block_counter = 0
    plaintext = ''
    key_dict = json.loads(key)

    for block in blocks:
        decrypted_block = rsa(block, key_dict)


        if block_counter != len(blocks) - 1:
            block_length_formatting = block_length

        else:
            block_length_formatting = math.ceil(len(str(decrypted_block)) / 3)

        decrypted_block = add_zero_block(str(decrypted_block), block_length_formatting)

        counter = 0

        ascii_char = ''

        for char in decrypted_block:
            ascii_char += char
            counter += 1

            if counter == 3:
                plaintext += chr(int(ascii_char))

                counter = 0
                ascii_char = ''

        block_counter += 1


    return plaintext




if __name__ == "__main__":
    pub, pri = generate_key(10, 10000000)
    print(pub, pri)

    # plaintext = 'HELLO ALICE MY NAME IS HAIDAR '
    # ciphertext = rsa_string_encrypt(plaintext, pub, 4)
    # print(ciphertext)
    # print(rsa_string_decrypt(ciphertext, pri, 4))

    # print('bruh', rsa(72069, pub), rsa(rsa(72069, pub), pri))


    # plaintext = 'HELLO ALICE MY NAME IS HAIDAR '

    # print(plaintext)


    plaintext = 'SAJIDNAEOIDW38M0EDMODFN2390MLKENDFOWNF23890DMFB8234F08FBN28FN[[[]]]'

    ciphertext = rsa_string_encrypt(plaintext, pub, 4)
    print(ciphertext)

    print('cipher', len(ciphertext))

    deciphered_plaintext = rsa_string_decrypt(ciphertext, pri, 4)
    print(deciphered_plaintext)
    
    print(plaintext == deciphered_plaintext)
    # print(plaintext_undecoded == deciphered_plaintext.encode('latin1'))

    print('bruh', rsa(72069076076, json.loads(pub)), rsa(rsa(72069076076, json.loads(pub)), json.loads(pri)))
