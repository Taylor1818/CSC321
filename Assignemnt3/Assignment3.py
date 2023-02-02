import random
from Crypto.Hash import SHA256
from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def task1_1():
    p = 37
    g = 5

    x = random.randint(1, p - 2)
    y = random.randint(1, p - 2)
    print("p = " + str(p))
    print("g = " + str(g))
    print("x = " + str(x))
    print("y = " + str(y))

    A = pow(g, x) % p
    B = pow(g, y) % p
    print("\n")
    print("A = " + str(A))
    print("B = " + str(B))

    s1 = pow(A, y) % p
    s2 = pow(B, x) % p
    print("\n")
    print("s1 = " + str(s1))
    print("s2 = " + str(s2))

    k = SHA256.new()
    k.update(bytes(s1))
    truncate_k = bytes(k.hexdigest()[0:16], encoding='utf8')
    print("The key is " + truncate_k.decode('utf8'))

    iv = get_random_bytes(16)
    alice_message = pad(bytes("Hi Bob!", encoding='utf8'), AES.block_size)
    bob_message = pad(bytes("Hi Alice!", encoding='utf8'), AES.block_size)
    print("\n")
    print(unpad(alice_message, AES.block_size))
    print(unpad(bob_message, AES.block_size))

    cipher = AES.new(truncate_k, AES.MODE_CBC, iv)
    alice_ciphertext = cipher.encrypt(alice_message)
    print("\n")
    print("Alice's ciphertext: ", end="")
    print(alice_ciphertext)

    cipher = AES.new(truncate_k, AES.MODE_CBC, iv)
    bob_ciphertext = cipher.encrypt(bob_message)
    print("Bob's ciphertext: ", end="")
    print(bob_ciphertext)

    cipher = AES.new(truncate_k, AES.MODE_CBC, iv)
    bob_message = cipher.decrypt(bob_ciphertext)
    print("\n")
    print("Bob's message: ", end="")
    print(unpad(bob_message, AES.block_size))

    cipher = AES.new(truncate_k, AES.MODE_CBC, iv)
    alice_message = cipher.decrypt(alice_ciphertext)
    print("Alice's message: ", end="")
    print(unpad(alice_message, AES.block_size))
    

def task1_2():
    p = "B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371"
    g = "A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5"
    p = int.from_bytes(bytes(p, encoding="utf8"), "big")
    g = int.from_bytes(bytes(g, encoding="utf8"), "big")

    x = random.randint(1, p - 2)
    y = random.randint(1, p - 2)

    A = pow(g, x, p)
    B = pow(g, y, p)
    print("\n")
    print("A = " + str(A))
    print("B = " + str(B))

    s1 = pow(A, y, p)
    s2 = pow(B, x, p)
    print("\n")
    print("s1 = " + str(s1))
    print("s2 = " + str(s2))

    k = SHA256.new(bytes(str(s1), encoding='utf8'))
    truncate_k = bytes(k.hexdigest()[0:16], encoding='utf8')
    print("The key is " + truncate_k.decode('utf8'))

    iv = get_random_bytes(16)
    alice_message = pad(bytes("Hi Bob!", encoding='utf8'), AES.block_size)
    bob_message = pad(bytes("Hi Alice!", encoding='utf8'), AES.block_size)
    print("\n")
    print(unpad(alice_message, AES.block_size))
    print(unpad(bob_message, AES.block_size))

    cipher = AES.new(truncate_k, AES.MODE_CBC, iv)
    alice_ciphertext = cipher.encrypt(alice_message)
    print("\n")
    print("Alice's ciphertext: ", end="")
    print(alice_ciphertext)

    cipher = AES.new(truncate_k, AES.MODE_CBC, iv)
    bob_ciphertext = cipher.encrypt(bob_message)
    print("Bob's ciphertext: ", end="")
    print(bob_ciphertext)

    cipher = AES.new(truncate_k, AES.MODE_CBC, iv)
    bob_message = cipher.decrypt(bob_ciphertext)
    print("\n")
    print("Bob's message: ", end="")
    print(unpad(bob_message, AES.block_size))

    cipher = AES.new(truncate_k, AES.MODE_CBC, iv)
    alice_message = cipher.decrypt(alice_ciphertext)
    print("Alice's message: ", end="")
    print(unpad(alice_message, AES.block_size))

def task1():
    print("\nTask 1 - Part 1\n")
    task1_1()
    print("\nTask1 1 - Part 2\n")
    task1_2()
    
    
def task2_1():
    p = 17
    g = 11

    # alice
    x_alice = random.randint(1, p-2)
    y_alice = pow(g, x_alice, p)  # sent to mal

    # mal
    x_mal_bob = random.randint(1, p-2)
    y_mal_bob = pow(g, x_mal_bob, p)  # sent to bob

    # bob
    x_bob = random.randint(1, p-2)
    y_bob = pow(g, x_bob) % p
    k_bob = pow(y_mal_bob, x_bob, p)  # sent to mal

    # mal
    x_mal_alice = random.randint(1, p-2)
    k_mal_bob = pow(y_bob, x_mal_bob) % p
    y_mal_alice = pow(g, x_mal_alice) % p  # sent to alice
    k_mal_alice = pow(y_alice, x_mal_alice, p)

    # alice
    k_alice = pow(y_mal_alice, x_alice, p)
    k = SHA256.new()
    k.update(bytes(k_alice))
    key_alice = bytes(k.hexdigest()[0:16], encoding='utf8')
    iv = get_random_bytes(16)
    cipher_alice = AES.new(key_alice, AES.MODE_CBC, iv)
    message_alice = pad(bytes("Hi Bob!", encoding='utf8'), AES.block_size)
    ciphertext_alice = cipher_alice.encrypt(message_alice)  # sent to mal

    # mal
    k = SHA256.new()
    k.update(bytes(k_mal_alice))
    key_mal_alice = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_mal_alice = AES.new(key_mal_alice, AES.MODE_CBC, iv)
    mal_decrypt_alice = cipher_mal_alice.decrypt(ciphertext_alice)
    print("Mal decrypts Alice's message: ", end="")
    print(unpad(mal_decrypt_alice, AES.block_size))  # mal decrypts alice's 's message

    k = SHA256.new()
    k.update(bytes(k_mal_bob))
    key_mal_bob = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_mal_bob = AES.new(key_mal_bob, AES.MODE_CBC, iv)
    ciphertext_mal_bob = cipher_mal_bob.encrypt(pad(bytes("Hi Bob!", encoding="utf8"), AES.block_size))  # sent to bob

    # bob
    k = SHA256.new()
    k.update(bytes(k_bob))
    key_bob = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_bob = AES.new(key_bob, AES.MODE_CBC, iv)
    bob_decrypt_mal = cipher_bob.decrypt(ciphertext_mal_bob)
    print("Bob decrypts Mal's message: ", end="")
    print(unpad(bob_decrypt_mal, AES.block_size))  # bob decrypts alice's 's message

    k = SHA256.new()
    k.update(bytes(k_bob))
    key_bob = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_bob = AES.new(key_bob, AES.MODE_CBC, iv)
    message_bob = pad(bytes("Hi Alice!", encoding='utf8'), AES.block_size)
    ciphertext_bob = cipher_bob.encrypt(message_bob)  # sent to mal

    # mal
    k = SHA256.new()
    k.update(bytes(k_mal_bob))
    key_mal_bob_1 = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_mal_bob_1 = AES.new(key_mal_bob_1, AES.MODE_CBC, iv)
    mal_decrypt_bob = cipher_mal_bob_1.decrypt(ciphertext_bob)
    print("Mal decrypts Bob's message: ", end="")
    print(unpad(mal_decrypt_bob, AES.block_size))  # Mal decrypts Bob's 's message

    k = SHA256.new()
    k.update(bytes(k_mal_alice))
    key_mal_bob_1 = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_mal_alice_1 = AES.new(key_mal_bob_1, AES.MODE_CBC, iv)
    ciphertext_mal_alice_1 = cipher_mal_alice_1.encrypt(
        pad(bytes("Hi Alice!", encoding="utf8"), AES.block_size))  # sent to alice

    # alice
    k = SHA256.new()
    k.update(bytes(k_alice))
    key_alice_1 = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_alice_1 = AES.new(key_alice_1, AES.MODE_CBC, iv)
    alice_decrypt_mal = cipher_alice_1.decrypt(ciphertext_mal_alice_1)
    print("Alice decrypts Mal's message: ", end="")
    print(unpad(alice_decrypt_mal, AES.block_size))  # Mal decrypts Bob's 's message
    print("Done with tampering A and B\n\n")
    
def task2_2():
    p = 37
    g = 1

    # alice
    x_alice = random.randint(1, p-2)
    y_alice = pow(g, x_alice, p)  # sent to mal

    # bob
    x_bob = random.randint(1, p-2)
    y_bob = pow(g, x_bob, p)
    k_bob = pow(y_alice, x_bob, p)  # sent to mal

    # alice
    k_alice = pow(y_bob, x_alice, p)
    k = SHA256.new()
    k.update(bytes(k_alice))
    key_alice = bytes(k.hexdigest()[0:16], encoding='utf8')
    iv = get_random_bytes(16)
    cipher_alice = AES.new(key_alice, AES.MODE_CBC, iv)
    message_alice = pad(bytes("Hi Bob!", encoding='utf8'), AES.block_size)
    ciphertext_alice = cipher_alice.encrypt(message_alice)  # sent to mal
    print("Alice sends ciphertext: ", end="")
    print(ciphertext_alice)

    # mal
    k = SHA256.new()
    k.update(bytes(1))
    key_mal = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_mal = AES.new(key_mal, AES.MODE_CBC, iv)
    mal_decrypt_alice = cipher_mal.decrypt(ciphertext_alice)
    print("Mal decrypts Alice's message: ", end="")
    print(unpad(mal_decrypt_alice, AES.block_size))  # mal decrypts alice's 's message

    # bob
    k = SHA256.new()
    k.update(bytes(k_bob))
    key_bob = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_bob = AES.new(key_bob, AES.MODE_CBC, iv)
    message_bob = pad(bytes("Hi Alice!", encoding='utf8'), AES.block_size)
    ciphertext_bob = cipher_bob.encrypt(message_bob)  # sent to mal
    print("Bob sends ciphertext: ", end="")
    print(cipher_bob)

    # mal
    k = SHA256.new()
    k.update(bytes(1))
    key_mal = bytes(k.hexdigest()[0:16], encoding='utf8')
    cipher_mal = AES.new(key_mal, AES.MODE_CBC, iv)
    mal_decrypt_bob = cipher_mal.decrypt(ciphertext_bob)
    print("Mal decrypts Bob's message: ", end="")
    print(unpad(mal_decrypt_bob, AES.block_size))  # mal decrypts alice's 's message
    print("\nDone with setting p = 1")

    
def task2():
    print("\nTask 2 - Part 1\n")
    task2_1()
    print("\nTask 2 - Part 2\n")
    task2_2()
    

def task3_1():
    
    p = getPrime(2048)
    q = getPrime(2048)

    n = p * q
    fn = (p-1) * (q-1)

    e = 65537
    d = pow(e, -1, fn)

    public_key = (e, n)
    private_key = (d, n)
    print("public key: ", public_key)
    print("private key: ", private_key)

    message = random.randrange(100, 1000)
    print("\nmessage is: ", message, "\n")

    ciphertext = pow(message, e, n) 
    print("Encripted cipher: ", ciphertext)

    plaintext = pow(ciphertext, d, n) 
    print("\nplaintext: ", plaintext, end="\n\n")

    
def modInverse(A, M):
    for X in range(1, M):
        if (((A % M) * (X % M)) % M == 1):
            return X
    return -1


def task3_2():
    p = 17
    q = 11
    
    n = p * q
    
    m = 160
    e = 7
    d = 23

    print("PU : ", (e, n))
    print("PR : ", (d, n))

    # bob
    plaintext = 88
    c_bob = pow(plaintext, e, n)  # sent
    print("Bob sent c ", c_bob)

    # mal
    random = 3
    c_mal = c_bob * pow(random, e, n)  # sent
    print("Mal sent c' ", c_mal)

    # ali
    s_ali = pow(c_mal, d, n)  # sent
    print("Alice sent back ", s_ali)

    # mal (decrypts)
    res = (s_ali * modInverse(random, n)) % n
    print("Mal decrypt original message as ", res)
    
def task3():
    print("\nTask 3 - Part 1\n")
    task3_1()
    print("\nTask 3 - Part 2\n")
    task3_2()
    
        
if __name__ == "__main__":
    print("\n----- TASK 1 ----\n")
    task1()
    print("\n----Task2----\n")
    task2()
    print("\n----Task3----\n")
    task3()