# This makefile calls protobuf compiler to auto-generate the comm inteface
PROTO_FILE = sample_packet.proto

all: sample_packet_py

sample_packet_py:
	protoc --python_out=../ $(PROTO_FILE)

clean:
	rm -rf ../*_pb2.py
