import gevent
import gevent.pywsgi
import gevent.queue
import base64

from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport

dispatcher = RPCDispatcher()
transport = WsgiServerTransport(queue_class=gevent.queue.Queue)

# start wsgi server as a background-greenlet
wsgi_server = gevent.pywsgi.WSGIServer(('127.0.0.1', 80), transport.handle)
gevent.spawn(wsgi_server.serve_forever)

rpc_server = RPCServerGreenlets(
    transport,
    JSONRPCProtocol(),
    dispatcher
)

@dispatcher.public
def reverse_string(s):
    return s[::-1]

@dispatcher.public
def peter(s):
    return "du er lort"

@dispatcher.public
def save_file(encoded_file, file_name):
    base64bytes = base64.b64decode(encoded_file)
    f = open(f"Storage/{file_name}", "wb")
    f.write(base64bytes)
    f.close()
    return "The file was succesfully stored"

# in the main greenlet, run our rpc_server
rpc_server.serve_forever()