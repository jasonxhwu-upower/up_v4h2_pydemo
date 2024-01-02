import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, HistoryPolicy, DurabilityPolicy, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage
#import v4h_relay.utils.mmap_v4h as mmap_utils

class orin_relay(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        qos_profile = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE
        )

def main(args=None):
    rclpy.init(args=args)

    orin_main = orin_relay()

    rclpy.spin(orin_main)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    orin_main.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
