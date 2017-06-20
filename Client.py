import socket, logging, sys, time
import sample_packet_pb2
from CmdDefinitions import *
from google.protobuf.message import EncodeError

class Client(object):
    def __init__(self, host="localhost", port=9999, frequency=100):
    	self.Host = host
    	self.Port = port
        self.CommFrequencyHz = frequency
        self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.MaxPacketSizeBytes = 255
        self.connect()

    def connect(self):
    	# Connect to the server
        self.ClientSocket.connect((self.Host, self.Port))

    def sendCmd(self, cmd):
        # Tx the command
        self.tx(cmd)
        # Give the device time to respond
        time.sleep(1.0/self.CommFrequencyHz)
        # Rx the telemetry
        try:
            response = self.readTelemetry()
        except IOError:
        	logging.info("Failed to send packet : " + str(cmd))
        # Print out what we got back
        logging.info("Received response : " + str(response))
    	return response

    def disconnect(self):
        cmd_packet = sample_packet_pb2.CommandPacket()
        disconnect_cmd = cmd_packet.RoverCmds.add()
        disconnect_cmd.Id = DISCONNECT
    	# Send a disconnect cmd
    	self.sendCmd(cmd_packet)
    	# Disconnect from the server
    	self.ClientSocket.close()

    def tx(self, cmd):
        if (isinstance(cmd, sample_packet_pb2.CommandPacket)):
            # Send down the serialized command
            try:
                self.ClientSocket.send(cmd.SerializeToString())
            except EncodeError:
                logging.error("Failed to encode command packet. Are all required fields set?")
                raise IOError

    def readTelemetry(self):
        bytes_rcvd = self.readRawBytes()
        if bytes_rcvd:
            return self.unpackTelemetry(bytes_rcvd)
        else:
            raise IOError

    def readRawBytes(self):
        return self.ClientSocket.recv(self.MaxPacketSizeBytes)

    def unpackTelemetry(self, raw_bytes):
        tlm = sample_packet_pb2.TelemetryPacket()
        logging.debug("Telemetry to be unpacked :")
        logging.debug(":".join("{:02x}".format(ord(c)) for c in raw_bytes))
        try:
            tlm.ParseFromString(raw_bytes)
        except Exception:
            raise IOError
        return tlm    	
