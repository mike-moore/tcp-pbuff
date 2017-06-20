import SocketServer, logging, sys, threading, time
import sample_packet_pb2
from CmdDefinitions import *

class ServerHandler(SocketServer.BaseRequestHandler):
	# Define the maximum acceptable tx/rx packet size.
	# 255 bytes is plenty for this demo packet.
    MaxPacketSizeBytes = 255

    def handle(self):
    	while True:
	        cmds_rcvd = self.readCmds()
	    	logging.info("Received commands : " + str(cmds_rcvd))
	    	self.sendResponse()
	    	if cmds_rcvd.RoverCmds[0].Id == DISCONNECT:
	    	    logging.info("Client disconnecting : " + str(cmds_rcvd))
	    	    break

    def readCmds(self):
        bytes_rcvd = self.readRawBytes()
        if bytes_rcvd:
            return self.unpackCmds(bytes_rcvd)
        else:
            raise IOError

    def readRawBytes(self):
        return self.request.recv(self.MaxPacketSizeBytes)

    def unpackCmds(self, raw_bytes):
        cmds = sample_packet_pb2.CommandPacket()
        logging.debug("Cmds to be unpacked :")
        logging.debug(":".join("{:02x}".format(ord(c)) for c in raw_bytes))
        try:
            cmds.ParseFromString(raw_bytes)
        except Exception:
            raise IOError
        return cmds

    def sendResponse(self):
        response = sample_packet_pb2.TelemetryPacket()
        response.MeasuredHeading = 5.0
        response.MeasuredDistance = 10.0
        status = response.RoverStatus.add()
        status.Id = CMD_ACCEPT
        self.request.sendall(response.SerializeToString())
