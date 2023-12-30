import cv2
import numpy as np
import mmap


def read_yuyv_image_to_8bit(width, height):
    with open("image_buffer_out.dat", "r+b") as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    # Read and print the data
    data = mmapped_file.read()
    numpy_array = np.frombuffer(data, dtype=np.uint8)
    return numpy_array.reshape((height, width, 2))

def convert_yuv_to_bgr(yuv_image):
    bgr_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR_YUYV)
    return bgr_image

file_path = 'test.raw'
output_path = 'output.bmp'
jpeg_filename = "output.jpg"
width = 1280 
height = 720
while True:
    uyvy_values = read_yuyv_image_to_8bit(width,height)
    rgb_image = convert_yuv_to_bgr(uyvy_values)
    #cv2.imwrite(jpeg_filename, rgb_image)
    cv2.imshow("Image", rgb_image)
    cv2.waitKey(1)

cv2.destroyAllWindows()
