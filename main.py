import cv2
from ultralytics import YOLO

# Initialize the YOLOv8 model
model = YOLO('yolov8n.pt')

# Initialize video capture (webcam in this case)
cap = cv2.VideoCapture(2)

def draw_boxes(image, result):
    try:
        for box in result.boxes:
            class_name = result.names[box.cls[0].item()]
            cords = box.xyxy[0].tolist()
            cords = [round(x) for x in cords]
            conf = round(box.conf[0].item(), 2)
    
        
            x1, y1, x2, y2 = cords
            label = class_name
            confidence = conf

            detections={
              "Coordinates":cords,
              "Class Name":class_name,
              "Confidence":confidence
            }

            # Draw the bounding box and label on the frame
            if class_name=="person" and confidence>0.50:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f'{label} {confidence:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        if class_name=="person" and confidence>0.50:   
            return image,detections
    except:
        return image,{}

while True:
    ret, frame = cap.read()
    
    if ret==True:
        
        results = model(frame)
        result = results[0]
        
        try:
            marked_iamge,detections=draw_boxes(frame, result)    
        # cv2.imwrite('detected_person.jpg', frame)
            cv2.imshow('Frame', marked_iamge)
        except:
            cv2.imshow('Frame', frame)
    else:
        pass
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture
cap.release()
cv2.destroyAllWindows()
