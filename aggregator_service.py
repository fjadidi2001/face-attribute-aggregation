import grpc
import json
import redis
import aggregator_pb2
import aggregator_pb2_grpc
from concurrent import futures
import time

# Redis setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class AggregatorService(aggregator_pb2_grpc.AggregatorServicer):
    def SaveFaceAttributes(self, request, context):
        try:
            redis_key = request.redis_key
            image_data = request.frame  # JPEG bytes
            timestamp = request.time

            # Retrieve stored attributes from Redis
            face_data = redis_client.get(redis_key)
            if not face_data:
                return aggregator_pb2.FaceResultResponse(response=False)

            # Convert JSON data
            face_data = json.loads(face_data)
            face_data["time"] = timestamp

            # Save as JSON file
            with open(f"data/face_attributes_{redis_key}.json", "w") as json_file:
                json.dump(face_data, json_file, indent=4)

            return aggregator_pb2.FaceResultResponse(response=True)

        except Exception as e:
            print(f"Error: {e}")
            return aggregator_pb2.FaceResultResponse(response=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aggregator_pb2_grpc.add_AggregatorServicer_to_server(AggregatorService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Aggregator gRPC server running on port 50052...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

