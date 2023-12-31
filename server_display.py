import cv2
import socket
import numpy as np
import struct

TCP_IP = "192.168.100.94"
TCP_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(1)

print(f"Server listening on {TCP_IP}:{TCP_PORT}")

connection, addr = server_socket.accept()
print(f"Connection address: {addr}")

cv2.namedWindow("Received Image", cv2.WINDOW_NORMAL)

try:
    while True:
        # Receive the length of the image data
        length_data = connection.recv(4)
        if not length_data:
            break
        length = struct.unpack("!I", length_data)[0]

        # Receive the image data
        image_data = connection.recv(length)
        if not image_data:
            break

        # Convert binary data to NumPy array
        image_np = np.frombuffer(image_data, dtype=np.uint8)

        # Decode the image array using OpenCV
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # Display the received image
        cv2.imshow("Received Image", image)

        # Press 'q' to exit the loop and close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    connection.close()
    server_socket.close()
    cv2.destroyAllWindows()
