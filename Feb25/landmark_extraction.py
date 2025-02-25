import dlib
import cv2
import numpy as np
import redis
import time

r = redis.Redis()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def process_landmarks(face_id):
    face_base64 = r.hget(face_id, 'face_image')
    face_img = cv2.imdecode(np.frombuffer(base64.b64decode(face_base64), dtype=np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    rect = dlib.rectangle(0, 0, face_img.shape[1], face_img.shape[0])
    
    start_time = time.time()
    landmarks = predictor(gray, rect)
    processing_time = time.time() - start_time
    r.hset('logs', f'landmarks_{face_id}', processing_time)
    
    landmarks_data = [(point.x, point.y) for point in landmarks.parts()]
    r.hset(face_id, 'landmarks', str(landmarks_data))
    r.publish('age_gender_queue', face_id)
