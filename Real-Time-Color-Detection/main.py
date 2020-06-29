import cv2
import  numpy as np





################################################################################################################################
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
###############################################################################################################################








#Track bar portion


def track(a):
    pass
cv2.namedWindow("Track Bars")
cv2.resizeWindow("Track Bars",740,240)

cv2.createTrackbar("Hue Min","Track Bars",0,179,track)#("left Bar Valu Indicator","Window Name",initial value,max value(179 is max value in open cv),function name)
cv2.createTrackbar("Hue Max","Track Bars",15,179,track)
cv2.createTrackbar("Sat Min","Track Bars",0,255,track)
cv2.createTrackbar("Sat Max","Track Bars",255,255,track)
cv2.createTrackbar("Val Min","Track Bars",0,255,track)
cv2.createTrackbar("Val Max","Track Bars",229,255,track)







cap= cv2.VideoCapture(0)#for showing webcam video here only need to put 0 or 1 other camera id
cap.set(3,640)
cap.set(4,480)

while True:
    success,img = cap.read()#read this video by image frame
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)#Converted into HSV
    h_min = cv2.getTrackbarPos("Hue Min","Track Bars")
    h_max = cv2.getTrackbarPos("Hue Max","Track Bars")
    s_min = cv2.getTrackbarPos("Sat Min","Track Bars")
    s_max = cv2.getTrackbarPos("Sat Max","Track Bars")
    v_min = cv2.getTrackbarPos("Val Min","Track Bars")
    v_max = cv2.getTrackbarPos("Val Max","Track Bars")
    print(h_max,h_min,s_max,s_min,v_max,v_min)
    lower =np.array([h_min,s_min,v_min])
    upper =np.array([h_max,s_max,v_max])
    mask =cv2.inRange(imgHSV,lower,upper)
    imgResult =cv2.bitwise_and(img,img,mask=mask)
    finalResult = stackImages(.6,([img,imgHSV],[mask,imgResult]))#Vertically added
    cv2.imshow("Final Result",finalResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):# Window will turn off after pressing 'q'
        break



