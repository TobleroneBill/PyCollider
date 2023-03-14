import pygame
import Colliders

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

GBACOLORS = (
    (15, 56, 15),# Darkest
    (48, 98, 48),
    (139, 172, 15),
    (155, 188, 15) # Lightest
)

# 800/5 = 160 - 10 = 150
# point, line, triangle, aabb, circle
shapeArr = [
    Colliders.Shape(150, 200,SCREEN),   # PT
    Colliders.Line(150,300,SCREEN,50,0),
    Colliders.Tri(300,100,SCREEN,(350,150),(300,50),(400,50)),
    Colliders.AABB(450,50,SCREEN,100,100),
    Colliders.Circle(650,100,50,SCREEN)
]

mouseShape = Colliders.Shape(0,0, SCREEN)
# saves last 2 mouse movements for dragging (normal pygame version is bad)
posList = []
Selected = None
screen = 0


#_______________________/Dragging example/_______________________#
def screen1():
    global Selected
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
        movementx = posList[1][0] - posList[0][0]
        movementy = posList[1][1] - posList[0][1]
        Selected.pos[0] = Selected.pos[0] + movementx
        Selected.pos[1] = Selected.pos[1] + movementy
        if pygame.mouse.get_pressed() != (1,0,0):
            Selected = None





def run():
    pygame.init()
    gaming = True
    pygame.mouse.set_visible(False)
    print(pygame.display.get_wm_info())

    GBOVERLAY = pygame.image.load("Collision Overlay.png")
    GBOVERLAY = pygame.transform.scale(GBOVERLAY,(800,800))
    screenOverlay = pygame.Rect(0,0,800,800)

    while gaming:
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

        if screen == 0:
            screen1()


        pygame.display.flip()
