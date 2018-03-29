# Sara Iyer - 1226751 - CMPUT 175 Assignment 1

def main ():
   
   # Input the lines
   lines = int(input())
   keyword = []
   message = []
   output = []
   
   for i in range(lines):
      # Get the keyword and message
      Cipher = input().upper()
      
      # Replace 'X' with 'KS' because it is easiest to do now
      xRemoved = removeX(Cipher)
      
      # Split the input into the keyword and message
      splitCipher = xRemoved.split()
      
      # Check if the input contains only one keyword and message
      # Otherwise, trigger an error.
      if not len(splitCipher) == 2:
         output.append("ERROR")
      
      # Check if only letters are contained in the input otherwise trigger error
      elif checkInputIsLetters(splitCipher):
         output.append("ERROR")

      # If the input is valid, then we split the keyword & message
      else:
         keyword.append(splitCipher[0])
         message.append(splitCipher[1])
         
         # Create the primary matrix key using the keyword
         primaryMatrix = createPrimaryMatrix(keyword)
         
         # Create the secondary matrix with strings ordered by the columns
         # in the primary matrix
         secondaryMatrix = createSecondaryMatrix(primaryMatrix)
         
         # Split the message up and insert 'Q' & 'Z' letters where needed
         newMessage = prepMessageToEncrypt(message)
         
         # Encrypt the split message using key matrices
         # Encrypted message is added to the output list
         outputString = encryption(primaryMatrix,secondaryMatrix,newMessage)
         output.append(outputString)        
                  
         # Clear the lists for the next line of input
         keyword = []
         message = []
   
   # Print all the outputs
   for encryptedMessage in output:
      print(encryptedMessage)

def removeX(word):
   
   # Looks through an input line and replaces the letter 'X' with 'KS'
   for character in word:
      if character is 'X':
         word = word.replace(character,'KS')
   
   # Sends back the line with any necessary replacements
   return word

def checkInputIsLetters(word):
   
   # If the input contains only letters in the alphabet then the function
   # returns True, otherwise, it returns false and triggers an error.
   for character in word:
      if not character.isalpha():
         return True
   return False 

def createPrimaryMatrix(aKeyword):
   alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWYZ'
   keyString = ''
   
   # Create a key with only one letter from the keyword
   for string in aKeyword:
      for char in string:
         if char not in keyString:
            keyString += char
   
   # Add the rest of the letters from alphabet to key
   for letter in alphabet:
      if letter not in string:
         keyString += letter
   
   # Generate the matrix key
   matrixKey = [keyString[i:i+5] for i in range(0, len(keyString), 5)]
   return matrixKey

def createSecondaryMatrix(aList):
   secondaryMatrix = []
   counter = 0
   
   # Create a cycle of 5 to circle through the aList 5 times.
   for counter in range(0,5):
      string = ''
      
      # For every cycle, take all the characters in the same string position,
      # string them together and add to the new matrix.
      for row in aList:
         for cell in row:
            if row.index(cell) == counter:
               string += cell
      secondaryMatrix.append(string)
      
      # The count increases by 1 to repeat the cycle again and string together
      # the next set of characters in the next position of each string.
      counter += 1
   
   return secondaryMatrix

def prepMessageToEncrypt(messageList):
   splitMessage = []
   for word in messageList:
      
      # Countdown the length of the word to 0 as we shorten it,
      # By taking two letters at a time
      while len(word) != 0:
         letterPair = word[:2]
         
         # If there is only one letter, then 'Z' is added
         # This statement MUST go first or else letterpairs are out of range
         # When it comes an odd word length
         if len(letterPair) == 1:
            letterPair += 'Z'
            splitMessage.append(letterPair)
            word = ''
         
         # If both letters are the same we insert a 'Q' and split them up
         elif letterPair[0] == letterPair[1]:
            letterPair = letterPair[0] + 'Q'
            splitMessage.append(letterPair)
            word = word[1:]
         
         # We have two different letters so, we append to the list.
         else:
            splitMessage.append(letterPair)
            word = word[2:]
   
   return splitMessage

def encryption(rowMatrix,columnMatrix,lineMessage):
   finalMessage = ''

   # Take each string of 2 letters and check if the letters
   # are in the same row, column or form a box.
   for letterSet in lineMessage:
      
      # If the letters are in the same row, switch letters in row and add to
      # final message
      if letterSet in rowPairCheck(lineMessage,rowMatrix):
         finalMessage += (rowFlip(letterSet,rowMatrix))
      
      # If the letters are in the same column, switch letters in column and
      # add to the final message
      elif letterSet in colPairCheck(lineMessage,columnMatrix):
         finalMessage += (colFlip(letterSet,rowMatrix))
      
      # If the letters are in opposite columns and rows, then switch letters
      # into a different column and add to the final message
      else:
         finalMessage += (boxFlip(letterSet,rowMatrix))
   
   # Send the message fully assembled and encrypted back
   return finalMessage

def rowPairCheck(theMessage,rowMatrix):
   rowPairs = []
   
   # Break down the message list into pairs of letters and for each pair,
   for letterSet in theMessage:
      rowList = []
      
      # Break down the pair into each letter and add to the list of letters
      for character in letterSet:
         rowList.append(character)
      
      # Break down the matrix into rows
      for row in rowMatrix:
        
         # See if both letters are in the same row
         if rowList[0] in row and rowList[1] in row:
            
            # If so, add the letter pair to the row pairs list.
            rowPairs.append(letterSet)
   
   return rowPairs

def rowFlip(letterSet,rowMatrix):
   letters = ''
   
   # Break down the pair of letters into each letter.
   for oneLetter in letterSet:
      
      # Map out the coordinates of the primary matrix key      
      for row in range(5):
         for col in range(5):
            
            # Find the location of that letter
            if rowMatrix[row][col] == oneLetter:
               
               # Move the column coordinate to the right by one and bring
               # to front if at the end
               col = (col + 1) % 5
               
               # Take the new coordinates, find the encrypted letter
               # Concatenate the two letters together
               letters += (rowMatrix[row][col])
   
   return letters

def colPairCheck(aMessage,columnMatrix):          
   colPairs = []
   
   # Break down the message list into pairs of letters and for each pair,
   for letterSet in aMessage:
      colList = []
      
      # Break down the pair into each letter and add to the list of letters
      for letter in letterSet:
         colList.append(letter)
      
      # Break down the matrix into columns
      for column in columnMatrix:
         
         # See if both letters are in the same column
         if colList[0] in column and colList[1] in column:
            
            # If so, add the letter pair to the column pairs list.
            colPairs.append(letterSet)
   
   return colPairs

def colFlip(letterSet,columnMatrix):
   letters = ''
   
   # Again, break down the pair of letters into each letter
   for oneLetter in letterSet:
      
      # Map out the coordinates of the secondary matrix key      
      for row in range(5):
         for col in range(5):
            
            # Find the location of that letter 
            if columnMatrix[row][col] == oneLetter:
               
               # Move the column coordinate to the right by one and bring
               # to front if at the end               
               row = (row + 1) % 5
               
               # Take the new coordinates, find the encrypted letter
               # Concatenate the two letters together               
               letters += (columnMatrix[row][col])
   
   return letters

def boxFlip(letterSet,rowMatrix):
   coordinates = []
   letters = ''
   
   # Again, break down the pair of letters into each letter
   for oneLetter in letterSet:
      
      # Map out the coordinates of the primary matrix key       
      for row in range(5):
         for col in range(5):
            
            # Find the coordinates of that letter and add them to the list
            if rowMatrix[row][col] == oneLetter:
               coordinates.append([row,col])
   
   # Execute a letter switch by switching the column coordinates of both letters
   # Take the new coordinates, find the encrypted letters, and put together
   letters += rowMatrix[coordinates[0][0]][coordinates[1][1]]
   letters += rowMatrix[coordinates[1][0]][coordinates[0][1]]

   return letters
  
main()