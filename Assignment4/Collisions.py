import hashlib
import time
import random
import matplotlib.pyplot as plt

def hash_string(input_string, truncate=256):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    hex_dig = sha256.hexdigest()
    truncated_hex_dig = hex_dig[:truncate//4]
    return truncated_hex_dig

def hamming_distance(str1, str2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(str1, str2))

def find_collision_weak(input_string, truncate=256):
    input_hash = hash_string(input_string, truncate)
    for i in range(len(input_string)):
        for j in range(256):
            new_string = input_string[:i] + chr(j) + input_string[i+1:]
            new_hash = hash_string(new_string, truncate)
            if input_hash == new_hash and input_string != new_string:
                return (input_string, new_string)
    return None

def find_collision_birthday(inputs, truncate):
    input_hashes = [hashlib.sha1(input_string.encode()).hexdigest()[:truncate] for input_string in inputs]
    for i in range(len(input_hashes)):
        for j in range(i+1, len(input_hashes)):
            if input_hashes[i] == input_hashes[j]:
                return (inputs[i], inputs[j])
    return None


def generate_random_inputs(num_inputs, length):
    inputs = []
    for i in range(num_inputs):
        random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length))
        inputs.append(random_string)
    return inputs

def measure_collision_time(truncate=256, method='weak'):
    input_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(12))
    start_time = time.time()
    if method == 'weak':
        find_collision_weak(input_string, truncate)
    else:
        inputs = generate_random_inputs(2**(truncate//2), 1)
        find_collision_birthday(inputs, truncate)
    return time.time() - start_time

def main():
    x_weak = []
    y_bday = []
    for truncate in range(8, 41, 2):
        weak_time = measure_collision_time(truncate, 'weak')
        birthday_time = measure_collision_time(truncate, 'birthday')
        print("Truncate: {} bits, Weak Time: {:.6f}s, Birthday Time: {:.6f}s".format(truncate, weak_time, birthday_time))
        x_weak.append(1)
        y_bday.append(birthday_time)


    plt.plot(x_weak, y_bday)
    plt.xlabel('Digest')
    plt.ylabel('Birthday Time')
    plt.title('Digest vs. Birthday Time')

    plt.show()
    plt.close()
    exit(0)

if __name__ == '__main__':
    main()