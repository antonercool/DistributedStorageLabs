import sys
import zmq

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5555")
# Subscribe to zipcode, default is NYC, 10001
zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
print(f"Collecting updates from weather server of zip code {zip_filter}")
# Process 5 updates
total_temp = 0
for update_nbr in range(5):
    string = socket.recv_string()
    zipcode, temperature, relhumidity = string.split()
    total_temp += int(temperature)
    print(f"Average temperature for zipcode '{zip_filter}' was {total_temp / (update_nbr+1)}F")