""" l = 6
w = 64
b = 1600
r = 1088 
c = 512
"""


def bytearray_to_int_array(b):
    result = []
    for i in range(0, len(b), 8):
        e = int.from_bytes(b[i : i + 8], byteorder="big")
        result.append(e)
    return result


def xor(a , b):
    # int_a = int.from_bytes(a, byteorder="little")
    # int_b = int.from_bytes(b, byteorder="little")
    # result_int = int_a ^ int_b
    # result = result_int.to_bytes(8, byteorder="little")
    result = a ^ b
    return result

def bytearray_not(a ):
    # result = bytearray((~b & 0xFF) for b in a)
    result = ~a 
    return result

def bytearray_and(a , b):
    # int_a = int.from_bytes(a, byteorder="little")
    # int_b = int.from_bytes(b, byteorder="little")
    # result_int = int_a & int_b
    # result = result_int.to_bytes(8, byteorder="little")
    result = a & b
    return result

def bytearray_or(a  , b ):
    # int_a = int.from_bytes(a, byteorder="little")
    # int_b = int.from_bytes(b, byteorder="little")
    # result_int = int_a | int_b
    # result = result_int.to_bytes(8, byteorder="little")
    result = a | b

    return result

def padding (input : bytearray, rate : int):

    if (rate <= 2):
        return 0
    n = len(input)
    byte_needed = rate - (n % rate)
    if byte_needed == 0:
        padding_bytes = b'\x06'
        for i in range(rate - 2):
            padding_bytes += b'\x00'
        padding_bytes += b'\x80'
    elif byte_needed == 1:
        padding_bytes = b'\x86'
    else : #byte_needed >= 2
        padding_bytes = b'\x06'
        for i in range(byte_needed - 2):
            padding_bytes += b'\x00'
        padding_bytes += b'\x80'
    return input + padding_bytes


def bitwise_rotation(b : bytes, r):
    # int_b = int.from_bytes(b, byteorder="little")
    # result_int = ( ((int_b << r) & (0XFFFFFFFFFFFFFFFF))  | (int_b >> (64 - r)))
    # result = result_int.to_bytes(8, byteorder="little")
    result = ( ((b << r) & (0XFFFFFFFFFFFFFFFF))  | (b >> (64 - r)))
    return ( result)


def keccak_round(A, round):
    RC = [
    0x0000000000000001, 0x0000000000008082,
    0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088,
    0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B,
    0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080,
    0x0000000080000001, 0x8000000080008008,
    ]
    r =  [
    [  0,  1, 62, 28, 27, ],
    [ 36, 44,  6, 55, 20, ],
    [  3, 10, 43, 25, 39, ],
    [ 41, 45, 15, 21,  8, ],
    [ 18,  2, 61, 56, 14, ]
    ]
    #Theta
    C = [ A[x][0] for x in range(5)] #Initalize
    D = [ A[x][0] for x in range(5)] 
    for x in range(5):
        C[x] = xor(xor(xor(A[x][0], A[x][1]) , xor(A[x][2], A[x][3])),A[x][4]  )
    for x in range(5):
        D[x] = xor(C[(x-1) % 5], bitwise_rotation(C[(x+1) % 5], 1))
    for x in range(5):
        for y in range(5):
            A[x][y] =  xor((A[x][y]),D[x])
    #Rho and Phi
    B = A[:] #Initialize
    for x in range(5):
        for y in range(5):
            B[y][(2*x + 3*y) % 5] = bitwise_rotation(A[x][y] , r[x][y])
    #Chi
    for x in range(5):
        for y in range(5):
            A[x][y] = xor(B[x][y] , bytearray_and( bytearray_not(B[(x+1) % 5][y])  , B[(x+2) % 5][y]))
    #Iota 
    A[0][0] = xor(A[0][0] , RC[round])
    return A

def keccak_permutation(A):
    for i in range(24):
        A = keccak_round(A,i)
    return A

def keccak_hash(message : bytearray ):
    # message = bytearray(message)
    state = [[0]*5 for i in range(5)] #init
    message = padding(message, 136) #1088/8
    #Absorb
    for i in range(0, len(message), 136):
        chunk = message[i: (i + 136) ]
        chunk = bytearray_to_int_array(chunk)
        for x in range(5):
            for y in range(5):
                if ((x + 5*y) < (len(chunk))): #Limiting to Rate
                    state[x][y] = xor(chunk[(x + 5*y)] , state[x][y])
        state = keccak_permutation(state)
    
    #Squeeze
    hashed_message = bytearray()
    count = 0
    array = []
    
    while (count < 4):
        for y in range(5):
            for x in range(5):
                if (count < 4 ):
                    temp = int.to_bytes(state[x][y], length=8, byteorder="big")
                    hashed_message += temp
                    count += 1
                    array.append(state[x][y])
        state = keccak_permutation(state)
    
    return hashed_message



import base64

# keccak_hash(b'\x01')

# print(keccak_hash(b'\x01'))

# print(bytearray_to_int_array(b'\x01\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80'))

# print(bytearray_to_int_array(b'\x01\x06\x00\x00\x00\x00\x00\x00'))
# print(int.from_bytes(b'\x01\x06\x00\x00\x00\x00\x00\x00', byteorder="big"))

if __name__ == "__main__":
    print(len(keccak_hash(b'\x12')))
    