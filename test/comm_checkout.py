#!/usr/bin/python

# Implements a unit-test for the Protobuf 
# TCP Client/Server
import unittest, logging, sys, SocketServer, time, threading
sys.path.append("../")
from Client import Client
from Server import ServerHandler
import sample_packet_pb2
from CmdDefinitions import *

class CommCheckout(unittest.TestCase):

    def setUp(self):
        self.testArticle = Client()
        self.SuccessTransmissionCount = 0
        self.FailTransmissionCount = 0
        self.NumTestsToRun = 10
    
    def tearDown(self):
        self.testArticle.disconnect()

    def test_sendCommands(self):
    	for testNum in range(1, self.NumTestsToRun+1):
            logging.info("\r\n")
            logging.info("#############################################")
            logging.info("## TEST NUMBER " + str(testNum))
            logging.info("#############################################")
            logging.info("\r\n")
            # Construct the test command packet
            cmd_packet = sample_packet_pb2.CommandPacket()
            control_signal_cmd = cmd_packet.RoverCmds.add()
            control_signal_cmd.Id = DO_STUFF
            control_signal_cmd.Value = 0.1 * testNum
            # Use the helper function to send the command packet and
            # check that we got a response
            response = self.helper_SendOneCmdPacket(cmd_packet)
            self.helper_checkResponse(response)
        if self.SuccessTransmissionCount != self.NumTestsToRun:
            self.assertTrue(False)

    def helper_SendOneCmdPacket(self, cmd_packet):
        try:
            response = self.testArticle.sendCmd(cmd_packet)
            return response
        except IOError:
            # Fail the test. No response
            self.assertTrue(False)
            return None

    def helper_checkResponse(self, response):
        if response:
            self.SuccessTransmissionCount += 1
            logging.info("Success Packet # : " + str(self.SuccessTransmissionCount))
        else:
            self.FailTransmissionCount += 1
            logging.info("Failed Packet # : " + str(self.FailTransmissionCount))

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='%(levelname)s:%(message)s')
    HOST, PORT = "localhost", 9999
    testServer = SocketServer.TCPServer((HOST, PORT), ServerHandler)
    testServerThread = threading.Thread(target=testServer.serve_forever)
    testServerThread.daemon = True
    testServerThread.start()
    # add some wait time before running tests to give the server time to start up
    time.sleep(1.0)
    # Run the unit-tests
    suite = unittest.TestLoader().loadTestsFromTestCase(CommCheckout)
    unittest.TextTestRunner(verbosity=2).run(suite)