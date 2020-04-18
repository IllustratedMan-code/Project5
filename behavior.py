import math


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


def colorsensor(boxlist, xy):

    pass

# distance sensor is fully functional, as long as the car moves in 90d
# increments
def distancesensor(boxlist, xp, yp, angle):
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
            thetalist.append((((xp)-i[0])**(2)+(yp-i[1])**(2))**.5)
            m = round(math.tan(math.radians(angle)), 4)
            b = yp - m*xp
            x = i[0]
            y = i[1]
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
        return(min(distances))
