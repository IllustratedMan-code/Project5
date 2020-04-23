import math
import random


def Drive(direction, angle):
    x = direction * math.sin(((-angle)/180)*math.pi)*0.001
    y = direction * math.cos(((-angle)/180)*math.pi)*0.001

    return(x, y)


def arrayofboxes(alist, xp, yp):
    locbox = []
    locboy = []
    for i in alist:
        if xp > i[0] and xp < i[0]+0.03:
            locbox.append(i[0])
            locboy.append(i[1])
        if yp > i[1] and yp < i[1]+0.03:
            locbox.append(i[0])
            locboy.append(i[1])
    if locbox != []:
        x = min(locbox, key=lambda x: abs(x-xp))
        y = min(locbox, key=lambda x: abs(x-yp))
        print(abs(x-xp), abs(y-yp))


'''def readbarcode(color, colorlist):
    b = [0, 0, 0, 1]
    w = [1, 1, 1, 1]
    r = [1, 0, 0, 0]
    if colorlist[0] == b and colorlist w]:
        return([], 1)
    elif colorlist == [b, w, b, w]:
        return([], 2)
    elif colorlist == [b, b, w, w]:

    for c in colorlist
        if color == [0, 0, 0, 1] or [1, 1, 1, 1]:

            colorlist.append(color)'''

def createnodematrix(size):
    nodematrix = []
    tempmatrix = []
    for i in range(size[0]):
        for a in range(size[1]):
            tempmatrix.append(1)
        nodematrix.append(tempmatrix)
        tempmatrix = []
    return(nodematrix)


def cnode(currentnode, angle):
    if angle == 0:
        currentnode[0] = currentnode[0] + 1
    elif angle == -90:
        currentnode[1] = currentnode[1] + 1
    elif angle == 180:
        currentnode[0] = currentnode[0] - 1
    elif angle == 90:
        currentnode[1] = currentnode[1] - 1
    return(currentnode)


def nodesense(currentnode, nodematrix):
    seenodes = []
    if currentnode[0] + 1 < len(nodematrix):
        seenodes.append([currentnode[0] + 1, currentnode[1]])

    if currentnode[0] - 1 >= 0:
        seenodes.append([currentnode[0] - 1, currentnode[1]])

    if currentnode[1] + 1 < len(nodematrix[currentnode[0]]):
        seenodes.append([currentnode[0], currentnode[1]+1])

    if currentnode[1]-1 >= 0:
        seenodes.append([currentnode[0], currentnode[1]-1])

    return(seenodes)


def nodepath(target, currentnode, nodematrix):
    if target == currentnode:
        return(currentnode)
    pathlist = []
    newpaths = []
    seenodes = nodesense(currentnode, nodematrix)
    for i in seenodes:
        pathlist.append([currentnode, i])
    foundpath = False

    while foundpath is False:
        for path in pathlist:

            seenodes = nodesense(path[len(path)-1], nodematrix)
            for node in seenodes:
                if node not in path:
                    newpaths.append(path + [node])
                    if node == target:
                        foundpath = False
                        return(path + [node])

        pathlist = newpaths
        newpaths = []

def colorsensor(boxlist, xy, barcodes):
    boxorientation = []
    k = 0
    for i in (boxlist):
        k += 1
        if k <= 4:
            boxorientation.append(0)
        elif k > 4:
            boxorientation.append(1)
            if k >= 8:
                k = 0
    r = 0
    for i in range(len(boxlist)):
        if barcodes[i] != 0:
            #print(barcodes[i])
            if boxorientation[i] == 0:
                r = 0
                for a in barcodes[i]:
                    barx = boxlist[i][0]
                    bary = boxlist[i][1] + r*(0.03/4)
                    barw = boxlist[i][0] + 0.03/5
                    barl = boxlist[i][1] + (r+1)*(0.03/4)
                    if barx <= xy[0] <= barw and bary <= xy[1] <= barl:
                        #print(i)
                        return [a, i]
                    r += 1

            else:
                r = 3
                for a in barcodes[i]:
                    barx = boxlist[i][0] + 0.03
                    bary = boxlist[i][1] + r*(0.03/4)
                    barw = boxlist[i][0] + 0.03 - 0.03/5
                    barl = boxlist[i][1] + (r+1)*(0.03/4)
                    if barw <= xy[0] <= barx and bary <= xy[1] <= barl:
                        #print(i)
                        return [a, i]

                    r -= 1


def createbarcode():
    color = random.randint(0, 3)
    if color == 0:
        a = 0
        b = 1
        c = 1
        d = 1
    if color == 1:
        a = 0
        b = 1
        c = 0
        d = 1
    if color == 2:
        a = 0
        b = 0
        c = 1
        d = 1
    if color == 3:
        a = 0
        b = 1
        c = 1
        d = 0
    return([[a, a, a, 1], [b, b, b, 1], [c, c, c, 1], [d, d, d, 1]])


# distance sensor is fully functional, as long as the car moves in 90d
# returns color and distance to avoid performance issues
# increments. xp, yp are coordinates of the car
def distancesensor(boxlist, xp, yp, angle, barcodes):
    thetalist = []
    intersections = []
    distances = []
    for i in boxlist:
        # corner 1-4 of box in boxlist
        c1 = (math.atan2((i[1]-yp), (i[0]-xp)))

        c2 = (math.atan2((i[1])-yp, (((i[0]+0.03))-xp)))

        c3 = (math.atan2(((i[1]+0.03)-yp), ((i[0]+0.03)-xp)))
        c4 = (math.atan2(((i[1]+0.03)-yp), (i[0])-xp))

        ma = min([c1, c2, c3, c4])
        Ma = max([c1, c2, c3, c4])

        if Ma-ma > math.pi:
            ma = ma + 2*math.pi

        if ((angle)/180)*math.pi >= min(Ma, ma) and ((angle)/180)*math.pi <= max(Ma, ma):
            # distance from center of car to cube corner
            thetalist.append((((xp)-i[0])**(2)+(yp-i[1])**(2))**.5)

            # calculates the slope
            m = round(math.tan(math.radians(angle)), 4)
            # calculates the y intercept
            b = yp - m*xp
            # x and y coordinates of the box
            x = i[0]
            y = i[1]
            #
            if abs(m) > 1.6*10**16:
                s2 = [xp, y]

                s4 = [xp, y+0.03]
                d2 = (((xp - s4[0])**2) + ((yp-s4[1])**2))**0.5
                d1 = (((xp - s2[0])**2) + ((yp-s2[1])**2))**0.5
                si = [[0, 0], s2, [0, 0], s4]
                for i in si:
                    intersections.append(i)
                li = [10, d1, 10, d2]
                for i in li:
                    distances.append(round(i, 4))
            elif m == 0:
                s1 = [x, yp]
                d1 = (((xp-s1[0])**2) + ((yp-s1[1])**2))**0.5
                s3 = [x+0.03, yp]
                d2 = (((xp-s3[0])**2) + ((yp-s3[1])**2))**0.5
                si = [s1, [0, 0], s3, [0, 0]]
                for i in si:
                    intersections.append(i)
                li = [d1, 10, d2, 10]
                for i in li:
                    distances.append(round(i, 4))

            else:
                # if there is time, fill in with distance equations
                pass

    if distances != []:

        xy = intersections[distances.index(min(distances))]
        color = colorsensor(boxlist, xy, barcodes)
        #print("this is the color{0}".format(color))
        return(min(distances), color, xy)
