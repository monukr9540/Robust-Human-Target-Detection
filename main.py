import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
ret = True
detection_threshold = 0.1

while ret :
    ret, frame = cap.read()
    results = model.track(frame, persist=True, classes = 0, tracker = 'bytetrack.yaml')
    for result in results:
        detections = []
        for r in result.boxes.data.tolist():
            if len(r)>=7:
                x1, y1, x2, y2,id, score, class_id = r
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
                id = [id]
                class_id = int(class_id)
                if score > detection_threshold:
                    detections.append([x1, y1, x2, y2, score, class_id, id])
                print(id)
            elif len(r)<=6:
                x1, y1, x2, y2, score, class_id = r
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
                
                class_id = int(class_id)
                if score > detection_threshold:
                    detections.append([x1, y1, x2, y2, score, class_id])
                print(id)
          
    frame_ = results[0].plot()
    
    cv2.imshow('frame', frame_)
    cap1 = cv2.VideoCapture(0)
    
    if cv2.waitKey(25) & 0xFF==ord('e'):
        personid = (input('enter numeber id you want to track'))
        for i in id:
            if i == int(personid):               
                print('ID found')
                while ret :
                    ret, frame1 = cap1.read()
                    results1 = model.track(frame1, persist=True, classes = 0, tracker = 'bytetrack.yaml')
                    for result in results1:
                        detections = []
                        for r in result.boxes.data.tolist(): 
                            x1, y1, x2, y2,id, score, class_id = r
                            x1 = int(x1)
                            x2 = int(x2)
                            y1 = int(y1)
                            y2 = int(y2)
                            id = int(id)
                            print(r)
                            if id == int(personid):                            
                                cv2.rectangle(frame1, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame1, personid, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                cv2.imshow('frame2', frame1)
                            if cv2.waitKey(25) & 0xFF == ord('w'):
                                break

            else:
                print("no vaalid id found")        
                continue

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break