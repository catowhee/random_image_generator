import zmq # For ZeroMQ

context = zmq.Context()
print("Client attempting to connect to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
print(f"Sending a request...")
socket.send_string("icecream")
message = socket.recv()
print(f"Server sent back: {message.decode()}")
#End server
socket.send_string("Q") # (Q)uit will ask server to stop.