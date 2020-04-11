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


def distancesensor(boxlist, xp, yp, angle):
    thetalist = []
    for i in boxlist:

        c1 = (math.atan2((i[1]-yp), (i[0]-xp)))

        c2 = (math.atan2((i[1])-yp, (((i[0]+0.03))-xp)))

        c3 = (math.atan2(((i[1]+0.03)-yp), ((i[0]+0.03)-xp)))
        c4 = (math.atan2(((i[1]+0.03)-yp), (i[0])-xp))
        #print(c1)
        ma = min([c1, c2, c3, c4])
        Ma = max([c1, c2, c3, c4])
        if Ma-ma > math.pi:
            ma = ma + 2*math.pi
        if ((angle)/180)*math.pi >= min(Ma, ma) and ((angle)/180)*math.pi <= max(Ma, ma):
            thetalist.append((((xp)-i[0])**(2)+(yp-i[1])**(2))**.5)
            #print(angle, c1, c2, c3, c4)
    if thetalist != []:
        #print(min(thetalist))
        return(min(thetalist))
