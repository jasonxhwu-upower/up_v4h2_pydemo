import os
import socket
import struct

def display_images_in_folder(folder_path, fps=30):
    # Get a list of all files in the folder
    file_list = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')])
    
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Server address
    server_address = ('192.168.100.94', 12345)
    
    # Connect to the server
    client_socket.connect(server_address)

    # Loop through each file and display the image
    for file_name in file_list:
        # Construct the full path to the image file
        image_path = os.path.join(folder_path, file_name)
        binary_data = None
        
        # Read the image
        with open(image_path, 'rb') as file:
            # Read the binary data from the file
            binary_data = file.read()

            # Identify the start of the image data (usually the SOI marker)
            soi_marker = binary_data.find(b'\xFF\xD8')
            if soi_marker == -1:
                raise ValueError("Not a valid JPG file")
        
        if binary_data is not None:
            #print(image_path)
            image_data = binary_data[soi_marker:]
            length_data = struct.pack("!I", len(image_data))
            client_socket.sendall(length_data)
            # Send the image data over the TCP connection
            client_socket.sendall(image_data)

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    folder_path = 'images'
    display_images_in_folder(folder_path, fps=30)
