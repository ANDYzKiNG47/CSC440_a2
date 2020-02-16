import math
import sys

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):
    x1, y1 = p1
    x2, y2 = p2
    x3 = x
    x4 = x
    px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
             float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
    py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
                    float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
    return (px, py)

'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c. 
Note that this area will be negative 
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
    return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
    return triangleArea(a,b,c) < -EPSILON;
'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
    return triangleArea(a,b,c) > EPSILON;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
    return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):
	# get mean x coord, mean y coord
    xavg = sum(p[0] for p in points) / len(points)
    yavg = sum(p[1] for p in points) / len(points)
    angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
    points.sort(key = angle)


def sortByXCoord(points):
    points.sort(key = lambda x: x[0])
    return points

def findMax(l):
    max_x = l[0]
    idx_x = 0
    for i in range(1, len(l)):
        if l[i][0] > max_x[0]:
            max_x = l[i]
            idx_x = i
    return max_x, idx_x 

def findMin(l):
    min_x = l[0]
    idx_x = 0
    for i in range(1, len(l)):
        if l[i][0] < min_x[0]:
            minx_x = l[i]
            idx = i
    return min_x, idx_x 

def initYVals(lCurr, lNext, lidx, rCurr, rNext, ridx, divider_x):
    
    y1 = yint(lCurr, rNext, divider_x, DIVIDER_Y[0], DIVIDER_Y[1])
    y2 = yint(lCurr, rCurr, divider_x, DIVIDER_Y[0], DIVIDER_Y[1])
    y3 = yint(lNext, rCurr, divider_x, DIVIDER_Y[0], DIVIDER_Y[1])
    return y1[1], y2[1], y3[1] 

def merge(left, right):
    
    clockwiseSort(left)
    clockwiseSort(right)

    # find top connector
    lCurr, lidx = findMax(left)
    rCurr, ridx = findMin(right)
    divider_x = int((lCurr[0] + rCurr[0]) / 2)
    rNext = right[(ridx + 1) % len(right)]
    lNext = left[(lidx - 1) % len(left)] 
    y1, y2, y3 = initYVals(lCurr, lNext, lidx, rCurr, rNext, ridx, divider_x)
    
    # while 
    #   y(lCurr, rNext) > y(lCurr, rCurr) or
    #   y(lNext, rCurr) > y(lCurr, rCurr)
    while y1 < y2 or y3 < y2:
        print(y1)
        if y1 < y2:
            ridx = (ridx + 1) % len(right)
            rCurr = right[ridx]
            rNext = right[(ridx + 1) % len(right)]
        else:
            lidx = (lidx - 1) % len(left)
            lCurr = left[lidx]
            lNext = left[(lidx - 1) % len(left)]
        y1, y2, y3 = initYVals(lCurr, lNext, lidx, rCurr, rNext, ridx, divider_x)
   
    
    hullTop_idx = (lidx, ridx)
    
    # find bottom connector
    lCurr, lidx = findMax(left)
    rCurr, ridx = findMin(right)
    divider_x = (lCurr[0] + rCurr[0]) / 2
    rNext = right[(ridx + 1) % len(right)]
    lNext = left[(lidx - 1) % len(left)] 
    y1, y2, y3 = initYVals(lCurr, lNext, lidx, rCurr, rNext, ridx, divider_x)

    
    while y1 > y2 or y3 > y2:
        if y1 > y2:
            ridx = (ridx - 1) % len(right)
            rCurr = right[ridx]
            rNext = right[(ridx - 1) % len(right)]
        else:
            lidx = (lidx + 1) % len(left)
            lCurr = left[lidx]
            lNext = left[(lidx + 1) % len(left)]         
        y1, y2, y3 = initYVals(lCurr, lNext, lidx, rCurr, rNext, ridx, divider_x)
    

    hullBot_idx = (lidx, ridx)
    i = hullBot_idx[0]
    newHull = []
    while (i != hullTop_idx[0]):
        newHull.append(left[i])
        i = (i + 1) % len(left)

    i = hullTop_idx[1]
    while (i != hullBot_idx[1]):
        newHull.append(right[i])
        i = (i + 1) % len(right)
    
    return newHull

'''
if there is not enough points for divide and conquer algorithm
use brute force to find convex convex hull 
'''
def naiveComputeHull(points):
    hullSet = set()
    for i in range(0, len(points)-1):
        for j in range(i+1, len(points)):
            if checkSide(i, j, points):
                hullSet.add(points[i])
                hullSet.add(points[j])

    hull = list(hullSet)
    clockwiseSort(hull)

    return hull

''' 
check if all points two one side of given line segment
point1 and point2 form segment
checks rest of points
'''
def checkSide(p1_idx, p2_idx, points):
    test = None
    point1 = points[p1_idx]
    point2 = points[p2_idx]
    for i in range(len(points)):
        if (i == p1_idx or i == p2_idx):
            continue
        
        p = points[i]
        d = (p[0] - point1[0]) * (point2[1] - point1[1]) - \
            (p[1] - point1[1]) * (point2[0] - point1[0])
        
        # first point tested
        if test == None:
            test = d
        
        # check if on same line
        elif (d > 0 and test < 0) or (d < 0 and test > 0):
            return False
    
    return True

'''
Replace the implementation of computeHull with a correct computation 
of the convex hull using the divide-and-conquer algorithm
'''
def divide(points):
    if (len(points) <= 6):
        points = naiveComputeHull(points)
        return points
    
    left = []
    right = []
    half = math.floor(len(points)/2)

    for i in range(0, half):
        left.append(points[i])

    for i in range(half, len(points)):
        right.append(points[i])

    left = divide(left)
    right = divide(right)
    return merge(left, right)

def computeHull(points):
    global DIVIDER_Y
    yMax = max(points, key = lambda x: x[1])
    DIVIDER_Y = (0, yMax[1])
    points = sortByXCoord(points)
    hull = divide(points)
    return hull



























