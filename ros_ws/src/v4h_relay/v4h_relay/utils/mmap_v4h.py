import cv2
import os
import numpy as np
import mmap

mmap_file_path = '/home/ubuntu/front_cam/image_buffer_out.dat'
mmap_frontcam = None
file_handle = None

def open_frontcam_mmap():
    global mmap_frontcam, file_handle
    try:
        file_handle = os.open(mmap_file_path, os.O_RDONLY)
        mmap_frontcam = mmap.mmap(file_handle, 0, mmap.MAP_SHARED, mmap.PROT_READ)
    except Exception as e:
        print(f"Error: {e}")

def close_frontcam_mmap():
    mmap_frontcam.close()
    try:
        os.close(file_handle)
    except Exception as e:
        print(f"Error: {e}")
              

def read_frontcam_membuf(width=1280, height=720, path='/home/ubuntu/front_cam/image_buffer_out.dat', bgr=True):
    mmap_frontcam.seek(0)
    data = mmap_frontcam.read()
    numpy_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 2))

    if bgr:
        image_data = cv2.cvtColor(numpy_array, cv2.COLOR_YUV2BGR_YUYV)
    else:
        image_data = cv2.cvtColor(numpy_array, cv2.COLOR_YUV2RGB_YUYV)
    
    return cv2.imencode('.jpg', image_data, [int(cv2.IMWRITE_JPEG_QUALITY), 80])[1]

def write_frontcam_membuf(data, width=1280, height=720):
    numpy_array = np.frombuffer(data, np.uint8)


def frontcam_sub_show(data):
    numpy_array = np.frombuffer(data, np.uint8)
    numpy_array = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
    """ print("v4h_subscriber")
    print(numpy_array.shape)
    print(numpy_array.size) """
    cv2.imshow("Image.jpg", numpy_array)
    cv2.waitKey(1)