import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, HistoryPolicy, DurabilityPolicy, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage
import orin_relay.utils.mmap_orin as mmap_utils


class orin_relay_sub(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        qos_profile = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )
        self.subscription = self.create_subscription(CompressedImage, '/v4h2_to_orin', self.listener_callback, qos_profile)
        self.mmap_handle = mmap_utils.open_from_v4h2_mmap()

    def listener_callback(self, msg):
        #self.get_logger().info("recieved:")
        mmap_utils.orin_sub_mmap(msg.data)

    def destroy_node(self):
        mmap_utils.close_from_v4h2_mmap
        return super().destroy_node() 

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
        self.timer = self.create_timer(0.033, self.timer_callback)
        self.fps_counter = self.create_timer(1, self.count_fps)
        #timer callback counter
        self.i = 0

        self.mmap_handle = mmap_utils.open_orin_inference_mmap()
    
    def timer_callback(self):
        msg = CompressedImage()
        msg.format = 'jpeg'
        msg.data = mmap_utils.orin_pub_mmap()
        self.publisher_.publish(msg)
        self.i += 1
        
    def count_fps(self):
        self.get_logger().info('Number of frames published per second: %d' % self.i)
        self.i = 0
    
    def destroy_node(self):
        mmap_utils.close_orin_inference_mmap
        return super().destroy_node() 

def main(args=None):
    rclpy.init(args=args)
    executor = rclpy.executors.MultiThreadedExecutor()
    orin_pub = orin_relay_pub()
    orin_sub = orin_relay_sub()

    executor.add_node(orin_pub)
    executor.add_node(orin_sub)

    #executor.spin()
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass 

    orin_pub.destroy_node()
    orin_sub.destroy_node()
    executor.shutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
