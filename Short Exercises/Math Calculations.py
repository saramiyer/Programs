# Enter a set of numbers and this program gives you the mean, standard deviation and median.

import math

def read_input():
    """
    This function should read the data input by the user using a command
    prompt and return a sorted list of values.

    Handles both int and float data types.
    """
    
    # Get an input of values
    input_numbers = input("Enter a set of numbers: ")
    
    # Split the values into a list
    splitNumbers = input_numbers.split()
    
    # Convert the values into integers
    for values in range(len(splitNumbers)):
        splitNumbers[values] = float(splitNumbers[values])    
    return splitNumbers


def my_mean(splitNumbers):
    """
    Write a function that takes a list of numbers and calculates the mean of
    the list of numbers. For example, if the function is given [3, 5, 7, 8] it
    should return 5.75.

    Parameter: data - a list of integers/floats

    Return: the mean of data
    """
    
    # Assign variables
    meanSum = 0
    totalValues = len(splitNumbers)
    
    # Add up the values in list
    for numbers in splitNumbers:
        meanSum += numbers 
    
    # Divide by the total amount of values
    meanCalculation = meanSum / totalValues
    
    return meanCalculation


def my_stdev(splitNumbers,meanCalculation):
    """
    This function should take a list of numbers and calculate the standard
    deviation of the whole list.

    This is a function that takes a integer/float value as a parameter 
    and returns the square root of the parameter.

    Parameter: data - a list of integers/floats

    Return: the standard deviation of data
    """
    
    # Assign Variables
    totalValues = len(splitNumbers)
    stdevSum = 0 
    interim = 0
    addingInterim = 0
    sqValue = 0
    
    # Find the difference from mean of each value
    for numbers in splitNumbers:
        interim = numbers - meanCalculation
    
    # Power of 2 to difference
        interim *= interim
    
    # Sum up integers
        addingInterim += interim
    
    # Divide sum total values by total amount of values
    stdevDivision = addingInterim / (totalValues-1)
    
    # Square root of the Division
    stdevCal = math.sqrt(stdevDivision)

    return stdevCal


def my_median(splitNumbers):
    """
    This function should take a list of numbers and calculate the median value
    amongst the numbers.

    Parameter: data - a list of integers/floats

    Return: the median of data
    """
    
    # Sort the list of values
    splitNumbers.sort()
    
    # Find the middle value of the list
    centerValue = len(splitNumbers) // 2
    
    # If the list is an even amount of values, take the 
    # two middle values and find the value between both which is the median
    if len(splitNumbers) % 2 == 0:
        return sum(splitNumbers[centerValue - 1:centerValue + 1]) / 2
    
    # If the list has an odd amount of values, just take the middle value
    # of the list.
    else:
        return splitNumbers[centerValue]


if __name__ == "__main__":

    data = read_input()
    data2 = my_mean(data)
    print("Mean: ", my_mean(data))
    print("Standard Deviation: ", my_stdev(data,data2))
    print("Median: ", my_median(data))
