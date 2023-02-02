
# Calpoly - CSC 321 - Dr. Bret Hartman
# Taylor Morgan - INDIVIDUAL

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16
KEY = get_random_bytes(BLOCK_SIZE)
IV = get_random_bytes(BLOCK_SIZE)

# Encyptes a BMP file with Cipher Block Chaining
def cbc( image ): 
    
    cbc = open("cbc.bmp", "wb")

    aes = AES.new(KEY, AES.MODE_ECB)
   
    with open(image, "rb") as image_file: 
        prev = IV
        header = image_file.read(54)
        cbc.write(header)
        body = image_file.read(BLOCK_SIZE)
        
        while body: 
            
            if len(body) < BLOCK_SIZE: 
                body = body + b"\x00"*(BLOCK_SIZE - len(body)%BLOCK_SIZE)
            
            xoring = bytes([a ^ b for a, b in zip(body, prev)])
            new_data = aes.encrypt(xoring)
            prev = new_data 
            cbc.write(new_data)
            body = image_file.read(BLOCK_SIZE)
    
    cbc.close() 

# Encypts a BMP image with Electronic Code-Book
def ecb( image ):     
    ecb = open("ecb.bmp", "wb")
    
    aes = AES.new(KEY, AES.MODE_ECB)
    
    with open(image, "rb") as image_file:
        header = image_file.read(54)
        ecb.write(header) 
        body = image_file.read(BLOCK_SIZE) 
        
        while body: 
            
            if len(body) < BLOCK_SIZE: 
                body = body + b"\x00"*(BLOCK_SIZE-len(body)%BLOCK_SIZE)
            
            new_data = aes.encrypt(body)
            ecb.write(new_data)
            body = image_file.read(BLOCK_SIZE)
    
    ecb.close()

def task1():
    print("Electronic Code-Book Mode:\n")
    ecb( "cp-logo.bmp" ) 
    print("Done! Electronic Codebook Mode\n")
    print("Cipher Block Chaining Mode:\n")
    cbc( "cp-logo.bmp" )
    print("Done! Cipher Block Chaining Mode\n")


#Task 2 Encryptions
CBC_cipher = AES.new(KEY, AES.MODE_CBC, IV)
CBC_cipher1 = AES.new(KEY, AES.MODE_CBC, IV)


# Recieves plain text and encyptes
def submit(msg:str) -> bytes:
  msg = 'userid=456;userdata=' + msg + ';session-id=31337'
  msg = pad(msg.encode('ASCII'), BLOCK_SIZE)
  return bytearray(CBC_cipher.encrypt(msg))

# Verifies that the resulting bits have the "admin=true"
def verify(cipher:bytes) -> bool:
  cipher = CBC_cipher1.decrypt(cipher)
  cipher = str(cipher)
  print("cipher", cipher)
  return ';admin=true;' in cipher

# Flips the bits and then adds the bits for the 'admin=true'
def bitFlipping(cipher:bytes) -> bytes:
  c1_no = cipher[:4]
  c1 = cipher[4]
  c1 =  (c1 ^ ord("@".encode("ASCII;")) ^ ord(";".encode("ASCII"))).to_bytes(1,"big")

  c2_no = cipher[5:10]
  c2 = cipher[10]
  c2 = (c2 ^ ord("$".encode("ASCII")) ^ ord("=".encode("ASCII"))).to_bytes(1,"big")
    
  c3_no = cipher[11:15]
  c3 = cipher[15]
  c3 =(c3 ^ ord("@".encode("ASCII")) ^ ord(";".encode("ASCII"))).to_bytes(1,"big")
  
  c4 = cipher[16:]
    
  c1_no += c1
  c1_no += c2_no
  c1_no += c2
  c1_no += c3_no
  c1_no += c3
  c1_no += c4

  return c1_no
    

def task2():
    print("Results for just verifying Plain Text 'Taylor Morgan':")
    print(verify(submit('Taylor Morgan')),"\n")
    
    print("Results for verifying ';admin=true;' :")
    print(verify(bitFlipping(submit('@admin$true@'))),"\n")
    
    print("Results for bit flipping and verifying Plain Text 'Taylor Morgan':")
    print(verify(bitFlipping(submit('@admin$true@'))),"\n")
    

def main():
    task1()
    task2()
    
if __name__ == "__main__":
    main()


