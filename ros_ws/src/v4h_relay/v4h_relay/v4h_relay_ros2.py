import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, HistoryPolicy, DurabilityPolicy, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage
import v4h_relay.utils.mmap_v4h as mmap_utils
class v4h2_relay(Node):

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
        self.fps_counter = self.create_timer(1, self.count_fps)
        #timer callback counter
        self.i = 0

    def timer_callback(self):
        msg = CompressedImage()
        msg.format = 'jpeg'
        msg.data = mmap_utils.read_frontcam_membuf().tobytes()
        self.publisher_.publish(msg)
        self.i += 1
        
    def count_fps(self):
        self.get_logger().info('Number of frames published per second: %d' % self.i)
        self.i = 30

def main(args=None):
    rclpy.init(args=args)

    v4h2_main = v4h2_relay()

    rclpy.spin(v4h2_main)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    v4h2_main.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()