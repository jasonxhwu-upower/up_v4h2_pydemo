import cv2
import numpy as np
import mmap

# Used by orin_pub
mmap_inf_path = '/home/nvidia/mmap_exchange/orin_to_v4h2.dat'
# Used by orin_sub
mmap_v4h_path = '/home/nvidia/mmap_exchange/v4h2_to_orin.dat'

# mmap to be used
mmap_file_inference = None
mmap_file_v4h = None
file_inference = None
file_v4h = None

# reads the mmap produced by inferencing. Used by orin_pub
def open_orin_inference_mmap():
    global mmap_file_inference, file_inference
    try:
        file_inference = open(mmap_inf_path, 'w+b')
        mmap_file_inference = mmap.mmap(file_inference.fileno(), 0, access=mmap.ACCESS_READ)
    except:
        file_inference.closer()
# writes the mmap from v4h => orin. Used by orin_sub
def open_from_v4h2_mmap():
    global mmap_file_v4h, file_v4h
    try:
        file_v4h = open(mmap_v4h_path, 'w+b')
        file_v4h.truncate(1280 * 720 * 3)
        mmap_file_v4h = mmap.mmap(file_v4h.fileno(), 1280 * 720 * 3, access=mmap.ACCESS_WRITE)
    except:
        file_v4h.close()

# closes the mmap from inferencing
def close_orin_inference_mmap():
    mmap_file_inference.close()
    try:
        file_inference.closer()
    except:
        pass

# closes the mmap from v4h => orin
def close_from_v4h2_mmap():
    mmap_file_v4h.close()
    try:
        file_v4h.closer()
    except:
        pass

#orin publisher. Reads mmap, compresses data, and then sends it back to the v4h
def orin_pub_mmap(width=1280, height=720, jpeg_compression=True):
    #reads the data from the mmap buffer that is opened. 
    data = mmap_file_inference.read()
    #put into np and then reshape into 3 channels
    numpy_array = np.frombuffer(data, dtype=np.uint8)
    #compression 
    if jpeg_compression:
        return cv2.imencode('.jpg', numpy_array, [int(cv2.IMWRITE_JPEG_QUALITY), 80])[1]
    return numpy_array.data

#orin subscriber. Takes the ros2 data, decompresses it, and then writes it to mmap
def orin_sub_mmap(data, width=1280, height=720, jpeg_compression=True):
    #reads in compressed rgb data
    numpy_array = np.frombuffer(data, np.uint8)
    if jpeg_compression:
        numpy_array = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
    with open(mmap_v4h_path, 'w+b') as f:
        f.truncate(1280 * 720 * 3)
        mmap_file_v4h = mmap.mmap(f.fileno(), 1280 * 720 * 3, access=mmap.ACCESS_WRITE)
        mmap_file_v4h.write(numpy_array.data)
        mmap_file_v4h.close()