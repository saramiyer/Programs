"""
Program simulates a browser's history. Type a website to update the current site. 
Type > or < to move forward or backward through the browser history.
"""

class Stack:
    
    def __init__(self):
        self.__items = []
        
    def push(self, item):
        self.__items.append(item)
        
    def pop(self):
        return self.__items.pop()
    
    def peek(self):
        return self.__items[len(self.__items)-1]
    
    def is_empty(self):
        return len(self.__items) == 0
    
    def size(self):
        return len(self.__items)
    
    def clear(self):
        del self.__items[:]

def main():
    
    # Create two stacks as the forward and backward buttons
    forward = Stack()
    back = Stack()
    
    # Create the starting home page
    forward.push("www.google.ca")
    currentSite = forward.peek()
    print("Starting at Home Page: "+currentSite)
    while True:
        userInput = input()
        
        # If someone tries to go back to the previous site
        if userInput == "<":
            try:
                # The previous site will become the current site
                if forward.size() > 1:
                    recentSite = forward.pop()
                    back.push(recentSite)
                    currentSite= forward.peek()
                    print("Current page: "+currentSite)                                     
                # If someone tries to go further back than the first site
                else:
                    print("< is an invalid action")
            except:
                pass              
        
        # If someone tries to go forward in the browser history
        elif userInput == ">":
            try:
                # The next site will become the current site
                if back.size() > 0:
                    putBack = back.pop()
                    forward.push(putBack)
                    currentSite= forward.peek()
                    print("Current page: "+currentSite)
                
                # If someone tries to go past the last entered site
                else:
                    print("> is an invalid action")
                    
            except:
                raise
        else:
            # If the history list has any content, it is deleted
            try: 
                if back.size() > 0:
                    back.clear() 
                forward.push(userInput)
                currentSite= forward.peek()
                print("Current page: " +currentSite)
            except:
                raise

main()
