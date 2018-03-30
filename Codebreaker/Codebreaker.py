def main():
    # Prompts user to input an encrypted file 
    try:
        fileUpload = input("Enter the input filename: ")
        # Input returned is used to open the file and returns a list of encrypted data
        fileName = open(fileUpload,"r")
        codes = getFileData(fileName)
        solveCode(codes)
    # The program restarts if the inputed file is not correct
    except: main()   
    

def getFileData(fileName):
    # Retrieves the data from files and adds it to the codes list.
    codes = [] #[word, key]
    
    for line in fileName:
        splitLine = line.split(' ')
        codes.append([splitLine[0].strip()]+[splitLine[-1].strip()])
        # Removes extra blank spaces that may be created in the list.
        while ['',''] in codes:
            codes.remove(['',''])
    
    return(codes)

def solveCode(codes):
    # Formats the codes into 2 separate lists
    for code in codes:
        cipher = code[0]
        key = code[1]
        
        # Filters the keys for numbers
        try:
            if int(key) <= 26 and float(key) >=1:
                # If the number is detected, the words are decrypted
                getNewWord(cipher,key)
            else:
                # If the key does not return an interger, the program is directed to "except" clause
                pass
        except:
            # The key is invalid and the statement is printed
            print("Missing key!")
    return()

def getNewWord(cipher,key):
    # Breaks down the encrypted words into letters for conversion
    newWord = ''
    for word in cipher:
        for letter in word:
            # Converts the letter into a number value and adds the key value
            number = str(ord(letter)+int(key))
            # If the number returns a value larger than 90, it needs to be looped back to 65 which equals "A"
            if int(number) > 90:
                number = str(int(number) - 26)
            else: # Value of number returned is within 65-90 value range (A-Z), value does not need to be looped.
                pass
            # Converts value of number to letter
            newLetter = chr(int(number))
        newWord += (newLetter)
    print(newWord)
    return(newWord)

main()
