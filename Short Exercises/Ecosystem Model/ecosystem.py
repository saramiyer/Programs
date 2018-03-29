import turtle
import random


class World:
    def __init__(self, mx, my):
        self.maxX = mx
        self.maxY = my
        self.thingList = []
        self.grid = [[None for x in range(mx)] for y in range(my)]
        self.offsetList = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]
        self.wturtle = turtle.Turtle()
        self.wscreen = turtle.Screen()
        self.wscreen.setworldcoordinates(0,0,mx-1,my-1)
        self.wscreen.addshape("Bear.gif")
        self.wscreen.addshape("BearM.gif")
        self.wscreen.addshape("BearF.gif")
        self.wscreen.addshape("Fish.gif")
        self.wscreen.addshape("Plant.gif")
        self.wturtle.hideturtle()

    def draw_line(self, x, y, heading, length):
        self.wturtle.up()
        self.wturtle.goto(x, y)
        self.wturtle.down()
        self.wturtle.setheading(heading)
        self.wturtle.forward(length)

    def draw(self):
        self.wscreen.tracer(0)
        for i in range(self.maxX):
            self.draw_line(i, 0, 90, self.maxY-1)
        for i in range(self.maxY):
            self.draw_line(0, i, 0, self.maxX-1)
        self.wscreen.tracer(1)

    def freezeWorld(self):
        self.wscreen.exitonclick()

    def addThing(self, athing, x, y):
        athing.setX(x)
        athing.setY(y)
        self.grid[y][x] = athing
        athing.setWorld(self)
        self.thingList.append(athing)
        athing.appear()

    def delThing(self,athing):
        athing.hide()
        self.grid[athing.getY()][athing.getX()] = None
        self.thingList.remove(athing)

    def moveThing(self,oldx,oldy,newx,newy):
        self.grid[newy][newx] = self.grid[oldy][oldx]
        self.grid[oldy][oldx] = None

    def withinGrid(self,x,y):
        return 0 <= x < self.maxX and 0 <= y < self.maxY

    def liveALittle(self):
        random.shuffle(self.thingList)
        for athing in self.thingList:
           athing.liveALittle()

    def emptyLocation(self,x,y):
        return self.grid[y][x] == None

    def lookAtLocation(self,x,y):
       return self.grid[y][x]

    def findEmptyLocation(self):
        x = random.randrange(self.maxX)
        y = random.randrange(self.maxY)
        while not self.emptyLocation(x,y):
            x = random.randrange(self.maxX)
            y = random.randrange(self.maxY)
        return (x,y)

    def randAdjLocation(self,xpos,ypos):
        nextx = nexty = -1
        while not self.withinGrid(nextx,nexty):
            randomOffsetIndex = random.randrange(len(self.offsetList))
            randomOffset = self.offsetList[randomOffsetIndex]
            nextx = xpos + randomOffset[0]
            nexty = ypos + randomOffset[1]
        return (nextx,nexty)


############################################################
class Organism:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.hideturtle()
        self.world = None
        self.xpos = 0
        self.ypos = 0
        self.starveTick = 0
        self.breedTick = 0

    def setX(self,newx):
        self.xpos = newx

    def setY(self,newy):
        self.ypos = newy

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def setWorld(self,aworld):
        self.world = aworld

    def appear(self):
        self.turtle.goto(self.xpos, self.ypos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def tryToBreed(self):
        (nextx,nexty) = self.world.randAdjLocation(self.xpos,self.ypos)

        if self.world.emptyLocation(nextx,nexty):
            theClass = self.__class__
            childThing = theClass()
            self.world.addThing(childThing,nextx,nexty)
            self.breedTick = 0

    def listOfAdjacent(self, aClass):
        adjprey = []
        for offset in self.world.offsetList:
            newx = self.xpos + offset[0]
            newy = self.ypos + offset[1]
            if self.world.withinGrid(newx,newy):
                if not self.world.emptyLocation(newx,newy):
                    thing = self.world.lookAtLocation(newx,newy)
                    if isinstance(thing, aClass):
                        adjprey.append(thing)
        return adjprey


############################################################
class Animal(Organism):

    def move(self,newx,newy):
        self.world.moveThing(self.xpos,self.ypos,newx,newy)
        self.xpos = newx
        self.ypos = newy
        self.turtle.goto(self.xpos, self.ypos)

    def tryToMove(self):
        (nextx,nexty) = self.world.randAdjLocation(self.xpos,self.ypos)
        if self.world.emptyLocation(nextx,nexty):
           self.move(nextx,nexty)

    def tryToEat(self, preyClass):
        adjprey = self.listOfAdjacent(preyClass)
        if len(adjprey) > 0:
            randomprey = adjprey[random.randrange(len(adjprey))]
            preyx = randomprey.getX()
            preyy = randomprey.getY()

            self.world.delThing(randomprey)
            self.move(preyx,preyy)
            self.starveTick = 0

    def liveALittle(self):
        self.starveTick = self.starveTick + 1
        if self.starveTick == self.starveTime:
            self.world.delThing(self)
        else:
            self.tryToMove()


############################################################
class Fish(Animal):
    def __init__(self):
        Organism.__init__(self)
        self.turtle.shape("Fish.gif")
        self.breedTime = 10
        self.starveTime = 25

    def liveALittle(self):
        adjfish = self.listOfAdjacent(Fish)
        if len(adjfish) >= 2:
            self.world.delThing(self)
        else:
            self.tryToEat(Plant)
            super().liveALittle()
            self.breedTick = self.breedTick + 1
            if self.breedTick >= self.breedTime:
                self.tryToBreed()


############################################################
class Plant(Organism):
    def __init__(self):
        super().__init__()
        self.turtle.shape("Plant.gif")
        self.breedTime = 5

    def liveALittle(self):
        self.breedTick = self.breedTick + 1
        if self.breedTick >= self.breedTime:
            self.tryToBreed()
