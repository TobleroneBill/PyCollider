import math
import pygame.draw

# By Billiams Mcbingus 14/03/2023
# A collection of not OOP collision detection methods for flexibility
# ____________________________Shape Collision Detection Methods____________________________#

GBACOLORS = (
    (15, 56, 15),  # Darkest
    (48, 98, 48),
    (139, 172, 15),
    (155, 188, 15)  # Lightest
)


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


# _____________________________/Line Functions/_____________________________#

def PointOnLine(Linestart, Lineend, P):
    """

        :param P:w
        :return A bool to check if point is on this line object:
        """
    # Theorm: if the magnitude to the point from both sides of the line added together is == to the line magnitude
    # Then it is on the line (triangle facts)

    length = DistanceFromPoint(Linestart, Lineend)
    p1Dist = DistanceFromPoint(Linestart, P)
    p2Dist = DistanceFromPoint(Lineend, P)

    # Gives some leeway to be less precise
    minLen = length - 2
    maxLen = length + 2

    if maxLen >= p1Dist + p2Dist >= minLen:
        return True
    return False


def LineIntersect(l1start, l1end, l2start, l2end, screenref=None):
    # get all positions (easier on my brain)
    a = l1start
    b = l1end
    c = l2start
    d = l2end

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
    if screenref is not None:
        # actual projection coords
        line1Projection = (a[0] + (uA * (b[0] - a[0])), a[1] + (uA * (b[1] - a[1])))
        line2Projection = (c[0] + (uB * (d[0] - c[0])), c[1] + (uB * (d[1] - c[1])))
        pygame.draw.line(screenref, (GBACOLORS[2]), a, line1Projection)
        pygame.draw.line(screenref, (GBACOLORS[2]), c, line2Projection)

    if (0 <= uA <= 1) and (0 <= uB <= 1):
        return True
    return False


def GetP2(Linestart, Angle, Size):
    # THIS IS COOL (found on quora lol) - SOHCAHTOA
    # angle is given in constructor, so if we assume a vector of 1 (normalized), then we can just use sin and cos to get
    # the x and y axis, then scale them by the given size. that is the 2nd point of this line
    x = math.sin(math.radians(Angle))  # math assumes radians instead of degrees, so must be converted
    y = math.cos(math.radians(Angle))
    x *= Size
    y *= Size
    return [Linestart[0] + x, Linestart[1] + y]


# _____________________________/Circle Functions/_____________________________#

def CircleLineCollide(CirclePos, LineStart, LineEnd, Radius):
    aDist = DistanceFromPoint(CirclePos, LineStart)
    bDist = DistanceFromPoint(CirclePos, LineEnd)
    if aDist <= Radius or bDist <= Radius:
        return True
    return False


def LineInRadius(Circlepos, Radius, LineStart, LineEnd, screenref=None):
    if CircleLineCollide(Circlepos, LineStart, LineEnd, Radius):
        return True

    u = (((Circlepos[0] - LineStart[0]) * (LineEnd[0] - LineStart[0])) + (
            (Circlepos[1] - LineStart[1]) * (LineEnd[1] - LineStart[1]))) / (DistanceFromPoint(LineStart, LineEnd) ** 2)

    newPos = (LineStart[0] + (u * (LineEnd[0] - LineStart[0])), LineStart[1] + (u * (LineEnd[1] - LineStart[1])))
    # Debug
    if screenref is not None:
        pygame.draw.line(screenref, GBACOLORS[3], Circlepos, newPos, 5)
        pygame.draw.circle(screenref, (255, 0, 0), newPos, 5)

    if PointOnLine(LineStart, LineEnd,
                   newPos):  # We use this new position to test if it lies on the line (since its an infinite line)
        if DistanceFromPoint(Circlepos,
                             newPos) <= Radius:  # If on the line, we just need to see if its within the radius of the Circle
            return True
    return False


def CircleCollide(c1Pos, c1R, c2Pos, c2R):
    """
    Checks if distance from self to circle is less than both radius' Combined
    :param CircleObj:
    :return:
    """
    return DistanceFromPoint(c1Pos, c2Pos) <= c1R + c2R


def CirlceAABBCollide(CirclePos, Radius, Rectpos, W, H, screenref=None):
    px = CirclePos[0]
    py = CirclePos[1]

    # which x side to check
    if CirclePos[0] < Rectpos[0]:  # left
        px = Rectpos[0]
    elif CirclePos[0] > Rectpos[0] + W:  # Right
        px = Rectpos[0] + W

    # Y side
    if CirclePos[1] < Rectpos[1]:  # above
        py = Rectpos[1]
    elif CirclePos[1] > Rectpos[1] + H:  # below
        py = Rectpos[1] + H

    # Book has some wierd ass subtraction that doesn't work :/
    distanceX = px
    distanceY = py

    Dist = DistanceFromPoint(CirclePos, (distanceX, distanceY))

    if screenref is not None:
        pygame.draw.line(screenref, GBACOLORS[2], CirclePos, (distanceX, distanceY))

    if Dist <= Radius:
        return True
    return False


# _____________________________/AABB Functions/_____________________________#

def AABBDetect(aabb1pos, W1, H1, aabb2pos, W2, H2):
    # self top left Less than aabb2 bottom right and
    # self bottom right greater than aabb2Y top left
    if aabb1pos[0] < aabb2pos[0] + W2 and aabb1pos[1] < aabb2pos[1] + H2 and aabb1pos[0] + W1 > aabb2pos[0] and \
            aabb1pos[1] + H1 > aabb2pos[0]:
        return True
    return False


def AABBPointCollide(AABBpos, W, H, newPos):
    # Just checks that point is within bounds of the aabb points (top left x/y and bottom right x/y)
    return AABBpos[0] <= newPos[0] <= AABBpos[0] + W and AABBpos[1] <= newPos[1] <= AABBpos[1] + H


def AABBLineCollide(AABBpos, W, H, Linestart, Lineend):
    # this uses the same ideas as the circle line collide method, just with more points
    # so its more complicated. would recommend this for something that requires a single check
    # Like line of sight, as continuous calling of this is likely very bad performance wise
    if AABBPointCollide(AABBpos, W, H, Linestart) or AABBPointCollide(AABBpos, W, H, Lineend):
        return True

    # Just applies the line intersection check on every line of the aabb.
    # this is why its slow, but accurate

    # def LineIntersect(l1start,l1end, l2start, l2end,screenref=None):
    left = LineIntersect(Linestart, Lineend, AABBpos, (AABBpos[0], AABBpos[1] + H))
    right = LineIntersect(Linestart, Lineend, (AABBpos[0] + W, AABBpos[1]), (AABBpos[0] + W, AABBpos[1] + H))
    top = LineIntersect(Linestart, Lineend, AABBpos, (AABBpos[0] + W, AABBpos[1]))
    bot = LineIntersect(Linestart, Lineend, (AABBpos[0], AABBpos[1] + H), (AABBpos[0] + W, AABBpos[1] + H))

    # if any intersect, its colliding
    if left or right or top or bot:
        return True

    return False


# _____________________________/Triangle Functions/_____________________________#

def GetTriArea(p1, p2, p3):
    return abs(DetemrinantP3(p1, p2, p3)) / 2


def TriPointCollide(p1, p2, p3, newpt):
    # this was super useful: https://www.gamedev.net/forums/topic.asp?topic_id=295943
    # This uses a matrix multiplication/determinant method to get areas
    # that's why it is so dumb and complicated (but more performant)
    # we would usually also /2 for each area as the results given are for squares
    # we don't actually need this, as it works exactly the same, just with bigger numbers
    # which is faster than division (I believe)

    area = abs(DetemrinantP3(p1, p2, p3))
    a1 = abs(DetemrinantP3(p1, p2, newpt))
    a2 = abs(DetemrinantP3(p2, p3, newpt))
    a3 = abs(DetemrinantP3(p3, p1, newpt))
    return a1 + a2 + a3 == area
