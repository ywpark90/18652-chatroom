from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory

#basic protocol/api for handling realtime chat
class MyChat(basic.LineReceiver):
    def connectionMade(self):
        print "Got new client!"
        self.transport.write('connected ....\n')
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Lost a client!"
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        print "received", repr(data)
        for c in self.factory.clients:
            c.message(data)

    def message(self, message):
        self.transport.write(message + '\n')

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import protocol
from twisted.application import service, internet

#Create a protocol factory
#The factory is usually a singleton, and
#all instantiated protocols should have a reference to it,
#so we'll use it to store shared state
#(the list of currently connected clients)
from twisted.internet.protocol import Factory
class ChatFactory(Factory):
    protocol = MyChat
    clients = []

resource = WebSocketsResource(lookupProtocolForFactory(ChatFactory()))
root = Resource()
#serve chat protocol on /ws
root.putChild("ws",resource)

application = service.Application("chatserver")
#run a TCP server on port 1025, serving the chat protocol.
internet.TCPServer(1025, Site(root)).setServiceParent(application)
