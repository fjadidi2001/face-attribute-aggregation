import cv2
from mtcnn import MTCNN
import uuid
import redis
import base64
import time

r = redis.Redis(host='localhost', port=6379, db=0)
detector = MTCNN()

def detect_faces(image_path):
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    start_time = time.time()
    faces = detector.detect_faces(image)
    processing_time = time.time() - start_time
    r.hset('logs', 'face_detection', processing_time)

    for face in faces:
        face_id = str(uuid.uuid4())
        x, y, w, h = face['box']
        face_img = image[y:y+h, x:x+w]
        _, buffer = cv2.imencode('.jpg', face_img)
        face_base64 = base64.b64encode(buffer).decode('utf-8')
        r.hset(face_id, 'face_image', face_base64)
        r.hset(face_id, 'bbox', f"{x},{y},{w},{h}")
        r.publish('landmark_queue', face_id)
