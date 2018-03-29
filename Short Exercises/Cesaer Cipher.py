"""
Program asks a user to enter E or D to encrypt or decrypt a message followed by a
colon, a numerical value as the key followed by a colon, and then the message
Example  E:175:Meet in the park
The message is then encoded or decoded based on the Cesaer cipher.
"""

def read_input():
    """
    Read input should prompt the user for a message and read and input.

    The function should then return three (3) variables:

        1. A string/character for mode
        2. A string with the key
        3. A string with the message
    """
    cipher = input().upper()
    splitCipher = cipher.split(':')
    mode = splitCipher[0]
    key = splitCipher[1]
    message = splitCipher[2:]

    return mode, key, message


def caesarEncrypt(word, shift):
    """
    Function should take a word and a shift and return the encrypted message
    produced using the Caesar Cipher with the word and shift.

    Parameter:  word - a string of alphabet characters
    Parameter:  shift - the shift distance
    Return:     the encrypted string
    """    
    newWord = ''
    for i in word:
        
        number = str(ord(i)+int(shift))
        if int(number)>90:
            number = str(int(number)- 26)
        else:
            pass
        newLetter = chr(int(number))
        newWord += (newLetter)
    return newWord


def caesarDecrypt(word, shift):
    """
    Function should take a word and a shift and return the decrypted message
    produced using the Caesar Cipher with the word and shift.

    Parameter:  word - a string of alphabet characters
    Parameter:  shift - the shift distance
    Return:     the decrypted string
    """
    newWord = ''
    for i in word:
        number = str(ord(i)-int(shift))
        if int(number)<65:
            number = str(int(number)+ 26)
        else:
            pass
        newLetter = chr(int(number))
        newWord += (newLetter)
    return newWord


def encrypt(message, key):
    """
    This function will take a whole message and a key and encrypt the message
    using the key.

    Parameter: message - a string, the whole message to be encrypted
    Parameter: key - a string, the encryption key
    Return:    the encrypted message
    """
    keys = []
    keyList = []
    variable = ''

    for i in message:
        words = i.split()

    keyIndex = 0
    for i in range(len(words)):
        if i == len(key):
            keyIndex = 0
            keys.append(key[keyIndex])
        else:
            keys.append(key[keyIndex])
            keyIndex +=1
    
    for i in range(len(words)):
        variable += caesarEncrypt(words[i],keys[i])
        variable += ' '

    return variable


def decrypt(message, key):
    """
    This function will take a whole message and a key and decrypt the message
    using the key.

    Parameter: message - a string, the whole message to be decrypted
    Parameter: key - a string, the encryption key
    Return:    the decrypted message
    """
    keys = []
    keyList = []
    variable = ''

    for i in message:
        words = i.split()

    keyIndex = 0
    for i in range(len(words)):
        if i == len(key):
            keyIndex = 0
            keys.append(key[keyIndex])
        else:
            keys.append(key[keyIndex])
            keyIndex +=1
    
    for i in range(len(words)):
        variable += caesarDecrypt(words[i],keys[i]) 
        variable += ' '

    return variable


if __name__ == "__main__":

    mode, key, message = read_input()

    if mode == "E" or mode == "e":

        print(encrypt(message, key))

    elif mode == 'D' or mode == 'd':

        print(decrypt(message, key))

    else:

        print("Invalid mode entered.")
