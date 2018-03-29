# Sara Iyer - 1226751 - Assignment 4 - Cmput 175

import sys
import re

def readCommandLineArgs():
   
   # Retrieving the file name of the encrypted ciphertext file.
   file = sys.argv[1]
   
   # Set the default number of most common bi-grams we want to map
   bigram_number = 3
   
   # Check if the user manually input a number of most common bi-grams
   if len(sys.argv) > 2:
      
      # If yes, set that value as the number of most common bi-grams to map
      bigram_number = sys.argv[2]
   
   # Feed out the created variables from the function
   return file, int(bigram_number)

def prep_plaintext():
   
   # Create the variables
   letters = 'ABCDEFGHIJKLMNOPQRSTUVXYZ'
   plaintext = ''
   blank = ' '   
   
   # Open the file
   file_name = "wells.txt"
   plain_file = open(file_name, "r")
   
   # For each line of that file
   for line in plain_file:
      
      # Remove the leading and trailing whitespace
      line = line.strip()
      
      # Add space at the end of line so last & first words don't stick together
      line = line+blank
      
      # Check if each character is an alphabetic character or a space
      # If so, then add it to the plaintext string
      for ch in line:
         if ch.isalpha():
            plaintext += ch.upper()
         elif ch == blank:
            plaintext += ch
   
   # Close the file since we don't need it anymore
   plain_file.close()
   
   # Feed out the text that contains words and spaces only
   return plaintext

def get_word_frequencies(plaintext):
   
   # Create variable
   word_freq_dict = {}
   
   # Split the text up into words
   plaintext = plaintext.split()
   
   # For each word in the split text
   for word in plaintext:
      
      # If it is already in the dictionary, then I increase the count
      if word in word_freq_dict.keys():
         word_freq_dict[word] += 1
      
      # Otherwise, it's new so I add it to the dictionary with a count of 1
      else:
         word_freq_dict[word] = 1
   
   # Feed out the count of plaintext words   
   return word_freq_dict

def get_plaintext_bigrams(plaintext):
   
   # Create variables
   plaintext_dictionary = {}
   plaintext_bigrams = []
   
   # Split the words using the spaces
   for word in plaintext.split():
      
      # Create a variable to parse through words
      parser = 0
      
      # Create a constraint to parse through words longer than 1 character
      if len(word) > 1:
         
         # (Create a constraint to parse through a word to the second last letter
         # To avoid creating a string of only 1 character)
         # Go through a word
         while parser + 1 < len(word):
            
            # Split word into 2 characters and add them to the list of bigrams
            plaintext_bigrams.append(word[parser:parser+2])
            
            # Move the parser over by one to get the next 2 characters
            parser += 1
   
   # To calculate the frequency, I need to get the total count of all occurences
   # So I retrieve the total count of bigrams
   total = len(plaintext_bigrams)
   
   # For each bigram in the bigram list
   for ch in plaintext_bigrams:
      
      # If it is already in the dictionary of bigrams, then I increase the count
      if ch in plaintext_dictionary.keys():
         plaintext_dictionary[ch] += 1
      
      # Otherwise, it's new so I add it to the dictionary with a count of 1
      else:
         plaintext_dictionary[ch] = 1
   
   # Clear the old bigram list
   plaintext_bigrams = []
   
   # For every item in the dictionary
   for ch in plaintext_dictionary:
      
      # Calculate the frequency and format the result
      plaintext_dictionary[ch] = "%.5f"%(plaintext_dictionary[ch] / total)
      
      # Add the frequency value and the bigram to the list
      plaintext_bigrams.append([plaintext_dictionary[ch],ch])
      
      # Sort the list so the highest frequency value is first
      plaintext_bigrams.sort(reverse = True)
   
   # Feed out the bigram frequency list
   return plaintext_bigrams

def prep_ciphertext(file_name):
   
   # Create variable
   cipher_list = []
   
   # Open the file
   file = open(file_name, "r")
   
   # For each line in that file
   for line in file:
      
      # Remove the leading and trailing whitespaces
      line = line.strip()
      
      # Parse through the line and take two 2 characters a time and
      # Add to the cipher bigram list
      cipher_list = [line[i:i+2] for i in range(0, len(line),2)]
   
   # To calculate the frequency, I need to get the total count of all occurences
   # So I retrieve the total count of bigrams from ciphertext
   total = len(cipher_list)
   
   # Close the file since we don't need it anymore.
   file.close()
   
   # Feed out the total amount of bigrams and the bigram list
   return total, cipher_list

def get_cipher_bigrams(total, cipher_list):
   
   # Create variable
   cipher_dictionary = {}
   
   # For each bigram in the list of cipher bigrams
   for ch in cipher_list:
      
      # If it is already in the dictionary, then I increase the count
      if ch in cipher_dictionary.keys():
         cipher_dictionary[ch] += 1
      
      # Otherwise, it's new so I add it to the dictionary with a count of 1
      else:
         cipher_dictionary[ch] = 1
   
   # Clear the old cipher bigram list
   cipher_list = []
   
   # For every item in the dictionary
   for ch in cipher_dictionary:
      
      # Calculate the frequency and format the result
      cipher_dictionary[ch] = "%.5f"%(cipher_dictionary[ch] / total)
      
      # Add the frequency value and the bigram to the list
      cipher_list.append([cipher_dictionary[ch],ch])
      
      # Sort the list so the highest frequency value is first
      cipher_list.sort(reverse = True)
   
   # Feed out the cipher bigram frequencies
   return cipher_list

def map_bigrams(plaintext_list, cipher_list, N):
   
   # Create variable
   map_dictionary = {}
   
   # Create a count to cycle through the value of N times
   # N corresponds to the top N amount of cipher and plaintext bigrams 
   # We want to associate together
   
   for count in range (0, int(N)):
      
      # For each count, add the bigram from the cipher list that
      # corresponds to the index position of the count as the dictionary key
      # AKA: when count 1 = index pos 1 = first item in the cipher bigram list
      #
      # Add the bigram from the plain list that corresponds to the index
      # position of the count as the dictionary value
      # AKA: when count 1 = index pos 1 = first item in plain bigram list
      #
      # GOAL= Associate nth bigram in cipher list to nth bigram in plain list
      map_dictionary[cipher_list[count][1]] = plaintext_list[count][1]
   
   # Feed out the dictionary of mapped bigrams
   return map_dictionary

def create_word_bank():
   
   # Create list to input the words
   word_bank = []
   
   # Open the file
   file = open("wordlist.txt","r")
   
   # For each word in a line
   for line in file:
      
      # Remove any leading or trailing whitespaces
      line = line.strip()
      
      # Add to the list of words
      word_bank.append(line)
   
   # Close the file since we are now finished using it
   file.close()
   
   # Feed out the list of words
   return word_bank

def replace_with_mapped_bigrams(mapped_dict, message):
   
   # Create variables
   new_message = ''
   chars = '' 
   blank = ' '
   
   # Create a variable to parse through the message
   parser = 0 
   
   # Go through the message
   while parser + 1 < len(message):
      
      # Two characters at a time
      bigram = message[parser:parser+2]
      
      # If the characters correspond to a mapped cipher bigram
      if bigram in mapped_dict.keys():
         
         # Retrieve the plaintext bigram
         chars = mapped_dict.get(bigram)
         
         # Replace with lowercase letters
         chars = chars.lower()
         
         # Add to the partially decode message string
         new_message += chars        
      
      else:
         
         # Add any still encrypted bigrams back to the string
         new_message += bigram
         
      # Increase the count by 2 to go through the next set of letters
      parser += 2
   
   # Feed out the message that's been potentially partially decoded.
   return new_message

def get_letter(t):
   
   # retrieves the item in 1st pos in the tuple & list is sorted alphabetically
   return t[0]

def get_freq(t):
   
   # retrieves the item in the 2nd pos in the tuple & list is sorted numerically
   return t[1]

def format_solutions(solution_list, word_freq):
   
   # Create variables
   format_dict = {}
   output_string = ''
   blank = ' '
   
   # Change the words to uppercase so they are compatible with word freq dict
   for word in solution_list:
      word = word.upper()

      # Search for word in dictionary
      if word in word_freq.keys():
         
         # If found, add word as key and its count as value in the dictionary
         format_dict[word] = word_freq.get(word)
      else:
         
         # If not found, add word as key and count of zero in the dictionary
         format_dict[word] = 0     
         
   # Convert the dictionary into a list so it can be sorted
   item_list = list(format_dict.items())
   
   # Sort list alphabetically
   item_list.sort(key=get_letter)
   
   # Next, sort list numerically by frequency value
   # By doing an initial alphabetical sort, words with same frequency value
   # stay sorted alphabetically and words with higher frequencies come to the
   # front of the list.
   item_list.sort(key=get_freq, reverse=True)
   
   # Go through the list
   for item in item_list:
      
      # Concatenate the list into one string with a space to separate each word
      output_string += item[0]+blank
   
   # Convert the string into lowercase which is supposed to be its final format
   output_string = output_string.lower()
   
   # Feed out the formatted output string
   return output_string

def re_search(message, word_bank, word_freq):
   
   # Create any necessary variables
   possible_solutions = []
   re_string = ''
   modified_string = ''
   dot = '.'
   
   # Check if the mystery word is fully decoded. 
   # If so, exit out of function with word unchanged.
   if message.islower() == True:
      return message
   
   # If not, check for other possible words it could be
   else:
      
      # Replace capital letters with dots
      for character in message:
         if character.isupper():
            re_string += '.'
         
         # If letter is already in lowercase, add to string as-is
         else:
            re_string += character
      
      # Modify new string so begin and middle remain fixed
      new_string = '(^%s$)'%re_string
      
      # Go through the word list and see if any words match the string
      for word in word_bank:
         answer = re.match(new_string, word)
         
         # If a word matches the string, add it to the list of solutions 
         if answer != None:
            possible_solutions.append(answer.group())
      
      # If the first string that was converted into a regular expression
      # ended with a dot, then there may be more solutions with one less dot
      if re_string[-1] == dot:
         
         # So modify the string to have one less dot
         re_string = re_string[:-1]
         
         # Format it again to fix the begin and ending of the string
         modified_string = '(^%s$)'%re_string
         
         # And search again through the word bank for possible matches   
         for word in word_bank:
            answer = re.match(modified_string, word)
            
            # If a match is found, add it as well to our solutions list
            if answer != None:
               possible_solutions.append(answer.group())         
      
      # Sort possible solutions by frequency, then alphabetically and format
      # as a string to adhere with how the final output is being printed
      possible_solutions = format_solutions(possible_solutions, word_freq)
      
      # Feed out the string of possible solutions
      return possible_solutions

def main():
   
   # Read and Process the command line arguments
   (ciphertext_file, N_bigrams) = readCommandLineArgs()
   
   # Modify the plaintext file to only have letters and spaces
   modified_plaintext= prep_plaintext()
   
   # Use modified plaintext to get the word frequencies
   word_frequencies = get_word_frequencies(modified_plaintext)
   
   # Use modified plaintext file to get the frequency of plaintext bigrams
   plain_freq_bigrams  = get_plaintext_bigrams(modified_plaintext)
   
   # Use ciphertext file to get a list of cipher bigrams and total length of list
   (cipher_length, init_cipher_list) = prep_ciphertext(ciphertext_file)
   
   # Use list of cipher bigrams and total length value to
   # get the frequency of the cipher bigrams
   cipher_freq_bigrams = get_cipher_bigrams(cipher_length, init_cipher_list)
   
   # Take N-bigrams value and the frequency lists for plain and cipher text bigrams
   # To associate the number of N_bigrams together and get a dictionary of
   # associated(mapped) bigrams
   n_mapped_bigrams = map_bigrams(plain_freq_bigrams, cipher_freq_bigrams, N_bigrams)
   
   # Create the word bank list to search for word possibilities
   word_bank = create_word_bank()   
   
   # Prompt the user to input the encrypted message
   mystery_word = input('Input: ')
   
   # If the user inputs characters
   while mystery_word != '':
      
      # In case the user does not input the mystery word with capital letters
      mystery_word = mystery_word.upper()
      
      # Check if any bigrams in mystery word match our mapped bigrams
      partial_word = replace_with_mapped_bigrams(n_mapped_bigrams, mystery_word)
      
      # Check if word has been fully decoded & if so, return it immediately
      # If not, find all word possibilities, format the order & type
      # and return a decoded string
      decoded_possibilities = re_search(partial_word, word_bank, word_frequencies)
      
      # Print out all decoded possibilities
      print("Output: %s"%decoded_possibilities)
      
      # Prompt for a new word again
      mystery_word = input('Input: ')
   
   # If the user inputs nothing then the program exits
   sys.exit()
   
if __name__ == "__main__":
   main()
