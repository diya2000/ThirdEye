#file to open up webcamp and display images and supply to browser
import cv2
from scipy.spatial import distance as dist
face_model=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
class VideoCamera(object):
    # getting the camera
    def __init__(self):
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    # incase user releases
    def __del__(self):
        self.cap.release()
    # duplicate function for releasing the camera
    def endme(self):
        self.cap.release()
    def get_frame(self):
        status, photo= self.cap.read()
        
        face_cor = face_model.detectMultiScale(photo)
      
        l = len(face_cor)
        photo = cv2.putText(photo, str(len(face_cor))+" Face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,1, ( 255,0,         0) , 2, cv2.LINE_AA)
        stack_x = []
        stack_y = []
        stack_x_print = []
        stack_y_print = []
        stack_x_print1 = []
        stack_y_print1 = []
        global D
        global D1
        global D2
        global D3
        D=0
        D=0
        D=0
        D=0
        # getting the face coordinates
        
        if len(face_cor) == 0:
            pass
        else:
            for i in range(0,len(face_cor)):
                x1 = face_cor[i][0]
                y1 = face_cor[i][1]
                x2 = face_cor[i][0] + face_cor[i][2]
                y2 = face_cor[i][1] + face_cor[i][3]
        # stack arrangement and creation
                mid_x = int((x1+x2)/2)
                mid_y = int((y1+y2)/2)
                stack_x.append(mid_x)
                stack_y.append(mid_y)
                stack_x_print.append(mid_x)
                stack_y_print.append(mid_y)
                stack_x_print1.append(mid_x)
                stack_y_print1.append(mid_y)
        
                photo = cv2.circle(photo, (mid_x, mid_y), 3 , [255,0,0] , -1)
                photo = cv2.rectangle(photo , (x1, y1) , (x2,y2) , [0,255,0] , 2)
            
            # if len(face_cor) == 0:
            #   continue
                
            if len(face_cor) == 2:
                D = int(dist.euclidean((stack_x.pop(), stack_y.pop()), (stack_x.pop(), stack_y.pop())))
                photo = cv2.line(photo, (stack_x_print.pop(), stack_y_print.pop()), (stack_x_print.pop(), stack_y_print.pop()), [0,255,0], 2)
                
            elif len(face_cor) == 3:
                x1=stack_x.pop()
                y1= stack_y.pop()
                x2=stack_x.pop()
                y2=stack_y.pop()
                x3=stack_x.pop()
                y3=stack_y.pop()
                D1=int(dist.euclidean((x1,y1), (x2,y2)))
                D2=int(dist.euclidean((x1,y1), (x3,y3)))
                D3=int(dist.euclidean((x2,y2), (x3,y3)))
                x11=stack_x_print.pop()
                y11=stack_y_print.pop()
                x22=stack_x_print.pop()
                y22=stack_y_print.pop()
                x33=stack_x_print.pop()
                y33=stack_y_print.pop()
                x111=stack_x_print1.pop()
                y111=stack_y_print1.pop()
                x222=stack_x_print1.pop()
                y222=stack_y_print1.pop()
                x333=stack_x_print1.pop()
                y333=stack_y_print1.pop()
                photo = cv2.line(photo, (x11,y11), (x22,y22), [0,255,0], 2)
                photo = cv2.line(photo, (x11,y11), (x33,y33), [0,255,0], 2)
                photo = cv2.line(photo, (x33,y33), (x22,y22), [0,255,0], 2)
                
            else:
                D = 0
                D1=0
                D2=0
                D3=0
            # detection the faces and if the distancing is followed
            if D<250 and D!=0 and len(face_cor) == 2:
                photo = cv2.putText(photo, "!!MOVE AWAY!!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,2, [0,0,255] , 4)
                photo = cv2.line(photo, (stack_x_print1.pop(), stack_y_print1.pop()), (stack_x_print1.pop(), stack_y_print1.pop()), [0,0,255], 2)

            
            # if 3 people detected
            if D1<250 and D1!=0 and len(face_cor) == 3:
                       photo = cv2.putText(photo, "!!MOVE AWAY!!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,2, [0,0,255] , 4)
                       photo = cv2.line(photo, (x111, y111), (x222,y222), [0,0,255], 2)
           
            if D2<250 and D2!=0 and len(face_cor) == 3:
                       photo = cv2.putText(photo, "!!MOVE AWAY!!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,2, [0,0,255] , 4)
                       photo = cv2.line(photo, (x111, y111), (x333,y333), [0,0,255], 2)
            
            if D3<250 and D3!=0  and len(face_cor) == 3:
                       photo = cv2.putText(photo, "!!MOVE AWAY!!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,2, [0,0,255] , 4)
                       photo = cv2.line(photo, (x333, y333), (x222,y222), [0,0,255], 2)
         
       
            
    
        # resizing according to browser
        photo = cv2.resize(photo, (900,500))
       # converting the image to the bytes
        status, jpeg =cv2.imencode('.jpg', photo)
         # sending the bytes file to the __init__.py
        return jpeg.tobytes()
