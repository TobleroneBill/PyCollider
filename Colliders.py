import math
import pygame.draw

# By Billiams Mcbingus 13/03/2023
# ____________________________Shape Collision Detection Methods____________________________#

GBACOLORS = (
    (15, 56, 15),  # Darkest
    (48, 98, 48),
    (139, 172, 15),
    (155, 188, 15)  # Lightest
)

# _____________________________/Module Functions/_____________________________#

def DotProd(p1, p2):
    return (p1[0] * p2[0]) + (p1[1] * p2[1])

def DetemrinantP3(p1, p2, p3):
    return ((p1[0] - p3[0]) * (p2[1] - p3[1])) - ((p2[0] - p3[0]) * (p1[1] - p3[1]))

def DistanceFromPoint(P1, P2):
    """
    :param P2:
    :param P1:
    :return  Returns Distance from P1 to p2 using Pythagoras:
    """
    #                       a2              +           B2
    return math.sqrt(((P1[0] - P2[0]) ** 2) + ((P1[1] - P2[1]) ** 2))

def CircleLineCollide(Circle, Line):
    aCollide = Circle.PointCollide(Line.pos)
    bCollide = Circle.PointCollide(Line.P2)
    if aCollide or bCollide:
        return True
    return False

def IsOOB(Pos,minPos,maxPos):
    return minPos[0] < Pos[0] < maxPos[0] and minPos[1] < Pos[1] < maxPos[1]

def Move(Shape, Distance,min,max):
    if pygame.key.get_pressed()[pygame.K_UP]:
        if IsOOB((Shape.pos[0], Shape.pos[1] - Distance),min,max):
            Shape.pos[1] -= Distance
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if IsOOB((Shape.pos[0], Shape.pos[1] + Distance),min,max):
            Shape.pos[1] += Distance
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if IsOOB((Shape.pos[0] - Distance, Shape.pos[1]),min,max):
            Shape.pos[0] -= Distance
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if IsOOB((Shape.pos[0] + Distance, Shape.pos[1]),min,max):
            Shape.pos[0] += Distance

class Shape:
    def __init__(self, x, y, scr):
        self.pos = [x, y]
        self.screenRef = scr
        self.color = (48, 98, 48)
        self.CollideColor = GBACOLORS[3]
        self.safeColor = GBACOLORS[1]
        self.debug = False  # Some shapes have debug settings to visually see what's going on

    def Draw(self):
        pygame.draw.circle(self.screenRef, self.color, self.pos, 5)

    def OriginPointCollide(self,pos,delta):
        minx = self.pos[0] - delta
        miny = self.pos[1] - delta
        maxx = self.pos[0] + delta
        maxy = self.pos[1] + delta

        if (pos[0] > minx and pos[0] < maxx) and (pos[1] > miny and pos[1] < maxy):
            return True
        return False

class Circle(Shape):

    def __init__(self, x, y, radius, scr):
        super().__init__(x, y, scr)
        self.r = radius
        self.borderSize = 5

    def LineInRadius(self, Line):
        if self.PointCollide(Line.pos) or self.PointCollide(Line.P2):
            return True

        u = (((self.pos[0] - Line.pos[0]) * (Line.P2[0] - Line.pos[0])) + (
                (self.pos[1] - Line.pos[1]) * (Line.P2[1] - Line.pos[1]))) / (Line.size ** 2)

        newPos = (Line.pos[0] + (u * (Line.P2[0] - Line.pos[0])), Line.pos[1] + (u * (Line.P2[1] - Line.pos[1])))
        # Debug
        if self.debug:
            pygame.draw.line(self.screenRef, (255, 255, 255), self.pos, newPos, 5)
            pygame.draw.circle(self.screenRef, (255, 0, 0), newPos, 5)

        if Line.PointCollide(
                newPos):  # We use this new position to test if it lies on the line (since its an infinite line)
            if self.PointCollide(newPos):  # If on the line, we just need to see if its within the radius of the Circle
                return True
        return False

    def Draw(self):
        pygame.draw.circle(self.screenRef, self.color, self.pos, self.r, self.borderSize)

    def PointCollide(self, Point):
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

    def RectCollide(self, RectObj):
        px = self.pos[0]
        py = self.pos[1]

        # which x side to check
        if self.pos[0] < RectObj.pos[0]:  # left
            px = RectObj.pos[0]
        elif self.pos[0] > RectObj.pos[0] + RectObj.w:  # Right
            px = RectObj.pos[0] + RectObj.w

        # Y side
        if self.pos[1] < RectObj.pos[1]:  # above
            py = RectObj.pos[1]
        elif self.pos[1] > RectObj.pos[1] + RectObj.h:  # below
            py = RectObj.pos[1] + RectObj.h

        # Book has some wierd ass subtraction that doesn't work :/
        distanceX = px
        distanceY = py

        Dist = DistanceFromPoint(self.pos, (distanceX, distanceY))

        if self.debug:
            pygame.draw.line(self.screenRef, GBACOLORS[2], self.pos, (distanceX, distanceY))

        if Dist <= self.r:
            return True
        return False


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

    def LineCollide(self, Line):
        # this uses the same ideas as the circle line collide method, just with more points
        # so its more complicated. would recommend this for something that requires a single check
        # Like line of sight, as continuous calling of this is likely very bad performance wise
        if self.PointCollide(Line.pos) or self.PointCollide(Line.P2):
            return True

        # Just applies the line intersection check on every line of the aabb.
        # this is why its slow, but accurate
        left = Line.LineIntersect(self.pos, (self.pos[0], self.pos[1] + self.h))
        right = Line.LineIntersect((self.pos[0] + self.w, self.pos[1]), (self.pos[0] + self.w, self.pos[1] + self.h))
        top = Line.LineIntersect(self.pos, (self.pos[0] + self.w, self.pos[1]))
        bot = Line.LineIntersect((self.pos[0], self.pos[1] + self.h), (self.pos[0] + self.w, self.pos[1] + self.h))

        # if any intersect, its colliding
        if left or right or top or bot:
            return True

        return False


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

    def Draw(self):
        pygame.draw.line(self.screenRef, self.color, self.pos, self.P2, 5)
        pygame.draw.circle(self.screenRef, (255, 0, 0), self.P2, 5)

    def PointCollide(self, P):
        """

        :param P:w
        :return A bool to check if point is on this line object:
        """
        # Theorm: if the magnitude to the point from both sides of the line added together is == to the line magnitude
        # Then it is on the line (triangle facts)

        length = DistanceFromPoint(self.pos, self.P2)
        p1Dist = DistanceFromPoint(self.pos, P)
        p2Dist = DistanceFromPoint(self.P2, P)

        # Gives some leeway to be less precise
        minLen = length - 0.5
        maxLen = length + 0.5

        if maxLen >= p1Dist + p2Dist >= minLen:
            return True
        else:
            return False

    def LineIntersect(self, LineP1, LineP2):
        # get all positions (easier on my brain)
        a = self.pos
        b = self.P2
        c = LineP1
        d = LineP2

        # we have to get the scalars of each line segment in relation to the points we are checking against
        # This uses the same method as the Circle line check, but just with 2 lines instead of 1

        denominator = (((d[1] - c[1]) * (b[0] - a[0])) - ((d[0] - c[0]) * (b[1] - a[1])))
        if denominator == 0:
            return False

        # I think this is basically ortho projection, but without actually getting the projection coords
        # the scalars will both be between 0 and 1 if the lines intersect, because the projection will
        # be on both line segments

        # scalar for line 1
        uA = (((d[0] - c[0]) * (a[1] - c[1])) - ((d[1] - c[1]) * (a[0] - c[0]))) / denominator
        # Inverse of above / scalar for line 2
        uB = (((b[0] - a[0]) * (a[1] - c[1])) - ((b[1] - a[1]) * (a[0] - c[0]))) / denominator

        # This looks super sick
        if self.debug:
            # actual projection coords
            line1Projection = (a[0] + (uA * (b[0] - a[0])), a[1] + (uA * (b[1] - a[1])))
            line2Projection = (c[0] + (uB * (d[0] - c[0])), c[1] + (uB * (d[1] - c[1])))
            pygame.draw.line(self.screenRef, (GBACOLORS[2]), a, line1Projection)
            pygame.draw.line(self.screenRef, (GBACOLORS[2]), c, line2Projection)

        if (0 <= uA <= 1) and (0 <= uB <= 1):
            return True
        return False


class Tri(Shape):
    def __init__(self, x, y, scr, p1, p2, p3):
        super().__init__(x, y, scr)
        self.points = [p1, p2, p3]  # arr of triangle points
        self.drawWidth = 5
        self.area = self.GetTriArea()

    def GetTriArea(self):
        return abs(DetemrinantP3(self.points[0], self.points[1], self.points[2])) / 2

    def Draw(self):
        for index, point in enumerate(self.points):
            pygame.draw.circle(self.screenRef, GBACOLORS[2], point, 5)
            if index == 0:
                pygame.draw.line(self.screenRef, self.color, self.points[index], self.points[len(self.points) - 1],
                                 self.drawWidth)
                continue
            pygame.draw.line(self.screenRef, self.color, self.points[index - 1], self.points[index], self.drawWidth)

    def PointCollide(self, pt):
        # this was super useful: https://www.gamedev.net/forums/topic.asp?topic_id=295943
        # This uses a matrix multiplication/determinant method to get areas
        # that's why it is so dumb and complicated (but more performant)
        # we would usually also /2 for each area as the results given are for squares
        # we don't actually need this, as it works exactly the same, just with bigger numbers
        # which is faster than division (I believe)

        # Makes life easier for me
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]

        area = abs(DetemrinantP3(p1, p2, p3))
        a1 = abs(DetemrinantP3(p1, p2, pt))
        a2 = abs(DetemrinantP3(p2, p3, pt))
        a3 = abs(DetemrinantP3(p3, p1, pt))
        return a1 + a2 + a3 == area
