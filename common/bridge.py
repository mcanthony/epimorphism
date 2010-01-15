from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys

Q = []

def parse(vals):
return "zn[0] = %f + 0.0j" % (1.0 + float(vals[1]) / 150.0 - 0.5)

class EchoClient(LineReceiver):
end="\n"
def connectionMade(self):
self.sendLine("status")
self.sendLine(self.end)
self.sendLine('display')
self.sendLine(self.end)
self.sendLine('watch 2')
self.sendLine(self.end)

def lineReceived(self, line):
msg = line.split()
if len(msg)==12:
bang, patient, seqNum, numCol = msg[:4]
data = msg[4:]
#print '\t',bang,patient,seqNum,numCol,'--',
data = parse(data)
print data


if line==self.end:
self.transport.loseConnection()

################################################################################

class EchoClientFactory(ClientFactory):
protocol = EchoClient

def clientConnectionFailed(self, connector, reason):
print 'connection failed:', reason.getErrorMessage()
#reactor.stop()

def clientConnectionLost(self, connector, reason):
print 'connection lost:', reason.getErrorMessage()
#reactor.stop()

################################################################################
def main():
adre = EchoClientFactory()
reactor.connectTCP('10.0.0.110', 8336, adre)
reactor.run()

if __name__ == '__main__':
main()
