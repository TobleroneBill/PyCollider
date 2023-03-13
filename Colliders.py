import math
import pygame.draw

GBACOLORS = (
    (15, 56, 15),  # Darkest
    (48, 98, 48),
    (139, 172, 15),
    (155, 188, 15)  # Lightest
)


# By Billiams Mcbingus 13/03/2023

# ____________________________Shape Collision Detection Methods____________________________#

def DotProd(p1, p2):
    return (p1[0] * p2[0]) + (p1[1] * p2[1])

def DetemrinantP3(p1,p2,p3):
    return (((p1[0] - p3[0]) * (p2[1] - p3[1])) - ((p2[0] - p3[0]) * (p1[1] - p3[1])))

def DistanceFromPoint(P1, P2):
    """
    :param P2:
    :param P1:
    :return  Returns Distance from P1 to p2 using Pythagoras:
    """
    #                       a2              +           B2
    return math.sqrt(((P1[0] - P2[0]) ** 2) + ((P1[1] - P2[1]) ** 2))


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
        self.debug = False  # Some shapes have debug settings to visually see what's going on

    def DrawPoint(self):
        pygame.draw.circle(self.screenRef, self.color, self.pos, 5)


class Circle(Shape):

    def __init__(self, x, y, radius, scr):
        super().__init__(x, y, scr)
        self.r = radius
        self.borderSize = 5

    def LineInRadius(self, Line):
        if self.ContainsPoint(Line.pos) or self.ContainsPoint(Line.P2):
            return True

        u = (((self.pos[0] - Line.pos[0]) * (Line.P2[0] - Line.pos[0])) + (
                    (self.pos[1] - Line.pos[1]) * (Line.P2[1] - Line.pos[1]))) / (Line.size ** 2)

        newPos = (Line.pos[0] + (u * (Line.P2[0] - Line.pos[0])), Line.pos[1] + (u * (Line.P2[1] - Line.pos[1])))
        # Debug
        if self.debug:
            pygame.draw.line(self.screenRef, (255, 255, 255), self.pos, newPos, 5)
            pygame.draw.circle(self.screenRef, (255, 0, 0), newPos, 5)

        if Line.PointOnLine(
                newPos):  # We use this new position to test if it lies on the line (since its an infinite line)
            if self.ContainsPoint(newPos):  # If on the line, we just need to see if its within the radius of the Circle
                return True
        return False

    '''
    # WE DONT GO TO RAVENHOLM #
    def LineInRadius(self, Line):
        newpos = (0,0)

        # This works, but doesn't take into account rotations :thinking:

        # Had to do A LOT OF SHIT to get to the point where this works.
        # UPDATE: This only works with Vertical lines :/
        # Formula of projection is:
        # scalar = Dot(line end, self.pos) / Dot(line end, line end) (or line x**2 + liney**2)
        # (self.x * scalar, self.y* scalar) = the closest position on the line i think (will test now)

        # This assumes origin 0,0, which is not the case

        x = (self.pos[0] + Line.pos[0],self.pos[1]+Line.pos[1])
        v = (Line.P2[0] + Line.pos[0],Line.P2[1]+Line.pos[1])

        #x = self.pos
        #v = Line.P2


        a = DotProd(v,x)
        b = DotProd(v,v)

        if a == 0 or b == 0:
            return

        c = a/b
        x = Line.P2[0] * c
        y = Line.P2[1] * c

        # I can use this to get the right angled triangle that is closest to the line
        newpos = (x,y)

        pygame.draw.line(self.screenRef,(255,255,255),Line.P2,self.pos)
        pygame.draw.line(self.screenRef,(255,255,255),Line.pos,self.pos)

        #Mid section:
        midx = Line.pos[0] + ((Line.P2[0] - Line.pos[0]) * 0.5)
        midy = Line.pos[1] + ((Line.P2[1] - Line.pos[1]) * 0.5)
        pygame.draw.line(self.screenRef,(100,100,100),self.pos,(midx,midy))

        #pygame.draw.line(self.screenRef,(100,200,0),newpos,self.pos,5)
        pygame.draw.circle(self.screenRef,(0,255,255),newpos,5)


        # If line is on the point and within the radius of the Circle then true
        if self.ContainsPoint(newpos):
            return True

        return False
    '''

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
        # self top left Less than BBY bottom right and
        # self bottom right greater than BBYY top left
        if self.pos[0] < BBY.pos[0] + BBY.w and self.pos[1] < BBY.pos[1] + BBY.h and self.pos[0] + self.w > BBY.pos[0] and self.pos[1] + self.h > BBY.pos[0]:
            return True
        return False

    def PointCollide(self, Pos):
        # Just checks that point is within bounds of the aabb points (top left x/y and bottom right x/y)
        return self.pos[0] <= Pos[0] <= self.pos[0] + self.w and self.pos[1] <= Pos[1] <= self.pos[1] + self.h


class Line(Shape):

    def __init__(self, x, y, scr, Size, Dir):
        super().__init__(x, y, scr)
        self.dir = Dir
        self.size = Size
        self.P2 = self.GetP2()

    def GetP2(self):
        # THIS IS COOL (found on quora lol) - SOHCAHTOA
        # angle is given in constructor, so if we assume a vector of 1 (normalized), then we can just use sin and cos to get
        # the x and y axis, then scale them by the given size. that is the 2nd point of this line
        x = math.sin(math.radians(self.dir))  # math assumes radians instead of degrees, so must be converted
        y = math.cos(math.radians(self.dir))
        x *= self.size
        y *= self.size
        return [self.pos[0] + x, self.pos[1] + y]

    def DrawLine(self):
        pygame.draw.line(self.screenRef, self.color, self.pos, self.P2, 5)
        pygame.draw.circle(self.screenRef, (255, 0, 0), self.P2, 5)

    def PointOnLine(self, P):
        """

        :param P:
        :return A bool to check if point is on this line object:
        """
        # Theorm: if the magnitude to the point from both sides of the line added together is == to the line magnitude
        # Then it is on the line (triangle facts)

        length = DistanceFromPoint(self.pos, self.P2)
        p1Dist = DistanceFromPoint(self.pos, P)
        p2Dist = DistanceFromPoint(self.P2, P)

        # Gives some leeway to be less precise
        minLen = length - 2
        maxLen = length + 2

        if maxLen >= p1Dist + p2Dist >= minLen:
            return True
        else:
            return False


class Tri(Shape):

    def __init__(self, x, y, scr, p1, p2, p3):
        super().__init__(x, y, scr)
        self.points = [p1, p2, p3]  # arr of triangle points
        self.drawWidth = 5
        self.area = self.GetTriArea()
        print(self.area)

    def GetTriArea(self):
        # not to be used with point collide as this is too slow and should just be used for comaprisons

        return None

    def Draw(self):
        for index, point in enumerate(self.points):
            pygame.draw.circle(self.screenRef, GBACOLORS[2], point, 5)
            if index == 0:
                pygame.draw.line(self.screenRef, self.color, self.points[index], self.points[len(self.points) - 1],
                                 self.drawWidth)
                continue
            pygame.draw.line(self.screenRef, self.color, self.points[index - 1], self.points[index], self.drawWidth)

    def PointCollide(self,pt):
        # This uses a matrix multiplication/determinant method to get areas
        # that's why it is so dumb and complicated (but more performant)
        # we would usually also /2 for each area as the results given are for squares
        # we don't actually need this, as it works exactly the same, just with bigger numbers
        # which is faster than division (I believe)

        # Makes life easier for me
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]

        area = abs(DetemrinantP3(p1,p2,p3))
        a1 = abs(DetemrinantP3(p1,p2,pt))
        a2 = abs(DetemrinantP3(p2,p3,pt))
        a3 = abs(DetemrinantP3(p3,p1,pt))
        return a1+a2+a3 == area
