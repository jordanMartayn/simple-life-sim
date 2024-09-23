import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#globals
herbivores = []
fps = 60

#classes
class Herbivore:
    color = pygame.Color(170,240,190)
    origin = (0,0)
    scale = 10
    size = 1
    radius = scale * size
    speed = 1

    def __init__(self, origin):
        self.origin = origin
        herbivores.append(self)

    def move(self):
        #to make this efficent i need to have it select a vector choose a distance and use fps
        #and a speed to deside its goal and then animate
        #azimuth
        print('working here')

    def draw(self):
        pygame.draw.circle( screen, self.color, self.origin, self.radius )

#methods
def spawnHerbivore():
    testHerb = Herbivore( (50,50) )

#executions
spawnHerbivore()

#game loop
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("grey")

    #draw
    for entity in herbivores:
        entity.draw()


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to 60

pygame.quit()