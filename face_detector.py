import cv2
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

img=cv2.imread("Abhishek_pic.png")
grey_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces=face_cascade.detectMultiScale(grey_img,scaleFactor=1.28,minNeighbors=4)
print(faces)
for x,y,w,h in faces:
    img=cv2.rectangle(img,(x,y),((x+w),(y+h)),(0,255,0),3)

# resize_img=cv2.resize(img,(int(img.shape[1]),int(img.shape[0])))

# cv2.imshow("grey",resize_img)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

