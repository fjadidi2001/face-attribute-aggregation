import grpc
import redis
import json
import cv2
import dlib
import numpy as np
import aggregator_pb2
import aggregator_pb2_grpc
from concurrent import futures

detector = dlib.get_frontal_face_detector()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class FaceDetectionService(aggregator_pb2_grpc.AggregatorServicer):
    def DetectFaceLandmarks(self, request, context):
        np_arr = np.frombuffer(request.frame, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        faces = detector(img)
        landmarks = [{"x": f.left(), "y": f.top()} for f in faces]

        redis_key = request.redis_key
        redis_client.set(redis_key, json.dumps({"landmarks": landmarks}))

        return aggregator_pb2.FaceResultResponse(response=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aggregator_pb2_grpc.add_AggregatorServicer_to_server(FaceDetectionService(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    print("Face Detection gRPC server running on port 50053...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
