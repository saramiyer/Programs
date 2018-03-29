import turtle

"""
Assignment 5 - CMPUT 175

Student ID: 1226751 

Creator: Sara Iyer

Read all comments and instructions very carefully.

Do NOT import any other modules (except the copy module if you need it.)

Remember, it is absolutely vital you are perfectly clear on what the data
structures are - you can always use the type() function to check.

"""
class Maze():
    def __init__(self, maze_spec):
        
        
        self.board = []
        self.dim = []
        self.start = []
        
        # List out any necessary additional variables
        wall_coords = []
        
        # Separate the string spec into dimensions, walls, start and goal
        specs = maze_spec.split('|')
        
        """ GET DIMENSIONS """
        # Take the section of the dimensions
        dimensions = specs[0]
        
        # Split the dimensions into the height and width
        dimensions = dimensions.split(',')
        
        # And append them to self.dim as integers.
        for item in dimensions:
            self.dim.append((int(item)))
        
        """ GET WALLS """
        # Take the section of the walls
        walls = specs[1:-2]
        
        # For each interval
        for wall in walls:
            
            # Split the beginning interval and the ending interval
            wall = wall.split(':')
            
            # Create a list to hold the beginning and ending coordinates
            wall_span = []
            
            # Split the coordinates into values and turn them into integers
            for coordinate in wall:
                coordinate = coordinate.split(',')
                wall_span.append((int(coordinate[0]),int(coordinate[1])))
                
                # Once we formatted the beginning and ending coordinates
                if len(wall_span) == 2:
                    
                    # Check if they are the same
                    # If they are then we will only add one x to the maze.
                    # So we append only one of the coordinates set
                    if wall_span[0] == wall_span[1]:
                        wall_coords.append(wall_span[0])
                    
                    # Check if the height is the same. If they are,
                    # that means width of coordinates are different.
                    # So we are adding x's to a section of coords in a row
                    elif wall_span[0][0] == wall_span[1][0]:
                        
                        # If the integer in the 1st coord has a larger value,
                        # the coords are listed from larger to smaller.
                        if wall_span[0][1] > wall_span[1][1]:
                            
                            # We flip the values so we can get an ascending
                            # list of coordinates within our interval. 
                            # We add them to our list of walls
                            for i in range(wall_span[1][1],wall_span[0][1]+1):
                                wall_coords.append((wall_span[0][0],i))
                        
                        # If the integer in the 1st coord has a smaller value
                        # hat means the coords are in the right order.
                        # Get the row coords from interval & add to walls list 
                        else:
                            for i in range(wall_span[0][1],wall_span[1][1]+1):
                                wall_coords.append((wall_span[0][0],i))
                    
                    # Check if the coords width are the same. If yes,
                    # that means the height of the coords are different.
                    # We are adding x's to a section of coords in a column
                    elif wall_span[0][1] == wall_span[1][1]:
                        
                        # If the integer in the 1st coord has a larger value,
                        # the coords are listed from larger to smaller.                        
                        if wall_span[0][0] > wall_span[1][0]:
                            
                            # We flip the values so we can get an ascending
                            # list of coordinates within our interval 
                            # that we add to our walls list                            
                            for i in range(wall_span[1][0],wall_span[0][0]+1):
                                wall_coords.append((i,wall_span[0][1]))
                        
                        # If the integer in the 1st coord has a smaller
                        # value that means the coords are in the right order.
                        # Get the col coords from interval & add to walls list                      
                        else:
                            for i in range(wall_span[0][0],wall_span[1][0]+1):
                                wall_coords.append((i,wall_span[0][1]))
                            
        """ GET START """
        # Take the section of the start
        start = specs[-2]
        
        # Split start into coordinates
        start = start.split(',')
        
        # And append the coordinates to self.start
        for coordinate in start:
            self.start.append(int(coordinate))
        
        """ MAKE THE BOARD """
        # For each line in the maze's height, we add a width-sized empty list
        for height in range(self.dim[0]):
            self.board.append([' ' for width in range(self.dim[1])])
        
        # Generate the maze's matrix to get access to modify all the squares
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                
                # When a square matches the start coords, add the start symbol
                if self.start[0] == row and self.start[1] == col:
                    self.board[row][col] = '@'
                
                # When a square matches the goal coords, add the goal symbol
                # Assumption: Do not create a goal variable
                # So I tried to add the information directly to the board
                elif int(specs[-1].split(',')[0]) == row and int(specs[-1].split(',')[1]) == col:
                    self.board[row][col] = 'O'
                    
                # When a square matches a wall's coords, add the wall symbol
                for a_wall in wall_coords:
                    if a_wall[0] == row and a_wall[1] == col:
                        self.board[row][col] = 'x'

    def print_maze(self):
        """
        In this function you must print out the maze board.
        """
        # For each line in the maze
        for line in self.board:
            
            # Add the maze's borders to the ends of the line and print.
            print('| '+' '.join(line)+' |')
        
        
class MazeSolver:
    def __init__(self, maze):
        """
        Takes a Maze object to create a solver. The init function initializes
        variables to hold these objects. self.start is created to make it
        easier to refer to. self.path is initially None to allow for checking
        during the recursive call. DO NOT CHANGE THESE VALUES.
        """

        self.maze = maze
        self.start = self.maze.start
        self.path = None


    def get_moves(self, pos, path):
        """
        This functions takes the current position and the explored path to
        produce a list of available moves/positions to move to.

        param: pos: a list of the current position
        param: path: a list of positions explored thus far

        return: moves: a list of new positions to explore

        DO NOT CHANGE!
        """

        moves = []

        # Check for North move

        if pos[0] - 1 >= 0:
            np = self.new_pos(pos, 'N')
            if self.maze.board[np[0]][np[1]] != 'x' and not np in path:
                moves.append(np)

        # Check for South move

        if pos[0] + 1 < self.maze.dim[0]:
            np = self.new_pos(pos, 'S')
            if self.maze.board[np[0]][np[1]] != 'x' and not np in path:
                moves.append(np)

        # Check for West move

        if pos[1] - 1 >= 0:
            np = self.new_pos(pos, 'W')
            if self.maze.board[np[0]][np[1]] != 'x' and not np in path:
                moves.append(np)

        # Check for East move

        if pos[1] + 1 < self.maze.dim[1]:
            np = self.new_pos(pos, 'E')
            if self.maze.board[np[0]][np[1]] != 'x' and not np in path:
                moves.append(np)

        return moves


    def new_pos(self, pos, move):
        """
        Utility function for get_moves()

        DO NOT CHANGE!
        """

        if move == "N":
            np =  [pos[0] - 1, pos[1]]
        elif move == "S":
            np = [pos[0] + 1, pos[1]]
        elif move == "E":
            np = [pos[0], pos[1] + 1]
        else:
            np = [pos[0], pos[1] - 1]

        return np


    def solve(self, pos, path):
        """
        This is the recursive function you will implement. The function takes
        the current position and explored path. At each call, if the current
        position is not the goal, you must retrieve the list of new moves
        available and call solve() again with each new move. If the goal is
        reached, store the path in self.path. Remember, the idea is to find the
        shortest path.
        """
        
        # Check if the position we are at corresponds to the goal
        if self.maze.board[pos[0]][pos[1]] == 'O':
            
            # If it does, check if there is already is a solution
            # If not, then store the solution as the self.path variable
            if self.path == None:
                self.path = path
                return
            
            # If there is a solution then check if it is shorter 
            # (aka more optimal) than the current path found.
            # If not, then store the new path as the self.path variable
            if len(path) < len(self.path):
                self.path = path
                return
        
        # Get the list of possible moves from our current position
        moves = self.get_moves(pos,path)
            
        # For each move in the list of possible moves
        # If there are no moves in the list then the function terminates
        # So there is no need to write code for that possibility.
        for a_move in moves:
                
            # Make a copy of the path so the one from the previous recursion
            # level is not altered and keep track of our progress throughout
            # the maze from the current move by adding it to our tentative path            
            path_copy = path[:] + [a_move]
                
            # Set the move as our new current position in the maze
            pos = a_move
   
            # Once we have moved to our new position we can call the function
            # To check for new and different possibilities
            self.solve(pos,path_copy)       


    def trace(self):
        """
        In this function you must add the solution path to the maze board. You
        can represent each unit in the path with '.'
        """
        # Generate the maze's matrix to get access to modify all the squares
        for row in range(self.maze.dim[0]):
            for col in range(self.maze.dim[1]):
                
                # Get the list of coordinates that match the path
                # Exclude start and goal points because they remain the same
                for coord in self.path[1:-1]:
                    
                    # When the coordinates match the position on the board
                    if coord[0] == row and coord[1] == col:
                        
                        # Replace that position with a dot to mark the path.
                        self.maze.board[row][col] = '.'   


class MazeGraphics:
    def __init__(self, board, path):
        """
        The maze illustrator. Takes a Maze board and the solution path. You
        can play around with the turtle settings here if you'd like.
        """

        turtle.speed('fastest')
        turtle.screensize(2000, 2000)
        self.draw_board(board)

        # Call your function to draw the path here
        # Insert the start position which is the first item in the path list.
        # Turtle looks at our coordinates as x,y and we have them as a y,x
        # So we flip the coordinates.
        self.move_to(path[0][1],path[0][0])
        self.trace(path)

        turtle.exitonclick()


    def draw_board(self, board):
        """
        Draws the entire board and returns turtle to the origin
        """

        rows = 0
        for i in range(len(board)):
            self.draw_row(board[i])


    def draw_row(self, row):
        """
        Draws the a row of the maze board and returns turtle to the start
        position of the row.

        param: row, list of strings, a row of the maze board
        """

        cols = 0
        for j in range(len(row)):
            self.draw_box(50)
            if row[j] == 'x':
                self.draw_wall('grey')
            elif row[j] == '@':
                self.draw_wall('red')
            elif row[j] == 'O':
                self.draw_wall('green')
            turtle.forward(50)
            cols += 1

        turtle.right(180)
        turtle.forward(cols * 50)
        turtle.left(90)
        turtle.forward(50)
        turtle.left(90)


    def draw_box(self, width):
        """
        Draws a unit of the maze. Each unit is a square that should be 50x50.

        param: width: int, the dimension of the unit
        """

        for i in range(4):
            turtle.forward(width)
            turtle.right(90)


    def draw_wall(self, color):
        """
        Draws a wall in a unit. A wall is a box that is 40x40 centered in a
        unit. You can represent walls as gray boxes, start with red and goal
        with green. You should call draw_box() here to do so.

        param: color: string, the color of the units wall/start/goal
        """

        turtle.penup()
        turtle.forward(5)
        turtle.right(90)
        turtle.forward(5)
        turtle.left(90)

        turtle.pendown()
        turtle.color("black", color)
        turtle.begin_fill()
        self.draw_box(40)
        turtle.end_fill()

        turtle.penup()
        turtle.left(180)
        turtle.forward(5)
        turtle.right(90)
        turtle.forward(5)
        turtle.right(90)
        turtle.pendown()


    def move_to(self, x, y):
        """
        Move the turtle to the position x,y WITHOUT drawing any lines.

        param: x: int, the x-position of the destination
        param: y: int, the y-position of the destination
        """
        # Adapt values from the start coordinates to the board drawn in turtle
        # I multiply by 50 because each position has a width of 50
        # To position the mouse in the middle of a square, add 25 to the coords
        x = (x*50) +25
        y = (y*50) +25
        
        # Lift the pen to avoid drawing
        turtle.penup()
        
        # Move the cursor to the calculated location
        # Set the coordinate values of y as a negative
        # because we're in the lower right part of turtle's coordinates map
        turtle.setx(x)
        turtle.sety(-y)

    def trace(self, path):
        """
        This function should take the solution path and draw the path on the
        illustrated maze.

        You must complete this function.

        param: path: a list of coordinates, the solution path of a maze
        """
        # To draw the path, put the pen down & set the colour and line thickness
        turtle.pendown()
        turtle.color('blue')
        turtle.pensize(5)
        
        # Take each set of coordinates in the solution path and compare to the
        # next set to move acccordingly.
        # The loop stops at the second last set because the final comparison
        # gets us to the maze's goal.
        for position in range(len(path)-1):
            
            # Reset the heading for the next move
            turtle.setheading(0)
            
            # If the current y coord is smaller than the next y coord then
            # according to how view the window, we are moving down.
            if path[position][0] < path[int(position)+1][0]:
                
                # So we turn the cursor 90 degrees right so the cursor is 
                # facing down and move it down by one square
                turtle.right(90)
                turtle.forward(50)
            
            # If the current y coord is larger than the next y coord then
            # according to how we view the window, we are moving up.
            elif path[position][0] > path[int(position)+1][0]:
                
                # We turn the cursor 90 degrees left so the cursor is 
                # facing up and then move it the length of one square
                turtle.left(90)
                turtle.forward(50)
            
            # If the current x coord is smaller than the next x coord then
            # according to how we view the window, we are moving right.
            elif path[position][1] < path[int(position)+1][1]:
                
                # Since our cursor faces that direction by default, 
                # we simply move it "forward" the length of one square
                turtle.forward(50)
            
            # Last option left is that the cursor moves left along the window
            else:
                
                # Our cursor already faces the opposite direction by default,
                # so we simply move back the cursor the length of one square.
                turtle.backward(50)
        
        # Reset the default heading as indicated in the picture.
        turtle.setheading(0)
        

spec = '5,5|0,1:0,2|2,1:3,1|2,3:2,4|3,0:3,0|3,3:3,3|0,4:0,4|0,0|3,4'

"""
The following code should work perfectly if your code is correctly implemented.
You can use it as a guide to see what data structures are being transferred
around.
"""

ms = MazeSolver(Maze(spec))

# I added a command to print out the initial maze as stated in the assignment directions
ms.maze.print_maze()
ms.solve(ms.start, [ms.start])
ms.trace()
ms.maze.print_maze()

mg = MazeGraphics(ms.maze.board, ms.path)