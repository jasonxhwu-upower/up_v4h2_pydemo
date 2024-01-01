import rclpy
import cv2 
from rclpy.node import Node
from rclpy.qos import QoSProfile, HistoryPolicy, DurabilityPolicy, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage
import mmap_opencv.utils.mmap_v4h as mmap_utils
class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        qos_profile = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )
        #publisher
        self.publisher_ = self.create_publisher(CompressedImage, 'v4h_topic', 10)
        self.timer = self.create_timer(0, self.timer_callback)
        
        #timer callback counter
        self.i = 0

    def timer_callback(self):
        self.i += 1
        msg = CompressedImage()
        msg.format = 'jpeg'
        msg.data = mmap_utils.read_frontcam_membuf().tobytes
        self.get_logger().info('Publishing Image: "%d"' % self.i)

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