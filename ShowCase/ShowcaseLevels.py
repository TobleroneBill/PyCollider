import copy
import math
import random
from random import randint
import pygame
import Colliders

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60
Level = 1
font = None
OOBCoords = [(75,100),(720,700)]
GBACOLORS = (
    (15, 56, 15),# Darkest
    (48, 98, 48),
    (139, 172, 15),
    (155, 188, 15) # Lightest
)


#_______________________/Dragging example/_______________________#
shapeArr = [
    Colliders.Shape(150, 200,SCREEN),
    Colliders.Line(400,400,SCREEN,200,0),
    Colliders.Tri(75,100,SCREEN,(75,150),(75,500),(150,150)),
    Colliders.AABB(450,150,SCREEN,100,100),
    Colliders.Circle(600,500,50,SCREEN)
]

mouseShape = Colliders.Shape(0,0, SCREEN)
# saves last 2 mouse movements for dragging (normal pygame version is bad)
posList = []
Selected = None

def SelectedCollideCheck(inshape):
    # AABB check
    if inshape.__class__.__name__ == 'AABB':
        for item in shapeArr:
            if item == inshape:
                continue
            if item.__class__.__name__ == 'Tri':
                if item.PointCollide(inshape.pos) or item.PointCollide((inshape.pos[0]+inshape.w,inshape.pos[1]+inshape.h)):
                    item.color = item.CollideColor
                else:
                    item.color = item.safeColor
            if item.__class__.__name__ == 'Line':
                if inshape.LineCollide(item):
                    item.color = item.CollideColor
                else:
                    item.color = item.safeColor
            if item.__class__.__name__ == 'Circle':
                if item.RectCollide(inshape):
                    item.color = item.CollideColor
                else:
                    item.color = item.safeColor
            if item.__class__.__name__ == 'AABB':
                if item.RectCollide(inshape):
                    item.color = item.CollideColor
                else:
                    item.color = item.safeColor
    # Circle
    if inshape.__class__.__name__ == 'Circle':
        for item in shapeArr:
            if item == inshape:
                continue
            if item.__class__.__name__ == 'Tri':
                if inshape.PointCollide(item.points[0]) or inshape.PointCollide(item.points[1]) or inshape.PointCollide(item.points[2]):
                    item.color = item.CollideColor
                else:
                    item.color = item.safeColor
            if item.__class__.__name__ == 'Line':
                if inshape.LineInRadius(item):
                    item.color = item.CollideColor
                else:
                    item.color = item.safeColor
            if item.__class__.__name__ == 'Circle':
                if item.CircleCollide(inshape):
                    item.color = item.CollideColor
                else:
                    item.color = item.safeColor
            if item.__class__.__name__ == 'AABB':
                if inshape.RectCollide(item):
                    item.color = item.CollideColor
                else:
                    item.color = item.safeColor

def movshape():
    movementx = posList[1][0] - posList[0][0]
    movementy = posList[1][1] - posList[0][1]
    newpos = (Selected.pos[0] + movementx, Selected.pos[1] + movementy)

    SelectedCollideCheck(Selected)
    if Selected.__class__.__name__ == 'AABB':
        if newpos[0] < OOBCoords[0][0] or newpos[0] + Selected.w > OOBCoords[1][0] or newpos[1] < OOBCoords[0][1] or newpos[1]  + Selected.h > OOBCoords[1][1]:
            return
    if Selected.__class__.__name__ == 'Circle':
        if newpos[0] - Selected.r < OOBCoords[0][0] or newpos[0] + Selected.r > OOBCoords[1][0] or newpos[1] - Selected.r < OOBCoords[0][1] or newpos[1] + Selected.r > OOBCoords[1][1]:
            return


    # prevent OOB
    if newpos[0] < OOBCoords[0][0] or newpos[0] > OOBCoords[1][0] or newpos[1] < OOBCoords[0][1] or newpos[1] > OOBCoords[1][1]:
        return
    Selected.pos = newpos

def screen1():
    global Selected
    shapeArr[1].dir +=1
    shapeArr[1].GetP2()
    pygame.display.set_caption('Drag Collision')
    # if player clicks on any shape, they can drag it around which will show weather collision occurs
    mouseShape.color = (255,255,255)
    mouseShape.pos = pygame.mouse.get_pos()
    mouseShape.Draw()

    # pt has a wierd method
    if shapeArr[0].OriginPointCollide(mouseShape.pos, 10):
        shapeArr[0].color = shapeArr[0].CollideColor
    else:
        shapeArr[0].color = shapeArr[0].safeColor
    shapeArr[0].Draw()

    for i,shape in enumerate(shapeArr):
        if i == 0:
            continue
        if Selected is None:
            if shape.PointCollide(mouseShape.pos) and pygame.mouse.get_pressed(num_buttons=3) == (1,0,0):
                Selected = shape
        shape.Draw()

        if shape.PointCollide(mouseShape.pos):
            shape.color = (255,255,255)
        else:
            shape.color = shape.safeColor

    if Selected is not None:
        movshape()
    if pygame.mouse.get_pressed() != (1, 0, 0):
        Selected = None

#_______________________/LineDodge example/_______________________#
shapeNum = 1
size = 100
dir = 0
player = Colliders.Shape(200,400,SCREEN)
timer = 60
time = 0
totalTime = 0
lineList = []
# switch between point, line or square for challenge
def setShape(shapeNum):
    global player, size,dir
    shapeNum += 1
    if shapeNum == 3:
        shapeNum = 1

def screen2():
    global timer,time,lineList,totalTime, font

    text = font.render(f'{totalTime}',False,GBACOLORS[1],None)
    textRect = text.get_rect()
    textRect[0] = OOBCoords[0][0] + 20
    textRect[1] = OOBCoords[0][1] + 20

    SCREEN.blit(text,textRect)
    time += 1
    totalTime += 1
    if time == timer:
        time = 0
        lineList.append(Colliders.Line(randint(75,720),randint(100,700),SCREEN,10,randint(0,359)))
    for line in lineList:
        line.Draw()
        if line.PointCollide(player.pos):
            lineList = []
            totalTime = 0
        if line.P2[0] < 0 or line.P2[0] > 800 or line.P2[1] < 0 or line.P2[1] > 800:
            continue
        else:
            line.size+=3
            line.P2 = line.GetP2()
    player.Draw()
    Colliders.Move(player,1,OOBCoords[0],OOBCoords[1])

#_______________________/Asteroids example/_______________________#
class Bullet:
    def __init__(self,x,y,angle,screenref,player):
        self.x = x
        self.y = y
        self.playerRef = player
        self.direction = (
            math.sin(math.radians(angle)),math.cos(math.radians(angle))
        )
        self.shape = Colliders.Line(x,y,screenref,10,angle)

    def Move(self):
        self.x += self.direction[0] * 10
        self.y += self.direction[1] * 10
        self.shape.pos = (self.x,self.y)
        self.shape.P2 = self.shape.GetP2()
        self.OOB()
        self.shape.Draw()

    def OOB(self):
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 800:
            self.playerRef.bullets.remove(self)

class Player:
    def __init__(self,x,y,screen):
        self.x = x
        self.y = y
        self.angle = 0
        self.forwardVel = 0
        self.bullets = []
        self.shape = Colliders.AABB(self.x,self.y,SCREEN,50,50)
        self.pointer = Colliders.Line(self.x,self.y,SCREEN,50,self.angle)
        self.score = 0
    def move(self):
        self.input()
        x = math.sin(math.radians(self.angle))  # math assumes radians instead of degrees, so must be converted
        y = math.cos(math.radians(self.angle))
        self.x += x * self.forwardVel
        self.y += y * self.forwardVel

        # oob
        if self.x < 0 - self.shape.w:
            self.x += 800 + self.shape.w
        if self.x > 800 + self.shape.w:
            self.x = -self.shape.w

        if self.y < 0 - self.shape.h:
            self.y += 800 + self.shape.h
        if self.y > 800 + self.shape.h:
            self.y = - self.shape.h

        #self.y += y * self.movespeed
        self.UpdateShape()

    def UpdateShape(self):
        self.shape.pos[0] = self.x
        self.shape.pos[1] = self.y
        self.pointer.pos = (self.shape.pos[0] + (self.shape.w * 0.5),self.shape.pos[1] + (self.shape.h * 0.5))
        self.pointer.dir = self.angle
        self.pointer.P2 = self.pointer.GetP2()
        self.shape.Draw()
        self.pointer.Draw()
        for bullet in self.bullets:
            bullet.Move()


    def input(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and len(self.bullets) < 1:
            self.Fire()

        # Update Rotations
        if pygame.key.get_pressed()[pygame.K_d]:
            self.angle-=1
        if pygame.key.get_pressed()[pygame.K_a]:
            self.angle+=1
        if self.angle< 0:
            self.angle = 360
        if self.angle > 360:
            self.angle = 0
        # add Velocity
        if pygame.key.get_pressed()[pygame.K_w]:
            if self.forwardVel < 3:
                self.forwardVel += 0.1
        # sub Vel
        if pygame.key.get_pressed()[pygame.K_s]:
            if self.forwardVel > -3:
                self.forwardVel -= 0.1


    def Fire(self):
        self.bullets.append(Bullet(self.x,self.y,self.angle,SCREEN,self))

class Asteroid:
    oobmin = OOBCoords[0]
    oobmax = OOBCoords[1]
    def __init__(self,x,y,screen):
        self.angle = random.randint(0,359)    #random dir vector
        self.x = x
        self.y = y
        self.level = 4  # goes from 4-0
        self.movespeed = 2
        self.shape = Colliders.Circle(self.x,self.y,80,screen)
    def move(self):
        self.x += math.sin(math.radians(self.angle)) * self.movespeed
        self.y += math.cos (math.radians(self.angle)) * self.movespeed
        if self.x < 0 - self.shape.r:
            self.x += 800 + self.shape.r
        if self.x > 800 + self.shape.r:
            self.x =self.shape.r

        if self.y < 0 - self.shape.r:
            self.y += 800 + self.shape.r
        if self.y > 800 + self.shape.r:
            self.y = -self.shape.r

        self.shape.pos[0] = self.x
        self.shape.pos[1] = self.y
        self.shape.Draw()

    def hit(self):  # if bullet (bullet calls this) hit, reduce level and create a clone. if level = 0 die
        self.level-= 1
        self.movespeed *= 1.1
        self.shape.r *= 0.8
        # make a new one


gamestart = False
Aplayer = None
asteroidList = []
score = 0

def Game():
    global gamestart, Aplayer, asteroidList, score
    font = pygame.font.SysFont('Ariel', 100)
    text = font.render(f'{score}', False, GBACOLORS[1], None)
    textRect = text.get_rect()
    textRect[0] = 100
    textRect[1] = 120
    SCREEN.blit(text,textRect)
    addlist = []
    if gamestart is False:
        score = 0
        Aplayer = Player(400,400,SCREEN)
        asteroidList = [Asteroid(randint(100, 500) - (Aplayer.x*0.5), randint(100, 500)- (Aplayer.y*0.5), SCREEN)]
        gamestart = True
    else:
        Aplayer.move()
        for i,asteroid in enumerate(asteroidList):
            asteroid.move()
            if asteroid.shape.RectCollide(Aplayer.shape):
                gamestart = False
            if len(Aplayer.bullets) > 0:
                if asteroid.shape.PointCollide((Aplayer.bullets[0].x,Aplayer.bullets[0].y)):
                    del Aplayer.bullets[0]
                    asteroid.hit()
                    score += 1
                    if asteroid.level <= 0:
                        asteroidList.remove(asteroid)
                        addlist.append(Asteroid(randint(100, 500) - (Aplayer.x*0.5), randint(100, 500)- (Aplayer.y*0.5), SCREEN))
                        addlist.append(Asteroid(randint(100, 500) - (Aplayer.x*0.5), randint(100, 500)- (Aplayer.y*0.5), SCREEN))
                    else:
                        new = Asteroid(asteroid.x,asteroid.y,SCREEN)
                        new.level = asteroid.level
                        new.angle = randint(0,360)
                        addlist.append(new)
    if len(addlist) > 0:
        for item in addlist:
            asteroidList.append(item)


def screen3():
    Game()



def SetLevel():
    global Level
    if pygame.key.get_pressed()[pygame.K_1]:
        Level = 1
    if pygame.key.get_pressed()[pygame.K_2]:
        Level = 2
    if pygame.key.get_pressed()[pygame.K_3]:
        Level = 3


def run():
    global font
    pygame.init()
    gaming = True
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont('Ariel', 100)
    GBOVERLAY = pygame.image.load("ShowCase/Collision Overlay.png")
    GBOVERLAY = pygame.transform.scale(GBOVERLAY,(800,800))
    screenOverlay = pygame.Rect(0,0,800,800)
    # Randomizer
    while gaming:
        SetLevel()
        SCREEN.fill(GBACOLORS[0])
        SCREEN.blit(GBOVERLAY,screenOverlay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                gaming = False

        # Get mouse movement
        if len(posList) == 2:
            posList[0] = posList[1]
            posList[1] = mouseShape.pos
        else:
            posList.append(mouseShape.pos)

        if Level == 1:
            screen1()
        elif Level == 2:
            screen2()
        elif Level == 3:
            screen3()



        pygame.display.flip()
