from math import floor
import bcrypt
from nltk.corpus import words
import time
import multiprocessing
import threading

salt = None
hash = None

def readWords():
    listOfWords = []
    for w in words.words():
        # Only test hash word if its within char limit for password
        if (len(w) > 5) and (len(w) < 11):
            listOfWords.append(w)
    return listOfWords


def chunckSize(wordCount):
    return int(wordCount/multiprocessing.cpu_count())


def task(dict):
    arr = []
    global salt
    global hash
    
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        arr = pool.map(crack_pw, [(word, salt, hash) for word in dict])
        pool.close()
        pool.join()
        #call here
    return arr

# #make it so that when the word is found, kills all other child processes
def crack_pw(args):
    word, salt, hash = args
    pwhash = bcrypt.hashpw(word.encode(), salt.encode())
    if pwhash == (salt+hash).encode():
        print(word)
        
        # return word

# def crack_pw(args, pool):
#     word, salt, hash = args
#     pwhash = bcrypt.hashpw(word.encode(), salt.encode())
#     if pwhash == (salt+hash).encode():
#         print(word)
#         pool.terminate()
#         return word

# def task(dict, salt, hash):
#     arr = []
#     with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
#         arr = pool.map(lambda x: crack_pw(x, pool), [(word, salt, hash) for word in dict])
#         pool.terminate()
#         pool.join()
#     return arr

def main():

    with open("shadow.txt", "r") as file:
        for line in file: 
            i = 0
            while line[i] != '$':
                i += 1

            global salt
            global hash
            user = line[:i]
            salt = line[i:i+29]
            hash = line[i+29:-1]

            
            print("\nUSER: " + user[:-1] +
                  "\nSALT: " + salt + "\nHASH: " + hash)

        words = readWords()
        words.sort(key=len)
        task(words)
        
        # start = time.time()
        # end = time.time()
    


if __name__ == '__main__':
    main()
