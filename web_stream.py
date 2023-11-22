import asyncio
import cv2
import websockets
import base64
from ultralytics import YOLO
from utils import *
def initialize_yolo():
    return YOLO('yolov8n.pt')


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

            # Draw the bounding box and label on the frame
            if class_name=="person" and confidence>0.50:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f'{label} {confidence:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        if class_name=="person" and confidence>0.70:
            cv2.imwrite("image Server/static/Image/marked_image.jpg",image)
            # send_sms(body="Somebody is detected, check soon.",reciver="+918690909695")  
            return image
    except:
        return image,{}


def encode_frame(frame):
    ret, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode()

async def video_stream_handler(websocket,path, model):
    
    cap = cv2.VideoCapture(2)
  
    while True:
        ret, frame = cap.read()
        if ret==True:
        
            if frame is None:
                continue
            # Process frame
            results = model(frame)
            result = results[0]
            marked_image = draw_boxes(frame, result)



            # Encode and send frame
            try:
                
                jpg_as_text = encode_frame(marked_image)
                previous= encode_frame(marked_image)
            except:
                jpg_as_text = encode_frame(frame)
           
            try:
                await websocket.send(jpg_as_text)
            except:
                continue
            # Check for a quit signal
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            continue


    cap.release()

def start_websocket_server():
    model = initialize_yolo()
    print("Server Started")
    start_server = websockets.serve(lambda ws, path: video_stream_handler(ws, path, model), 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

# Run the server
start_websocket_server()
