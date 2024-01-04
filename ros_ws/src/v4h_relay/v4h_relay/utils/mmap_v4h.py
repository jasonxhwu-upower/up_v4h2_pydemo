import cv2
import os
import numpy as np
import mmap
import time
import array
import threading

mmap_file_path = '/home/ubuntu/front_cam/image_buffer_out.dat'
mmap_frontcam = None
file_handle = None
size = 1280 * 720 * 2

thread_lock = threading.Lock()

def open_frontcam_mmap():
    global mmap_frontcam, file_handle
    attempts = 0
    while True:
        try:
            if attempts < 5:
                file_handle = os.open(mmap_file_path, os.O_RDONLY)
                mmap_frontcam = mmap.mmap(file_handle, size, mmap.MAP_SHARED, mmap.PROT_READ)
            else:
                file_handle = os.open(mmap_file_path, os.O_RDWR | os.O_CREAT | os.O_EXCL)
                os.truncate(file_handle, size)
                mmap_frontcam = mmap.mmap(file_handle, size, mmap.MAP_SHARED, mmap.PROT_READ)
                print(f"Warning: File not found, creating ad-hoc mmap buffer")
            return True
            
        except (FileNotFoundError, OSError) as e:
            print(f"Error: {e}")
            attempts += 1
        
        time.sleep(0.025)


def close_frontcam_mmap():
    mmap_frontcam.close()
    try:
        os.close(file_handle)
    except (FileNotFoundError, OSError) as e:
        print(f"Error: {e}")
        time.sleep(0.01)
              

def read_frontcam_membuf(width=1280, height=720, path='/home/ubuntu/front_cam/image_buffer_out.dat', bgr=True):
    with thread_lock:
        mmap_frontcam.seek(0)
        data = mmap_frontcam.read()
    numpy_array = np.frombuffer(data, dtype=np.uint8)
    #numpy_array = np.clip(numpy_array, 0, 255)
    numpy_array = numpy_array.reshape((height, width, 2))
    if bgr:
        image_data = cv2.cvtColor(numpy_array, cv2.COLOR_YUV2BGR_YUYV)
    else:
        image_data = cv2.cvtColor(numpy_array, cv2.COLOR_YUV2RGB_YUYV)
    compressed = cv2.imencode('.jpg', image_data, [int(cv2.IMWRITE_JPEG_QUALITY), 80])[1]
    return array.array('B', compressed.tobytes())

def frontcam_sub_create():
    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)

def frontcam_sub_close():
    cv2.destroyWindow("Video")

def frontcam_sub_show(data):
    
    numpy_array = np.frombuffer(data, np.uint8)
    numpy_array = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
    """ print("v4h_subscriber")
    print(numpy_array.shape)
    print(numpy_array.size) """
    with thread_lock:
        cv2.imshow("Video", numpy_array)
        cv2.waitKey(1)