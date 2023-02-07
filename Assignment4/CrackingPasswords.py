import asyncio
import bcrypt
from nltk.corpus import words
import multiprocessing
import time

salt = None
hash = None
user = None

#Generates the Dictionary that will be used and then is sorted by length: smaller words come first
def readWords():
    listOfWords = []
    for w in words.words():
        if (len(w) > 5) and (len(w) < 11):
            listOfWords.append(w)
    return listOfWords.sort(key=len)

# needs to be async so that main knows to wait for this method to finish
async def task(word_list):
    
    #breaks up the dictionary into chunks that evenly goes into each of the allocated cores
    process_list = []
    chunk_len = int(len(word_list)/multiprocessing.cpu_count())
    chunk1 = 0
    chunk2 = chunk_len - 1

    #Allocates cores to each process
    for core in range(multiprocessing.cpu_count()): # ran with 8 cores 
        if (core == multiprocessing.cpu_count()):
            p = multiprocessing.Process(
                target=hack, args=(user, salt, hash, word_list[chunk1:]))
            process_list.append(p)
        else:
            p = multiprocessing.Process(target=hack, args=(
                user, salt, hash, word_list[chunk1: chunk2]))
            process_list.append(p)
            chunk1 += chunk_len
            chunk2 += chunk_len

        p.start() #starts the process

    #kills all processes when one finishes
    while process_list:
        for p in process_list:
            if not p.is_alive():
                process_list.remove(p)
                for q in process_list:
                    q.terminate()
                break

    #sets the flag that the task is done
    return "Task completed for words: {}".format(words)


def hack(user, salt, hash, words):
    start = time.time()
    for word in words:
        pwhash = bcrypt.hashpw(word.encode(), salt.encode())
        if pwhash == (salt+hash).encode():
            total_time = time.time() - start
            print("Time took to find the word: '",word,"' was", total_time)
            with open("passwords.txt", "a") as f:
                f.write(user + " '" + word + "' \tTime: " + str(total_time) + "\n")
            return word #flag that the process is completed

#waits for the method to finish 
async def main():
    with open("shadow.txt", "r") as file:
        for line in file:
            i = 0
            while line[i] != '$':
                i += 1
            
            global salt
            global hash
            global user
            
            user = line[:i]
            salt = line[i:i+29]
            hash = line[i+29:-1]

            print("\nUSER: " + user[:-1] +
                  "\nSALT: " + salt + "\nHASH: " + hash)

            words = readWords()
            await task(words)


if __name__ == '__main__':
    asyncio.run(main())
