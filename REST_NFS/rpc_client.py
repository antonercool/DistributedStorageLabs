from tinyrpc import RPCClient
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.http import HttpPostClientTransport
import base64

def convert_file_to_base64(file_name):
    with open(file_name, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
        return encoded_string

rpc_client = RPCClient(
    JSONRPCProtocol(),
    HttpPostClientTransport('http://localhost')
)


str_server = rpc_client.get_proxy()
# ...

# call a method called 'reverse_string' with a single string argument
print(len(convert_file_to_base64("lake.jpg")))
result = str_server.save_file(convert_file_to_base64("lake.jpg"), "lake.png")

print("Server answered:", result)


