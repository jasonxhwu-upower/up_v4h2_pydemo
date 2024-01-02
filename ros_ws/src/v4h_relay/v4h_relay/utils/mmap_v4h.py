import cv2
import numpy as np
import mmap
#template
'''
Summary:
Return Type:
Note(s):
'''

'''
Summary: Reads the mmap memory buffer outputed by the frontcam application and converts it to a NP array.
Return Type: 2-Channel YUYV Numpy Array
Note(s): Keep the default parameters unless you know what you are doing
'''
def read_frontcam_membuf(width=1280, height=720, path='/home/ubuntu/front_cam/image_buffer_out.dat', bgr=True, jpeg_compression=True):
    with open(path, "r+b") as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    data = mmapped_file.read()
    numpy_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 2))
    if bgr:
        image_data = convert_yuv_to_bgr(numpy_array)
    else:
        image_data = convert_yuv_to_rgb(numpy_array)
    
    if jpeg_compression:
        return ocv_jpeg_conversion(image_data)
    return image_data.data

def write_frontcam_membuf(data, width=1280, height=720, path='', bgr=True, jpeg_compression=True):
    numpy_array = np.frombuffer(data, np.uint8)

    if jpeg_compression:
        # Check if it's already an image array
        if not isinstance(numpy_array[0], np.uint8):
            numpy_array = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

    with open(path, 'wb') as file:
        file.write(numpy_array.data.tobytes())

'''
Summary: Simple function to convert YUYV NP Array/OCV Mat to BGR
Return Type: OpenCV BGR Mat
Note(s): N/A
'''
def convert_yuv_to_bgr(yuv_image):
    bgr_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR_YUYV)
    return bgr_image

'''
Summary: Simple function to convert YUYV NP Array/OCV Mat to RGB
Return Type: OpenCV RGB Mat
Note(s): N/A
'''
def convert_yuv_to_rgb(yuv_image):
    rgb_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2RGB_YUYV)
    return rgb_image

def ocv_jpeg_conversion(image_data):
    compressed_image = cv2.imencode('.jpg', image_data)[1]
    return compressed_image

