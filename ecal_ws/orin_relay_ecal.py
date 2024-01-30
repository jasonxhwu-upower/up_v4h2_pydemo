import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber

# Import the "hello_world_pb2.py" file that we have just generated from the
# proto_messages directory 
import proto_messages.compressed_image_pb2 as compressed_image_pb2
import mmap_orin as mmap_utils

# Callback for receiving messages
def callback(topic_name, compressed_image_protobuf_message, time):
  print("Getting Image Data with format {} from V4H".format(
    compressed_image_protobuf_message.format))
#   print(compressed_image_protobuf_message.data[:29])

if __name__ == "__main__":
  # initialize eCAL API. The name of our Process will be
  # "Orin eCAL CompressedImage Protobuf Subscriber"
  ecal_core.initialize(sys.argv, "Orin eCAL CompressedImage Protobuf Subscriber")

  # Create a Protobuf Subscriber that subscribes on the topic
  sub = ProtoSubscriber("compressed_image_protobuf_topic"
                      , compressed_image_pb2.CompressedImage)

  mmap_utils.open_from_v4h2_mmap()
  # Set the Callback
  sub.set_callback(callback)
  
  # Just don't exit
  while ecal_core.ok():
    time.sleep(0.033)
  
  mmap_utils.close_from_v4h2_mmap()
  # finalize eCAL API
  ecal_core.finalize()