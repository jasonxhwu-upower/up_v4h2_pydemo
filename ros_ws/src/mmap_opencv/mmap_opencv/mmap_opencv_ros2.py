import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import cv2
import numpy as np
import mmap


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
        self.mmap_main() # uncomment this line to run mmap_opencv function

    
    def read_yuyv_image_to_8bit(self, width, height):
        with open("image_buffer_out.dat", "r+b") as f:
            mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        # Read and print the data
        data = mmapped_file.read()
        numpy_array = np.frombuffer(data, dtype=np.uint8)
        return numpy_array.reshape((height, width, 2))

    def convert_yuv_to_bgr(self, yuv_image):
        bgr_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR_YUYV)
        return bgr_image
    
    def mmap_main(self):
        file_path = 'test.raw'
        output_path = 'output.bmp'
        jpeg_filename = "output.jpg"
        width = 1280 
        height = 720
        while True:
            uyvy_values = self.read_yuyv_image_to_8bit(width,height)
            rgb_image = self.convert_yuv_to_bgr(uyvy_values)
            #cv2.imwrite(jpeg_filename, rgb_image)
            cv2.imshow("Image", rgb_image)
            cv2.waitKey(1)

        cv2.destroyAllWindows()


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()