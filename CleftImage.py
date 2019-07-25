from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ImageTk
import numpy as np
import math
import PIL.ImageFont as ImageFont
np.set_printoptions(precision = 2)
MINFLOAT = 0.00001      #10^-5

counter = 0

def GetPointsListUsingTkinter():
    pointslist = [[0,0]]*6
    root = Tk()
    frame = Frame(root, bd = 2, relief = SUNKEN)
    frame.grid_rowconfigure(0, weight = 1)
    frame.grid_columnconfigure(0, weight = 1)
    xscroll = Scrollbar(frame, orient = HORIZONTAL)
    xscroll.grid(row = 1, column = 0, sticky = E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1,sticky = N+S)
    canvas = Canvas(frame, bd = 0, xscrollcommand = xscroll.set, yscrollcommand = yscroll.set)
    canvas.grid(row=0, column=0,sticky = N+S+E+W)
    xscroll.config(command = canvas.xview)
    yscroll.config(command = canvas.yview)
    frame.pack(fill=BOTH, expand = 1)

    #Adding the image
    File = askopenfilename(parent = root, initialdir = "~", title = "Choose and image")
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img, anchor = "nw")
    canvas.config(scrollregion = canvas.bbox(ALL))

    def printcoords(event):
        global counter
        pointslist[counter] = [event.x, event.y]
        counter+=1
        print(event.x, event.y)

    #mouseclick event
    canvas.bind("<Button 1>", printcoords)
    Button(root, text = "Close Window", command = root.destroy).pack()
    root.mainloop()

    print("Pointslist: {0}".format(pointslist))
    return pointslist

def getDist(pt1, pt2):
    xdist = pt1[0]-pt2[0]
    ydist = pt1[1] - pt2[1]
    xdist = xdist*xdist
    ydist = ydist*ydist
    distance = math.sqrt(xdist+ydist)
    return distance

def getDistFromLine(line=[0,0,0], pt = [0,0]):
    numerator = abs(line[0]*pt[0]+line[1]*pt[1]+line[2])
    denominator = math.sqrt(line[0]**2+line[1]**2)
    #print(numerator, denominator)
    if(denominator==0):
        denominator = 1
    return (numerator*1.0)/denominator

def getSlope(pt1, pt2):
    ydiff = pt2[1]-pt1[1]
    xdiff = pt2[0]-pt1[0]
    if(ydiff == 0): 
        ydiff = MINFLOAT
    if(xdiff == 0): 
        xdiff = MINFLOAT

    return (ydiff*1.0)/xdiff


def getLineFromTwoPoints(pt1, pt2):
    m = getSlope(pt1, pt2)
    a = m
    b = -1
    c = -m*pt1[0]+pt1[1]
    print("Line: {0:0.1f}x+{1:0.1f}y+{2:0.1f}c=0".format(a,b,c))
    return [a, b, c]

def findYCoordinate(line, x):
    y = (-1.0*line[2]-x*line[0])/line[1]
    return y


def findXCoordinate(line, y):
    x = (-1.0*line[2]-y*line[1])/line[0]
    return x

def findPtAtDistOnLineSegment(line, pt, targetDistance, segStart, segEnd):
    eps = 2
    xstart = min(segStart[0], segEnd[0])
    xend = max(segStart[0], segEnd[0])
    ystart = min(segStart[1], segEnd[1])
    yend = max(segStart[1], segEnd[1])

    for x in range(xstart, xend):
        y = findYCoordinate(line, x)
        dist = getDist(pt, [x,y])
        print("Dist: {0}, {1}, {2}".format(dist, targetDistance, abs(targetDistance-dist)))
        if(abs(targetDistance-dist)<eps):
            return [x,y]

    #If not able to find distance by iterative over x axis
    for y in range(ystart, yend):
        x = findXCoordinate(line, y)
        dist = getDist(pt, [x,y])
        if(abs(targetDistance-dist)<eps):
            return [x,y]

    return [0,0]

def getAngleBetweenTwoLines(line1,line2):
    m1 = (-1.0*line1[0]/line1[1])
    m2 = (-1.0*line2[0]/line2[1])
    tantheta = abs((m2-m1)/(1+m1*m2))
    theta = math.degrees(math.atan(tantheta))
    #print(m1, m2, tantheta, theta)
    return theta



#Draw points on the image
r = 1           #radius of points
width = 2      #line width
NUMPOINTS = 6
# x1,y1 = 1670,1270
# x2,y2 = 1880,1350
# x3,y3 = 1880,1430
# x4,y4 = 1750,1440
# x5,y5 = 1690,1360
# x6,y6 = 1900,1360

# pt1 = [1660, 1260, 1680, 1280]
# pt2 = [1870, 1340, 1890, 1360]
# pt3 = [1870,1420,1890,1440]

pointslist = [[611, 844], [603, 795], [588, 798], [590, 819], [598, 834], [597, 797]] #GetPointsListUsingTkinter()
#pointslist = GetPointsListUsingTkinter()
x1,y1 = pointslist[0]
x2,y2 = pointslist[1]
x3,y3 = pointslist[2]
x4,y4 = pointslist[3]
x5,y5 = pointslist[4]
x6,y6 = pointslist[5]
ImageName = "child2.jpg"
ResultsDir = "results"

line_color = "yellow"
font_size = 11
font = ImageFont.truetype("Arial.ttf", font_size)


#draw on image
ptlarge = Image.open(ImageName).convert("RGB")
ptdraw = ImageDraw.Draw(ptlarge)
ptdraw.ellipse([x1-r, y1-r, x1+r, y1+r], fill = "red")
ptdraw.ellipse([x2-r, y2-r, x2+r, y2+r], fill = "red")
ptdraw.ellipse([x3-r, y3-r, x3+r, y3+r], fill = "red")
ptdraw.ellipse([x4-r, y4-r, x4+r, y4+r], fill = "red")
ptdraw.ellipse([x5-r, y5-r, x5+r, y5+r], fill = "red")
ptdraw.ellipse([x6-r, y6-r, x6+r, y6+r], fill = "red")

ptlarge.show()
ptlarge.save(ResultsDir + "/" + ImageName + "Points.jpg")



#Coordinate Geometry
philtralLen = getDist([x1,y1],[x2,y2])
print("Length of normal philtral column: {0:0.2f}".format(philtralLen))
ptdraw.line([x1,y1,x2,y2], fill=line_color, width = width)
midLine = getLineFromTwoPoints([x5,y5],[x6,y6])
ptdraw.line([x5,y5,x6,y6], fill=line_color, width=width)
#ptlarge.show()
cleftLen = getDist([x3,y3],[x4,y4])
deficitLen = philtralLen - cleftLen
print("Cleft side column length: {0:0.2f}".format(cleftLen))
print("Length deficit: {0:0.2f}".format(deficitLen))
distFromMidLine = getDistFromLine(midLine, [x3,y3])
print("Perpendicular distance from midline: {0:0.2f}".format(distFromMidLine))


#Find target point on line
targetPtOnLine = findPtAtDistOnLineSegment(midLine, [x3,y3], deficitLen, [x5,y5], [x6, y6])
backCutLine = getLineFromTwoPoints([x3,y3], targetPtOnLine)
x7,y7 = targetPtOnLine

ptdraw.line([x3,y3,targetPtOnLine[0], targetPtOnLine[1]], fill=line_color, width=width)



#Find angle betweeen C flap line and back cut line
CFlapLine = getLineFromTwoPoints([x4,y4],[x3,y3])
BackCutAngle = getAngleBetweenTwoLines(CFlapLine, backCutLine)
AdvancementFlapAngle = getAngleBetweenTwoLines(backCutLine, midLine)

ptdraw.line([x3,y3,x4,y4], fill=line_color, width=width)
ptdraw.arc([1820, 1380, 1920, 1480], start = 180, end = 180+BackCutAngle, fill="white", width = width)
print("BackCutAngle: {0:0.1f} degrees".format(BackCutAngle))
print("Rotation angle: {0:0.1f}".format(AdvancementFlapAngle))

ptdraw.text((x1+30, y1+40), "Back cut angle {0:0.2f} degrees".format(BackCutAngle), font = font)
ptdraw.text((x1+30, y1+60), "Rotation angle {0:0.2f} degrees".format(AdvancementFlapAngle), font = font)
ptdraw.text((x1,y1), "1", font = font)
ptdraw.text((x2,y2), "2", font = font)
ptdraw.text((x3,y3), "3", font = font)
ptdraw.text((x4,y4), "4", font = font)
ptdraw.text((x5,y5), "5", font = font)
ptdraw.text((x6,y6), "6", font = font)
ptdraw.text((targetPtOnLine[0],targetPtOnLine[1]),"7",font=font)

ptdraw.ellipse([x7-r, y7-r, x7+r, y7+r], fill = "red")

ptlarge.show()
ptlarge.save(ResultsDir + "/" + ImageName + "Lines.jpg")


