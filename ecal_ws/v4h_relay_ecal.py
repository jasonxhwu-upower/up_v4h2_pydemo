import sys
import time

import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
from ecal.core.subscriber import ProtoSubscriber

import proto_messages.compressed_image_pb2 as compressed_image_pb2

import mmap_v4h as mmap_utils
import cv2

# Callback for receiving messages
def callback(topic_name, compressed_image_protobuf_message, time):
  print("Getting Image Data with format {} from Orin".format(
    compressed_image_protobuf_message.format))
  mmap_utils.frontcam_sub_show(compressed_image_protobuf_message.data)

if __name__ == "__main__":
  # initialize eCAL API. The name of our Process will be
  # "V4H eCAL CompressedImage Protobuf Publisher"
  ecal_core.initialize(sys.argv, "V4H eCAL CompressedImage Protobuf Publisher")

  # Create a Protobuf Publisher that publishes on the topic
  pub = ProtoPublisher("v4h2_to_orin_img_protobuf"
                      , compressed_image_pb2.CompressedImage)
  # Create a Protobuf Subscriber that subscribes on the topic
  sub = ProtoSubscriber("orin_to_v4h2_img_protobuf"
                      , compressed_image_pb2.CompressedImage)

  mmap_utils.open_frontcam_mmap()
  mmap_utils.frontcam_sub_create()

  # Set the Callback
  sub.set_callback(callback)

  # Infinite loop (using ecal_core.ok() will enable us to gracefully shutdown
  # the process from another application)
  while ecal_core.ok():
    # Create a message and fill it with some data
    compressed_image_protobuf_message = compressed_image_pb2.CompressedImage()
    compressed_image_protobuf_message.format = "jpeg"
    compressed_image_protobuf_message.data.extend(mmap_utils.read_frontcam_membuf())

    # actually send the message to the topic this publisher was created for
    pub.send(compressed_image_protobuf_message)
    
    # Sleep 0.033s, 30 FPS
    time.sleep(0.033)

  mmap_utils.close_frontcam_mmap()
  mmap_utils.frontcam_sub_close()

  # finalize eCAL API
  ecal_core.finalize()