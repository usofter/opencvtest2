import sys
import cv2
import gxipy as gx
# Enumerate device. dev_info_list is a list of device information.
# The number of elements in the list is the number of devices
# enumerated. The list elements are dictionaries, which contain
# device information such as device index, ip information and so on
device_manager = gx.DeviceManager()
dev_num, dev_info_list = device_manager.update_device_list()
if dev_num == 0:
  sys.exit(1)
# Open device
# Get the list of basic device information
strSN = dev_info_list[0].get("sn")
# Open the device by serial number
cam = device_manager.open_device_by_sn(strSN)
# *************************************settings***************************************
# Get the settable range and maximum value of the exposure time
float_range = cam.ExposureTime.get_range()
print("exposure range",float_range)
float_max = float_range["max"]
# Set the current exposure time to any value in the range
cam.ExposureAuto.set(0)
# cam.ExposureTime.set(25000.0)
# Get the current exposure time
float_exposure_value = cam.ExposureTime.get()
print("exposure value",float_exposure_value)
float_range = cam.Gain.get_range()
print("gain range",float_range)
cam.Gain.set(10)
float_gain_value = cam.Gain.get()
print(float_gain_value)

# ************************************************************************************
# Start acquisition
cam.stream_on()
# Get the number of stream channels
# If int_channel_num == 1, the device has only one stream channel,
# and the number of data_stream elements in the list is 1
# If int_channel_num > 1, the device has multiple stream channels,
# and the number of data_stream elements in the list is greater than
# 1
# Currently, GigE, USB3.0, and USB2.0 cameras do not support
# multi-stream channels
# int_channel_num = cam.get_stream_channel_num()
# Get data
# num is the number of images acquired
count=0
while True:

  num = 1
  for i in range(num):
    # Get an image from the 0th stream channel
    raw_image = cam.data_stream[0].get_image()
    # Get RGB images from color raw images

    # rgb_image = raw_image.convert("RGB")
    # if rgb_image is None:
    #  continue
    # Create numpy array from RGB image data
    # numpy_image = rgb_image.get_numpy_array()
    numpy_image = raw_image.get_numpy_array()
    # count+=1
    if numpy_image is None:
     continue
    # Display and save the acquired RGB image
    # image = Image.fromarray(numpy_image, 'RGB')
    nump_im_bgr = cv2.cvtColor(numpy_image, cv2.COLOR_BayerRG2BGR)
    cv2.imshow("daheng",nump_im_bgr)
    cv2.waitKey(1)
    # image.show()
    # image.save("image.jpg")
    # if count==1: cv2.imwrite("image.tif",nump_im_bgr)
    # cv2.waitKey(300)
  # Stop acquisition, close device
cam.stream_off()
cam.close_device()