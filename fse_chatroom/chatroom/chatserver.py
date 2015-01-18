from twisted.protocols import basic
from twisted.web.websockets import WebSocketsResource, WebSocketsProtocol, lookupProtocolForFactory
import time, datetime

class MyChat(basic.LineReceiver):
    def connectionMade(self):
        print "New client has joined"
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Client has left"
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        print repr(data)
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
from twisted.internet.protocol import Factory

class ChatFactory(Factory):
    protocol = MyChat
    clients = []

resource = WebSocketsResource(lookupProtocolForFactory(ChatFactory()))
root = Resource()
root.putChild("ws",resource)

application = service.Application("chatserver")
internet.TCPServer(1025, Site(root)).setServiceParent(application)
