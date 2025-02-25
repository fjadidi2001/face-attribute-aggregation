import json
import redis

r = redis.Redis()

def aggregate_data(face_id):
    face_data = {
        'face_id': face_id,
        'bbox': r.hget(face_id, 'bbox').decode(),
        'landmarks': eval(r.hget(face_id, 'landmarks').decode()),
        'age': r.hget(face_id, 'age').decode(),
        'gender': r.hget(face_id, 'gender').decode()
    }
    json_data = json.dumps(face_data)
    r.hset(face_id, 'aggregated', json_data)
    with open(f'output/{face_id}.json', 'w') as f:
        f.write(json_data)
