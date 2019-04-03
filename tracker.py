import cv2
import imutils
from imutils.video import FPS
import argparse
import time
import numpy as np

ap = argparse.ArgumentParser()

ap.add_argument("-t", "--tracker", type=str, default="mil",
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

initBoundaries = None
fps = None

cap = cv2.VideoCapture(1)

while(True):
    ret, frame = cap.read()    
    
    if frame is None:
        break
    
    frame = imutils.resize(frame, width=1000)
    (H, W) = frame.shape[:2]
    
    if initBoundaries is not None:
        
        (success, box) = tracker.update(frame)
        
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 235, 25), 1)
        
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

