''"Step 1: Installing Necessary Libraries""
pip install opencv-python facenet-pytorch torch torchvision

import cv2
import torch
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
import os

# Initialize MTCNN for face detection and InceptionResnetV1 for face recognition
mtcnn = MTCNN(keep_all=True, device='cpu')
resnet = InceptionResnetV1(pretrained='vggface2').eval()  # FaceNet pre-trained model

# Load and prepare known faces (dataset of known people)
def load_known_faces(known_faces_dir="known_faces"):
    known_face_encodings = []
    known_face_names = []
    
    for filename in os.listdir(known_faces_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # Load image and detect faces
            img = cv2.imread(os.path.join(known_faces_dir, filename))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            faces, _ = mtcnn.detect(img_rgb)
            
            if faces is not None:
                # Assuming only one face per image for simplicity
                x1, y1, x2, y2 = map(int, faces[0])
                face = img_rgb[y1:y2, x1:x2]
                face_tensor = torch.tensor(face).permute(2, 0, 1).unsqueeze(0).float() / 255.0
                # Get embedding (128-dimensional vector)
                embedding = resnet(face_tensor).detach().numpy().flatten()
                
                known_face_encodings.append(embedding)
                known_face_names.append(filename.split('.')[0])  # Use the filename as the person's name
                
    return known_face_encodings, known_face_names

# Load known faces
known_face_encodings, known_face_names = load_known_faces()

# Function to recognize a face
def recognize_face(embedding, known_face_encodings, known_face_names, threshold=0.6):
    distances = np.linalg.norm(known_face_encodings - embedding, axis=1)
    best_match_index = np.argmin(distances)
    if distances[best_match_index] < threshold:
        return known_face_names[best_match_index]
    return "Unknown"

# Real-time Face Detection and Recognition
def recognize_faces_in_video():
    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to RGB for face detection
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        faces, _ = mtcnn.detect(frame_rgb)
        
        if faces is not None:
            for (x1, y1, x2, y2) in faces:
                x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
                
                # Draw rectangle around the face
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                
                # Extract face
                face = frame_rgb[y1:y2, x1:x2]
                face_tensor = torch.tensor(face).permute(2, 0, 1).unsqueeze(0).float() / 255.0
                
                # Get the face embedding (FaceNet)
                embedding = resnet(face_tensor).detach().numpy().flatten()
                
                # Recognize the face
                name = recognize_face(embedding, known_face_encodings, known_face_names)
                
                # Display name
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        
        # Show the frame with the detection and recognition
        cv2.imshow("Face Detection and Recognition", frame)
        
        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the recognition system
recognize_faces_in_video()
