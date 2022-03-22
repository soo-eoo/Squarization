import cv2
from matplotlib import pyplot as plt
import numpy as np
import os

print('***** type name of image file and name of text input. ex) image.png text.txt')
print('***** you can use sample image (1) dog.png, (2) heart.png (3) map.png')
print('***** you can use sample text inputText.txt')
imageName, inputText = input().split()
print('***** image file:', imageName, '/ text file:', inputText)
#           Change Here         #
# imageName = 'map2.png'
#           Change Here         #

image = cv2.imread(imageName)
image_gray = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)

b, g, r = cv2.split(image)
image2 = cv2.merge([r, g, b])


# plt.imshow(image2)
plt.xticks([])
plt.yticks([])
# plt.show()


blur = cv2.GaussianBlur(image_gray, ksize=(5,5), sigmaX=0)
ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
edged = cv2.Canny(blur, 50, 200)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
total = 0

contours_xy = np.array(contours)

x_min, x_max = 0,0
value = list()
for i in range(len(contours_xy)):
    for j in range(len(contours_xy[i])):
        value.append(contours_xy[i][j][0][0]) #네번째 괄호가 0일때 x의 값
        x_min = min(value)
        x_max = max(value)

# y의 min과 max 찾기
y_min, y_max = 0,0
value = list()
for i in range(len(contours_xy)):
    for j in range(len(contours_xy[i])):
        value.append(contours_xy[i][j][0][1]) #네번째 괄호가 0일때 x의 값
        y_min = min(value)
        y_max = max(value)
# print(x_min, x_max, y_min, y_max)

x = x_min
y = y_min
w = x_max-x_min
h = y_max-y_min

img_trim = image[y:y+h, x:x+w]
cv2.imwrite('org_trim.jpg', img_trim)
org_image = cv2.imread('org_trim.jpg')

contourArea = float(cv2.contourArea(contours[0]))


# -*- coding: utf-8 -*- 

import re

def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]。：.', '', readData)
    return text


#           Change Here         #
with open(inputText, mode="r") as file:
    lines = file.readlines()
#           Change Here         #


lines = ' '.join(lines)
lines = lines.replace(" ", "")
lines = lines.replace('\n', "")
lines = lines.replace('：', "")

lines = lines.replace('，', "")
lines = lines.replace(',', "")
lines = lines.replace('一', "")
lines = lines.replace('>', "")
lines = lines.replace('?', "")
lines = lines.replace('>', "")
lines = lines.replace('”', "")
lines = lines.replace('“', "")

lines = lines.replace('\'', "")
lines = lines.replace('\'', "")

#full stop
lines = lines.replace('.', "")
lines = lines.replace('。', "")
lines = cleanText(lines)


# print(lines)
# print(len(lines))


numLetter = len(lines)
linesList = list(lines)

import math
size = round(math.sqrt(float(contourArea)/float(numLetter)), 3)
minSize = float(0)
maxSize = float(size*2)

# print(numLetter, size, minSize, maxSize)
# print("required number of letters is ", numLetter, ", and initial size is ", size)

breaks = False
prevCount = -1



#           Change Here         #
direction = 'center'
#           Change Here         #


#case 1: direction == left-top
if direction == 'left-top':
    while(True):
        points = []
        pointsOutside = []
        k1 = math.ceil(float(w)/size)
        k2 = math.ceil(float(h)/size)
        count = 0

        for ix in range(1, k1):
            for iy in range(1, k2):
                point = ((float(ix) - 0.5)*size + float(x_min), (float(iy) - 0.5)*size+ float(y_min))
                if (cv2.pointPolygonTest(contours[0], point, True) >= w * 0.03):
                    count += 1
                    points.append(point)
                
                elif (cv2.pointPolygonTest(contours[0], point, False) == 0):
                    pointsOutside.append(point)

            if(count > numLetter):
                # print("count number(", count, ") is more than the number of letters: ", numLetter)
                minSize = size
                size = (float(maxSize) + float(minSize))/float(2)
                # print("updated size(min, max, size): ", minSize, maxSize, size)

                if(minSize == size):
                    breaks = True
                    break
                break
                
            if(breaks):
                break

        if(breaks):
            break

        if(prevCount == count):
            break

        if(count < numLetter):
            prevCount = count
            # print("count number(", count, ") is less than the number of letters: ", numLetter)
            maxSize = size
            size = (float(maxSize) + float(minSize))/float(2)
            # print("updated size(min, max, size): ", minSize, maxSize, size)


        if(count == numLetter):
            break

#case2 direction == center
elif direction == 'center':
    while(True):
        points = []
        pointsOutside = []
        k1 = math.ceil(float(w)/size)
        k2 = math.ceil(float(h)/size)
        count = 0

        rowRangeList = list(range(1, k1))
        colRangeList = list(range(1, k2))



        rowRangeList = sorted(rowRangeList, key = lambda x : abs(x-round(k1/2))%round(k1/2))
        colRangeList = sorted(colRangeList, key = lambda x : abs(x-round(k2/2))%round(k2/2))

        #print(k1, rowRangeList)
        #print(k2, colRangeList)

        for ix in rowRangeList:
            for iy in colRangeList:
                point = ((float(ix))*size + float(x_min), (float(iy))*size+ float(y_min))
                #print(point, cv2.pointPolygonTest(contours[0], point, False))
                if (cv2.pointPolygonTest(contours[0], point, True) >= w * 0.03):
                    count += 1
                    points.append(point)
                
                elif (cv2.pointPolygonTest(contours[0], point, False) == 0):
                    pointsOutside.append(point)

            if(count > numLetter):
                # print("count number(", count, ") is more than the number of letters: ", numLetter)
                minSize = size
                size = (float(maxSize) + float(minSize))/float(2)
                # print("updated size(min, max, size): ", minSize, maxSize, size)

                if(minSize == size):
                    breaks = True
                    break
                break
                
            if(breaks):
                # print('break1')
                break

        if(breaks):
            # print('break2')
            break

        if(prevCount == count):
            # print('break3')
            break

        if(count < numLetter):
            prevCount = count
            # print("count number(", count, ") is less than the number of letters: ", numLetter)
            maxSize = size
            size = (float(maxSize) + float(minSize))/float(2)
            # print("updated size(min, max, size): ", minSize, maxSize, size)


        if(count == numLetter):
            # print('break4')
            break


# print(size)

# print(count)

newPoints = []
newPointsOutside = []

#print(points)

for point in points:
    newpoint = list(point)
    newpoint.append(cv2.pointPolygonTest(contours[0], point, True))
    newPoints.append(newpoint)

for point in pointsOutside:
    newpoint = list(point)
    newpoint.append(abs(cv2.pointPolygonTest(contours[0], point, True)))
    newPointsOutside.append(newpoint)


# print(len(newPoints), len(newPointsOutside))
diff = count-numLetter
# print("count, numLetter, diff: ", count, numLetter, diff)

newPoints = sorted(newPoints, key = lambda x : x[2])
newPointsOutside = sorted(newPointsOutside, key = lambda x : x[2])

indexs = []


while(True):
    print("Start!")
    indexs = []
    count = 0

    # print(diff)
    if(diff > 0):
        newPoints = sorted(newPoints, key = lambda x : x[2])
        newPointsOutside = sorted(newPointsOutside, key = lambda x : x[2])
        for cnt in range(diff):
            newPointsOutside.append(newPoints[count])
            del newPoints[count]
            count += 1

    elif(diff < 0):
        newPoints = sorted(newPoints, key = lambda x : x[2])
        newPointsOutside = sorted(newPointsOutside, key = lambda x : x[2])
        for cnt in range(-diff):
            newPoints.append(newPointsOutside[count])
            del newPointsOutside[count]
            count += 1

    # print("length of newPoints: ", len(newPoints))

    for point in newPoints:
        ix = round(float(point[0])/float(size)+0.5)
        iy = round(float(point[1])/float(size)+0.5)
        #print("point, ix, iy: ", point, ix, iy)
        indexs.append([ix, iy])
    
    indexs = list(set(map(tuple, indexs)))
    diff = len(indexs) - numLetter
    # print("length of indexs:", len(indexs))

    if(diff == 0):
        break


#print(indexs)


from PIL import ImageFont, ImageDraw, Image

#font coloring
fontColor = (255, 0, 0)



#print(indexs)
indexs = sorted(indexs, key = lambda x : x[0])
indexs = sorted(indexs, key = lambda x : x[1])

finalImage = image

h, w, c = finalImage.shape

originalSize = size

#if resize
resizing = True
if resizing:
    resizingRate = 2048/w
    w = w*resizingRate
    h = h*resizingRate
    size = size*resizingRate


newImage = Image.new("RGBA", (round(w*1.2), round(h*1.2)), color = (255, 255, 255))
draw = ImageDraw.Draw(newImage)

fontSize = round(size*float(4/3)*0.5)

font = cv2.FONT_HERSHEY_SIMPLEX
fontPath = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
drawFont = ImageFont.truetype(fontPath, fontSize)
fontScale = 2
color = (0, 0, 0)
thickness = 0.3

# print(indexs)


for i, (index, letter) in enumerate(zip(indexs, linesList)):
    #print("i, index[0], index[1], letter: ", i, index[0], index[1], letter)
    #print(letter)

    startPoint = tuple([round(float(index[0]-1)*originalSize), round(float(index[1]-1)*originalSize)])
    endPoint = tuple([round(float(index[0])*originalSize), round(float(index[1])*originalSize)])

    setPoint = (round(w*0.1 + float(index[0]-1)*size), round(h*0.1 + float(index[1])*size))

    cv2.rectangle(image, startPoint, endPoint, (0, 255, 0), 1)
    draw.text(setPoint, letter, font=drawFont, fill=fontColor)
    


cv2.imwrite('final_image.png', image)
newImage.show()
newImage.save('final_letter_image.png')
#cv2.imshow('final_image', newImage)
cv2.waitKey(0)
cv2.destroyAllWindows()

