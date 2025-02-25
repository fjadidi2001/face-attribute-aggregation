from keras.models import load_model
import numpy as np
import cv2
import redis
import time

r = redis.Redis()
model = load_model('age_gender_model.h5')  # Pretrained model

def predict_age_gender(face_id):
    face_base64 = r.hget(face_id, 'face_image')
    face_img = cv2.imdecode(np.frombuffer(base64.b64decode(face_base64), dtype=np.uint8), cv2.IMREAD_COLOR)
    resized = cv2.resize(face_img, (224, 224)) / 255.0
    input_data = np.expand_dims(resized, axis=0)
    
    start_time = time.time()
    age, gender_prob = model.predict(input_data)[0]
    processing_time = time.time() - start_time
    r.hset('logs', f'age_gender_{face_id}', processing_time)
    
    gender = 'Male' if gender_prob > 0.5 else 'Female'
    r.hset(face_id, 'gender', gender)
    r.hset(face_id, 'age', int(age))
    check_aggregation(face_id)

def check_aggregation(face_id):
    if r.hexists(face_id, 'landmarks') and r.hexists(face_id, 'age') and r.hexists(face_id, 'gender'):
        aggregate_data(face_id)
