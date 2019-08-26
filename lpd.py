import numpy as np
import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\Tesseract.exe"

# Read the image file
image = cv2.imread('C:/Users/Deva/Desktop/aa.jpg')


# Image Size
height, width = image.shape[:2]

# Resize the image - change width to 500

image = imutils.resize(image, width=500)

# Display the orginal image

cv2.imshow("Original Image", image)
cv2.waitKey(0)

# RGB to Gray Scale Conversion

gray = cv2.cvtColor (image, cv2.COLOR_BGR2GRAY)
cv2.imshow("1 - Grayscale Coversion", gray)
cv2.waitKey(0)

# Noise removal using Bilateral Filter

gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("2 -Bilateral Filter", gray)
cv2.waitKey(0)

# Find the Edge of grayscale image

edged = cv2.Canny(gray, 170, 200)
cv2.imshow("3 -Canny Edges", edged)
cv2.waitKey(0)

# find contours

cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# create copy of original

img1 = image.copy()
cv2.drawContours(img1, cnts, -1, (0,255,0), 3)
cv2.imshow("4- All Contours", img1)
cv2.waitKey(0)

# sort contours based on their area

cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
NumberPlateCnt = None #currently have no number plate contour

# Top 30 Contours

img2 = image.copy()
cv2.drawContours(img2, cnts, -1, (0,255,0), 3)
cv2.imshow("5- Top 30 contours",img2)
cv2.waitKey(0)

# loop over our contours to find best possible approximate

count = 0
idx = 7
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # print ("approx = ", approx)
    if len(approx) == 4: # select contours with 4 corners
       NumberPlateCnt = approx  # this is our approximate number plate

    # crop and store
    x, y, w, h = cv2.boundingRect(c)   # This will find out the co-ord
    new_img = gray[y:y +h, x:x +w]     # create new image
    cv2.imwrite('C:/Users/Deva/Desktop/' +str(idx) + '.png', new_img) #store new image
    idx+=1

    break

 # Drawing the selected contur
 # print number plate
cv2.drawContours(image, NumberPlateCnt, -1, (0, 255, 0), 3)
cv2.imshow("Final image", image)
cv2.waitKey(0)

Cropped_img_loc = 'C:/Users/Deva/Desktop/7.png'
cv2.imshow("Cropped image ", cv2.imread(Cropped_img_loc))
# use tesseract
text = pytesseract.image_to_string(Cropped_img_loc, lang='eng')
print("Number is : ", text)



