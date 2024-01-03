import cv2
import numpy as np
import mmap

def read_frontcam_membuf(width=1280, height=720, path='/home/ubuntu/front_cam/image_buffer_out.dat', bgr=True):
    with open(path, "r+b") as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        data = mmapped_file.read()
        mmapped_file.close()
        
    numpy_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 2))

    if bgr:
        image_data = cv2.cvtColor(numpy_array, cv2.COLOR_YUV2BGR_YUYV)
    else:
        image_data = cv2.cvtColor(numpy_array, cv2.COLOR_YUV2RGB_YUYV)
    
    return cv2.imencode('.jpg', image_data, [int(cv2.IMWRITE_JPEG_QUALITY), 80])[1]

def write_frontcam_membuf(data, width=1280, height=720):
    numpy_array = np.frombuffer(data, np.uint8)

