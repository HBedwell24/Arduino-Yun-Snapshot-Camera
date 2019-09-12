Facial Recognition Web Enabled Camera
==================================================================
A UVC compatible camera is triggered by a PIR motion sensor to store a .png image on an Arduino Yun. After this task has been completed, the image is then uploaded to Amazon S3 (to be compared on an image to image basis with existing records in the opposing S3 bucket). If a face is captured that does not exist in the collection, a lambda function is triggered, which sends a warning message to the user.

Source Code
------------------------------------------------------------------
To get the software side of the local project up and running:
1. Ensure that upload_picture.py (located under 'src') has been stored under the root of the microSD card along with Temboo's Python SDK libaries (which can be found at https://temboo.com/python).
2. Verify that the 'sketch.ino' file has been successfully transferred to the Arduino via USB or Wi-Fi respectively.
