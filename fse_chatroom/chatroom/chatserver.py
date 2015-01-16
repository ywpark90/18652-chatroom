from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory

import time, datetime

#basic protocol/api for handling realtime chat
class MyChat(basic.LineReceiver):
    def connectionMade(self):
        print "Got new client!"
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Lost a client!"
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        print "received", repr(data)
        for c in self.factory.clients:
            uname_msg = data.split(":", 1)
            u = uname_msg[0]
            m = uname_msg[1]
            t = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

            msg = "<div class=\"message\">"
            msg += "<div class=\"message_header\">"
            msg += "<div class=\"message_name\">" + u + "</div>"
            msg += "<div class=\"message_time\">" + t + "</div></div>"
            msg += "<div class=\"message_content\">" + m + "</div></div>"
            c.message(msg)

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
