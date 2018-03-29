"""
This program asks you to enter a phone number in a ###-####-#### format.
It takes the largest number and replaces it with an "X" and the second largest
number with a "Y". If the phone number does not comply with the format or contains
characters other than numbers, the program returns a message saying it is invalid.
"""

LEN = 12
POS_HYPHEN_1 = 3
POS_HYPHEN_2 = 7

def check_length(phone_number):
    """
    This function should determine if the length of the phone_number is correct
    """
    if len(phone_number) == LEN:
        return True
    else:
        return False

def check_hyphens(phone_number):
    """
    This function should determine if the hyphens are at the correct positions
    """
    if phone_number[POS_HYPHEN_1] == chr(45) and phone_number[POS_HYPHEN_2] == chr(45):
        return True
    else:
        return False   

def check_digits(phone_number):
    """
    This function should determine if all the characters other than the 
    hyphens are digits 
    """
    try:
        if int(phone_number[0:3]) and int(phone_number[4:7]) and int(phone_number[8:]):
            return True
    except:
        return False


def modify(phone_number):
    """
    Given a valid phone_number, this function should replace the
    largest digits with 'X' and the second largest digits with 'Y'
    """
    X = phone_number[0]
    Y = phone_number[0]   
    for digit in phone_number:
        if digit > X:
            temp = X
            X = digit
            Y = temp
        elif digit > Y and digit < X:
            Y = digit
    for digit in phone_number:
        interim_phone_number = phone_number.replace(X,'X')
        modified_phone_number = interim_phone_number.replace(Y,'Y')

    return modified_phone_number


def validate(phone_number):
    """
    This function should check if phone_number input by the user is valid
    Return True if its valid otherwise return False
    """

    # Test the length of the phone number
    if check_length(phone_number) != True:
        return False

    # Test if the hyphens are placed correctly
    if check_hyphens(phone_number) != True:
        return False

    # Test if the digits are placed correctly
    if check_digits(phone_number) != True:
        return False

    return True


def main():

    while True:
        phone_number = input('Enter a phone number: ')
        # If the User enters an empty string: Exit
        if phone_number == '':
            return
        # Test if the number is valid
        if not validate(phone_number):
            print ('The phone number is not valid')
        else:
            # If the number is valid, replace the largest digit with X
            # and the second largest with Y
            print (modify(phone_number))

if __name__ == '__main__':
    main()
