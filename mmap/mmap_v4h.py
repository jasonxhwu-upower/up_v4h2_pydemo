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
def read_frontcam_membuf(width=1280, height=720, path='/home/ubuntu/front_cam/image_buffer_out.dat'):
    with open("image_buffer_out.dat", "r+b") as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    data = mmapped_file.read()
    numpy_array = np.frombuffer(data, dtype=np.uint8)
    return numpy_array.reshape((height, width, 2))

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

def dummy_test()
    while True:
        uyvy_values = read_frontcam_membuf()
        rgb_image = convert_yuv_to_bgr(uyvy_values)
        #cv2.imwrite(jpeg_filename, rgb_image)
        cv2.imshow("Image", rgb_image)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
