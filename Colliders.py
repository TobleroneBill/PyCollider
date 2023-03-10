import math

import pygame.draw


# ____________________________Shape Collision Detection Methods____________________________#

def DistanceFromPoint(P1, P2):
    """
    :param P2:
    :param P1:
    :return  Returns Distance from P1 to p2 using Pythagoras:
    """
    return math.sqrt(((P2[0] - P1[0]) ** 2) + ((P2[1] - P1[1]) ** 2))


def CircleLineCollide(Circle, Line):
    aCollide = Circle.ContainsPoint(Line.pos)
    bCollide = Circle.ContainsPoint(Line.P2)
    if aCollide or bCollide:
        return True
    return False


class Shape:
    def __init__(self, x, y, scr):
        self.pos = [x, y]
        self.screenRef = scr
        self.color = (48, 98, 48)

    def DrawPoint(self):
        pygame.draw.circle(self.screenRef, self.color, self.pos, 5)


class Circle(Shape):

    def __init__(self, x, y, radius, scr):
        super().__init__(x, y, scr)
        self.r = radius
        self.borderSize = 5

    def LineInRadius(self, Line):

        # Had to do A LOT OF SHIT to get to the point where this works.
        x = Line.pos[0] - self.pos[0]
        y = Line.pos[1] - self.pos[1]

        xpos = self.pos[0] + x
        ypos = Line.pos[1] - y



        newpos = (xpos,ypos)
        pygame.draw.line(self.screenRef,(255,255,255),newpos,self.pos)

        # External point check, because the rest of this formula is wierd
        if self.ContainsPoint(Line.pos) or self.ContainsPoint(Line.P2):
            return True


        # If line is on the point and within the radius of the Circle then true
        if Line.PointOnLine(newpos):
            if self.ContainsPoint(newpos):
                return True

        return False

    def Draw(self):
        pygame.draw.circle(self.screenRef, self.color, self.pos, self.r, self.borderSize)

    def ContainsPoint(self, Point):
        """
        Checks if Point is within Circle Radius
        :param Point: (x,y) Vector
        :return: T/F
        """
        return DistanceFromPoint(self.pos, Point) <= self.r

    def CircleCollide(self, CircleObj):
        """
        Checks if distance from self to circle is less than both radius' Combined
        :param CircleObj:
        :return:
        """
        return DistanceFromPoint(self.pos, CircleObj.pos) <= self.r + CircleObj.r


class AABB(Shape):

    def __init__(self, x, y, scr, w, h):
        super().__init__(x, y, scr)
        self.w = w
        self.h = h

    def Draw(self):
        pygame.draw.rect(self.screenRef, self.color, (self.pos[0], self.pos[1], self.w, self.h), 5)

    def DetectAABB(self, BBY):
        # This is more truncated for demo purposes

        # self top left Less than BBY bottom right
        if self.pos[0] < BBY.pos[0] + BBY.w and self.pos[1] < BBY.pos[1] + BBY.h:
            # self bottom right greater than BBYY top left
            if self.pos[0] + self.w > BBY.pos[0] and self.pos[1] + self.h > BBY.pos[0]:
                return True

        return False


class Line(Shape):

    def __init__(self, x, y, scr, Size, Dir):
        super().__init__(x, y, scr)
        self.dir = Dir  # So its always within 360 degrees)
        self.size = Size
        self.P2 = self.GetP2()

    def GetP2(self):
        # Had a good few hours doing this one:
        # THIS IS COOL (found on quora lol) - SOHCAHTOA
        # angle is given in constructor, so if we assume a vector of 1 (normalized), then we can just use sin and cos to get
        # the x and y axis, then scale them by the given size. that is the 2nd point of this line
        x = math.sin(math.radians(self.dir))  # math assumes radians instead of degrees, so must be converted
        y = math.cos(math.radians(self.dir))
        # print(f'P2 Pos X: {x}, Y: {y}')
        x *= self.size
        y *= self.size
        return [self.pos[0] + x, self.pos[1] + y]

    def DrawLine(self):
        pygame.draw.line(self.screenRef, self.color, self.pos, self.P2, 5)

    def PointOnLine(self, P):
        """

        :param P:
        :return A bool to check if point is on this line object:
        """
        # Theorm: if the magnitude to the point from both sides of the line added together is == to the line magnitude
        # Then it is on the line (triangle facts)

        length = math.ceil(DistanceFromPoint(self.pos, self.P2))
        p1Dist = math.ceil(DistanceFromPoint(self.pos, P))
        p2Dist = math.ceil(DistanceFromPoint(self.P2, P))

        # Gives some leeway to be less precise
        minLen = length - 2
        maxLen = length + 2

        if maxLen >= p1Dist + p2Dist >= minLen:
            return True
        else:
            return False
