import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, HistoryPolicy, DurabilityPolicy, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage
#import v4h_relay.utils.mmap_v4h as mmap_utils

class orin_relay_sub(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')

        qos_profile = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )
        
        #subscriber
        self.subscription = self.create_subscription(CompressedImage, '/v4h2_to_orin', self.listener_callback, qos_profile)
        self.publisher_ = self.create_publisher(CompressedImage, '/inference_results', qos_profile) # TODO: change CompressedImage to inference results type
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        test_data = msg.data[:15]
        self.get_logger().info('The image is: "%s"...' % test_data)
        self.publisher_.publish(msg) # TODO: change test_data to inference results

class orin_relay_pub(Node):
    def __init__(self):
        super().__init__('minimal_publisher')

        qos_profile = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )
        #publisher
        self.publisher_ = self.create_publisher(CompressedImage, '/orin_to_v4h2', qos_profile)
        self.timer = self.create_timer(0, self.timer_callback)
        self.fps_counter = self.create_timer(1, self.count_fps)
        #timer callback counter
        self.i = 0
    
    def timer_callback(self):
        msg = CompressedImage()
        msg.format = 'jpeg'
        #msg.data = mmap_utils.read_frontcam_membuf().tobytes()
        #self.publisher_.publish(msg)
        self.i += 1
        
    def count_fps(self):
        self.get_logger().info('Number of frames published per second: %d' % self.i)
        self.i = 0

def main(args=None):
    rclpy.init(args=args)
    executor = rclpy.executors.MultiThreadedExecutor()
    orin_pub = orin_relay_pub()
    orin_sub = orin_relay_sub()

    executor.add_node(orin_pub)
    executor.add_node(orin_sub)

    try:
        while rclpy.ok():
            executor.spin_once()
    except:
        pass
    
    orin_sub.destroy_node()
    orin_pub.destroy_node()
    executor.shutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
