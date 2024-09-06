import cv2
import json

def detect_faces():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        face_detected = len(faces) > 0
        if face_detected:
            fan_command = "ON"
            light_command = "ON"
        else:
            fan_command = "OFF"
            light_command = "OFF"
        
        commands = {
            "fan": fan_command,
            "light": light_command
        }
        try:
            with open("commands.json", "w") as file:
                json.dump(commands, file)
        except IOError as e:
            print(f"Error writing to commands.json: {e}")
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        cv2.imshow('Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_faces()
