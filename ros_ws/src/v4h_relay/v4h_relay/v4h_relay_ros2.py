import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, HistoryPolicy, DurabilityPolicy, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage
import v4h_relay.utils.mmap_v4h as mmap_utils
import cv2

class v4h2_relay_pub(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        qos_profile = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )
        #publisher
        self.publisher_ = self.create_publisher(CompressedImage, '/v4h2_to_orin', qos_profile)
        self.timer = self.create_timer(0.010, self.timer_callback)
        self.fps_counter = self.create_timer(1, self.count_fps)
        #timer callback counter
        self.i = 0

        self.mmap_handle = mmap_utils.open_frontcam_mmap()

    def timer_callback(self):
        msg = CompressedImage()
        msg.format = 'jpeg'
        msg.data = mmap_utils.read_frontcam_membuf()
        self.publisher_.publish(msg)
        self.i += 1
        
    def count_fps(self):
        self.get_logger().info('Number of frames published per second: %d' % self.i)
        self.i = 0

    def destroy_node(self):
        mmap_utils.close_frontcam_mmap()
        return super().destroy_node()
        
class v4h2_relay_sub(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')

        qos_profile = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )
        
        self.subscription = self.create_subscription(CompressedImage, '/orin_to_v4h2', self.listener_callback, qos_profile)
    
    def listener_callback(self, msg):
        mmap_utils.frontcam_sub_show(msg.data)
def main(args=None):
    rclpy.init(args=args)
    executor = rclpy.executors.SingleThreadedExecutor()
    v4h2_pub = v4h2_relay_pub()
    v4h2_sub = v4h2_relay_sub()

    executor.add_node(v4h2_pub)
    executor.add_node(v4h2_sub)
    """ try:
        executor.spin()
    except KeyboardInterrupt:
        pass """
    executor.spin()

    v4h2_pub.destroy_node()
    v4h2_sub.destroy_node()
    executor.shutdown()
    rclpy.shutdown()


if __name__ == '__main__':
    main()