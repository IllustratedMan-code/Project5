import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

def Warehouse(fig, ax):
    zeros = [[255 for i in range(1,103)] for j in range(-6,103)]		#Create white square
    ax.imshow( zeros,cmap='gray', vmin=0, vmax=255, origin='lower')

    # Zone A Shelves
    rect = patches.Rectangle((12,12),36,12,linewidth=1,edgecolor='black',facecolor='none')
    ax.add_patch(rect)
    rect = patches.Rectangle((12,36),36,12,linewidth=1,edgecolor='black',facecolor='none')
    ax.add_patch(rect)
    # Zone B Shelves
    rect = patches.Rectangle((60,12),36,12,linewidth=1,edgecolor='black',facecolor='none')
    ax.add_patch(rect)
    rect = patches.Rectangle((60,36),36,12,linewidth=1,edgecolor='black',facecolor='none')
    ax.add_patch(rect)
    # Zone C Shelves
    rect = patches.Rectangle((12,60),36,12,linewidth=1,edgecolor='black',facecolor='none')
    ax.add_patch(rect)
    rect = patches.Rectangle((12,84),36,12,linewidth=1,edgecolor='black',facecolor='none')
    ax.add_patch(rect)
    # Zone D Shelves
    rect = patches.Rectangle((60,60),36,12,linewidth=1,edgecolor='black',facecolor='none')
    ax.add_patch(rect)
    rect = patches.Rectangle((60,84),36,12,linewidth=1,edgecolor='black',facecolor='none')
    ax.add_patch(rect)
    #Zone A and C Boxes - place randomly on shelves
    #Designate Locations and Bar Codes in Matrix M
    M = [[0 for i in range(0,103)] for j in range(0,103)]
    Barcode = [[1, 2, 2, 2],[1, 2, 1, 2],[1, 1, 2, 2],[1, 2, 2, 1]]
    y_list = [12,36,60,84]
    for y in y_list:
        x = [random.randrange(12,44,1) for i in range(2)]
        while ((x[0]-x[1])**2)**0.5 < 4:
            x = [random.randrange(12,44,1) for i in range(2)]
        code1 = random.randint(0,3)
        for k in range(4):
            M[y][x[0]+k] = 10 
            M[y+1][x[0]+k] = Barcode[code1][k]
        code2 = random.randint(0,3)
        for k in range(4):
            M[y][x[1]+k] = 10
            M[y+1][x[1]+k] = Barcode[code2][k]
        for i in x:
            rect = patches.Rectangle((i,y),4,4,linewidth=1,edgecolor='black',facecolor='gray')
            ax.add_patch(rect)
    y_list = [24,48,72,96]
    for y in y_list:
        x = [random.randrange(12,44,1) for i in range(2)]
        while ((x[0]-x[1])**2)**0.5 < 4:
            x = [random.randrange(12,44,1) for i in range(2)]
        code1 = random.randint(0,3)
        for k in range(4):
            M[y][x[0]+k] = 10 
            M[y-1][x[0]+k] = Barcode[code1][3-k]
        code2 = random.randint(0,3)
        for k in range(4):
            M[y][x[1]+k] = 10
            M[y-1][x[1]+k] = Barcode[code2][3-k]
        for i in x:
            rect = patches.Rectangle((i,y-4),4,4,linewidth=1,edgecolor='black',facecolor='gray')
            ax.add_patch(rect)
    #Zone B and D Boxes - place randomly on shelves
    #Designate Locations and Bar Codes in Matrix M       
    y_list = [12,36,60,84]
    for y in y_list:
        x = [random.randrange(60,92,1) for i in range(2)]
        while ((x[0]-x[1])**2)**0.5 < 4:
            x = [random.randrange(60,92,1) for i in range(2)]
        code1 = random.randint(0,3)
        for k in range(4):
            M[y][x[0]+k] = 10 
            M[y+1][x[0]+k] = Barcode[code1][k]
        code2 = random.randint(0,3)
        for k in range(4):
            M[y][x[1]+k] = 10
            M[y+1][x[1]+k] = Barcode[code2][k]
        for i in x:
            rect = patches.Rectangle((i,y),4,4,linewidth=1,edgecolor='black',facecolor='gray')
            ax.add_patch(rect)
    y_list = [24,48,72,96]
    for y in y_list:
        x = [random.randrange(60,92,1) for i in range(2)]
        while ((x[0]-x[1])**2)**0.5 < 4:
            x = [random.randrange(60,92,1) for i in range(2)]
        code1 = random.randint(0,3)
        for k in range(4):
            M[y][x[0]+k] = 10 
            M[y-1][x[0]+k] = Barcode[code1][3-k]
        code2 = random.randint(0,3)
        for k in range(4):
            M[y][x[1]+k] = 10
            M[y-1][x[1]+k] = Barcode[code2][3-k]
        for i in x:
            rect = patches.Rectangle((i,y-4),4,4,linewidth=1,edgecolor='black',facecolor='gray')
            ax.add_patch(rect)

    return M, fig, ax

