Facial Recognition Web Enabled Camera
==================================================================
A cloud security device tasked with monitoring a given premise for suspicious activity, using a whitelist of known faces stored in Amazon S3 for reference. Faces that are detected using the device’s onboard PIR motion sensor are saved locally to an Arduino Yun via microSD card (as prescribed in the Arduino’s C/C++ codebase) and are then uploaded to AWS using Temboo’s Python SDK, to be analyzed by Amazon Rekognition accordingly. 

Materials Checklist
-----------------------------------------------------------------
* [x] Arduino Yun Rev 2
* [x] 4GB MicroSD Card
* [x] MicroSD to SD Converter
* [x] UVC Compatible Camera (i.e. Logitech C270)
* [x] PIR Motion Sensor With 3 Outward Facing Female Headers
* [x] A Dozen Female to Male Jumper Wires
* [x] Type B Micro USB Cable

Configuring The Device
-----------------------------------------------------------------
After one has acquired the various materials needed to start on building the device, it is probably easiest to start with connecting to the Arduino Yun in order to get setting it up out of the way. To complete this process, first connect the small end of the micro USB cable into the respective port on the Arduino Yun, and the other end into a computer. After this, make sure to wait at least 60 seconds for the Arduino Yun to boot up. This event will be indicated by the blue WLAN LED turning on and/or flashing. In addition, the WiFi network will display a new network, bearing the syntax of Arduino-YUN90XXXXXX. This is the Arduino Yun’s WiFi hotspot, which will be active if the microcontroller has not been previously connected to WiFi (by factory default). Connect to the hotspot, open a browser, and visit arduino.local. If this doesn’t work, then visit 192.168.240.1. Once the landing page has been reached, proceed to the configure button in the top right. It is here where the Arduino Yun’s name, password, and/or network connection will be altered, and will be vital to the moment in time when SSH is needed to run updates on the devices MAC Address. Make all necessary changes, and then proceed to opening up a terminal of choice on the computer. 

In the command line, enter ssh root@arduino.local (or root@yourarduinoname.local if the name of the Yun was changed in an earlier step), followed by Yes to add the Yun as a known host. The program will ask for a password, in which one would pass in the credentials found earlier on the Yun’s configure page. Once successfully SSHed, the user is now in a position to run the necessary updates in order to ensure the projects’ successful operation. These commands can be found as follows:

### Package Manager Update
```sh
opkg update
```

### UVC Drivers
```sh
opkg install kmod-video-uvc
```

### Python-OpenSSL Package
```sh
opkg install python-openssl
```

### FSWebcam Utility
```sh
opkg install fswebcam
```

### MJPG Streaming Library
```sh
opkg install mjpg-streamer
```

After all of the necessary software-side upgrades to the Yun have been taken care of, it is at this point that the construction of the device can begin to occur. The construction phase, which is much more simplistic in nature compared to the steps seen prior, is comprised of inserting the microSD card into the Arduino board, connecting the camera to the USB port of the Yun, and running the Female to Male jumper wires from the PIR motion sensor to the Yun (where the VCC pin goes to the Yun 5V pin, GND goes to GND, and the SIG pin goes to the Yun pin number 8). A visual reference to this process can be found as follows.

Adding Cloud Functionality (feat @rwchinn)
-----------------------------------------------------------------
By migrating over to the Internet of Things part of this project, it can be found that the entirety of the facial recognition tasks were performed with assets from Amazon Web Services (AWS). Included in this process were the following AWS services: Amazon S3, AWS Lambda Indexer, Amazon Dynamodb, and Amazon Rekognition. For this project, Python and AWS CLI were used to implement these assets. Any user or role that executes commands related to the AWS services need, at a minimum, the following managed policies:
..* AmazonRekognitionFullAccess
..* AmazonDynamoDBFullAccess
..* AmazonS3FullAccess
..* IAMFullAccess
	
Implementation begins with creating a whitelist of facial profiles to be used by Rekognition. This list will be used for various use cases, such as matching a face to a collection, and verifying an identity based on facial matching. In the AWS CLI:

```sh
aws rekognition create-collection \
--collection-id chinncollectionfaces --region us-east-1
```

An Amazon DynamoDB table is used to maintain a key-value store to reference the FaceId returned from Rekognition to the full name of the person.

```sh
aws dynamodb create-table --table-name chinncollectionfaces \
--attribute-definitions AttributeName=RekognitionId,AttributeType=S \
--key-schema AttributeName=RekognitionId,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
--region us-east-1
```

Images for Rekognition to process can be provided as bytes or made available to Rekognition through an Amazon S3 bucket. In the first iteration of this project, a bucket was created to handle the images to which the collection was populated with.

```sh
aws s3 mb s3://chinnbucketfaces --region us-east-1
```
	
The following policies are needed to create an IAM role for Amazon Lambda to access the Amazon S3 and access the images. Two JSON documents are needed.

### trust-policy.json
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### access-policy.json
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::chinnbucketfaces/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem"
            ],
            "Resource": [
                "arn:aws:dynamodb:us-east-1:854134920532:table/chinncollectionfaces"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "rekognition:IndexFaces"
            ],
            "Resource": "*"
        }
    ]
}
```
 
Source Code
------------------------------------------------------------------
To get the software side of the local project up and running:
1. Ensure that upload_picture.py (located under 'src') has been stored under the root of the microSD card along with Temboo's Python SDK libaries (which can be found at https://temboo.com/python).
2. Verify that the 'sketch.ino' file has been successfully transferred to the Arduino via USB or Wi-Fi respectively.
