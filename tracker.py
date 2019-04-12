import cv2
import imutils
from imutils.video import FPS
import argparse
import serial
import time


ap = argparse.ArgumentParser()

ap.add_argument("-t", "--tracker", type=str, default="mosse",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
		"boosting": cv2.TrackerBoosting_create,
		"mil": cv2.TrackerMIL_create,
		"tld": cv2.TrackerTLD_create,
		"medianflow": cv2.TrackerMedianFlow_create,
		"mosse": cv2.TrackerMOSSE_create
}

tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

center_point = {
        'x': 0,
        'y': 0
}
vertical = 0

initBoundaries = None
fps = None

cap = cv2.VideoCapture(1)

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

def send_data(vertical, x):
    if x < vertical:
        return 1
    elif x > vertical:
        return -1
    else:
        return 0
    

ard = serial.Serial('COM4',115200,timeout=0.05)
time.sleep(2) # wait for Arduino

while(True):
    ret, frame = cap.read()    

    
    if frame is None:
        break
    
    length=600
    
    frame = imutils.resize(frame, length)
    (H, W) = frame.shape[:2]
 
    cv2.line(frame,(int(length/2),0),(int(length/2),int(length)),(0,255,0),1)
    #cv2.line(frame,(int(width/2),0),(int(width/2),int(height)),(0,255,0),1)
    #cv2.circle(frame,(int(width/2.5),int(height/2.5)), 2, (0,0,255), -1)   
    
    ard.flush()
    
    vertical = int(length/2)
   # print('ret: ' + str(send_data(vertical, center_point['x'])))
   # print('v: ' + str(vertical))
   # print(str(center_point['x']) + ' ' + str(center_point['y']))

    if initBoundaries is not None:
        
        (success, box) = tracker.update(frame)
        
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 235, 25), 1)
            cv2.circle(frame,(int(float(x + (x + w))/2),int(float(y + (y + h))/2)), 5, (0,0,255), -1)   
           
            center_point['x'] = int(float(x + (x + w))/2);
            center_point['y'] = int(float(y + (y + h))/2);
            
            ard.write(str.encode(str(send_data(vertical, center_point['x']))))
            msg = ard.readline()
            print("Message from arduino: ")
            print (msg.decode('utf-8'))

    
        fps.update()
        fps.stop()
        info = [
			("FPS", "{:.2f}".format(fps.fps())),
		]
        
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 245, 0), 2)
        
    cv2.imshow('frame', frame)
   
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('i'):
        initBoundaries = cv2.selectROI("frame", frame, fromCenter=False,
                                       showCrosshair=True)
        tracker.init(frame, initBoundaries)
        fps = FPS().start()
        
    elif key == ord("q"):
        break
 
    
cap.release()
cv2.destroyAllWindows()

