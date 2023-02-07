from Crypto.Hash import SHA256
import random
import time
import matplotlib.pyplot as plt


def hash_sha256(input_string, truncate_length=None):
    sha256 = SHA256.new()
    sha256.update(input_string.encode())
    hex_digest = sha256.hexdigest()
    
    if truncate_length is not None:
        hex_digest = hex_digest[:truncate_length]
    
    return hex_digest

input_string = input("Enter an input string: ")
truncate_length = int(input("Enter the truncated length (8 to 50 bits): "))
hex_digest = hash_sha256(input_string, truncate_length)
print("The truncated hexadecimal digest of the input is:", hex_digest)


def generate_strings(length):
    string1 = ''.join(str(random.randint(0, 1)) for i in range(length))
    string2 = list(string1)
    flip_index = random.randint(0, length - 1)
    string2[flip_index] = str(1 - int(string2[flip_index]))
    string2 = ''.join(string2)
    return string1, string2

def hamming_distance(string1, string2):
    distance = 0
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            distance += 1
    return distance

length = int(input("Enter the length of the strings: "))
for i in range(5):
    string1, string2 = generate_strings(length)
    print("Generated Strings:", string1, string2)
    distance = hamming_distance(string1, string2)
    print("Hamming Distance:", distance)
    print()


inputs = []
digest = []
times = []

def birthday_collision(truncate_bits):
    # Create a dictionary to store the hashes
    start = time.time()
    input = 0
    hashes = {}
    collision = False
    # Keep generating random strings until a collision is found
    while not collision:
        # Generate a random string
        input += 1
        input_string = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for i in range(12))
        hex_digest = hash_sha256(input_string)[:truncate_bits//4]
        # Check if the hash already exists in the dictionary
        if hex_digest in hashes:
            collision = True
            inputs.append(input)
            input == 0
            total_time = time.time()-start
            print(f"Collision found! Strings: {input_string} and {hashes[hex_digest]}")
            print("Time it took to find the Hexidecimal Digest '",hex_digest,"' was", total_time, "\n")
            times.append(total_time)
        else:
            hashes[hex_digest] = input_string
    return


for i in range(8, 51, 2):
    print("Truncated Bit: ",i)
    birthday_collision(i)
    digest.append(i)
    
plt.plot(digest, times)
plt.xlabel('Digest')
plt.ylabel('Birthday Time')
plt.title('Digest vs. Birthday Time')

plt.show()
plt.close()

plt.plot(digest, inputs)
plt.xlabel('Digest')
plt.ylabel('No. Inputs')
plt.title('Digest vs. No. Inputs')

plt.show()
plt.close()
exit(0)