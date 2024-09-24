import random
import math
import pygame

# pygame setup
screenX = 1280
screenY = 720
pygame.init()
screen = pygame.display.set_mode((screenX, screenY))
clock = pygame.time.Clock()
running = True

# globals
herbivores = []
fps = 60
stop = False
numberOfHerbs = 100

# classes
class Herbivore:
    color = pygame.Color(170,240,190)
    origin = (0,0)
    scale = 10
    size = 1
    radius = scale * size
    speed = 100 #pixels/second
    goal = (0,0)
    moveAgregate = (0,0)

    def __init__(self, origin):
        self.origin = origin
        herbivores.append(self)

    def updateGoal(self):
        # to being with lets randomize an azemuth normally rads is standard for sohcahtoa but 
        # pygame has rotate in degrees so lets try that first.
        randomAzimuth = random.randint(0,360)
        randomAzRads = math.radians(randomAzimuth)

        # now a distance do i do this in pixels, percentage of boundry or time spend traveling
        # lets try pixels to see the limitations and benifits.
        randomDistance = random.randint(1,600) 

        # using it's current position we need to know the hypothetical position it will travel to
        # if its off screen i want it to un wittingly head towards the goal regardless.
        randomDistanceX = math.sin(randomAzRads) * randomDistance
        randomDistanceY = math.cos(randomAzRads) * randomDistance
        goalXpos = randomDistanceX - self.origin[0]
        goalYpos = randomDistanceY - self.origin[1]
        self.goal[0] = goalXpos
        self.goal[1] = goalYpos
    
    # need a way to check if colided with boundry then updateGoal

    def move(self):
        global stop
        if stop == True:
            return
        # speed should be a measure of pixels/second or similar so it isn't tied to the frame rate.
        # lets start with 10px/s to figure out what we need to do we need to think how far I 
        # we need to travel and how long it will take and convert to what to do on a frame bases
        # so lets say a distance of 600 pixels with our 10px/s it should take a minute 
        # to get how many px it can move in a frame we do speed in px/s and time / by FPS
        frameTime = 1 / fps
        frameDist = self.speed * frameTime

        
        distToGoalX = self.goal[0] - self.origin[0]
        distToGoalY = self.goal[1] - self.origin[1]
        distXYRatio = 0
        if not distToGoalY == 0: 
            distXYRatio = distToGoalX / distToGoalY
        

        # so it gets a bit wild here, im using the ratio between x and y & the frameDist to find the x and y componants to frame distance (d)
        # after subsiting in r = x/y and d = 2root of (x^2 + y^2) we can get y = d / sqroot(r^2 + 1) and x = d*r / sqroot(r^2 + 1)
        frameDistXComp = (frameDist * distXYRatio) / math.sqrt( distXYRatio ** 2 + 1 )
        frameDistYComp = frameDist / math.sqrt( distXYRatio ** 2 + 1)
        #print('x comp: ',frameDistXComp,'y comp: ',frameDistYComp)

        # because the distance per frame will be so small we need to do a running agregate so when it's 
        # big enough we act, pixels is intergers after all.
        newAgregate = ( frameDistXComp + self.moveAgregate[0] , frameDistYComp + self.moveAgregate[1])
        self.moveAgregate = newAgregate
        #print('x move agregate: ',self.moveAgregate[0],'y move agregate: ',self.moveAgregate[1])

        ##new pos
        if self.moveAgregate[0] >= 1:
            newPosXupdated = ( self.origin[0] + self.moveAgregate[0] , self.origin[1])
            self.origin = newPosXupdated
            self.moveAgregate = ( (self.moveAgregate[0] - 1) ,self.moveAgregate[1])
        if self.moveAgregate[1] >= 1:
            newPosYupdated = ( self.origin[0] , self.origin[1]  + self.moveAgregate[1])
            self.origin = newPosYupdated
            self.moveAgregate = (self.moveAgregate[0] , (self.moveAgregate[1] - 1))

        #print('origin: ',self.origin)
        # stop = True


    def draw(self):
        pygame.draw.circle( screen, self.color, self.origin, self.radius )

# methods
def spawnHerbivore():
    randomXStart = random.randint(0,screenX)
    randomYStart = random.randint(0,screenY)
    Herbivore( (randomXStart,randomYStart) )

# executions
for i in range(numberOfHerbs):
    spawnHerbivore()

# game loop
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("grey")

    # draw
    for entity in herbivores:
        entity.move()
        entity.draw()


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to 60

pygame.quit()