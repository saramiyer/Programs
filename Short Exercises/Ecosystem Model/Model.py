from ecosystem import *

class Bear(Animal):
    def __init__(self):
        super().__init__()
        self.turtle.shape("Bear.gif")
        self.breedTime = 4
        self.starveTime = 12

    def liveALittle(self):
        self.tryToEat(Fish)
        super().liveALittle()

### Define MaleBear and FemaleBear here
class MaleBear(Bear):
    def __init__(self):
        super().__init__()
        self.turtle.shape("BearM.gif")

    def liveALittle(self):
        super().liveALittle()
        self.breedTick += 1
        if self.breedTick >= self.breedTime:
            self.tryToMate()

    def tryToMate(self):
        possible_mates = self.listOfAdjacent(FemaleBear)
        if len(possible_mates) > 0:
            mate = possible_mates[random.randrange(len(possible_mates))]
            mate.getPregnant()
            self.breedTick = 0

class FemaleBear(Bear):
    def __init__(self):
        super().__init__()
        self.turtle.shape("BearF.gif")
        self.pregnant = False

    def liveALittle(self):
        super().liveALittle()
        if self.pregnant:
            self.breedTick += 1
            if self.breedTick > self.breedTime:
                self.tryToBreed()

    def tryToBreed(self):
        (nextx, nexty) = self.world.randAdjLocation(self.xpos, self.ypos)

        if self.world.emptyLocation(nextx, nexty) and self.pregnant and \
                self.breedTick > self.breedTime:

            choice = random.randint(0, 1)
            if choice == 0:
                self.world.addThing(MaleBear(), nextx, nexty)
                print("Gave birth to a male")
            else:
                self.world.addThing(FemaleBear(), nextx, nexty)
                print("Gave birth to a female")
            self.breedTick = 0
            self.pregnant = False

    def getPregnant(self):
        if self.pregnant:
            print("Already pregnant")
        else:
            self.pregnant = True
            print("Successfuly impregnated")

def mainSimulation():
    numberOfBears = 15
    numberOfFish = 15
    numberOfPlants = 0
    worldLifeTime = 50
    worldWidth = 10
    worldHeight = 10

    random.seed(0)
    myworld = World(worldWidth,worldHeight)
    myworld.draw()

    for i in range(numberOfFish):
        newfish = Fish()
        (x,y) = myworld.findEmptyLocation()
        myworld.addThing(newfish,x,y)

    mCount, fCount = 0, 0
    for i in range(numberOfBears):
        # TODO change the following line so that either MaleBear or FemaleBear
        # is created with equal probability
        choice = random.randint(0,1)
        if choice == 0:
            newbear = MaleBear()
            mCount += 1 
        else:
            newbear = FemaleBear()
            fCount += 1
        (x,y) = myworld.findEmptyLocation()
        myworld.addThing(newbear,x,y)

    print("Males: {}\nFemales: {}\n".format(mCount, fCount))

    for i in range(numberOfPlants):
        newplant = Plant()
        (x,y) = myworld.findEmptyLocation()
        myworld.addThing(newplant,x,y)

    for i in range(worldLifeTime):
        myworld.liveALittle()

    myworld.freezeWorld()

if __name__ == "__main__":
    mainSimulation()