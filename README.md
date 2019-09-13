Facial Recognition Web Enabled Camera
==================================================================
A cloud security device tasked with monitoring a given premise for suspicious activity, using a whitelist of known faces stored in Amazon S3 for reference. Faces that are detected using the device’s onboard PIR motion sensor are saved locally to an Arduino Yun via microSD card (as prescribed in the Arduino’s C/C++ codebase) and are then uploaded to AWS using Temboo’s Python SDK, to be analyzed by Amazon Rekognition accordingly. 

Source Code
------------------------------------------------------------------
To get the software side of the local project up and running:
1. Ensure that upload_picture.py (located under 'src') has been stored under the root of the microSD card along with Temboo's Python SDK libaries (which can be found at https://temboo.com/python).
2. Verify that the 'sketch.ino' file has been successfully transferred to the Arduino via USB or Wi-Fi respectively.
