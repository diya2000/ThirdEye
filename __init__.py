#bytes.io
import os
from flask_sqlalchemy import SQLAlchemy
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
from camera import VideoCamera
from flask import Flask, render_template,url_for, Response, request
import smtplib
from datetime import datetime

app=Flask(__name__,static_folder='static',
            template_folder='templates')


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db= SQLAlchemy(app)

# this is a model of the Contact table
# add the table rows according to the need 
class Contact(db.Model):
    __tablename__ = "customers" 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String,nullable=False)

    email = db.Column(db.String)
    purpose = db.Column(db.String)
    date_created= db.Column(db.DateTime, default=datetime.utcnow
    )
    def __repr__(self):
        return '<Customer %r>' % self.id # self increasing attribute
# smtp mail service
def sendEmail(receiver,subject,message):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("send_email","password")
    server.sendmail("address_of_user",receiver,message)
    
    print("succesful")


# making the predection of the images received by user 
# classification of the images according to the classes
def detect_and_predict_mask(frame, faceNet, maskNet):

	
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	
	faceNet.setInput(blob)
	detections = faceNet.forward()
	print(detections.shape)

	faces = []
	locs = []
	preds = []

	for i in range(0, detections.shape[2]):
		
		confidence = detections[0, 0, i, 2]

		
		if confidence > 0.5:
		
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

		
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

		
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	if len(faces) > 0:
	
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	
	return (locs, preds)
# the main function for the face mask detection 
# using the predection method
def flaskfun():
    
    cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    prototxtPath = r"face_detector\deploy.prototxt"
    weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
    maskNet = load_model("mask_detector.model")
    print("[INFO] starting video stream...")
    global vs
    vs = VideoStream(src=0).start()

    while(valueCam==0):
	
        frame = vs.read()
        
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            cv2.putText(frame, label, (startX, startY - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        frame = cv2.resize(frame, (840,560))
        status, jpeg =cv2.imencode('.jpg', frame)
        key = cv2.waitKey(1) & 0xFF
        ff=jpeg.tobytes()
        
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + ff + b'\r\n\r\n')
        


    cv2.destroyAllWindows()
    cap.release()
    print("going off")
    vs.stop()
		
# setting the routes for the page using get and post
@app.route("/", methods=['GET', 'POST'])

def index():
    task=0
    global valueCam
    valueCam=0
    if request.method == 'POST':
        print("its post")
        # when distancing tracker is used
        if request.form.get("submit_a"):
            pass
       # when distancing tracker is closed
        if request.form.get("submit_b"):
            pass
        # when the mask detecter is clicked 
        if request.form.get("maskButton"):
            pass
        # when the mask detecter is closed 
        if request.form.get("maskOff"):
            valueCam = 1
            pass
        # when the contact us page is clicked
        if request.form.get("cu"):
            print("innnn")
            name= request.form.get('name')
            email = request.form.get('email')
            purpose=""
            if request.form.get('App'):
	            purpose+=" App Design,"
            if request.form.get('Graphic'):
	            purpose+=" Graphic Design,"
         
            if request.form.get('IOT'):
	            purpose+=" IOT Setting,"
            if request.form.get('CCTV'):
	            purpose+=" CCTV Setting,"
            if request.form.get('Mask'):
	            purpose+=" Mask Detection,"
            if request.form.get('Social'):
	            purpose+=" Social_Distancing Tracker,"
            purpose=purpose[0:-1]
            print(purpose)
            new_customer=Contact(name=name,email=email,purpose=purpose)
            try:
                db.session.add(new_customer)
                db.session.commit()
                return redirect('/')
            except:
                print("error")
                
            purpose= name + " with email address = "+email+" wants you to " + purpose
            sendEmail("email","receiver",purpose)
            # purpose is the message made by combining data

            
		
			
            
			
    # rendering the index			            
    return render_template('index.html',task=task)


  # function for the inter modular communication 
  # social distancing tracker function is called  
def gen(camera):
    while True:
        frame= camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # it will convert the data from the html to bytes and vice versa
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame') 
@app.route('/video_feed2')
# this one is for mask detection
def video_feed2():
    
  
    return Response(flaskfun(), mimetype='multipart/x-mixed-replace; boundary=frame') 
@app.route('/data')
def data():
    taskss=Contact.query.order_by(Contact.date_created).all()
            
    return render_template('table.html',task=taskss)

if __name__ == '__main__':
    app.run(debug=True,port=80,use_reloader=False) 