import rclpy
import cv2 
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from rmw_qos_profiles import rmw_qos_profile_sensor_data
import mmap_opencv.utils
class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        #QOS profile
        qos_profile = rmw_qos_profile_sensor_data
        qos_profile.reliability = rmw_qos_reliability_policy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT
        qos_profile.durability = rmw_qos_durability_policy.DurabilityVolatile
        qos_profile.deadline = {'sec': 0, 'nsec': int(1e8)}  # 100 milliseconds
        qos_profile.lifespan = qos_profile.deadline
        qos_profile.history = rmw_qos_history_policy.KeepLast
        qos_profile.depth = 1  # Keep only the latest message

        #publisher
        self.publisher_ = self.create_publisher(CompressedImage, 'v4h_topic', 10)
        self.timer = self.create_timer(0, self.timer_callback)
        
        #timer callback counter
        self.i = 0

    def timer_callback(self):
        self.i += 1
        msg = CompressedImage()
        msg.format = 'jpeg'
        msg.data = mmap_opencv.utils.read_frontcam_membuf().tobytes
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