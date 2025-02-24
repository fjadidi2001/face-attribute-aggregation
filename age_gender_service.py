import grpc
from concurrent import futures
import time
import aggregator_pb2
import aggregator_pb2_grpc

class AgeGenderService(aggregator_pb2_grpc.AggregatorServicer):
    def SaveFaceAttributes(self, request, context):
        print("✅ Received request in AgeGenderService")
        print(f"📷 Image size: {len(request.frame)} bytes")
        print(f"🔑 Redis Key: {request.redis_key}")
        # Simulate age/gender processing
        return aggregator_pb2.FaceResultResponse(response=True)

def serve():
    print("🚀 Starting Age/Gender Service on port 50054...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aggregator_pb2_grpc.add_AggregatorServicer_to_server(AgeGenderService(), server)
    server.add_insecure_port("[::]:50054")
    server.start()
    print("✅ Age/Gender Service is running!")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
