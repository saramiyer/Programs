import math, urllib.request

def main():
   
   # Retrieve the raw data from the webpages
   (customerData,callData) = getData()
   
   # Take raw customer data and format it into a list of data
   customers = (formatCustomerData(customerData))
   
   # Take raw call data and format it into a list of data
   calls = (formatCallsData(callData))
   
   # Count number of calls originating from original customer numbers list
   callCount = getCallCount(customers,calls)
   
   # Calculate the total talk time for each phone number
   callDuration = getDuration(customers,calls)
   
   # Calculate the amount due for each customer
   (customerDue,totalDues) = getDue(customers,calls)
     
   # Takes the customer list & reformats the phone numbers with brackets
   # Adds call count, call duration and customer due to the list
   # An updated, organized and sorted report data list is created
   reportOutput = compileReportValues(customers,callCount,callDuration,customerDue)
   
   # Compile and print final report
   tabulateReport(reportOutput,totalDues)

 
def getData():
   
   # Format the hyperlinks as a string variable
   customerURL = 'https://webdocs.cs.ualberta.ca/~kondrak/cmput175/customer_table.html'
   callURL = 'https://webdocs.cs.ualberta.ca/~kondrak/cmput175/call_table.html'
   
   # Open both webpages
   customerPage = urllib.request.urlopen(customerURL)
   callPage = urllib.request.urlopen(callURL)
   
   # Read the content of the webpages
   customerContent = customerPage.read()
   callContent = callPage.read()
   
   return (customerContent,callContent)

def formatCustomerData(rawCustData):

   customersData = []
   keyCustomerInfo = []
   
   # Isolate the table data in the downloaded webpage information
   customerTableSplit = rawCustData.split(b'table>')
   
   # Convert the data from bytes to string and create variable for string
   customerTableSplit[1] =  customerTableSplit[1].decode('ISO-8859-1')
   rawCustTable = customerTableSplit[1]
   
   # Remove the excess webpage coding
   custTableReplace1 = rawCustTable.replace('<tr><td>','')
   custTableReplace2 = custTableReplace1.replace('</td></tr>','')
   custTableReplace3 = custTableReplace2.replace('</','')
   custTableReplace4 = custTableReplace3.replace('td><td>',',')
   
   # Remove the line indent formatting and add to list of customer data
   # The first and last string are empty so we exclude them.
   customersData = custTableReplace4.split('\r\n')[1:-1]
   
   # Remove the city information of customers since we will not use it.
   for lines in customersData:
      keyCustomerInfo.append(lines.split(',')[:2])
   
   # Feed out only the crucial customer information needed for analysis 
   return keyCustomerInfo

def formatCallsData(rawCallData):
   
   callsData = []
   formattedCallsData = []
   
   # Isolate the table data in the downloaded webpage information
   callTableSplit = rawCallData.split(b'table>')
   
   # Convert the data from bytes to string and create variable for string
   callTableSplit[1] =  callTableSplit[1].decode('ISO-8859-1')
   rawCallTable = callTableSplit[1]
   
   # Remove the excess webpage coding
   callTableReplace1 = rawCallTable.replace('<tr><td>','')
   callTableReplace2 = callTableReplace1.replace('</td></tr>','')
   callTableReplace3 = callTableReplace2.replace('</','')
   callTableReplace4 = callTableReplace3.replace('td><td>',',')
   
   # Remove the line indent formatting and add to list of calls data
   # The first and last strings are empty so we exclude them.   
   callsData = callTableReplace4.split('\r\n')[1:-1]
   
   # Format the data so the numerical values are integers and floats as needed
   for lines in callsData:
      lineSplit = lines.split(',')
      formattedCallsData.append(lineSplit[:3]+[int(lineSplit[3])]+[float(lineSplit[4])])
   
   # Feed out the properly formatted calls data list needed for analysis
   return formattedCallsData

def getCallCount(customerList, callList):
   
   # Create a dictionary to keep track of customers and count.
   numberCount = {}
   
   # Take phone numbers in customer list and append to dictionary key
   for customerLine in customerList:
      numberCount[customerLine[0]] = 0
   
   # Loop to search for caller phone numbers in call list 
   for line in callList:
      
      # Every time a number in the list is found, increase count by 1
      if line[1] in numberCount.keys(): 
         numberCount[line[1]] += 1

   # Return dictionary of call counts
   return numberCount

def getDuration(customerList,callList):
   
   # Create a dictionary to keep track of customers and call length
   callTime = {}
   
   # Take phone numbers in customer list and append to dictionary key
   for customerLine in customerList:
      callTime[customerLine[0]] = 0
   
   # Loop to search for caller phone numbers in call list 
   for line in callList:
         
      # Sum up time for each phone number
      if line[1] in callTime.keys(): 
         callTime[line[1]] += line[3]
   
   # Format time, time provided in seconds
   for time in callTime.values():
      hrs = time/3600 # Because there are 3600 seconds in an hour
      wholeHrs = time//3600 # To get integer value of hours
      
      # Find the remainder of the hour and multiply by 60 to get the minutes
      mins = (hrs-wholeHrs)*60 # Because there is 60 minutes in an hour
      
      # Find the remainder of the mins, multiply by 60 and round up to get secs
      secs = round((mins-int(mins))*60) # Because there is 60 secs in a minute 
      
      # Compile the duration in a string as per formatting requirements
      duration = '%02d'%(wholeHrs) + 'h' + '%02d'%(mins) + 'm' + '%02d'%(secs) + 's'
      
      # Replace time in seconds with the formatted duration string
      for number in callTime.keys():
         if callTime.get(number) == time:
            callTime[number] = duration
   
   # Return dicitonary of call duration
   return callTime

def getDue(customerList,callList):
   
   # Create a dictionary to keep track of customers and amount due
   amountDue = {}
   allDues = 0
   
   # Take phone numbers in customer list and append to dictionary key
   for customerLine in customerList:
      amountDue[customerLine[0]] = 0
   
   # Loop to search for caller phone numbers in call list 
   for line in callList:
         
      # If the caller's number corresponds to number in customer list,
      # calculate charge for the call and add to value in dictionary by:
      if line[1] in amountDue.keys():
         
         # Rounding time for call to largest minute integer
         minute = math.ceil(line[3]/60)

         # Getting rate for that call
         rate = line[4]
         
         # Adding cost of the call to customer's total amount due
         amountDue[line[1]] += (minute*rate)
         
         # Suming up the total dues for the customers
         allDues += (minute*rate)
   
   # Round each customer's due amounts to two decimal points
   for customer in amountDue.keys():
      amount = amountDue.get(customer)
      amountDue[customer] = '%.2f'%(amount)
   
   # Round the amount of the total dues to two decimal points
   allDues = round(allDues,2)
   
   return (amountDue, allDues)

def compileReportValues(customerList,countDict,timeDict,dueDict):
   
   output = []
   
   # Goes through each customer in the list
   for customer in customerList:  
      
      # Temporarily holds the original number in memory
      temp = customer[0]
      
      # Concatenates the brackets and spaces with the original digits
      newNumber = '(' + temp[:3] + ') ' + temp[3:6] + ' ' + temp[6:]
      
      # Retrieves the call count for each customer
      if temp in countDict.keys():
         count = countDict.get(temp)
      
      # Retrieves the duration for each customer
      if temp in timeDict.keys():
         time = timeDict.get(temp)
      
      # Retrieves the amount due for each customer
      if temp in dueDict.keys():
         due = dueDict.get(temp)
      
      # Creates a new list with information needed for table report
      # comprised of reformatted phone number, customer name, 
      # number of calls, total duration of calls and amount due by customer.
      output.append([newNumber,customer[1],count,time,due])
   
   # Sort the output by phone number as it is to appear in the table report
   output.sort()
   
   return output

def tabulateReport(outputList,dues):
   
   # Format the report titles
   print("+" + "-"*14 + "+" + "-"*30 + "+" + "-"*3 + "+" + "-"*9 + "+" + "-"*8 + "+")
   print("|" + "%-14s"%(" Phone number") + "|" + "%-30s"%(" Name") + "|" + "%-3s"%(" #") + "|" + "%-9s"%("Duration") + "|" + "%-8s"%(" Due") + "|" )
   print("+" + "-"*14 + "+" + "-"*30 + "+" + "-"*3 + "+" + "-"*9 + "+" + "-"*8 + "+")
   
   # Add symbols to customer line in report for any customer meeting manager's criteria
   for customerInfo in outputList:
      symbol = ""
      if float(customerInfo[4]) > 850:
         symbol = "**"
      elif int(customerInfo[2]) > 350:
         symbol = "++"
      
      # Fill out report with customers' information
      print("|" + "%-14s"%(customerInfo[0]) + "|" + "%-30s"%(customerInfo[1]) + "|" + "%-3s"%(customerInfo[2]) + "|" + "%-9s"%(customerInfo[3]) + "|" + "$" + "%+7s"%(customerInfo[4]) + "|" + symbol)
   
   # Add summary of report
   print("+" + "-"*14 + "+" + "-"*30 + "+" + "-"*3 + "+" + "-"*9 + "+" + "-"*8 + "+")
   print("|" + "%-14s"%(" Total dues") + "|" + "%+43s"%("$") + "%+10s"%(dues) + "|")
   print("+" + "-"*14 + "+" + "-"*(53) + "+")

main()
