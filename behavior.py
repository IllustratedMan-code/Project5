import math


def Drive(direction, angle):
    x = -direction * math.sin(((angle)/180)*math.pi)*0.001
    y = -direction * math.cos(((angle)/180)*math.pi)*0.001

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
        c1 = math.atan2((i[0]-xp), (i[1]-yp))
        c2 = math.atan2(((i[0]+0.03)-xp), (i[1])-yp)
        c3 = math.atan2(((i[0]+0.03)-xp), ((i[1]+0.03)-yp))
        c4 = math.atan2((i[0])-xp, ((i[1]+0.03)-yp))

        if ((angle-90)/180)*math.pi > min([c1, c2, c3, c4]) and ((angle-90)/180)*math.pi < max([c1, c2, c3, c4]):
            thetalist.append((((xp)-i[0])**(2)+(yp-i[1])**(2))**.5)

    if thetalist != []:

        return(min(thetalist))
