import pygame
import Colliders

GBACOLORS = (
    (15, 56, 15),# Darkest
    (48, 98, 48),
    (139, 172, 15),
    (155, 188, 15) # Lightest
)

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60


def IsOOB(Pos):
    """

    :param Pos:
    :return Returns weather object is within Level bounds:
    """
    return 0 < Pos[0] < WIDTH and 0 < Pos[1] < HEIGHT


def MoveObj(obj, Distance):
    """

    :param Distance:
    :param obj:
    :return Moves Object using Arrow Keys:
    """
    if pygame.key.get_pressed()[pygame.K_UP]:
        if IsOOB((obj.pos[0], obj.pos[1] - Distance)):
            obj.pos[1] -= Distance
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if IsOOB((obj.pos[0], obj.pos[1] + Distance)):
            obj.pos[1] += Distance
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if IsOOB((obj.pos[0] - Distance, obj.pos[1])):
            obj.pos[0] -= Distance
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if IsOOB((obj.pos[0] + Distance, obj.pos[1])):
            obj.pos[0] += Distance


if __name__ == '__main__':
    pygame.init()
    gaming = True

    c1 = Colliders.Circle(300, 300, 50, SCREEN)
    #c2 = Colliders.Circle(30, 700, 30, SCREEN)

    AABB1 = Colliders.AABB(30, 30, SCREEN, 100, 100)
    #AABB2 = Colliders.AABB(400, 400, SCREEN, 100, 100)

    Line = Colliders.Line(400, 400, SCREEN, 100, 45)

    player = Colliders.Shape(0, 0, SCREEN)

    c1.LineInRadius(Line)

    print(f'''
    Line start: {Line.pos}
    Line end: {Line.P2}
    Circle Pos: {c1.pos}
    
    ''')

    while gaming:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                gaming = False

        SCREEN.fill(GBACOLORS[0])
        player.pos = pygame.mouse.get_pos()

        player.DrawPoint()

        # Move Circle
        AABB1.Draw()
        #AABB2.Draw()

        MoveObj(c1, 5)

        if pygame.key.get_pressed()[pygame.K_a]:
            Line.dir += 1
            Line.P2 = Line.GetP2()
        if pygame.key.get_pressed()[pygame.K_d]:
            Line.dir -= 1
            Line.P2 = Line.GetP2()

        if c1.LineInRadius(Line):
            Line.color = GBACOLORS[3]
        else:
            Line.color = GBACOLORS[1]

        c1.Draw()
        pygame.draw.line(SCREEN, Line.color, c1.pos, player.pos, 4)

        Line.DrawLine()

        pygame.display.flip()
        CLOCK.tick(FPS)
