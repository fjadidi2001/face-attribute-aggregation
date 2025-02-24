import grpc
import aggregator_pb2
import aggregator_pb2_grpc

print("🚀 Starting Image Input Service...")

try:
    channel = grpc.insecure_channel("localhost:50053")
    stub = aggregator_pb2_grpc.AggregatorStub(channel)
    print("✅ Connected to Face Landmark Service")
except Exception as e:
    print(f"❌ Error connecting to Face Landmark Service: {e}")

try:
    channel2 = grpc.insecure_channel("localhost:50054")
    stub2 = aggregator_pb2_grpc.AggregatorStub(channel2)
    print("✅ Connected to Age/Gender Service")
except Exception as e:
    print(f"❌ Error connecting to Age/Gender Service: {e}")
