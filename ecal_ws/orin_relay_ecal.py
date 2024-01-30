import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber

# Import the "hello_world_pb2.py" file that we have just generated from the
# proto_messages directory 
import proto_messages.compressed_image_pb2 as compressed_image_pb2

# Callback for receiving messages
def callback(topic_name, compressed_image_protobuf_message, time):
  print("Getting Image Data with format {} from V4H".format(
    compressed_image_protobuf_message.format))

if __name__ == "__main__":
  # initialize eCAL API. The name of our Process will be
  # "Orin eCAL CompressedImage Protobuf Subscriber"
  ecal_core.initialize(sys.argv, "Orin eCAL CompressedImage Protobuf Subscriber")

  # Create a Protobuf Subscriber that subscribes on the topic
  sub = ProtoSubscriber("compressed_image_protobuf_topic"
                      , compressed_image_pb2.CompressedImage)

  # Set the Callback
  sub.set_callback(callback)
  
  # Just don't exit
  while ecal_core.ok():
    time.sleep(0.033)
  
  # finalize eCAL API
  ecal_core.finalize()